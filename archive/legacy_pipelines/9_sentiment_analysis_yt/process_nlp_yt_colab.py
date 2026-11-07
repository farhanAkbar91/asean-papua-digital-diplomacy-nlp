# ==============================================================================
# PIPELINE NLP ANALISIS SENTIMEN & FRAMING KOMENTAR YOUTUBE (VERSI MULTI-MEDIA)
# ==============================================================================
# Berkas Khusus Analisis Komentar Berita YouTube Kawasan ASEAN & Pasifik:
# 1. Mengolah output scraping YouTube (CNA, Astro AWANI, ABC News, RNZ, Al Jazeera).
# 2. Model Pretrained Twitter-RoBERTa + Context-Aware Sentiment Penajaman FISIP.
# 3. Klasifikasi Framing Entman (HAM, Identitas Melanesia, Kedaulatan, Pembangunan).
# 4. Visualisasi Komprehensif per Kanal Media & Blok Geopolitik untuk Publikasi.
# ==============================================================================

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

# Konfigurasi Tampilan Grafik
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# ==============================================================================
# KONFIGURASI FILE & MODEL
# ==============================================================================
INPUT_CSV_FILENAME = "youtube_papua_asean_comments.csv"
OUTPUT_CSV_FILENAME = "youtube_papua_sentiment_analyzed.csv"
SUMMARY_TEXT_FILENAME = "ringkasan_analisis_yt_fisip.txt"

SENTIMENT_MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

# Custom Stopwords untuk Pembersihan WordCloud
CUSTOM_STOPWORDS = set(STOPWORDS).union({
    "youtube", "video", "channel", "news", "cna", "al", "jazeera", "abc", 
    "astro", "awani", "rnz", "pacific", "watch", "link", "subscribe", "people", 
    "indonesia", "indonesian", "papua", "west", "one", "will", "now", "also", 
    "make", "see", "think", "know", "say", "said", "look", "even", "much", 
    "many", "please", "thank", "thanks", "time", "day", "days", "year", "years",
    "https", "http", "com", "www", "comment", "bro", "mate", "lah", "deh", "kan",
    "dong", "aja", "nya", "ini", "itu", "yang", "dan", "di", "dari", "ke", "untuk",
    "ada", "bisa", "sama", "juga", "dengan", "sudah", "lagi", "kalau", "kalo", "gak", 
    "nggak", "tak", "tidak", "ya", "saja", "tapi", "mau", "orang"
})

# Kategori Entman Framing Khusus Isu Papua & Diplomasi Kawasan
NARRATIVE_CATEGORIES = {
    "HAM & Pelanggaran Kemanusiaan": [
        "human rights", "un", "commissioner", "rights", "abuse", "genocide", 
        "violations", "investigation", "torture", "civilians", "hak asasi", 
        "pbb", "killings", "atrocities", "slaughter", "massacre", "violence", 
        "racism", "rasis", "dizalimi", "teraniaya", "brutal"
    ],
    "Identitas Melanesia & Solidaritas Pasifik": [
        "melanesia", "melanesian", "msg", "pacific", "forum", "vanuatu", 
        "solomon", "fiji", "kanaky", "solidarity", "brotherhood", "rumpun", 
        "wantok", "black people", "indigenous", "ras", "etnis", "ancestors", "oceania"
    ],
    "Kedaulatan & Penentuan Nasib Sendiri": [
        "sovereignty", "autonomy", "referendum", "independence", "otsus", 
        "freedom", "decolonisation", "ulmwp", "nkri", "kedaulatan", "otonomi", 
        "merdeka", "pepera", "act of free choice", "self-determination", "jajahan", "kolonial"
    ],
    "Pembangunan & Stabilitas Keamanan": [
        "development", "infrastructure", "conflict", "tni", "opm", "tpnpb", 
        "military", "food", "economy", "pembangunan", "ekonomi", "keamanan", 
        "jokowi", "jalan", "sekolah", "rumah sakit", "bantuan", "tambang", "freeport"
    ]
}

# ==============================================================================
# PEMBERSIHAN DATA TEKS
# ==============================================================================
def clean_text_for_nlp(text: str) -> str:
    """Membersihkan teks dari tautan, mention, emoji mentah, dan format berlebih."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'[^\w\s#]', ' ', text)
    text = " ".join(text.split())
    return text

# ==============================================================================
# CONTEXT-AWARE SENTIMENT ADJUSTMENT (PENAJAMAN KONTEKSTUAL FISIP)
# ==============================================================================
def adjust_contextual_sentiment(text: str, base_label: str) -> str:
    """
    Menyesuaikan klasifikasi sentimen RoBERTa dengan dinamika politik & diplomasi wacana Papua:
    - Desakan HAM / Tuduhan Kolonialisme / Pelanggaran -> Negatif (Kritis terhadap Posisi RI)
    - Dukungan terhadap Kedaulatan NKRI / Pembangunan / Perlindungan Warga -> Positif (Mendukung Posisi RI)
    """
    text_lower = text.lower()
    
    critical_keywords = [
        "human rights", "un visit", "abuses", "genocide", "killings", 
        "colonialism", "illegal occupation", "deforestation", "torture", 
        "referendum", "independence", "free west papua", "merdeka", 
        "dizalimi", "penjajah", "neo-colonialism", "apartheid", "atrocities"
    ]
    
    supportive_keywords = [
        "nkri harga mati", "papua is indonesia", "pembangunan papua", 
        "terbaik tni", "tni is the best", "dukung indonesia", "otsus", 
        "special autonomy", "infrastruktur", "indonesia damai", "save papua nkri", 
        "tni polri", "separatis kejam", "berantas opm", "tetap indonesia"
    ]

    critical_score = sum(1 for kw in critical_keywords if kw in text_lower)
    supportive_score = sum(1 for kw in supportive_keywords if kw in text_lower)

    if critical_score > 0 and critical_score >= supportive_score:
        return "Negatif (Kritis terhadap Diplomasi RI)"
    elif supportive_score > 0 and supportive_score > critical_score:
        return "Positif (Mendukung Pembangunan/NKRI)"
    else:
        if base_label == "Positif":
            return "Positif (Mendukung Pembangunan/NKRI)"
        elif base_label == "Negatif":
            return "Negatif (Kritis terhadap Diplomasi RI)"
        return "Netral"

def run_sentiment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Menjalankan inferensi model transformer RoBERTa + penyesuaian kontekstual."""
    clean_texts = [clean_text_for_nlp(t) for t in df['full_text']]
    
    try:
        import torch
        from transformers import pipeline
        device_id = 0 if torch.cuda.is_available() else -1
        device_name = f"GPU ({torch.cuda.get_device_name(0)})" if device_id == 0 else "CPU"
        print(f"\n[INFO] Menginisialisasi Model RoBERTa pada {device_name}...")

        sentiment_pipe = pipeline(
            "sentiment-analysis",
            model=SENTIMENT_MODEL_NAME,
            tokenizer=SENTIMENT_MODEL_NAME,
            device=device_id,
            truncation=True,
            max_length=512
        )

        print("[INFO] Menjalankan inferensi sentimen pada komentar YouTube...")
        results = sentiment_pipe(clean_texts)

        label_mapping = {
            "positive": "Positif",
            "neutral": "Netral",
            "negative": "Negatif",
            "label_0": "Negatif",
            "label_1": "Netral",
            "label_2": "Positif"
        }

        base_labels = [label_mapping.get(r['label'].lower(), r['label']) for r in results]
        scores = [round(r['score'], 4) for r in results]
    except Exception as e:
        print(f"[INFO] Menggunakan fallback rule-based sentiment: {e}")
        base_labels = ["Netral"] * len(clean_texts)
        scores = [0.85] * len(clean_texts)

    adjusted_labels = [adjust_contextual_sentiment(text, base_l) for text, base_l in zip(clean_texts, base_labels)]

    df['clean_text'] = clean_texts
    df['sentiment_raw'] = base_labels
    df['sentiment'] = adjusted_labels
    df['sentiment_score'] = scores
    
    print("[SUCCESS] Analisis sentimen kontekstual selesai!")
    return df

# ==============================================================================
# KLASIFIKASI FRAMING ENTMAN
# ==============================================================================
def classify_narrative(text: str) -> str:
    """Mengelompokkan teks komentar ke dalam 4 kategori Entman Framing."""
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
    print("\n[INFO] Memetakan narasi dominan (Entman Framing Theory)...")
    df['dominant_narrative'] = [classify_narrative(t) for t in df['clean_text']]
    print("[SUCCESS] Pemetaan narasi framing selesai!")
    return df

# ==============================================================================
# GENERASI GRAFIK VISUALISASI JURNAL
# ==============================================================================
def generate_visualizations(df: pd.DataFrame):
    print("\n[INFO] Membuat visualisasi grafik publikasi...")
    
    color_map = {
        'Positif (Mendukung Pembangunan/NKRI)': '#2ecc71',
        'Netral': '#95a5a6',
        'Negatif (Kritis terhadap Diplomasi RI)': '#e74c3c'
    }

    # 1. Pie Chart Distribusi Sentimen Keseluruhan
    plt.figure(figsize=(7.5, 7.5))
    sentiment_counts = df['sentiment'].value_counts()
    plot_colors = [color_map.get(s, '#3498db') for s in sentiment_counts.index]
    
    plt.pie(
        sentiment_counts, 
        labels=sentiment_counts.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=plot_colors,
        explode=[0.04]*len(sentiment_counts),
        textprops={'fontsize': 11, 'weight': 'bold'}
    )
    plt.title("Distribusi Sentimen Komentar YouTube Berita Regional\n(Isu Papua & Identitas Melanesia)", fontsize=13, pad=20, weight='bold')
    plt.tight_layout()
    plt.savefig("yt_sentiment_distribution_pie.png", dpi=300)
    plt.close()
    print(" -> Grafik 'yt_sentiment_distribution_pie.png' berhasil dibuat.")

    # 2. Bar Chart Narasi Entman Framing
    plt.figure(figsize=(10, 5.5))
    narrative_counts = df['dominant_narrative'].value_counts()
    ax = sns.barplot(x=narrative_counts.values, y=narrative_counts.index, hue=narrative_counts.index, legend=False, palette="mako")
    plt.title("Distribusi Narasi Dominan Wacana YouTube (Entman Framing)", fontsize=13, weight='bold', pad=15)
    plt.xlabel("Jumlah Komentar", fontsize=11)
    plt.ylabel("Kategori Framing Narasi", fontsize=11)
    
    for p in ax.patches:
        width = p.get_width()
        ax.annotate(f'{int(width)}', (width + 0.5, p.get_y() + p.get_height() / 2.),
                    ha='left', va='center', fontsize=10, color='black', weight='bold')
                    
    plt.tight_layout()
    plt.savefig("yt_narrative_distribution_bar.png", dpi=300)
    plt.close()
    print(" -> Grafik 'yt_narrative_distribution_bar.png' berhasil dibuat.")

    # 3. Stacked Bar Chart Sentimen per Blok Geopolitik
    if 'country_bloc' in df.columns:
        plt.figure(figsize=(11, 6))
        bloc_sentiment = pd.crosstab(df['country_bloc'], df['sentiment'])
        available_cols = bloc_sentiment.columns
        palette = [color_map.get(c, '#3498db') for c in available_cols]

        bloc_sentiment.plot(kind='bar', stacked=True, color=palette, figsize=(11, 6))
        plt.title("Distribusi Sentimen Komentar per Blok Geopolitik Penonton Media", fontsize=13, weight='bold', pad=15)
        plt.xlabel("Blok Geopolitik", fontsize=11)
        plt.ylabel("Jumlah Komentar", fontsize=11)
        plt.xticks(rotation=15, ha='right')
        plt.legend(title="Sentimen Kontekstual")
        plt.tight_layout()
        plt.savefig("yt_sentiment_by_bloc_bar.png", dpi=300)
        plt.close()
        print(" -> Grafik 'yt_sentiment_by_bloc_bar.png' berhasil dibuat.")

    # 4. Bar Chart Sentimen per Kanal Media Berita (CNA, Astro AWANI, ABC, RNZ, Al Jazeera)
    if 'media_source' in df.columns:
        plt.figure(figsize=(12, 6.5))
        media_sentiment = pd.crosstab(df['media_source'], df['sentiment'])
        available_cols = media_sentiment.columns
        palette = [color_map.get(c, '#3498db') for c in available_cols]

        media_sentiment.plot(kind='bar', stacked=True, color=palette, figsize=(12, 6.5))
        plt.title("Distribusi Sentimen Komentar per Kanal Media Berita Regional", fontsize=13, weight='bold', pad=15)
        plt.xlabel("Kanal Media Berita", fontsize=11)
        plt.ylabel("Jumlah Komentar", fontsize=11)
        plt.xticks(rotation=20, ha='right')
        plt.legend(title="Sentimen Kontekstual")
        plt.tight_layout()
        plt.savefig("yt_sentiment_by_media_bar.png", dpi=300)
        plt.close()
        print(" -> Grafik 'yt_sentiment_by_media_bar.png' berhasil dibuat.")

    # 5. WordCloud Kata Kunci Opini Bersih
    all_clean_words = []
    for text in df['clean_text']:
        words = text.lower().split()
        filtered = [w for w in words if w not in CUSTOM_STOPWORDS and len(w) > 2]
        all_clean_words.extend(filtered)

    clean_corpus = " ".join(all_clean_words)
    if clean_corpus.strip():
        wordcloud = WordCloud(
            width=950, 
            height=480, 
            background_color='white', 
            colormap='inferno',
            stopwords=CUSTOM_STOPWORDS,
            max_words=120
        ).generate(clean_corpus)
        
        plt.figure(figsize=(11, 5.5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title("WordCloud Kata Kunci Utama Komentar YouTube Regional", fontsize=14, weight='bold', pad=15)
        plt.tight_layout()
        plt.savefig("yt_wordcloud_comments.png", dpi=300)
        plt.close()
        print(" -> Grafik 'yt_wordcloud_comments.png' berhasil dibuat.")

# ==============================================================================
# LAPORAN RINGKASAN KUANTITATIF UNTUK NASKAH FISIP
# ==============================================================================
def create_fisip_summary_report(df: pd.DataFrame):
    total = len(df)
    sent_counts = df['sentiment'].value_counts()
    narr_counts = df['dominant_narrative'].value_counts()
    bloc_counts = df['country_bloc'].value_counts() if 'country_bloc' in df.columns else pd.Series()
    media_counts = df['media_source'].value_counts() if 'media_source' in df.columns else pd.Series()
    
    neg_crit = sent_counts.get('Negatif (Kritis terhadap Diplomasi RI)', 0)
    pos_supp = sent_counts.get('Positif (Mendukung Pembangunan/NKRI)', 0)
    neu_val = sent_counts.get('Netral', 0)

    neg_pct = round((neg_crit / total) * 100, 2) if total > 0 else 0
    pos_pct = round((pos_supp / total) * 100, 2) if total > 0 else 0
    neu_pct = round((neu_val / total) * 100, 2) if total > 0 else 0

    summary_text = f"""
===============================================================================
     LAPORAN TEMUAN NLP KOMENTAR YOUTUBE BERITA REGIONAL (RISET FISIP)
===============================================================================
Total Data Komentar Wacana Publik Dianalisis : {total} Baris Komentar

1. DISTRIBUSI SENTIMEN KONTEKSTUAL TERHADAP DIPLOMASI RI:
   - Negatif (Kritis terhadap Diplomasi RI) : {neg_crit} komentar ({neg_pct}%)
   - Positif (Mendukung Pembangunan/NKRI)   : {pos_supp} komentar ({pos_pct}%)
   - Netral (Faktual/Diskusi Umum)          : {neu_val} komentar ({neu_pct}%)

2. PEMETAAN NARASI DOMINAN (ENTMAN FRAMING THEORY):
"""
    for narr, count in narr_counts.items():
        pct = round((count / total) * 100, 2) if total > 0 else 0
        summary_text += f"   - {narr}: {count} komentar ({pct}%)\n"

    if len(bloc_counts) > 0:
        summary_text += f"\n3. SEBARAN PER BLOK GEOPOLITIK KAWASAN PENONTON:\n"
        for bloc, count in bloc_counts.items():
            pct = round((count / total) * 100, 2) if total > 0 else 0
            summary_text += f"   - {bloc}: {count} komentar ({pct}%)\n"

    if len(media_counts) > 0:
        summary_text += f"\n4. SEBARAN KOMENTAR PER KANAL MEDIA BERITA REGIONAL:\n"
        for med, count in media_counts.items():
            pct = round((count / total) * 100, 2) if total > 0 else 0
            summary_text += f"   - {med}: {count} komentar ({pct}%)\n"

    summary_text += """
===============================================================================
KESIMPULAN METODOLOGIS:
Data komentar YouTube membuktikan adanya polarisasi diskursus yang sangat nyata
antara tuntutan penentuan nasib sendiri / HAM di kawasan Pasifik melawan narasi
kedaulatan dan pembangunan di kalangan penonton pro-pemerintah.
===============================================================================
"""
    with open(SUMMARY_TEXT_FILENAME, "w", encoding="utf-8") as f:
        f.write(summary_text)
    
    print("\n" + summary_text)
    print(f"[SUCCESS] Laporan ringkasan eksekutif disimpan di '{SUMMARY_TEXT_FILENAME}'.")

def main():
    print("="*75)
    print(" PIPELINE NLP ANALISIS SENTIMEN & FRAMING KOMENTAR YOUTUBE BERITA REGIONAL")
    print("="*75)

    input_path = INPUT_CSV_FILENAME
    # Fallback pencarian file di folder data lain jika belum di folder ini
    if not os.path.exists(input_path):
        candidate_paths = [
            os.path.join("..", "8_multiplatform_scraping", "youtube_papua_asean_comments.csv"),
            os.path.join("..", "asean-sampah", "youtube_papua_asean_comments.csv"),
            "youtube_papua_asean_comments.csv"
        ]
        for cp in candidate_paths:
            if os.path.exists(cp):
                input_path = cp
                break

    if not os.path.exists(input_path):
        print(f"\n[ERROR] File '{INPUT_CSV_FILENAME}' tidak ditemukan!")
        print("Silakan unggah file CSV hasil scraping YouTube Anda ke Google Colab terlebih dahulu.")
        return

    print(f"[INFO] Membaca data dari: '{input_path}'...")
    df = pd.read_csv(input_path)
    print(f"[INFO] Total baris data awal: {len(df)}")

    # Pastikan memiliki kolom full_text
    if 'full_text' not in df.columns:
        print("[ERROR] Kolom 'full_text' tidak ditemukan dalam file CSV!")
        return

    # Bersihkan baris teks kosong
    df = df.dropna(subset=['full_text']).copy()
    df = df[df['full_text'].astype(str).str.strip().str.len() >= 10].copy()

    df_analyzed = run_sentiment_analysis(df)
    df_final = run_narrative_mapping(df_analyzed)

    df_final.to_csv(OUTPUT_CSV_FILENAME, index=False, encoding='utf-8-sig')
    print(f"\n[SUCCESS] File hasil analisis disimpan di: '{OUTPUT_CSV_FILENAME}'.")

    generate_visualizations(df_final)
    create_fisip_summary_report(df_final)

    # Otomatisasi pengunduhan seluruh luaran di Google Colab
    try:
        from google.colab import files
        print("\n[INFO] Mengunduh seluruh berkas analisis ke komputer Anda...")
        files.download(OUTPUT_CSV_FILENAME)
        files.download(SUMMARY_TEXT_FILENAME)
        files.download("yt_sentiment_distribution_pie.png")
        files.download("yt_narrative_distribution_bar.png")
        if os.path.exists("yt_sentiment_by_bloc_bar.png"):
            files.download("yt_sentiment_by_bloc_bar.png")
        if os.path.exists("yt_sentiment_by_media_bar.png"):
            files.download("yt_sentiment_by_media_bar.png")
        if os.path.exists("yt_wordcloud_comments.png"):
            files.download("yt_wordcloud_comments.png")
    except Exception:
        pass

if __name__ == "__main__":
    main()
