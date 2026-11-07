# ==============================================================================
# SKRIP SCRAPING X (TWITTER) WACANA ASEAN - VERSI GOOGLE COLAB
# ==============================================================================
# Petunjuk:
# 1. Buka https://colab.research.google.com
# 2. Upload berkas scrape_x_asean_colab.ipynb ATAU buat Notebook Baru dan copy-paste kode ini.
# 3. Jalankan Sel 1 (Install), Sel 2 (Isi Cookie), dan Sel 3 (Jalankan Scraping)
# ==============================================================================

# ------------------------------------------------------------------------------
# SEL 1: INSTALL LIBRARIES (Jalankan sel ini terlebih dahulu di Colab)
# ------------------------------------------------------------------------------
"""
!pip install twikit pandas nest_asyncio beautifulsoup4
"""

# ------------------------------------------------------------------------------
# SEL 2 & 3: KODE UTAMA SCRAPING (Salin seluruh kode di bawah ke dalam 1 Sel Colab)
# ------------------------------------------------------------------------------
import asyncio
import os
import random
import sys
import pandas as pd
import nest_asyncio
import bs4
import twikit
from twikit import Client
import twikit.x_client_transaction.transaction as t
import twikit.client.gql as g
import twikit.user as u

# Mengaktifkan nest_asyncio agar kompatibel dengan lingkungan Jupyter/Google Colab
nest_asyncio.apply()

# ==============================================================================
# PATCH TWIKIT CORE (Perbaikan Bug 404, KeyError 'urls', & ClientTransaction)
# ==============================================================================
def apply_all_twikit_patches():
    # Patch 1: Safe ClientTransaction Init
    async def safe_init(self, session, headers):
        try:
            home_page_response = await t.handle_x_migration(session, headers)
            self.home_page_response = self.validate_response(home_page_response)
        except Exception:
            self.home_page_response = bs4.BeautifulSoup(
                '<html><head><meta name="twitter-site-verification" content="mentU+1yPz+IcNS+RaF+b"/></head><body></body></html>', 
                'html.parser'
            )

        try:
            self.DEFAULT_ROW_INDEX, self.DEFAULT_KEY_BYTES_INDICES = await self.get_indices(self.home_page_response, session, headers)
        except Exception:
            self.DEFAULT_ROW_INDEX = 2
            self.DEFAULT_KEY_BYTES_INDICES = [12, 14, 7]

        try:
            self.key = self.get_key(response=self.home_page_response)
        except Exception:
            self.key = "mentU+1yPz+IcNS+RaF+b"

        self.key_bytes = self.get_key_bytes(key=self.key)
        try:
            self.animation_key = self.get_animation_key(key_bytes=self.key_bytes, response=self.home_page_response)
        except Exception:
            self.animation_key = "00000000"

    # Patch 2: GQLClient search_timeline (Gunakan POST bukan GET untuk mencegah 404)
    async def patched_search_timeline(self, query: str, product: str, count: int, cursor: str | None):
        variables = {
            'rawQuery': query,
            'count': count,
            'querySource': 'typed_query',
            'product': product
        }
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_post(g.Endpoint.SEARCH_TIMELINE, variables, g.FEATURES)

    # Patch 3: Safe User Init (Cegah KeyError: 'urls' yang membuang tuitan)
    def safe_user_init(self, client, data):
        self._client = client
        legacy = data.get('legacy', {})

        self.id = data.get('rest_id', '')
        self.created_at = legacy.get('created_at', '')
        self.name = legacy.get('name', '')
        self.screen_name = legacy.get('screen_name', '')
        self.profile_image_url = legacy.get('profile_image_url_https', '')
        self.profile_banner_url = legacy.get('profile_banner_url')
        self.url = legacy.get('url')
        self.location = legacy.get('location', '')
        self.description = legacy.get('description', '')
        
        entities = legacy.get('entities', {})
        desc_entities = entities.get('description', {}) if isinstance(entities, dict) else {}
        self.description_urls = desc_entities.get('urls', []) if isinstance(desc_entities, dict) else []
        
        url_entities = entities.get('url', {}) if isinstance(entities, dict) else {}
        self.urls = url_entities.get('urls', []) if isinstance(url_entities, dict) else []
        
        self.pinned_tweet_ids = legacy.get('pinned_tweet_ids_str', [])
        self.is_blue_verified = data.get('is_blue_verified', False)
        self.verified = legacy.get('verified', False)
        self.possibly_sensitive = legacy.get('possibly_sensitive', False)
        self.can_dm = legacy.get('can_dm', False)
        self.can_media_tag = legacy.get('can_media_tag', False)
        self.want_retweets = legacy.get('want_retweets', False)
        self.default_profile = legacy.get('default_profile', False)
        self.default_profile_image = legacy.get('default_profile_image', False)
        self.has_custom_timelines = legacy.get('has_custom_timelines', False)
        self.followers_count = legacy.get('followers_count', 0)
        self.fast_followers_count = legacy.get('fast_followers_count', 0)
        self.normal_followers_count = legacy.get('normal_followers_count', 0)
        self.following_count = legacy.get('friends_count', 0)
        self.favourites_count = legacy.get('favourites_count', 0)
        self.listed_count = legacy.get('listed_count', 0)
        self.media_count = legacy.get('media_count', 0)
        self.statuses_count = legacy.get('statuses_count', 0)
        self.is_translator = legacy.get('is_translator', False)
        self.translator_type = legacy.get('translator_type', '')
        self.withheld_in_countries = legacy.get('withheld_in_countries', [])
        self.protected = legacy.get('protected', False)

    t.ClientTransaction.init = safe_init
    g.GQLClient.search_timeline = patched_search_timeline
    u.User.__init__ = safe_user_init

apply_all_twikit_patches()

# ==============================================================================
# KONFIGURASI PENCARIAN & FILTER LOKASI
# ==============================================================================
OUTPUT_CSV_PATH = "asean_papua_x_tweets.csv"
MAX_TWEETS_TO_COLLECT = 500  # Batas maksimum tuitan per sesi
MIN_DELAY = 3.0
MAX_DELAY = 7.0

# Query Pencarian Utama
SEARCH_QUERIES = [
    '("West Papua" OR "Papua" OR "Melanesia" OR "MSG") ("sovereignty" OR "human rights" OR "diplomacy" OR "identity" OR "autonomy")',
    '("West Papua" OR "Papua" OR "Melanesian") ("independence" OR "conflict" OR "Pacific" OR "ASEAN")',
    '("Isu Papua" OR "Rakyat Papua" OR "Identiti Melanesia")'
]

# Kata Kunci Lokasi Pengguna ASEAN Non-Indonesia
ASEAN_LOCATION_KEYWORDS = {
    "Malaysia": ["malaysia", "kuala lumpur", "kl", "penang", "johor", "selangor", "cyberjaya", "my"],
    "Singapore": ["singapore", "sg"],
    "Thailand": ["thailand", "bangkok", "chiang mai", "phuket", "th"],
    "Philippines": ["philippines", "manila", "quezon city", "cebu", "ph"],
    "Vietnam": ["vietnam", "hanoi", "ho chi minh", "saigon", "vn"],
    "Myanmar": ["myanmar", "yangon", "mandalay", "burma", "mm"],
    "Cambodia": ["cambodia", "phnom penh", "kh"],
    "Laos": ["laos", "vientiane", "la"],
    "Brunei": ["brunei", "bandar seri begawan", "bn"]
}

# Kata Kunci Lokasi Indonesia yang Harus Dieliminasi
EXCLUDE_LOCATION_KEYWORDS = [
    "indonesia", "jakarta", "surabaya", "bandung", "yogyakarta", "jogja", 
    "bali", "medan", "semarang", "makassar", "palembang", "depok", "tangerang",
    "bekasi", "bogor", "jayapura", "idn", "id"
]

# ==============================================================================
# FUNGSI HELPER
# ==============================================================================
def is_indonesia_location(user_location: str) -> bool:
    if not user_location:
        return False
    loc_lower = user_location.lower().strip()
    for ex_key in EXCLUDE_LOCATION_KEYWORDS:
        if ex_key in loc_lower:
            return True
    return False

def detect_asean_country(user_location: str) -> str:
    if not user_location:
        return "ASEAN (Lainnya/Tidak Spesifik)"
    
    loc_lower = user_location.lower().strip()
    if is_indonesia_location(loc_lower):
        return "INDONESIA_EXCLUDED"

    for country, keywords in ASEAN_LOCATION_KEYWORDS.items():
        for kw in keywords:
            if kw in loc_lower:
                return country
                
    return "ASEAN (Lainnya/Non-ID)"

def load_existing_tweet_ids(filepath: str) -> set:
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath, usecols=["tweet_id"])
            return set(df["tweet_id"].astype(str).tolist())
        except Exception:
            return set()
    return set()

def save_to_csv(tweets_list: list, filepath: str):
    df_new = pd.DataFrame(tweets_list)
    file_exists = os.path.exists(filepath)
    df_new.to_csv(filepath, mode='a' if file_exists else 'w', index=False, header=not file_exists, encoding='utf-8-sig')
    print(f"[CHECKPOINT] {len(tweets_list)} tuitan baru berhasil disimpan ke CSV.")

# ==============================================================================
# FUNGSI UTAMA SCRAPING
# ==============================================================================
async def main():
    print("="*70)
    print(" SKRIP SCRAPING DATA X (TWITTER) WACANA ASEAN - GOOGLE COLAB")
    print("="*70)
    
    auth_token = input("Masukkan auth_token dari cookie X Anda: ").strip()
    ct0 = input("Masukkan ct0 dari cookie X Anda: ").strip()

    if not auth_token or not ct0:
        print("[ERROR] auth_token dan ct0 tidak boleh kosong!")
        return

    print("\n[INFO] Menginisialisasi Klien X...")
    client = Client(language='en-US')
    cookies = {
        "auth_token": auth_token,
        "ct0": ct0
    }
    client.set_cookies(cookies)
    print("[SUCCESS] Cookies berhasil dipasang!")

    collected_tweets = []
    seen_ids = load_existing_tweet_ids(OUTPUT_CSV_PATH)
    total_collected_this_run = 0

    print(f"[INFO] Memulai scraping... Data awal di CSV: {len(seen_ids)} tuitan.")

    for query in SEARCH_QUERIES:
        if total_collected_this_run >= MAX_TWEETS_TO_COLLECT:
            print(f"[INFO] Batas kuota per sesi ({MAX_TWEETS_TO_COLLECT}) tercapai.")
            break

        print(f"\n[QUERY PENCARIAN] Running: {query}")
        try:
            tweets = await client.search_tweet(query, product='Top', count=20)
            page_count = 0

            while tweets and total_collected_this_run < MAX_TWEETS_TO_COLLECT:
                page_count += 1
                print(f" -> Halaman {page_count} ({len(tweets)} tuitan ditemukan dalam batch)...")

                for tweet in tweets:
                    tweet_id = str(tweet.id)

                    if tweet_id in seen_ids:
                        continue

                    user = tweet.user
                    user_location = getattr(user, 'location', '') or ''
                    
                    country_status = detect_asean_country(user_location)
                    if country_status == "INDONESIA_EXCLUDED":
                        continue

                    full_text = getattr(tweet, 'full_text', '') or getattr(tweet, 'text', '')
                    cleaned_text = " ".join(full_text.split())

                    tweet_data = {
                        "tweet_id": tweet_id,
                        "created_at": str(tweet.created_at),
                        "username": user.screen_name,
                        "user_name": user.name,
                        "user_location": user_location,
                        "detected_country": country_status,
                        "full_text": cleaned_text,
                        "language": getattr(tweet, 'lang', 'unknown'),
                        "retweet_count": getattr(tweet, 'retweet_count', 0),
                        "like_count": getattr(tweet, 'favorite_count', 0),
                        "reply_count": getattr(tweet, 'reply_count', 0),
                        "tweet_url": f"https://x.com/{user.screen_name}/status/{tweet_id}"
                    }

                    collected_tweets.append(tweet_data)
                    seen_ids.add(tweet_id)
                    total_collected_this_run += 1

                if len(collected_tweets) >= 20:
                    save_to_csv(collected_tweets, OUTPUT_CSV_PATH)
                    collected_tweets = []

                delay = random.uniform(MIN_DELAY, MAX_DELAY)
                await asyncio.sleep(delay)

                try:
                    tweets = await tweets.next()
                except Exception as e:
                    print(f" [INFO] Akhir batch hasil pencarian: {e}")
                    break

        except Exception as e:
            print(f"[ERROR] Kendala query '{query}': {e}")
            await asyncio.sleep(5)

    if collected_tweets:
        save_to_csv(collected_tweets, OUTPUT_CSV_PATH)

    print("\n" + "="*70)
    print(f"[SELESAI] Total tuitan baru berhasil disimpan: {total_collected_this_run}")
    print(f"[FILE OUTPUT] {OUTPUT_CSV_PATH}")
    print("="*70 + "\n")

    try:
        from google.colab import files
        print("[INFO] Mengunduh file CSV hasil scraping ke komputer Anda...")
        files.download(OUTPUT_CSV_PATH)
    except Exception:
        pass

if __name__ == "__main__":
    asyncio.run(main())
