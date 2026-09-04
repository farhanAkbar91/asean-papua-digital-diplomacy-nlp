# ASEAN-Papua Digital Diplomacy NLP Pipeline
### Multi-Platform Computational Social Science & Data Triangulation Architecture

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c?logo=pytorch)](https://pytorch.org/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-ffcc00?logo=huggingface)](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)
[![Scopus Target](https://img.shields.io/badge/Research-Scopus%20Indexed%20FISIP-4c1d95)](file:///d:/portfolio/asean/MABA%20SCOPUS.pdf)
[![Triangulation](https://img.shields.io/badge/Data%20Triangulation-X%20%7C%20YouTube%20%7C%20News-059669)](#-the-golden-triangle-triangulasi-data-n--1571)
[![License](https://img.shields.io/badge/License-MIT-gray)](LICENSE)

Repositori ini berisi **pipeline komputasional, rekayasa data (*data engineering*), dan pemodelan Natural Language Processing (NLP)** untuk menganalisis wacana digital, framing media, dan sentimen publik internasional terkait **Isu Papua dan Klaim Identitas Kemelanesiaan di Kawasan ASEAN dan Pasifik**.

Riset ini dirancang sebagai pemenuhan **Research Question 1 (RQ1)** dalam kerangka riset kolaboratif multidisiplin (Teknologi Informasi, Sosiologi, dan Hubungan Internasional) untuk target publikasi jurnal internasional bereputasi tinggi (**Scopus Q1/Q2**).

---

## 📐 The Golden Triangle: Triangulasi Data ($N = 1.571$)

Riset ini mengadopsi pendekatan **triangulasi multi-platform** untuk mengatasi bias algoritma tunggal media sosial:

```
                      [ MEDIA MASSA RESMI ]
                 (Agenda Setting Institusional)
                       N = 312 Artikel
                             / \
                            /   \
                           /     \
                          /       \
                         /  RISET  \
                        /   PAPUA   \
                       /   KOMPUTASI \
                      /_______________\
      [ PLATFORM X (TWITTER) ]      [ KOMENTAR YOUTUBE ]
       (Aktivisme Transnasional)    (Debat Dialektis Publik)
             N = 375 Tuitan              N = 884 Komentar
```

| Pilar Platform | Sumber Data | Jumlah Korpus | Karakteristik Wacana Ilmiah |
| :--- | :--- | :---: | :--- |
| **1. Platform X (Twitter)** | Postingan Publik Akun Kawasan | **375** tuitan | **Aktivisme Digital**: Kampanye hashtag satu arah, seruan kunjungan PBB, dan solidaritas diaspora Pasifik. |
| **2. YouTube Comments** | Komentar Video Berita Arus Utama | **884** komentar | **Debat Dialektis Publik**: Respon publik awam dan terdidik terhadap liputan audiovisual (CNA, Awani, ABC, Al Jazeera). |
| **3. Media Berita Online** | Portal Pers Resmi Singapura, Malaysia, Pasifik | **312** artikel utuh | **Agenda Setting Institusional**: Pemberitaan formal kawat berita, hukum internasional, dan kebijakan resmi negara. |
| **TOTAL MASTER KORPUS** | **3 Pilar Terintegrasi** | **1.571 data** | **Basis empiris utuh bebas bias platform tunggal**. |

---

## 🧠 Metodologi Komputasional & Arsitektur NLP

```
┌─────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│ Web Crawlers &  │ ───► │  Data Sanitation &      │ ───► │ Deep Learning Model:    │
│ Platform Scraper│      │  Anti-Noise Filtering   │      │ Twitter-RoBERTa (base)  │
└─────────────────┘      └─────────────────────────┘      └─────────────────────────┘
                                                                       │
                                                                       ▼
┌─────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│ Master Dataset  │ ◄─── │ Entman Framing Lexicon: │ ◄─── │ Context-Aware Diplomatic│
│ (1.571 Records) │      │ 5 Dominant Narratives   │      │ Rule-Based Adjustment   │
└─────────────────┘      └─────────────────────────┘      └─────────────────────────┘
```

1. **Model Transformer**: Menggunakan Pretrained Model `cardiffnlp/twitter-roberta-base-sentiment-latest` via Hugging Face Transformers & PyTorch.
2. **Inverted Pyramid Lead Processing**: Menganalisis judul + *lead paragraph* (250 kata pertama) untuk inferensi sentimen artikel berita panjang, dan teks utuh untuk anotasi framing.
3. **Penajaman Kontekstual Hubungan Internasional**: Rule-based adjustment yang menyelaraskan prediksi semantik umum dengan dinamika diplomasi kedaulatan vs isu pelanggaran HAM.
4. **Operasionalisasi Entman Framing (5 Dimensi)**:
   * **HAM & Pelanggaran Kemanusiaan**: Desakan akses PBB, investigasi independen, perlindungan sipil.
   * **Identitas Melanesia & Solidaritas Pasifik**: Kekerabatan ras, forum MSG (*Melanesian Spearhead Group*), ikatan budaya Pasifik.
   * **Kedaulatan & Penentuan Nasib Sendiri**: Tuntutan referendum, dekolonisasi, status Pepera 1969 vs integritas teritorial NKRI.
   * **Pembangunan & Stabilitas Keamanan**: Kasus sandera pilot, penegakan hukum aparat, investasi strategis energi/SDA.
   * **Diplomasi & Hubungan Internasional**: Hubungan bilateral, norma *ASEAN Non-Interference*, kaukus internasional.

---

## 📊 Ringkasan Temuan Awal Komputasional

* **Distribusi Sentimen Teranotasi**:
  * **Netral (Faktual/Diskusi Umum)**: `757 data` (**48.19%**)
  * **Negatif (Kritis terhadap Posisi RI)**: `650 data` (**41.37%**)
  * **Positif (Mendukung Kedaulatan/Pembangunan RI)**: `164 data` (**10.44%**)
* **Distribusi Blok Geopolitik Kawasan**:
  * **Mitra Global**: `750 data` (**47.74%**)
  * **Blok ASEAN (Singapura & Malaysia)**: `493 data` (**31.38%**)
  * **Blok Pasifik & Melanesia**: `287 data` (**18.27%**)
  * **Wacana Regional Non-Spesifik**: `41 data` (**2.61%**)
* **Temuan Kunci Sikap Pers ASEAN (RQ2)**:
  * Media arus utama Singapura (*CNA, The Straits Times*) dan Malaysia (*The Star, Astro AWANI*) menunjukkan tingkat pemberitaan netral-faktual dan positif mencapai **~69%**, mencerminkan kepatuhan kuat terhadap prinsip *ASEAN Non-Interference*.
  * Kritik terhadap posisi RI terkonsentrasi di media Pasifik (*RNZ Pacific, ABC News Australia*) dan *Al Jazeera English*.

---

## 🗂️ Struktur Direktori Proyek

Proyek ini disusun secara berurutan dan transparan untuk mendokumentasikan setiap iterasi rekayasa data:

```text
asean-papua-digital-diplomacy-nlp/
├── 📁 0_data/                      <-- Korpus data mentah X, YouTube, dan Berita Online
├── 📁 1_scraping/                  <-- Modul eksperimen scraping X (Twikit Session-Based)
├── 📁 2_sentiment_analysis/        <-- Baseline model NLP iterasi 1
├── 📁 3_hasil1_x/                  <-- Output sampel uji coba lokal iterasi 1
├── 📁 4_hasil2_x/                  <-- Evaluasi komputasional hasil scraping X awal
├── 📁 5_sentiment_analysis_v2/     <-- Pipeline NLP V2 (Context-Aware Adjustment)
├── 📁 6_hasil3_x/                  <-- Output iterasi 2 data X
├── 📁 7_hasil4_x/                  <-- Hasil final data X (375 data bersih - Opsi 1 Geoclustering)
├── 📁 8_multiplatform_scraping/    <-- Arsitektur scraper YouTube (30 Registry Video Berita)
├── 📁 9_sentiment_analysis_yt/     <-- Pipeline NLP khusus komentar berita YouTube
├── 📁 10_hasil5_yt/                <-- Hasil final analisis komentar YouTube (884 data bersih)
├── 📁 11_media_berita_scraping/    <-- Crawler portal media berita (Google News RSS & Decoder)
├── 📁 12_sentiment_analysis_news/  <-- Pipeline NLP teks berita (Inverted Pyramid Lead Processing)
├── 📁 13_hasil_news/               <-- Hasil final analisis media berita online (312 artikel)
└── 📁 14_laporan_dan_master_dataset/ <-- FOLDER UTAMA SERAH-TERIMA DOKUMEN:
    ├── master_triangulation_asean_papua.csv    (Master dataset terpadu 1.571 data)
    ├── Laporan_Teknis_RQ1_Data_NLP_Papua_ASEAN.docx (Laporan teknis format Word)
    ├── Laporan_Teknis_RQ1_Data_NLP_Papua_ASEAN.pdf  (Laporan teknis format PDF)
    └── README.md
```

---

## 🚀 Cara Menjalankan Pipeline (Reproduction Guide)

Seluruh modul komputasional dirancang kompatibel untuk dijalankan pada mesin lokal maupun **Google Colab (CPU/GPU)**:

### 1. Kloning Repositori
```bash
git clone https://github.com/USERNAME/asean-papua-digital-diplomacy-nlp.git
cd asean-papua-digital-diplomacy-nlp
```

### 2. Instalasi Dependensi
```bash
pip install -r 14_laporan_dan_master_dataset/../12_sentiment_analysis_news/requirements.txt
```

### 3. Menjalankan Pipeline NLP
* **Data X / Twitter**: Buka [`5_sentiment_analysis_v2/process_nlp_v2_colab.ipynb`](5_sentiment_analysis_v2/process_nlp_v2_colab.ipynb)
* **Komentar YouTube**: Buka [`9_sentiment_analysis_yt/process_nlp_yt_colab.ipynb`](9_sentiment_analysis_yt/process_nlp_yt_colab.ipynb)
* **Media Berita Online**: Buka [`12_sentiment_analysis_news/process_nlp_news_colab.ipynb`](12_sentiment_analysis_news/process_nlp_news_colab.ipynb)

---

## 👥 Tim Peneliti & Kolaborasi Multidisiplin

Riset ini merupakan bagian dari kolaborasi akademik antarbidang studi:
* **Bidang Teknologi Informasi / Computer Science**: Rekayasa data digital, web scraping multi-platform, pemodelan NLP Transformer RoBERTa, dan komputasi framing Entman (**Research Question 1**).
* **Bidang Sosiologi**: Analisis survei lapangan panel *attentive public* di Malaysia dan Singapura (**Research Question 2**).
* **Bidang Hubungan Internasional**: Sintesis evaluasi efektivitas diplomasi publik luar negeri Indonesia (**Research Question 3**).

---

## 📄 Lisensi
Dataset dan kode sumber ini didistribusikan di bawah lisensi [MIT License](LICENSE) untuk tujuan penelitian dan keterbukaan sains (*Open Science*).
