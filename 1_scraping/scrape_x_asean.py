import asyncio
import os
import random
import sys
import pandas as pd
import bs4
from dotenv import load_dotenv
import twikit
from twikit import Client
import twikit.x_client_transaction.transaction as t
import twikit.client.gql as g
import twikit.user as u

import config

load_dotenv()

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

async def init_client() -> Client:
    client = Client(language='en-US')
    
    if os.path.exists(config.COOKIES_FILE_PATH):
        print(f"[INFO] Memuat cookies dari {config.COOKIES_FILE_PATH}...")
        try:
            client.load_cookies(config.COOKIES_FILE_PATH)
            print("[SUCCESS] Cookies berhasil dimuat.")
            return client
        except Exception as e:
            print(f"[WARNING] Gagal memuat cookies.json: {e}")

    auth_token = os.getenv("X_AUTH_TOKEN")
    ct0 = os.getenv("X_CT0")
    
    if auth_token and ct0 and auth_token != "your_auth_token_here":
        print("[INFO] Menggunakan cookies dari .env (X_AUTH_TOKEN & X_CT0)...")
        cookies = {
            "auth_token": auth_token,
            "ct0": ct0
        }
        client.set_cookies(cookies)
        client.save_cookies(config.COOKIES_FILE_PATH)
        print("[SUCCESS] Cookies dari .env berhasil diterapkan dan disimpan.")
        return client

    username = os.getenv("X_USERNAME")
    email = os.getenv("X_EMAIL")
    password = os.getenv("X_PASSWORD")

    if username and password and username != "your_x_username":
        print(f"[INFO] Mencoba login ke X menggunakan username '{username}'...")
        try:
            await client.login(
                auth_info=username,
                email=email,
                password=password
            )
            client.save_cookies(config.COOKIES_FILE_PATH)
            print("[SUCCESS] Login berhasil. Cookies telah disimpan untuk sesi berikutnya.")
            return client
        except Exception as e:
            print(f"[ERROR] Gagal login ke X: {e}")

    print("\n" + "="*70)
    print("[PERHATIAN] Kredensial X belum diisi!")
    print("Silakan isi file .env dengan X_AUTH_TOKEN & X_CT0 atau X_USERNAME & X_PASSWORD.")
    print("Lihat petunjuk lengkap pada file README.md.")
    print("="*70 + "\n")
    sys.exit(1)


def is_indonesia_location(user_location: str) -> bool:
    if not user_location:
        return False
    loc_lower = user_location.lower().strip()
    for ex_key in config.EXCLUDE_LOCATION_KEYWORDS:
        if ex_key in loc_lower:
            return True
    return False


def detect_asean_country(user_location: str) -> str:
    if not user_location:
        return "ASEAN (Lainnya/Tidak Spesifik)"
    
    loc_lower = user_location.lower().strip()
    
    if is_indonesia_location(loc_lower):
        return "INDONESIA_EXCLUDED"

    for country, keywords in config.ASEAN_LOCATION_KEYWORDS.items():
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


async def scrape_tweets():
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    client = await init_client()

    collected_tweets = []
    seen_ids = load_existing_tweet_ids(config.OUTPUT_CSV_PATH)
    print(f"[INFO] Memulai scraping... Data awal di CSV: {len(seen_ids)} tuitan.")

    total_collected_this_run = 0

    for query in config.SEARCH_QUERIES:
        if total_collected_this_run >= config.MAX_TWEETS_TO_COLLECT:
            print(f"[INFO] Kuota maksimum per sesi ({config.MAX_TWEETS_TO_COLLECT}) tercapai.")
            break

        print(f"\n[QUERY PENCARIAN] Running: {query}")
        try:
            tweets = await client.search_tweet(query, product='Top', count=20)
            
            page_count = 0
            while tweets and total_collected_this_run < config.MAX_TWEETS_TO_COLLECT:
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
                    save_to_csv(collected_tweets, config.OUTPUT_CSV_PATH)
                    collected_tweets = []

                delay = random.uniform(config.MIN_DELAY, config.MAX_DELAY)
                await asyncio.sleep(delay)

                try:
                    tweets = await tweets.next()
                except Exception as e:
                    print(f" [INFO] Akhir hasil pencarian atau limit batch: {e}")
                    break

        except Exception as e:
            print(f"[ERROR] Kendala saat mengeksekusi query '{query}': {e}")
            await asyncio.sleep(5)

    if collected_tweets:
        save_to_csv(collected_tweets, config.OUTPUT_CSV_PATH)

    print("\n" + "="*70)
    print(f"[SELESAI] Total tuitan baru berhasil disimpan di sesi ini: {total_collected_this_run}")
    print(f"[FILE OUTPUT] {config.OUTPUT_CSV_PATH}")
    print("="*70 + "\n")


def save_to_csv(tweets_list: list, filepath: str):
    df_new = pd.DataFrame(tweets_list)
    file_exists = os.path.exists(filepath)
    df_new.to_csv(filepath, mode='a' if file_exists else 'w', index=False, header=not file_exists, encoding='utf-8-sig')
    print(f"[CHECKPOINT] {len(tweets_list)} tuitan berhasil ditulis ke CSV.")


if __name__ == "__main__":
    asyncio.run(scrape_tweets())
