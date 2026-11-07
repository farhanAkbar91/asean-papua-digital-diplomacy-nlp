import os

# Direktori Output Data
OUTPUT_DIR = os.path.dirname(__file__)
NEWS_CSV_PATH = os.path.join(OUTPUT_DIR, "news_papua_asean_articles.csv")

# Skema Kolom Standar Multi-Platform (Kompatibel 100% dengan X dan YouTube)
STANDARDIZED_COLUMNS = [
    "platform",        # 'News Media'
    "post_id",         # hash unik / slug artikel
    "created_at",      # tanggal publikasi (YYYY-MM-DD)
    "username",        # jurnalis / news agency (e.g. 'CNA Desk', 'Reuters', 'FMT Reporter')
    "user_location",   # lokasi kantor media / atribusi negara
    "country_bloc",    # Blok Geopolitik ('Blok ASEAN', 'Blok Pasifik & Melanesia', 'Mitra Global')
    "media_source",    # Nama portal berita resmi
    "full_text",       # Judul + Ringkasan + Teks lengkap artikel
    "like_count",      # Default 0 (standar metrik media berita)
    "url"              # URL kanonikal artikel asli
]

# SYARAT MUTLAK SUBJEK TOPIK (Judul atau isi artikel WAJIB memuat minimal satu entitas ini)
MANDATORY_CORE_SUBJECTS = [
    "papua", "west papua", "papua barat", "melanesia", "melanesian", "ulmwp"
]

# KATA KUNCI RELEVANSI DIPLOMASI & GEOPOLITIK (Menjawab RQ1, RQ2, RQ3)
RELEVANT_TOPIC_TERMS = [
    "indonesia", "jakarta", "asean", "msg", "melanesian spearhead group", 
    "pacific islands forum", "referendum", "human rights", "hak asasi", 
    "sovereignty", "kedaulatan", "separatis", "separatist", "protest", 
    "rebel", "freedom", "merdeka", "pilot", "hostage", "tni", "military", 
    "benny wenda", "pepera", "freeport", "unrest", "indigenous"
]

# KATA KUNCI EKSKLUSI NOISE BENCANA MURNI (Bencana alam tanpa sudut pandang geopolitik/diplomasi)
EXCLUDE_DISASTER_NOISE = [
    "earthquake", "gempa", "magnitude", "tsunami", "landslide", "tanah longsor", 
    "volcano", "letusan", "flood", "banjir"
]

# TARGET PORTAL MEDIA BERITA REGIONAL RESMI
TARGET_NEWS_MEDIA = [
    # 1. SINGAPURA (Blok ASEAN - Menjawab RQ2 & Ekosistem Attentive Public)
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

    # 2. MALAYSIA (Blok ASEAN - Menjawab RQ2 & Ekosistem Attentive Public)
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

    # 3. KAWASAN PASIFIK & MELANESIA (Blok Pasifik & Melanesia - Komparator Diplomasi Regional)
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

    # 4. MITRA GLOBAL & REGIONAL (Mitra Global)
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
