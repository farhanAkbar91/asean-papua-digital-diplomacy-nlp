# Implementation Plan - Pipeline NLP (Sentiment Analysis, Topic Modeling, & Visualisasi FISIP)

Rencana ini mencakup pembangunan pipeline pengolahan data teks hasil *scraping* X (Twitter) berbasis GPU di Google Colab. Pipeline ini melakukan pembersihan *noise*, klasifikasi sentimen menggunakan model Transformer (Hugging Face), pemetaan narasi/topik (*Entman Framing*), serta pembuatan grafik visualisasi untuk diserahkan ke tim FISIP.

## User Review Required

> [!IMPORTANT]
> **Penggunaan GPU di Colab**: Proses *Sentiment Analysis* dan *Topic Modeling* akan memanfaatkan akselerator **GPU T4 (gratis di Colab)** menggunakan library `transformers`, `torch`, `sentence-transformers`, `bertopic`, `matplotlib`, dan `seaborn`.

> [!TIP]
> **Model NLP yang Digunakan**: 
> - **Sentiment Analysis**: `cardiffnlp/twitter-roberta-base-sentiment-latest` (SOTA Model sentimen Twitter).
> - **Topic Modeling / Framing**: *BERTopic* & *Zero-Shot Classification* (`facebook/bart-large-mnli`) untuk mengelompokkan teks ke kluster narasi FISIP (HAM, Kedaulatan, Identitas Melanesia, Pembangunan/Konflik).

---

## Open Questions

> [!IMPORTANT]
> 1. **File Input CSV**: Apakah nama file CSV yang baru saja Anda *download* dari Colab scraping adalah `asean_papua_x_tweets.csv`?
> 2. **Kategori Narasi FISIP**: Apakah 4 kategori narasi dasar ini sudah pas untuk tim FISIP:
>    - **HAM & UN Visit** (Pelanggaran HAM, Kunjungan PBB, Korban)
>    - **Identitas Melanesia & MSG/Pasifik** (Ikatan Rumpun Melanesia, Dukungan Negara Pasifik)
>    - **Kedaulatan & Autonomi** (Otonomi Khusus, Kedaulatan NKRI, Hukum Internasional)
>    - **Pembangunan & Stabilitas** (Infrastruktur, Konflik Bersenjata/OPM/TNI)

---

## Proposed Changes

### NLP Processing & Visualization Component

#### [NEW] [process_nlp_colab.ipynb](file:///d:/portfolio/asean/process_nlp_colab.ipynb)
- File Jupyter Notebook untuk Google Colab (GPU execution) yang berisi 4 sel:
  1. **Sel 1**: Instalasi pustaka `transformers`, `torch`, `bertopic`, `wordcloud`, `matplotlib`, `seaborn`.
  2. **Sel 2**: Upload file CSV `asean_papua_x_tweets.csv`.
  3. **Sel 3 (Core Pipeline)**:
     - **Cleansing & Noise Filtering**: Menghapus spam/tuitan yang tidak relevan, mentranslasikan teks non-Inggris (bila ada), menghapus URL/mention/emoji.
     - **GPU Sentiment Inference**: Menghitung skor probabilitas & label sentimen (*Positive*, *Neutral*, *Negative*).
     - **Framing & Topic Modeling**: Pengelompokkan narasi otomatis & *Zero-Shot Framing*.
     - **Grafik & Visualisasi**: Pie Chart Sentimen, Bar Chart Distribusi Narasi per Negara, dan WordCloud.
  4. **Sel 4**: Otomatis mengunduh CSV hasil analisis (`asean_papua_sentiment_analyzed.csv`) dan paket grafik visualisasi (`png`).

#### [NEW] [process_nlp_colab.py](file:///d:/portfolio/asean/process_nlp_colab.py)
- Berkas skrip Python mandiri *all-in-one* yang dapat langsung di-*copy-paste* ke sel Colab.

---

## Verification Plan

### Automated Tests
- Menjalankan uji kompilasi dan sintaks `python -m py_compile process_nlp_colab.py`.
- Memastikan pemrosesan `pandas`, `transformers`, dan `matplotlib` berjalan tanpa sintaks error.

### Manual Verification
- Pengguna menjalankan sel di Google Colab dengan GPU T4.
- Memeriksa file output `asean_papua_sentiment_analyzed.csv` untuk memastikan kolom `sentiment`, `sentiment_score`, dan `dominant_narrative` terisi dengan akurat.
- Memeriksa tampilan grafik visualisasi yang dihasilkan di Colab.
