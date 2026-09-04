import os

# Direktori & File Output
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_CSV_PATH = os.path.join(OUTPUT_DIR, "asean_papua_x_tweets.csv")
COOKIES_FILE_PATH = os.path.join(os.path.dirname(__file__), "cookies.json")

# Jumlah Maksimum Tuitan yang Diambil per Sesi Execution
MAX_TWEETS_TO_COLLECT = 500

# Pengaturan Jeda (Delay in seconds) untuk Menghindari Rate Limit X
MIN_DELAY = 3.0
MAX_DELAY = 7.0

# Query Pencarian Utama (Boolean Search Query)
SEARCH_QUERIES = [
    '("West Papua" OR "Papua" OR "Melanesia" OR "MSG") ("sovereignty" OR "human rights" OR "diplomacy" OR "identity" OR "autonomy")',
    '("West Papua" OR "Papua" OR "Melanesian") ("independence" OR "conflict" OR "Pacific" OR "ASEAN")',
    '("Isu Papua" OR "Rakyat Papua" OR "Identiti Melanesia")'
]

# Kata Kunci Lokasi Pengguna ASEAN Non-Indonesia (Dibersihkan dari singkatan 2-huruf ambigu seperti la/my/th/ph)
ASEAN_LOCATION_KEYWORDS = {
    "Malaysia": ["malaysia", "kuala lumpur", "kl", "penang", "johor", "selangor", "cyberjaya", "sarawak", "sabah", "putrajaya", "malaysian"],
    "Singapore": ["singapore", "sg", "singapura", "lion city"],
    "Thailand": ["thailand", "bangkok", "chiang mai", "phuket", "thai"],
    "Philippines": ["philippines", "manila", "quezon city", "cebu", "davao", "filipino", "pinoy"],
    "Vietnam": ["vietnam", "hanoi", "ho chi minh", "saigon", "vietnamese"],
    "Myanmar": ["myanmar", "yangon", "mandalay", "burma"],
    "Cambodia": ["cambodia", "phnom penh"],
    "Laos": ["laos", "vientiane"],
    "Brunei": ["brunei", "bandar seri begawan"],
    "Kawasan Pasifik & Mitra": ["papua new guinea", "png", "vanuatu", "fiji", "solomon islands", "palau", "new caledonia", "port moresby", "suva", "honiara", "port vila"]
}

# Kata Kunci Lokasi yang Harus Dihapus/Dikecualikan (Lokasi Indonesia)
EXCLUDE_LOCATION_KEYWORDS = [
    "indonesia", "jakarta", "surabaya", "bandung", "yogyakarta", "jogja", 
    "bali", "medan", "semarang", "makassar", "palembang", "depok", "tangerang",
    "bekasi", "bogor", "jayapura", "idn"
]
