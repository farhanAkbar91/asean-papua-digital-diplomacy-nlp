"""
=============================================================================
PIPELINE SCRAPING MEDIA BERITA ONLINE REGIONAL (RISET FISIP - SCOPUS)
=============================================================================
Target: Media Berita Malaysia, Singapura, Pasifik & Global
Tujuan: Melengkapi Triangulasi Data (X, YouTube, Media Berita) untuk
        menjawab RQ1 (Sentimen & Narasi), RQ2 (Attentive Public ASEAN),
        dan RQ3 (Efektivitas Diplomasi Publik RI).
Metode: Google News RSS Endpoint + GoogleNewsDecoder + BeautifulSoup4
=============================================================================
"""

import os
import sys
import time
import hashlib
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, *args, **kwargs):
        return iterable

try:
    import googlenewsdecoder
except ImportError:
    print("[INFO] Menginstall googlenewsdecoder...")
    os.system("pip install googlenewsdecoder")
    import googlenewsdecoder

# Konfigurasi Target Media & Kueri
TARGET_NEWS_MEDIA = [
    # 1. SINGAPURA (Blok ASEAN - Menjawab RQ2)
    {
        "country": "Singapore",
        "bloc": "Blok ASEAN",
        "media": "CNA (Channel NewsAsia)",
        "location": "Singapore",
        "queries": [
            "site:channelnewsasia.com \"West Papua\"",
            "site:channelnewsasia.com \"Papua\" Indonesia"
        ]
    },
    {
        "country": "Singapore",
        "bloc": "Blok ASEAN",
        "media": "The Straits Times",
        "location": "Singapore",
        "queries": [
            "site:straitstimes.com \"West Papua\"",
            "site:straitstimes.com \"Papua\" Indonesia"
        ]
    },

    # 2. MALAYSIA (Blok ASEAN - Menjawab RQ2)
    {
        "country": "Malaysia",
        "bloc": "Blok ASEAN",
        "media": "The Star",
        "location": "Kuala Lumpur, Malaysia",
        "queries": [
            "site:thestar.com.my \"West Papua\"",
            "site:thestar.com.my \"Papua\" Indonesia"
        ]
    },
    {
        "country": "Malaysia",
        "bloc": "Blok ASEAN",
        "media": "Free Malaysia Today",
        "location": "Petaling Jaya, Malaysia",
        "queries": [
            "site:freemalaysiatoday.com \"West Papua\"",
            "site:freemalaysiatoday.com \"Papua\" Indonesia"
        ]
    },
    {
        "country": "Malaysia",
        "bloc": "Blok ASEAN",
        "media": "New Straits Times",
        "location": "Kuala Lumpur, Malaysia",
        "queries": [
            "site:nst.com.my \"West Papua\"",
            "site:nst.com.my \"Papua\" Indonesia"
        ]
    },
    {
        "country": "Malaysia",
        "bloc": "Blok ASEAN",
        "media": "Astro AWANI",
        "location": "Kuala Lumpur, Malaysia",
        "queries": [
            "site:astroawani.com \"Papua\"",
            "site:astroawani.com \"West Papua\""
        ]
    },
    {
        "country": "Malaysia",
        "bloc": "Blok ASEAN",
        "media": "Malay Mail",
        "location": "Petaling Jaya, Malaysia",
        "queries": [
            "site:malaymail.com \"West Papua\"",
            "site:malaymail.com \"Papua\" Indonesia"
        ]
    },

    # 3. PASIFIK & MELANESIA (Blok Pasifik & Melanesia)
    {
        "country": "New Zealand",
        "bloc": "Blok Pasifik & Melanesia",
        "media": "RNZ Pacific",
        "location": "Wellington, New Zealand",
        "queries": [
            "site:rnz.co.nz \"West Papua\"",
            "site:rnz.co.nz \"Papua\" Indonesia"
        ]
    },
    {
        "country": "Australia",
        "bloc": "Blok Pasifik & Melanesia",
        "media": "ABC News Australia",
        "location": "Sydney, Australia",
        "queries": [
            "site:abc.net.au \"West Papua\"",
            "site:abc.net.au \"Papua\" Indonesia"
        ]
    },
    {
        "country": "Pacific Regional",
        "bloc": "Blok Pasifik & Melanesia",
        "media": "Asia Pacific Report",
        "location": "Auckland, New Zealand",
        "queries": [
            "site:asiapacificreport.nz \"West Papua\"",
            "site:asiapacificreport.nz \"Melanesia\" Papua"
        ]
    },

    # 4. MITRA GLOBAL (Mitra Global)
    {
        "country": "Pasifik & Global",
        "bloc": "Mitra Global",
        "media": "Al Jazeera English",
        "location": "Doha / Regional Bureau",
        "queries": [
            "site:aljazeera.com \"West Papua\"",
            "site:aljazeera.com \"Papua\" Indonesia"
        ]
    },
    {
        "country": "Regional Asia-Pacific",
        "bloc": "Mitra Global",
        "media": "BenarNews",
        "location": "Washington / Regional Bureau",
        "queries": [
            "site:benarnews.org \"West Papua\"",
            "site:benarnews.org \"Papua\""
        ]
    }
]

# SYARAT MUTLAK SUBJEK TOPIK
MANDATORY_CORE_SUBJECTS = ["papua", "west papua", "papua barat", "melanesia", "melanesian", "ulmwp"]

# KATA KUNCI PENOLAKAN BENCANA MURNI
EXCLUDE_DISASTER_TERMS = ["magnitude", "gempa", "earthquake", "tsunami", "aftershocks", "volcano", "letusan"]

def fetch_rss_items(query, max_items=60):
    """Mengambil daftar artikel dari Google News RSS berdasarkan kueri terfokus."""
    encoded_q = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_q}&hl=en&gl=US&ceid=US:en"
    req = urllib.request.Request(rss_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    })
    
    items_data = []
    try:
        res = urllib.request.urlopen(req, timeout=12)
        root = ET.fromstring(res.read())
        for item in root.findall('.//item')[:max_items]:
            title = item.find('title').text if item.find('title') is not None else ""
            link = item.find('link').text if item.find('link') is not None else ""
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
            source = item.find('source').text if item.find('source') is not None else ""
            
            if title and link:
                items_data.append({
                    "rss_title": title,
                    "rss_link": link,
                    "pub_date": pub_date,
                    "source": source
                })
    except Exception as e:
        print(f"      [!] Gagal mengambil RSS untuk '{query[:40]}...': {e}")
    return items_data

def decode_google_news_url(rss_url):
    """Mendekode URL Google News menjadi URL asli portal berita."""
    try:
        res = googlenewsdecoder.new_decoderv1(rss_url)
        if res.get("status"):
            return res.get("decoded_url")
    except Exception:
        pass
    return None

def extract_article_content(url, session):
    """Mengekstrak teks judul, tanggal, dan isi berita dari halaman web portal berita."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8,ms;q=0.7'
    }
    
    try:
        resp = session.get(url, headers=headers, timeout=12, allow_redirects=True)
        if resp.status_code != 200:
            return None
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Hapus elemen tidak relevan (iklan, navigasi, skrip)
        for noise in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside', 'noscript', 'svg']):
            noise.decompose()
        
        # Ekstrak Judul
        title = ""
        h1 = soup.find('h1')
        if h1 and len(h1.get_text().strip()) > 10:
            title = h1.get_text().strip()
        elif soup.title:
            title = soup.title.get_text().strip()
            
        # Ekstrak Paragraf Isi Berita
        # Cari container artikel utama bila ada
        article_elem = soup.find('article') or soup.find('div', class_=lambda c: c and any(k in c.lower() for k in ['content', 'article', 'body', 'story', 'post-text']))
        search_scope = article_elem if article_elem else soup
        
        paragraphs = []
        for p in search_scope.find_all('p'):
            text = p.get_text().strip()
            # Filter paragraf berita substansial (bukan navigasi/disclaimer)
            if len(text) > 45 and not any(k in text.lower() for k in ['cookie', 'subscribe', 'terms of use', 'all rights reserved', 'advertisement', 'sign up']):
                paragraphs.append(text)
        
        if not paragraphs:
            return None
        
        full_body = " ".join(paragraphs)
        return {
            "title": title,
            "body": full_body
        }
    except Exception:
        return None

def is_valid_academic_sample(title, body):
    """Validasi ketat agar artikel 100% relevan dengan isu Papua & Diplomasi."""
    combined = f"{title} {body}".lower()
    
    # 1. Wajib memuat subjek Papua / Melanesia
    if not any(sub in combined for sub in MANDATORY_CORE_SUBJECTS):
        return False
    
    # 2. Filter gempa/bencana alam murni (kecuali jika membahas kedaulatan/konflik/bantuan diplomasi)
    if any(dis in title.lower() for dis in EXCLUDE_DISASTER_TERMS):
        diplomatic_triggers = ["conflict", "rebel", "military", "tni", "diplomacy", "sovereignty", "rights", "aid", "australia", "indonesia"]
        if not any(dip in combined for dip in diplomatic_triggers):
            return False
            
    # 3. Panjang teks minimum (menghindari stub/paywall kosong)
    if len(body) < 150:
        return False
        
    return True

def run_news_scraper(output_csv="news_papua_asean_articles.csv", max_articles_per_media=40):
    print("=" * 80)
    print("      CRAWLER & SCRAPER MEDIA BERITA REGIONAL (RISET FISIP - SCOPUS)")
    print("=" * 80)
    print(f"Target Media: {len(TARGET_NEWS_MEDIA)} Portal Berita Terkemuka di ASEAN, Pasifik & Global")
    print(f"Output File : {output_csv}\n")
    
    session = requests.Session()
    collected_articles = []
    seen_urls = set()
    
    for media_cfg in TARGET_NEWS_MEDIA:
        media_name = media_cfg["media"]
        country = media_cfg["country"]
        bloc = media_cfg["bloc"]
        location = media_cfg["location"]
        queries = media_cfg["queries"]
        
        print(f"\n[+] Memproses Portal: {media_name} ({country} | {bloc})")
        media_count = 0
        
        for q in queries:
            if media_count >= max_articles_per_media:
                break
                
            print(f"    --> Kueri: {q}")
            rss_items = fetch_rss_items(q, max_items=40)
            print(f"        Ditemukan {len(rss_items)} entri RSS. Mengambil artikel asli...")
            
            for item in tqdm(rss_items, desc=f"        {media_name[:15]}", leave=False):
                if media_count >= max_articles_per_media:
                    break
                    
                rss_link = item["rss_link"]
                real_url = decode_google_news_url(rss_link)
                
                if not real_url or real_url in seen_urls:
                    continue
                seen_urls.add(real_url)
                
                # Ekstrak konten artikel
                article = extract_article_content(real_url, session)
                if not article:
                    continue
                    
                title = article["title"] if article["title"] else item["rss_title"]
                body = article["body"]
                
                # Validasi Relevansi
                if not is_valid_academic_sample(title, body):
                    continue
                
                # Parsing Tanggal
                raw_date = item.get("pub_date", "")
                try:
                    # Format standar RSS: "Sat, 03 Aug 2024 07:00:00 GMT"
                    dt = datetime.strptime(raw_date[:25].strip(), "%a, %d %b %Y %H:%M:%S")
                    formatted_date = dt.strftime("%Y-%m-%d")
                except Exception:
                    formatted_date = datetime.now().strftime("%Y-%m-%d")
                
                # Generate Hash ID Unik
                article_id = "news_" + hashlib.md5(real_url.encode('utf-8')).hexdigest()[:12]
                full_text = f"{title}. {body}"
                
                collected_articles.append({
                    "platform": "News Media",
                    "post_id": article_id,
                    "created_at": formatted_date,
                    "username": media_name + " Desk",
                    "user_location": location,
                    "country_bloc": bloc,
                    "media_source": media_name,
                    "full_text": full_text,
                    "like_count": 0,
                    "url": real_url
                })
                media_count += 1
                time.sleep(0.5)  # Rate limiting sopan
                
        print(f"    [✓] Berhasil mengumpulkan {media_count} artikel dari {media_name}")
    
    # Konversi ke DataFrame
    df = pd.DataFrame(collected_articles)
    if not df.empty:
        df.to_csv(output_csv, index=False, encoding='utf-8')
        print("\n" + "=" * 80)
        print("                 HASIL AKHIR SCRAPING MEDIA BERITA")
        print("=" * 80)
        print(f"Total Artikel Berhasil Dikumpulkan : {len(df)} artikel")
        print("\nDistribusi Artikel per Blok Geopolitik:")
        print(df["country_bloc"].value_counts().to_string())
        print("\nDistribusi Artikel per Media Berita:")
        print(df["media_source"].value_counts().to_string())
        print("=" * 80)
        print(f"[✓] File tersimpan di: {output_csv}")
    else:
        print("[!] Tidak ada artikel yang memenuhi kriteria.")
    
    return df

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "news_papua_asean_articles.csv")
    run_news_scraper(out_file)
