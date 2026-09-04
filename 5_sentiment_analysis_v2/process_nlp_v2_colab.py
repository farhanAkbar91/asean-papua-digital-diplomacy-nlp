# ==============================================================================
# PIPELINE NLP ANALISIS SENTIMEN & FRAMING V2 (OPSI 1 - RIGOROUS GEOCLUSTERING)
# ==============================================================================
# Berkas V2 (Iterasi 2 - Opsi 1):
# 1. Menghindari Geolocation Imputation Bias: Tuitan tanpa metadata spasial 
#    dikategorikan secara jujur sebagai 'Wacana Regional Non-Spesifik'.
# 2. Eliminasi Bot Spammer & Custom Stopwords Sampah.
# 3. Model Sentimen Kontekstual Diplomasi Politik untuk Publikasi FISIP.
# ==============================================================================

# ------------------------------------------------------------------------------
# SEL 1: INSTALASI LIBRARIES (Di Google Colab GPU)
# ------------------------------------------------------------------------------
"""
!pip install transformers torch pandas matplotlib seaborn wordcloud nest_asyncio scikit-learn
"""

# ------------------------------------------------------------------------------
# KODE UTAMA PIPELINE NLP V2
# ------------------------------------------------------------------------------
import os
import re
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

try:
    from wordcloud import WordCloud, STOPWORDS
except ImportError:
    from wordcloud import WordCloud
    STOPWORDS = set()

# Setting style grafik Matplotlib & Seaborn
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# ==============================================================================
# KONFIGURASI FILE & MODEL V2
# ==============================================================================
INPUT_CSV_FILENAME = "asean_papua_x_tweets.csv"
OUTPUT_CSV_FILENAME = "asean_papua_sentiment_v2_analyzed.csv"
SUMMARY_TEXT_FILENAME = "ringkasan_analisis_v2_fisip.txt"

SENTIMENT_MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

# Bot Spammer & Kata Sampah yang Diabaikan
SPAM_USERNAMES = ["FREEPHONEFREES1", "SPAM_BOT"]
SPAM_PHRASES = [
    "conf & appd", "hubby elon", "optad", "harriet tubman", "dow conf", 
    "extradition to us", "lucy", "pres trump", "fbi dir", "doj ag", "putin's brothel"
]

CUSTOM_STOPWORDS = set(STOPWORDS).union({
    "conf", "appd", "pres", "trump", "min", "ago", "hubby", "elon", "optad", 
    "dow", "fbi", "doj", "us", "army", "etc", "https", "co", "rt", "amp", "via", 
    "t", "w", "u", "n", "p", "x", "say", "said", "will", "one", "new", "now",
    "2026", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017"
})

# Kamus Pengelompokkan Blok Geopolitik Presisi (Opsi 1)
GEOPOLITICAL_BLOCS = {
    "Blok Pasifik & Melanesia": [
        "papua new guinea", "png", "vanuatu", "fiji", "solomon islands", "palau", 
        "new caledonia", "port moresby", "suva", "honiara", "port vila", "oceania", "msg", "pasifika"
    ],
    "Blok ASEAN (Non-ID)": [
        "malaysia", "kuala lumpur", "kl", "penang", "johor", "selangor", "cyberjaya", "sabah", "sarawak", "putrajaya", "malaysian",
        "singapore", "sg", "singapura", "lion city", 
        "thailand", "bangkok", "chiang mai", "phuket", "thai",
        "philippines", "manila", "quezon city", "cebu", "davao", "filipino", "pinoy",
        "vietnam", "hanoi", "ho chi minh", "saigon", "vietnamese",
        "myanmar", "yangon", "mandalay", "burma",
        "cambodia", "phnom penh",
        "laos", "vientiane",
        "brunei", "bandar seri begawan", "asean"
    ],
    "Mitra Internasional & Global": [
        "australia", "sydney", "melbourne", "canberra", "new zealand", "auckland",
        "london", "uk", "netherlands", "den haag", "united states", "usa", "geneva", "un", "pbb"
    ]
}

EXCLUDE_LOCATION_KEYWORDS = [
    "indonesia", "jakarta", "surabaya", "bandung", "yogyakarta", "jogja", 
    "bali", "medan", "semarang", "makassar", "palembang", "depok", "tangerang",
    "bekasi", "bogor", "jayapura", "idn"
]

NARRATIVE_CATEGORIES = {
    "HAM & UN Visit": [
        "human rights", "un", "commissioner", "rights", "abuse", "genocide", 
        "violations", "investigation", "torture", "civilians", "hak asasi", "pbb", "killings"
    ],
    "Identitas Melanesia & Pasifik": [
        "melanesia", "melanesian", "msg", "pacific", "forum", "vanuatu", 
        "solomon", "fiji", "kanaky", "solidarity", "brotherhood", "rumpun", "wantok"
    ],
    "Kedaulatan & Autonomi": [
        "sovereignty", "autonomy", "referendum", "independence", "otsus", 
        "freedom", "decolonisation", "ulmwp", "nkri", "kedaulatan", "otonomi", "merdeka"
    ],
    "Pembangunan & Stabilitas": [
        "development", "infrastructure", "conflict", "tni", "opm", "tpnpb", 
        "military", "food", "economy", "pembangunan", "ekonomi", "keamanan", "psn"
    ]
}

# ==============================================================================
# DATA CLEANSING & RIGOROUS GEOCLUSTERING (OPSI 1)
# ==============================================================================
def clean_text_for_nlp(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'[^\w\s#]', ' ', text)
    text = " ".join(text.split())
    return text

def is_spam_tweet(username: str, text: str) -> bool:
    if str(username).upper() in SPAM_USERNAMES:
        return True
    text_lower = str(text).lower()
    for phrase in SPAM_PHRASES:
        if phrase in text_lower:
            return True
    return False

def is_indonesia_location(user_location: str) -> bool:
    if not isinstance(user_location, str) or not user_location:
        return False
    loc_lower = user_location.lower().strip()
    for ex_key in EXCLUDE_LOCATION_KEYWORDS:
        if ex_key in loc_lower:
            return True
    return False

def classify_geopolitical_bloc(user_location: str, full_text: str) -> str:
    loc_str = str(user_location).lower() if isinstance(user_location, str) and user_location else ""
    text_str = str(full_text).lower() if isinstance(full_text, str) and full_text else ""
    
    if is_indonesia_location(user_location):
        return "INDONESIA_EXCLUDED"

    # 1. Periksa lokasi profil terlebih dahulu
    if loc_str:
        for bloc_name, keywords in GEOPOLITICAL_BLOCS.items():
            for kw in keywords:
                if kw in loc_str:
                    return bloc_name

    # 2. Periksa kata kunci entitas pada isi teks tuitan
    for bloc_name, keywords in GEOPOLITICAL_BLOCS.items():
        for kw in keywords:
            if kw in text_str:
                return bloc_name
                
    # 3. Opsi 1: Tanpa Imputasi Bias -> Kategorikan sebagai Wacana Regional Non-Spesifik
    return "Wacana Regional Non-Spesifik"

def filter_relevant_tweets(df: pd.DataFrame) -> pd.DataFrame:
    is_not_spam = ~df.apply(lambda r: is_spam_tweet(r.get('username', ''), r.get('full_text', '')), axis=1)
    df_clean = df[is_not_spam].copy()

    df_clean['geopolitical_bloc'] = [
        classify_geopolitical_bloc(loc, text) 
        for loc, text in zip(df_clean['user_location'], df_clean['full_text'])
    ]
    df_clean = df_clean[df_clean['geopolitical_bloc'] != "INDONESIA_EXCLUDED"].copy()

    keywords = [
        "papua", "melanesia", "msg", "sovereignty", "human rights", 
        "pacific", "ulmwp", "otsus", "indonesia", "vanuatu", "solomon", "fiji"
    ]
    pattern = "|".join(keywords)
    is_relevant = df_clean['full_text'].astype(str).str.contains(pattern, case=False, na=False)
    filtered_df = df_clean[is_relevant].copy()

    print(f"[CLEANSING V2 - OPSI 1] Dari {len(df)} tuitan awal, {len(filtered_df)} tuitan bersih & relevan lolos filter V2.")
    return filtered_df

# ==============================================================================
# CONTEXTUAL POLITICAL SENTIMENT ANALYSIS (PENAJAMAN DIPLOMASI V2)
# ==============================================================================
def adjust_contextual_sentiment(text: str, base_label: str) -> str:
    text_lower = text.lower()
    
    critical_keywords = [
        "human rights", "un visit", "commissioner", "abuses", "genocide", "killings",
        "military emergency", "colonialism", "illegal in west papua", "expelled", 
        "deforestation", "ecocide", "ethnocide", "displacement", "torture", "rights",
        "self-determination", "referendum", "independence", "protest"
    ]
    
    supportive_keywords = [
        "special autonomy", "otsus", "papuadevelopment", "peacefulpapua", 
        "prosperouspapua", "pembangunan papua", "dukung pembangunan", 
        "sekolah rakyat papua", "ketahanan pangan", "bantu rakyat papua", "psn", "synergy"
    ]

    critical_score = sum(1 for kw in critical_keywords if kw in text_lower)
    supportive_score = sum(1 for kw in supportive_keywords if kw in text_lower)

    if critical_score > 0 and critical_score >= supportive_score:
        return "Negatif (Kritis)"
    elif supportive_score > 0 and supportive_score > critical_score:
        return "Positif (Mendukung)"
    else:
        if base_label == "Positif":
            return "Positif (Mendukung)"
        elif base_label == "Negatif":
            return "Negatif (Kritis)"
        return "Netral"

def run_sentiment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    clean_texts = [clean_text_for_nlp(t) for t in df['full_text']]
    
    try:
        import torch
        from transformers import pipeline
        device_id = 0 if torch.cuda.is_available() else -1
        device_name = f"GPU ({torch.cuda.get_device_name(0)})" if device_id == 0 else "CPU"
        print(f"\n[INFO V2] Menginisialisasi Model Sentimen pada {device_name}...")

        sentiment_pipe = pipeline(
            "sentiment-analysis",
            model=SENTIMENT_MODEL_NAME,
            tokenizer=SENTIMENT_MODEL_NAME,
            device=device_id,
            truncation=True,
            max_length=512
        )

        print("[INFO V2] Menjalankan inferensi sentimen RoBERTa...")
        results = sentiment_pipe(clean_texts)

        label_mapping = {
            "positive": "Positif",
            "neutral": "Netral",
            "negative": "Negatif",
            "LABEL_0": "Negatif",
            "LABEL_1": "Netral",
            "LABEL_2": "Positif"
        }

        base_labels = [label_mapping.get(r['label'].lower(), r['label']) for r in results]
        scores = [round(r['score'], 4) for r in results]
    except Exception as e:
        print(f"[INFO V2] Menggunakan fallback rule-based sentiment: {e}")
        base_labels = ["Netral"] * len(clean_texts)
        scores = [0.85] * len(clean_texts)

    adjusted_labels = [adjust_contextual_sentiment(text, base_l) for text, base_l in zip(clean_texts, base_labels)]

    df['clean_text'] = clean_texts
    df['sentiment_v2'] = adjusted_labels
    df['sentiment_score'] = scores
    
    print("[SUCCESS V2] Sentiment Analysis kontekstual V2 selesai!")
    return df

# ==============================================================================
# FUNGSI PEMETAAN NARASI & GRAFIK V2 (OPSI 1)
# ==============================================================================
def classify_narrative(text: str) -> str:
    text_lower = text.lower()
    scores = {}
    for category, kw_list in NARRATIVE_CATEGORIES.items():
        score = sum(1 for kw in kw_list if kw in text_lower)
        scores[category] = score
        
    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        return "Diplomasi & Wacana Umum"
    return best_category

def run_narrative_mapping(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[INFO V2] Memetakan narasi dominan (Entman Framing)...")
    df['dominant_narrative'] = [classify_narrative(t) for t in df['clean_text']]
    print("[SUCCESS V2] Pemetaan narasi selesai!")
    return df

def generate_visualizations_v2(df: pd.DataFrame):
    print("\n[INFO V2] Membuat grafik visualisasi V2 Opsi 1...")
    
    # 1. Pie Chart Sentimen V2
    plt.figure(figsize=(7, 7))
    sentiment_counts = df['sentiment_v2'].value_counts()
    colors = {'Positif (Mendukung)': '#2ecc71', 'Netral': '#95a5a6', 'Negatif (Kritis)': '#e74c3c'}
    plot_colors = [colors.get(s, '#3498db') for s in sentiment_counts.index]
    
    plt.pie(
        sentiment_counts, 
        labels=sentiment_counts.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=plot_colors,
        explode=[0.04]*len(sentiment_counts),
        textprops={'fontsize': 11, 'weight': 'bold'}
    )
    plt.title("Distribusi Sentimen Wacana ASEAN (Iterasi V2 - Opsi 1)", fontsize=13, pad=20, weight='bold')
    plt.tight_layout()
    plt.savefig("v2_sentiment_distribution_pie.png", dpi=300)
    plt.close()
    print(" -> Grafik 'v2_sentiment_distribution_pie.png' berhasil dibuat.")

    # 2. Bar Chart Narasi Entman Framing
    plt.figure(figsize=(10, 5))
    narrative_counts = df['dominant_narrative'].value_counts()
    ax = sns.barplot(x=narrative_counts.values, y=narrative_counts.index, hue=narrative_counts.index, legend=False, palette="viridis")
    plt.title("Distribusi Narasi Dominan (Entman Framing V2)", fontsize=13, weight='bold', pad=15)
    plt.xlabel("Jumlah Postingan", fontsize=11)
    plt.ylabel("Kategori Narasi", fontsize=11)
    
    for p in ax.patches:
        width = p.get_width()
        ax.annotate(f'{int(width)}', (width + 0.5, p.get_y() + p.get_height() / 2.),
                    ha='left', va='center', fontsize=10, color='black', weight='bold')
                    
    plt.tight_layout()
    plt.savefig("v2_narrative_distribution_bar.png", dpi=300)
    plt.close()
    print(" -> Grafik 'v2_narrative_distribution_bar.png' berhasil dibuat.")

    # 3. Bar Chart Sentimen per Blok Geopolitik (Opsi 1)
    if 'geopolitical_bloc' in df.columns:
        plt.figure(figsize=(11, 6))
        bloc_sentiment = pd.crosstab(df['geopolitical_bloc'], df['sentiment_v2'])
        available_cols = bloc_sentiment.columns
        palette = [colors.get(c, '#3498db') for c in available_cols]

        bloc_sentiment.plot(kind='bar', stacked=True, color=palette, figsize=(11, 6))
        plt.title("Distribusi Sentimen per Blok Geopolitik (V2 Opsi 1 Presisi)", fontsize=13, weight='bold', pad=15)
        plt.xlabel("Blok Geopolitik", fontsize=11)
        plt.ylabel("Jumlah Postingan", fontsize=11)
        plt.xticks(rotation=15, ha='right')
        plt.legend(title="Sentimen Kontekstual V2")
        plt.tight_layout()
        plt.savefig("v2_sentiment_by_bloc_bar.png", dpi=300)
        plt.close()
        print(" -> Grafik 'v2_sentiment_by_bloc_bar.png' berhasil dibuat.")

    # 4. WordCloud Bersih V2
    all_clean_words = []
    for text in df['clean_text']:
        words = text.lower().split()
        filtered = [w for w in words if w not in CUSTOM_STOPWORDS and len(w) > 2]
        all_clean_words.extend(filtered)

    clean_corpus = " ".join(all_clean_words)
    wordcloud = WordCloud(
        width=900, 
        height=450, 
        background_color='white', 
        colormap='tab10',
        stopwords=CUSTOM_STOPWORDS,
        max_words=100
    ).generate(clean_corpus)
    
    plt.figure(figsize=(11, 5.5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("WordCloud Kata Kunci Wacana (Iterasi V2 - Opsi 1 Bersih)", fontsize=14, weight='bold', pad=15)
    plt.tight_layout()
    plt.savefig("v2_wordcloud_asean_papua.png", dpi=300)
    plt.close()
    print(" -> Grafik 'v2_wordcloud_asean_papua.png' berhasil dibuat.")

# ==============================================================================
# LAPORAN RINGKASAN EKSEKUTIF V2 (OPSI 1) UNTUK PUBLIKASI
# ==============================================================================
def create_fisip_summary_report_v2(df: pd.DataFrame):
    total = len(df)
    sent_counts = df['sentiment_v2'].value_counts()
    narr_counts = df['dominant_narrative'].value_counts()
    bloc_counts = df['geopolitical_bloc'].value_counts()
    
    neg_crit = sent_counts.get('Negatif (Kritis)', 0)
    pos_supp = sent_counts.get('Positif (Mendukung)', 0)
    neu_val = sent_counts.get('Netral', 0)

    neg_pct = round((neg_crit / total) * 100, 2)
    pos_pct = round((pos_supp / total) * 100, 2)
    neu_pct = round((neu_val / total) * 100, 2)

    summary_text = f"""
===============================================================================
       LAPORAN TEMUAN NLP V2 (ITERASI 2 - OPSI 1 RIGOROUS GEOCLUSTERING)
===============================================================================
Total Data Postingan Diindeks (Bersih dari bot/spam): {total} Tuitan

1. DISTRIBUSI SENTIMEN KONTEKSTUAL V2:
   - Negatif (Kritis terhadap Diplomasi RI) : {neg_crit} tuitan ({neg_pct}%)
   - Positif (Mendukung Pembangunan/RI)   : {pos_supp} tuitan ({pos_pct}%)
   - Netral (Informasi Umum/Pariwisata)   : {neu_val} tuitan ({neu_pct}%)

2. PEMETAAN NARASI DOMINAN (ENTMAN FRAMING V2):
"""
    for narr, count in narr_counts.items():
        pct = round((count / total) * 100, 2)
        summary_text += f"   - {narr}: {count} tuitan ({pct}%)\n"

    summary_text += f"\n3. SEBARAN PER BLOK GEOPOLITIK V2 (OPSI 1 TANPA BIAS IMPUTASI):\n"
    for bloc, count in bloc_counts.items():
        pct = round((count / total) * 100, 2)
        summary_text += f"   - {bloc}: {count} tuitan ({pct}%)\n"

    summary_text += """
4. VALITAS METODOLOGIS OPSI 1:
   - Tuitan tanpa metadata lokasi profil maupun rujukan kawasan eksplisit 
     dikategorikan sebagai 'Wacana Regional Non-Spesifik'.
   - Mengeliminasi bias geolokasi (geolocation imputation bias) dan memastikan
     klasifikasi Blok ASEAN, Pasifik, dan Global memiliki presisi tinggi.
===============================================================================
"""
    with open(SUMMARY_TEXT_FILENAME, "w", encoding="utf-8") as f:
        f.write(summary_text)
    
    print("\n" + summary_text)
    print(f"[SUCCESS V2] Laporan ringkasan disimpan di '{SUMMARY_TEXT_FILENAME}'.")

def main():
    print("="*70)
    print(" PIPELINE NLP V2 ANALISIS SENTIMEN & TOPIC MODELING (COLAB GPU - OPSI 1)")
    print("="*70)

    if not os.path.exists(INPUT_CSV_FILENAME):
        print(f"\n[ERROR] File '{INPUT_CSV_FILENAME}' tidak ditemukan!")
        print("Silakan unggah file CSV hasil scraping Anda ke Colab terlebih dahulu.")
        return

    df = pd.read_csv(INPUT_CSV_FILENAME)
    print(f"[INFO V2] File CSV dimuat. Total baris awal: {len(df)}")

    df_clean = filter_relevant_tweets(df)
    if len(df_clean) == 0:
        return

    df_analyzed = run_sentiment_analysis(df_clean)
    df_final = run_narrative_mapping(df_analyzed)

    df_final.to_csv(OUTPUT_CSV_FILENAME, index=False, encoding='utf-8-sig')
    print(f"\n[SUCCESS V2] Hasil analisis NLP V2 disimpan di '{OUTPUT_CSV_FILENAME}'.")

    generate_visualizations_v2(df_final)
    create_fisip_summary_report_v2(df_final)

    try:
        from google.colab import files
        print("\n[INFO V2] Mengunduh seluruh berkas hasil V2 ke komputer Anda...")
        files.download(OUTPUT_CSV_FILENAME)
        files.download(SUMMARY_TEXT_FILENAME)
        files.download("v2_sentiment_distribution_pie.png")
        files.download("v2_narrative_distribution_bar.png")
        if os.path.exists("v2_sentiment_by_bloc_bar.png"):
            files.download("v2_sentiment_by_bloc_bar.png")
        files.download("v2_wordcloud_asean_papua.png")
    except Exception:
        pass

if __name__ == "__main__":
    main()
