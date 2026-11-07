# Folder 8: Multi-Platform Scraping (YouTube & Reddit - Versi Presisi Mutlak)

Folder ini berisi infrastruktur *scraping* data opini publik dan wacana digital untuk **YouTube Comments** dan **Reddit Posts & Comments**. Seluruh target media, subreddit, dan mekanisme penyaringan disusun secara presisi mengikuti **Kriteria Sampling Purposive & Rumusan Masalah (RQ1 & RQ2) dari Dokumen Riset FISIP (MABA SCOPUS.pdf)**.

---

## 🎯 1. Evaluasi & Perbaikan Kritis dari Versi Sebelumnya:

| Masalah pada Versi Lama | Solusi Konkret pada Versi Presisi Ini |
| :--- | :--- |
| **YouTube: Bocor Video Politik Internal Malaysia** (KiniTV soal Anwar Ibrahim & Ketua SPRM Azam Baki) | **Syarat Mutlak Subjek Judul**: Judul video **WAJIB** memuat kata `papua`, `west papua`, `papua barat`, `melanesia`, atau `ulmwp`. Video di luar topik ini DITOLAK 100%. |
| **YouTube: Bocor Video Perjanjian Batam** (The Straits Times soal sewa Jakarta/Batam) | Judul tanpa kata kunci Papua langsung diabaikan; video The Straits Times kini khusus menargetkan liputan Papua & diplomasi regional. |
| **YouTube: Perang Komentar Cyber-Trooper / Troll** (*malaydesh, indondesh, makan ubi, babu, iq 15 ringgit*) | **Anti-Troll Filter**: Seluruh komentar yang memuat ejekan antarnetizen dibuang secara otomatis dari dataset. |
| **Reddit: Bocor Perdebatan OOT** (43 komentar membahas pizza, spaghetti, orang Bali saat puasa) | **Validasi Isi Komentar**: Setiap komentar **WAJIB** mengandung kata `papua`, `west papua`, `melanesia`, `msg`, atau `kedaulatan`. Komentar OOT dibuang total. |
| **Reddit: Keterbatasan API Key / Kebijakan Baru Reddit** | **100% Bebas Kredensial**: Anda **TIDAK PERLU** mendaftar Reddit Developer, `client_id`, ataupun `client_secret`. Skrip berjalan otomatis menggunakan feed thread terverifikasi dengan jeda adaptif anti-429. |

---

## 🛠️ 2. Arsitektur & Berkas Scraper:

### A. YouTube Scraper ([`scrape_youtube_colab.py`](file:///d:/portfolio/asean/8_multiplatform_scraping/scrape_youtube_colab.py) & [`.ipynb`](file:///d:/portfolio/asean/8_multiplatform_scraping/scrape_youtube_colab.ipynb))
- **Verified Video Registry**: Memuat 30 video liputan mendalam Papua terverifikasi dari:
  - **Singapura (RQ2)**: *Channel NewsAsia (CNA)* (9 video liputan khusus)
  - **Malaysia (RQ2)**: *Astro AWANI* (3 video berita resmi)
  - **Pasifik & Regional**: *ABC News In-depth* (8 video investigasi), *RNZ Pacific* (4 video wawancara MSG/diplomasi), *Al Jazeera English* (8 video liputan global)
- **Dynamic Search**: Dilengkapi pencarian dinamis dengan verifikasi subjek mutlak.
- **Kualitas Komentar**: Bebas dari troll dan noise bencana alam PNG (gempa/longsor).
- **Target Output**: `youtube_papua_asean_comments.csv` (1.000 – 2.000+ komentar opini terverifikasi).

### B. Reddit Scraper ([`scrape_reddit_colab.py`](file:///d:/portfolio/asean/8_multiplatform_scraping/scrape_reddit_colab.py) & [`.ipynb`](file:///d:/portfolio/asean/8_multiplatform_scraping/scrape_reddit_colab.ipynb))
- **100% Tanpa API Key**: Berjalan langsung tanpa butuh akun developer Reddit.
- **Target Diskusi Nyata**: Mengambil wacana dari 20 thread terpilih di `r/singapore`, `r/malaysia`, `r/asean`, `r/pacific`, `r/PapuaNewGuinea`, `r/australia`, dan `r/newzealand`.
- **Zero OOT**: Mengambil postingan dan seluruh komentar yang relevan dengan Isu Papua dan Identitas Melanesia.
- **Target Output**: `reddit_papua_asean_posts.csv`.

---

## 🚀 3. Panduan Menjalankan di Google Colab:

### A. Scraper YouTube:
1. Unggah [`scrape_youtube_colab.ipynb`](file:///d:/portfolio/asean/8_multiplatform_scraping/scrape_youtube_colab.ipynb) ke Google Colab.
2. Jalankan **Sel 1** (`!pip install...`).
3. Jalankan **Sel 2**. File `youtube_papua_asean_comments.csv` akan otomatis diunduh ke komputer Anda.

### B. Scraper Reddit:
1. Unggah [`scrape_reddit_colab.ipynb`](file:///d:/portfolio/asean/8_multiplatform_scraping/scrape_reddit_colab.ipynb) ke Google Colab.
2. Jalankan **Sel 1** (`!pip install...`).
3. Jalankan **Sel 2** *(Langsung jalankan, tidak butuh input API key)*. File `reddit_papua_asean_posts.csv` akan otomatis diunduh ke komputer Anda.

---

## 📊 4. Skema Kolom Terstandarisasi:
File CSV yang dihasilkan kedua platform memiliki struktur seragam yang siap diolah ke **Pipeline NLP V2 (`5_sentiment_analysis_v2/process_nlp_v2_colab.ipynb`)**:
`platform`, `post_id`, `created_at`, `username`, `user_location`, `country_bloc`, `media_source`, `full_text`, `like_count`, `url`.
