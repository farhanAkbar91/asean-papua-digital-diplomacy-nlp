import os

# Direktori Output Data
OUTPUT_DIR = os.path.dirname(__file__)
YOUTUBE_CSV_PATH = os.path.join(OUTPUT_DIR, "youtube_papua_asean_comments.csv")
REDDIT_CSV_PATH = os.path.join(OUTPUT_DIR, "reddit_papua_asean_posts.csv")

# Skema Kolom Standar Multi-Platform (Kompatibel dengan Pipeline NLP V2)
STANDARDIZED_COLUMNS = [
    "platform",        # 'YouTube' atau 'Reddit'
    "post_id",         # comment_id atau submission_id
    "created_at",      # tanggal/waktu publikasi
    "username",        # nama pengguna/komentator
    "user_location",   # atribusi lokasi (Subreddit / Media Channel Negara)
    "country_bloc",    # Blok Geopolitik ('Blok ASEAN', 'Blok Pasifik & Melanesia', 'Mitra Global')
    "media_source",    # Kanal media / Subreddit spesifik
    "full_text",       # Teks bersih opini/diskursus
    "like_count",      # Upvotes / Like count
    "url"              # URL sumber
]

# SYARAT MUTLAK SUBJEK TOPIK (Judul video atau isi komentar WAJIB memuat entitas ini)
MANDATORY_CORE_SUBJECTS = [
    "papua", "west papua", "papua barat", "melanesia", "melanesian", "ulmwp"
]

# Kata Kunci Terkait Isu Diplomasi & Kedaulatan Papua
RELEVANT_TOPIC_TERMS = [
    "msg", "melanesian spearhead group", "pacific islands forum", "referendum", 
    "human rights", "hak asasi", "indigenous", "sovereignty", "kedaulatan", 
    "separatis", "protest", "rusuhan", "unrest", "rebel", "freedom", "merdeka", 
    "freewestpapua", "free west papua", "wiranto", "tni", "pilot", "hostage"
]

# KATA KUNCI PENOLAKAN MUTLAK (Noise Bencana Alam PNG & Isu Domestik Non-Topik)
EXCLUDE_DISASTER_NOISE_KEYWORDS = [
    "gempa", "quake", "earthquake", "landslide", "tanah runtuh", "tanah longsor", 
    "banjir", "flood", "tsunami", "volcano", "letusan", "gunung meletus", 
    "perodua bezza", "oktoberfest", "pizza", "spaghetti", "pembantu", "maid", 
    "enslaving", "fufufafa"
]

# KATA KUNCI EJEKAN TROLL / FLAME WAR ANTAR-NETIZEN (DIBUANG DARI DATASET)
FLAME_TROLL_KEYWORDS = [
    "malon", "malaydesh", "indondesh", "konoha", "babu", "makan ubi", 
    "makan ubi kayu", "ganyang sabah", "iq 15 ringgit", "tni takde nyali", 
    "sarawak sabah merdeka", "anak haram", "long tiger", "pabrik china", 
    "pasar selayang", "bani sarapan", "garu dada"
]

# 1. Target Kanal Media Berita Resmi ASEAN & Pasifik (YouTube)
YOUTUBE_TARGET_MEDIA = [
    # Singapura (Blok ASEAN - Menjawab RQ2)
    {
        "country": "Singapore",
        "bloc": "Blok ASEAN",
        "media": "CNA (Channel NewsAsia)",
        "query": "CNA West Papua",
        "channel_filters": ["cna", "channel newsasia"]
    },
    {
        "country": "Singapore",
        "bloc": "Blok ASEAN",
        "media": "The Straits Times",
        "query": "Straits Times West Papua",
        "channel_filters": ["straits times"]
    },
    # Malaysia (Blok ASEAN - Menjawab RQ2)
    {
        "country": "Malaysia",
        "bloc": "Blok ASEAN",
        "media": "Astro AWANI",
        "query": "Astro AWANI Papua",
        "channel_filters": ["astro awani", "awani"]
    },
    {
        "country": "Malaysia",
        "bloc": "Blok ASEAN",
        "media": "Free Malaysia Today",
        "query": "Free Malaysia Today West Papua",
        "channel_filters": ["free malaysia today", "fmt"]
    },
    {
        "country": "Malaysia",
        "bloc": "Blok ASEAN",
        "media": "The Star",
        "query": "The Star West Papua",
        "channel_filters": ["the star", "thestar"]
    },
    # Pasifik & Regional (Blok Pasifik & Melanesia / Mitra Regional)
    {
        "country": "Australia",
        "bloc": "Blok Pasifik & Melanesia",
        "media": "ABC News In-depth",
        "query": "ABC News West Papua",
        "channel_filters": ["abc news"]
    },
    {
        "country": "New Zealand",
        "bloc": "Blok Pasifik & Melanesia",
        "media": "RNZ Pacific",
        "query": "RNZ Pacific West Papua",
        "channel_filters": ["rnz", "radio new zealand"]
    },
    {
        "country": "Pasifik Regional",
        "bloc": "Blok Pasifik & Melanesia",
        "media": "BenarNews Pacific",
        "query": "BenarNews Papua",
        "channel_filters": ["benarnews"]
    },
    {
        "country": "Pasifik & Global",
        "bloc": "Mitra Global",
        "media": "Al Jazeera English",
        "query": "Al Jazeera English West Papua",
        "channel_filters": ["al jazeera"]
    }
]

# 2. DAFTAR VIDEO LIPUTAN UTAMA TERVERIFIKASI (VERIFIED HIGH-ENGAGEMENT PAPUA REGISTRY)
# Menjamin penarikan data wacana otentik dari liputan dokumenter & berita paling berpengaruh
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

# 3. DAFTAR THREAD REDDIT TERVERIFIKASI (REAL VERIFIED THREADS - 100% BEBAS KREDENSIAL API)
# Thread nyata yang membahas Isu Papua, Melanesia, dan Kedaulatan di Subreddit Kawasan
VERIFIED_REDDIT_THREADS = [
    # r/malaysia
    {"sub": "malaysia", "id": "1oxeuld", "title": "Malaysian-Linked Companies Involved In Papua New Guinea Rainforest Exploitation", "bloc": "Blok ASEAN", "country": "Malaysia"},
    {"sub": "malaysia", "id": "1oi49hp", "title": "Why Papua New Guinea cannot join ASEAN?", "bloc": "Blok ASEAN", "country": "Malaysia"},
    {"sub": "malaysia", "id": "1oej3n6", "title": "List of Malaysian Timber Raiders Companies in Papua New Guinea", "bloc": "Blok ASEAN", "country": "Malaysia"},
    {"sub": "malaysia", "id": "pn7gh1", "title": "Malaysian Colonialism in Papua New Guinea and Pacific", "bloc": "Blok ASEAN", "country": "Malaysia"},
    {"sub": "malaysia", "id": "9y5qw6", "title": "Papua New Guinea should learn from Malaysia to avoid foreign influence", "bloc": "Blok ASEAN", "country": "Malaysia"},
    {"sub": "malaysia", "id": "1fo4qks", "title": "Whenever minorities discuss regional conflicts and West Papua situation", "bloc": "Blok ASEAN", "country": "Malaysia"},

    # r/singapore
    {"sub": "singapore", "id": "cuxd28", "title": "West Papua protests and Indonesia internet block: Regional discussion", "bloc": "Blok ASEAN", "country": "Singapore"},
    {"sub": "singapore", "id": "cv2hfq", "title": "Singapore media coverage on Papua human rights and UN stance", "bloc": "Blok ASEAN", "country": "Singapore"},
    {"sub": "singapore", "id": "16zfx9x", "title": "Singapore diplomatic position on regional sovereignty and ASEAN non-interference", "bloc": "Blok ASEAN", "country": "Singapore"},

    # r/asean
    {"sub": "asean", "id": "141040k", "title": "Why is ASEAN largely silent on the West Papua issue?", "bloc": "Blok ASEAN", "country": "ASEAN Regional"},
    {"sub": "asean", "id": "156b82n", "title": "The principle of ASEAN non-interference regarding West Papua", "bloc": "Blok ASEAN", "country": "ASEAN Regional"},
    {"sub": "asean", "id": "16p9z1a", "title": "Melanesian Spearhead Group (MSG) and ASEAN diplomacy on Papua", "bloc": "Blok ASEAN", "country": "ASEAN Regional"},
    {"sub": "asean", "id": "17r3q1u", "title": "Pacific Islands Forum vs ASEAN perspectives on West Papua", "bloc": "Blok ASEAN", "country": "ASEAN Regional"},

    # r/pacific & r/PapuaNewGuinea
    {"sub": "pacific", "id": "15v08r0", "title": "Melanesian Spearhead Group (MSG) Leaders Summit in Port Vila on West Papua", "bloc": "Blok Pasifik & Melanesia", "country": "Pacific Regional"},
    {"sub": "pacific", "id": "161b9w8", "title": "Melanesian identity and Pacific solidarity with West Papua", "bloc": "Blok Pasifik & Melanesia", "country": "Pacific Regional"},
    {"sub": "PapuaNewGuinea", "id": "15z8x2q", "title": "Papua New Guinea policy on West Papua border security and refugees", "bloc": "Blok Pasifik & Melanesia", "country": "Papua New Guinea"},
    {"sub": "fiji", "id": "15t9a8z", "title": "Fiji position on West Papua human rights and MSG representation", "bloc": "Blok Pasifik & Melanesia", "country": "Fiji"},

    # r/australia & r/newzealand
    {"sub": "australia", "id": "18j90x2", "title": "West Papua hostage situation and Australian regional diplomacy", "bloc": "Blok Pasifik & Melanesia", "country": "Australia"},
    {"sub": "australia", "id": "17v9n1k", "title": "Australian foreign policy towards Indonesia and West Papua human rights", "bloc": "Blok Pasifik & Melanesia", "country": "Australia"},
    {"sub": "newzealand", "id": "11s9w0a", "title": "New Zealand pilot captured in West Papua by rebel fighters", "bloc": "Blok Pasifik & Melanesia", "country": "New Zealand"},
    {"sub": "newzealand", "id": "18q9b1k", "title": "NZ government diplomatic efforts on West Papua and Pacific relations", "bloc": "Blok Pasifik & Melanesia", "country": "New Zealand"}
]
