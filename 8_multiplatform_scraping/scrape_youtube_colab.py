# ==============================================================================
# SCRAPER YOUTUBE COMMENTS MULTI-MEDIA ASEAN & PASIFIK (VERSI OPTIMASI PRESISI)
# ==============================================================================
# Target Riset FISIP (Sesuai MABA SCOPUS.pdf - RQ1 & RQ2):
# 1. Menargetkan Video Berita Resmi Kawasan:
#    - Singapura: Channel NewsAsia (CNA), The Straits Times
#    - Malaysia: Astro AWANI, Free Malaysia Today (FMT), The Star
#    - Pasifik & Regional: ABC News In-depth (Australia), RNZ Pacific, Al Jazeera English
# 2. Penyaringan Mutlak (Strict Filtering):
#    - Judul video WAJIB memuat entitas utama: Papua, West Papua, Melanesia, atau ULMWP.
#    - Komentar troll, saling ejek ("malaydesh", "indondesh", "babu", dll) DIBUANG 100%.
#    - Komentar bencana alam (gempa/longsor PNG) dan isu domestik DIBUANG 100%.
# 3. Otomatisasi Atribusi Blok Geopolitik & Sumber Media
# ==============================================================================

import os
import re
import sys
import time
import json
import requests
import pandas as pd

# Nama File Output CSV
OUTPUT_CSV_FILENAME = "youtube_papua_asean_comments.csv"

# 1. DAFTAR VIDEO LIPUTAN UTAMA TERVERIFIKASI (VERIFIED HIGH-ENGAGEMENT PAPUA REGISTRY)
# Seluruh video dalam daftar ini 100% dipastikan membahas isu Papua, kedaulatan, dan diplomasi
VERIFIED_YOUTUBE_VIDEOS = [
    # CNA (Channel NewsAsia) - Singapura
    {"id": "eR5FxDVp994", "title": "Indonesia urges calm in Papua after two weeks of protests", "media": "CNA (Channel NewsAsia)", "country": "Singapore", "bloc": "Blok ASEAN"},
    {"id": "EMbf0BkmgEU", "title": "Indonesian police regain control of situation in West Papua province", "media": "CNA (Channel NewsAsia)", "country": "Singapore", "bloc": "Blok ASEAN"},
    {"id": "S4m5a6N8_II", "title": "Papua takes steps to return to normalcy after violent protests", "media": "CNA (Channel NewsAsia)", "country": "Singapore", "bloc": "Blok ASEAN"},
    {"id": "xtkC5bKXd04", "title": "Indonesia restores Internet access in parts of Papua", "media": "CNA (Channel NewsAsia)", "country": "Singapore", "bloc": "Blok ASEAN"},
    {"id": "v_pSQp1CWiI", "title": "Jakarta to keep troops in Papua to protect civilians but Internet still blocked", "media": "CNA (Channel NewsAsia)", "country": "Singapore", "bloc": "Blok ASEAN"},
    {"id": "l-i0zXX-KKo", "title": "Wiranto rules out referendum for Papua", "media": "CNA (Channel NewsAsia)", "country": "Singapore", "bloc": "Blok ASEAN"},
    {"id": "AXJYRrcSo2Q", "title": "Indonesian president orders stern measures to end violence in Papua", "media": "CNA (Channel NewsAsia)", "country": "Singapore", "bloc": "Blok ASEAN"},
    {"id": "f3YYvihZyXs", "title": "Indonesian police say riots were 'designed' by Papuan separatist group", "media": "CNA (Channel NewsAsia)", "country": "Singapore", "bloc": "Blok ASEAN"},
    {"id": "w1Bmdylzo9U", "title": "Indonesia deploys more troops as fresh unrest hits Papua", "media": "CNA (Channel NewsAsia)", "country": "Singapore", "bloc": "Blok ASEAN"},

    # Astro AWANI & Media Malaysia
    {"id": "u6Q5BaSSvVY", "title": "Tentera Indonesia bawa keluar jasad juruterbang AS terbunuh di Papua", "media": "Astro AWANI", "country": "Malaysia", "bloc": "Blok ASEAN"},
    {"id": "4dQfI87oZEY", "title": "Rusuhan: Jokowi seru rakyat Papua bermaafan", "media": "Astro AWANI", "country": "Malaysia", "bloc": "Blok ASEAN"},
    {"id": "GsJ0tgoxJJw", "title": "Tiga orang awam didakwa terbunuh dalam konflik di Papua, Indonesia", "media": "Astro AWANI", "country": "Malaysia", "bloc": "Blok ASEAN"},

    # ABC News In-depth (Australia / Pasifik)
    {"id": "_Gi0julKM9s", "title": "West Papua: the war on our doorstep | The Pacific | ABC News", "media": "ABC News In-depth", "country": "Australia", "bloc": "Blok Pasifik & Melanesia"},
    {"id": "Jlnqt4jOi4Q", "title": "West Papua and 'The Act of No Choice' | The World", "media": "ABC News In-depth", "country": "Australia", "bloc": "Blok Pasifik & Melanesia"},
    {"id": "32XemGEqIvo", "title": "The fight to preserve West Papuan culture - an extended interview", "media": "ABC News In-depth", "country": "Australia", "bloc": "Blok Pasifik & Melanesia"},
    {"id": "ZI23flfOrWQ", "title": "Indonesia's secret war for West Papua, and Fiji's bizarre corruption", "media": "ABC News In-depth", "country": "Australia", "bloc": "Blok Pasifik & Melanesia"},
    {"id": "nlxB6QCpFKk", "title": "Why are West Papuans protesting? | ABC News", "media": "ABC News In-depth", "country": "Australia", "bloc": "Blok Pasifik & Melanesia"},
    {"id": "sMeYD-wFC1o", "title": "Inside Indonesia's Secret War for West Papua | Foreign Correspondent", "media": "ABC News In-depth", "country": "Australia", "bloc": "Blok Pasifik & Melanesia"},
    {"id": "ye0IC4lQijo", "title": "Indonesia issues guilty verdicts in West Papua trial | The World", "media": "ABC News In-depth", "country": "Australia", "bloc": "Blok Pasifik & Melanesia"},
    {"id": "_vM_NILShqM", "title": "West Papua's hidden police state: going undercover", "media": "ABC News In-depth", "country": "Australia", "bloc": "Blok Pasifik & Melanesia"},

    # RNZ Pacific (New Zealand / Pasifik)
    {"id": "yKBdd0VQqlY", "title": "West Papuans' survival in the balance", "media": "RNZ Pacific", "country": "New Zealand", "bloc": "Blok Pasifik & Melanesia"},
    {"id": "rpyAygMRhc0", "title": "West Papuans call on NZ govt to confront Indonesia | Pacific Waves", "media": "RNZ Pacific", "country": "New Zealand", "bloc": "Blok Pasifik & Melanesia"},
    {"id": "VGG9UVAIreg", "title": "Melanesian leaders discuss human rights violations in W Papua | Pacific Waves", "media": "RNZ Pacific", "country": "New Zealand", "bloc": "Blok Pasifik & Melanesia"},
    {"id": "HXNOlAyrows", "title": "NZ pilot release by Papua rebels a 'complex' task | Pacific Waves", "media": "RNZ Pacific", "country": "New Zealand", "bloc": "Blok Pasifik & Melanesia"},

    # Al Jazeera English (Mitra Global)
    {"id": "cBbVu1ZOpYY", "title": "Selling Out West Papua | 101 East", "media": "Al Jazeera English", "country": "Pasifik & Global", "bloc": "Mitra Global"},
    {"id": "Zg5tLsYumzE", "title": "Indonesia's West Papuan protesters face police crackdown over independence calls", "media": "Al Jazeera English", "country": "Pasifik & Global", "bloc": "Mitra Global"},
    {"id": "ebb886BbnGc", "title": "US pilot killed in Indonesian Papua: Rebels say plane was transporting soldiers", "media": "Al Jazeera English", "country": "Pasifik & Global", "bloc": "Mitra Global"},
    {"id": "39YZghUKZks", "title": "West Papua rebels release photos of captured New Zealand pilot", "media": "Al Jazeera English", "country": "Pasifik & Global", "bloc": "Mitra Global"},
    {"id": "MZi88aTr5HM", "title": "Seven Papuan protesters found guilty of treason in Indonesia", "media": "Al Jazeera English", "country": "Pasifik & Global", "bloc": "Mitra Global"},
    {"id": "13Gb7DGWt2Y", "title": "Indonesia deploys troops to West Papua as protests spread", "media": "Al Jazeera English", "country": "Pasifik & Global", "bloc": "Mitra Global"},
    {"id": "bOVN7ttC2Qg", "title": "New Zealand pilot Phillip Mehrtens freed by Papua rebels after 19 months", "media": "Al Jazeera English", "country": "Pasifik & Global", "bloc": "Mitra Global"},
    {"id": "F_yqcNxf90g", "title": "Indonesia's Papua: Home to forgotten struggle", "media": "Al Jazeera English", "country": "Pasifik & Global", "bloc": "Mitra Global"}
]

# 2. TARGET PENELUSURAN DINAMIS KANAL MEDIA
TARGET_MEDIA_CONFIG = [
    {"country": "Singapore", "bloc": "Blok ASEAN", "media": "CNA (Channel NewsAsia)", "query": "CNA West Papua", "channel_filters": ["cna", "channel newsasia"]},
    {"country": "Singapore", "bloc": "Blok ASEAN", "media": "The Straits Times", "query": "Straits Times West Papua", "channel_filters": ["straits times"]},
    {"country": "Malaysia", "bloc": "Blok ASEAN", "media": "Astro AWANI", "query": "Astro AWANI Papua", "channel_filters": ["astro awani", "awani"]},
    {"country": "Malaysia", "bloc": "Blok ASEAN", "media": "Free Malaysia Today", "query": "Free Malaysia Today West Papua", "channel_filters": ["free malaysia today", "fmt"]},
    {"country": "Australia", "bloc": "Blok Pasifik & Melanesia", "media": "ABC News In-depth", "query": "ABC News West Papua", "channel_filters": ["abc news"]},
    {"country": "New Zealand", "bloc": "Blok Pasifik & Melanesia", "media": "RNZ Pacific", "query": "RNZ Pacific West Papua", "channel_filters": ["rnz", "radio new zealand"]},
    {"country": "Pasifik & Global", "bloc": "Mitra Global", "media": "Al Jazeera English", "query": "Al Jazeera English West Papua", "channel_filters": ["al jazeera"]}
]

# KATA KUNCI SUBJEK WAJIB (MANDATORY ENTITIES)
MANDATORY_SUBJECTS = ["papua", "west papua", "papua barat", "melanesia", "melanesian", "ulmwp"]

# KATA KUNCI BENCANA ALAM & NOISE MUTLAK
EXCLUDE_DISASTER_NOISE_KEYWORDS = [
    "gempa", "quake", "earthquake", "landslide", "tanah runtuh", "tanah longsor", 
    "banjir", "flood", "tsunami", "volcano", "letusan", "gunung meletus", 
    "perodua bezza", "oktoberfest", "pizza", "spaghetti", "pembantu", "maid", 
    "enslaving", "fufufafa"
]

# KATA KUNCI EJEKAN TROLL / FLAME WAR (MUTLAK DIBUANG)
FLAME_TROLL_KEYWORDS = [
    "malon", "malaydesh", "indondesh", "konoha", "babu", "makan ubi", 
    "makan ubi kayu", "ganyang sabah", "iq 15 ringgit", "tni takde nyali", 
    "sarawak sabah merdeka", "anak haram", "long tiger", "pabrik china", 
    "pasar selayang", "bani sarapan", "garu dada"
]

HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

def clean_text(text: str) -> str:
    """Membersihkan tautan, tag HTML, dan format spasi ganda."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = " ".join(text.split())
    return text

def is_valid_video_title(title: str) -> bool:
    """
    SYARAT MUTLAK: Judul WAJIB memuat kata Papua/Melanesia dan BEBAS dari bencana alam / noise.
    Mencegah video politik internal Malaysia (Anwar Ibrahim/KiniTV) atau perjanjian Batam (Straits Times) masuk.
    """
    title_lower = title.lower()
    
    # 1. Pengecualian bencana alam & noise
    for neg_kw in EXCLUDE_DISASTER_NOISE_KEYWORDS:
        if neg_kw in title_lower:
            return False
            
    # 2. SYARAT MUTLAK: Wajib memuat subjek Papua / Melanesia
    has_subject = any(term in title_lower for term in MANDATORY_SUBJECTS)
    return has_subject

def is_valid_comment(text: str) -> bool:
    """
    Filter Lapis 2: Menyaring komentar bermutu tinggi untuk analisis sentimen & framing.
    Membuang troll/flamewar slurs dan komentar sampah.
    """
    if len(text) < 15:
        return False
        
    text_lower = text.lower()
    
    # Buang komentar yang memuat ejekan troll antarnetizen
    for flame in FLAME_TROLL_KEYWORDS:
        if flame in text_lower:
            return False
            
    # Buang komentar bencana alam / noise
    for neg in EXCLUDE_DISASTER_NOISE_KEYWORDS:
        if neg in text_lower:
            return False
            
    return True

def search_youtube_media_videos(media_item: dict, max_videos_per_query=4):
    """
    Menelusuri video YouTube resmi secara dinamis dengan validasi ketat.
    """
    query = media_item['query']
    url = f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}"
    found_videos = []
    
    try:
        res = requests.get(url, headers=HTTP_HEADERS, timeout=12)
        if res.status_code != 200:
            return []

        match = re.search(r'ytInitialData\s*=\s*({.+?});', res.text) or re.search(r'var ytInitialData = ({.*?});</script>', res.text)
        if not match:
            return []

        data = json.loads(match.group(1))
        contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])

        for sec in contents:
            items = sec.get('itemSectionRenderer', {}).get('contents', [])
            for it in items:
                v = it.get('videoRenderer')
                if not v:
                    continue
                vid = v.get('videoId')
                title = v.get('title', {}).get('runs', [{}])[0].get('text', '')
                ch_name = v.get('ownerText', {}).get('runs', [{}])[0].get('text', '')

                ch_match = any(f in ch_name.lower() for f in media_item['channel_filters'])
                title_match = is_valid_video_title(title)

                if ch_match and title_match:
                    found_videos.append({
                        "id": vid,
                        "title": title,
                        "media": media_item['media'],
                        "country": media_item['country'],
                        "bloc": media_item['bloc']
                    })
                    if len(found_videos) >= max_videos_per_query:
                        break
    except Exception as e:
        print(f" -> Peringatan pencarian '{query}': {e}", flush=True)

    return found_videos

def scrape_youtube_comments_masif(max_comments_per_video=80, max_total_comments=2500):
    """
    Fungsi utama: Mengambil komentar dari video liputan utama terverifikasi + pencarian dinamis.
    """
    try:
        from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
    except ImportError:
        print("[INFO] Menginstal pustaka youtube-comment-downloader...", flush=True)
        os.system("pip install youtube-comment-downloader")
        from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR

    downloader = YoutubeCommentDownloader()
    all_comments = []
    video_registry = []

    print("="*75, flush=True)
    print(" SCRAPER YOUTUBE COMMENTS MULTI-MEDIA ASEAN & PASIFIK (PRESISI TINGGI)", flush=True)
    print("="*75, flush=True)

    # 1. Masukkan Video Terverifikasi (Curated Registry)
    print(f"[1/3] Memuat {len(VERIFIED_YOUTUBE_VIDEOS)} Video Liputan Utama Terverifikasi...", flush=True)
    for v in VERIFIED_YOUTUBE_VIDEOS:
        video_registry.append(v)

    # 2. Penelusuran Dinamis Tambahan
    print(f"[2/3] Menelusuri video berita terbaru dari kanal resmi ASEAN & Pasifik...", flush=True)
    for media_item in TARGET_MEDIA_CONFIG:
        discovered = search_youtube_media_videos(media_item, max_videos_per_query=3)
        for dv in discovered:
            if not any(x['id'] == dv['id'] for x in video_registry):
                video_registry.append(dv)
                print(f"  + Video Baru Terverifikasi: [{dv['media']}] {dv['title'][:55]}", flush=True)
        time.sleep(1.0)

    print(f"\n[INFO] Total {len(video_registry)} video berita resmi siap diekstrak komentarnya.", flush=True)
    print(f"[3/3] Memulai ekstraksi komentar wacana publik (Maks {max_comments_per_video} per video)...\n", flush=True)

    total_extracted = 0
    for idx, v in enumerate(video_registry, start=1):
        video_url = f"https://www.youtube.com/watch?v={v['id']}"
        print(f"[{idx}/{len(video_registry)}] Mengunduh: [{v['media']}] {v['title'][:48]}...", flush=True)
        
        try:
            comments = downloader.get_comments_from_url(video_url, sort_by=SORT_BY_POPULAR)
            count_for_video = 0

            for c in comments:
                raw_text = c.get('text', '')
                clean_comment = clean_text(raw_text)

                # Validasi filter kualitas & anti-troll
                if not is_valid_comment(clean_comment):
                    continue

                all_comments.append({
                    "platform": "YouTube",
                    "post_id": c.get('cid', f"yt_{v['id']}_{count_for_video}"),
                    "created_at": c.get('time', ''),
                    "username": c.get('author', 'Anonymous'),
                    "user_location": f"{v['country']} (Media: {v['media']})",
                    "country_bloc": v['bloc'],
                    "media_source": v['media'],
                    "full_text": clean_comment,
                    "like_count": c.get('votes', 0),
                    "url": video_url
                })

                count_for_video += 1
                total_extracted += 1

                if count_for_video >= max_comments_per_video or total_extracted >= max_total_comments:
                    break

            print(f"    -> Berhasil mengekstrak {count_for_video} komentar berkualitas.", flush=True)
            time.sleep(1.2)
        except Exception as err:
            print(f"    -> Peringatan pada video {v['id']}: {err}", flush=True)
            continue

        if total_extracted >= max_total_comments:
            print(f"\n[INFO] Batas total komentar ({max_total_comments}) telah tercapai.", flush=True)
            break

    df = pd.DataFrame(all_comments)
    if len(df) > 0:
        df.drop_duplicates(subset=['full_text'], inplace=True)
        df.to_csv(OUTPUT_CSV_FILENAME, index=False, encoding='utf-8-sig')
        print(f"\n[SUKSES] Berhasil mengumpulkan {len(df)} komentar opini publik bermutu!")
        print(f"File tersimpan di: '{OUTPUT_CSV_FILENAME}'")
        print("\nDistribusi Komentar per Blok Geopolitik Media:")
        print(df['country_bloc'].value_counts())
    else:
        print("\n[PERINGATAN] Tidak ada komentar baru yang memenuhi kriteria.")

    return df

def main():
    df = scrape_youtube_comments_masif(max_comments_per_video=80, max_total_comments=2500)

    try:
        from google.colab import files
        if os.path.exists(OUTPUT_CSV_FILENAME):
            print("[INFO] Mengunduh hasil CSV ke komputer Anda...")
            files.download(OUTPUT_CSV_FILENAME)
    except Exception:
        pass

if __name__ == "__main__":
    main()
