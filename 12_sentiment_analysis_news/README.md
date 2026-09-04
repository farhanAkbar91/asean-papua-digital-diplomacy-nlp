# Modul 12: Analisis Sentimen & Framing NLP Media Berita Online (Riset FISIP - Scopus)

Modul ini memproses korpus artikel berita dari portal berita arus utama di **Singapura**, **Malaysia**, **Kawasan Pasifik & Melanesia**, serta **Mitra Global** (`news_papua_asean_articles.csv` dari Folder `0_data/`).

Modul ini adalah tahapan analisis pilar ketiga dari **"Segitiga Emas" (*Golden Triangle*)** triangulasi data penelitian:
1. **Platform X (Twitter)** (`7_hasil4_x/`): Wacana aktivisme & opini publik mikro.
2. **YouTube Comments** (`10_hasil5_yt/`): Ruang perdebatan dialektis publik penonton video berita.
3. **Media Berita Online** (`12_sentiment_analysis_news/`): Agenda setting institusional yang memapar kelompok *attentive public*.

---

## 🎯 Kerangka Teoretis & Relevansi Akademik (`MABA SCOPUS.pdf`)

1. **Menjawab RQ1 (*Entman Framing Analysis*)**:
   * Memetakan 5 kategori narasi dominan:
     * **HAM & Pelanggaran Kemanusiaan**: Dugaan pelanggaran HAM, pemadaman internet, pengungsian warga sipil.
     * **Kedaulatan & Penentuan Nasib Sendiri**: Tuntutan referendum, dekolonisasi, status Pepera 1969 vs integritas NKRI.
     * **Diplomasi & Hubungan Internasional**: Hubungan bilateral RI-Pasifik, KTT Melanesian Spearhead Group (MSG), ASEAN.
     * **Pembangunan & Stabilitas Keamanan**: Kasus sandera pilot Susi Air, operasi penegakan hukum aparat, investasi strategis/SDA.
     * **Identitas Melanesia & Solidaritas Pasifik**: Hubungan kekerabatan budaya Melanesia, ras, dan solidaritas regional.

2. **Menjawab RQ2 (*Attentive Public* Malaysia & Singapura)**:
   * Mengukur eksposur bingkai pemberitaan dari media terkemuka Singapura (*CNA*, *The Straits Times*) dan Malaysia (*The Star*, *Free Malaysia Today*, *New Straits Times*, *Astro AWANI*) yang dikonsumsi kelompok terdidik dan pemerhati kebijakan publik.

3. **Menjawab RQ3 (Sintesis Efektivitas Diplomasi Luar Negeri RI)**:
   * Menilai bagaimana wacana resmi pemerintah Indonesia diakomodasi atau dikritisi dalam peliputan pers regional.

---

## 🔬 Inovasi Metodologis Jurnalisme Komputasional: *Inverted Pyramid Lead Processing*

Teks artikel berita memiliki karakteristik berbeda dari media sosial:
* **Teks Sangat Panjang** (rata-rata 624 kata) yang melampaui batas 512 token model Transformer standar.
* Dalam tradisi jurnalistik (*Inverted Pyramid*), **tesis utama, sudut pandang (*slant*), dan framing editorial diletakkan pada judul dan paragraf pembuka (*lead paragraph*)**.
* Oleh karena itu, pipeline ini mengekstrak judul + *lead text* (250 kata pertama) untuk inferensi sentimen RoBERTa, sementara keseluruhan teks berita dianalisis untuk pemetaan kata kunci Entman Framing.

---

## 📁 Berkas dalam Modul Ini

* [**`process_nlp_news_colab.ipynb`**](file:///d:/portfolio/asean/12_sentiment_analysis_news/process_nlp_news_colab.ipynb): Notebook Google Colab siap pakai (GPU/CPU).
* [**`process_nlp_news_colab.py`**](file:///d:/portfolio/asean/12_sentiment_analysis_news/process_nlp_news_colab.py): Skrip Python mandiri untuk inferensi lokal.
* [**`requirements.txt`**](file:///d:/portfolio/asean/12_sentiment_analysis_news/requirements.txt): Daftar dependensi pemrosesan.

---

## 🚀 Panduan Menjalankan di Google Colab

1. Buka Google Colab dan unggah file [`process_nlp_news_colab.ipynb`](file:///d:/portfolio/asean/12_sentiment_analysis_news/process_nlp_news_colab.ipynb).
2. Jalankan sel **Langkah 1**: Menginstall pustaka (`transformers`, `torch`, `wordcloud`, dll).
3. Jalankan sel **Langkah 2**: Mengunggah berkas `news_papua_asean_articles.csv` dari folder `0_data/`.
4. Jalankan sel **Langkah 3 & 4**: Menjalankan model RoBERTa dan penajaman kontekstual FISIP.
5. Jalankan sel **Langkah 5 & 6**: Menghasilkan 5 visualisasi ilmiah (300 DPI) dan ringkasan temuan.
6. Jalankan sel **Langkah 7**: Mengunduh semua grafik PNG, laporan teks, dan CSV hasil analisis.

---

## 📊 Luaran yang Akan Dihasilkan (300 DPI)

1. `news_sentiment_distribution_pie.png`: Proporsi sentimen (Positif, Negatif, Netral).
2. `news_narrative_distribution_bar.png`: Sebaran 5 kategori Entman Framing.
3. `news_sentiment_by_bloc_bar.png`: Sentimen komparatif per Blok Geopolitik (ASEAN vs Pasifik vs Global).
4. `news_sentiment_by_media_bar.png`: Distribusi sentimen per kanal media resmi (CNA, The Star, FMT, RNZ, ABC, dll).
5. `news_wordcloud_articles.png`: Visualisasi kata kunci dominan media berita.
6. `news_papua_sentiment_analyzed.csv`: Dataset lengkap teranotasi.
7. `ringkasan_analisis_news_fisip.txt`: Laporan metrik eksekutif riset.
