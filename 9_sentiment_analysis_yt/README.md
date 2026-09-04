# Folder 9: Sentiment Analysis & Entman Framing (YouTube Comments Dataset)

Folder ini berisi pipeline NLP lengkap untuk melakukan inferensi model **Analisis Sentimen Kontekstual & Pemetaan Framing Narasi Dominan (Entman Theory)** khusus pada data **Komentar YouTube Berita Regional** (`youtube_papua_asean_comments.csv`).

---

## 🎯 1. Kerangka Metodologi & Relevansi Riset FISIP (RQ1 & RQ2):

1. **Model NLP SOTA (*State of the Art*)**:
   - Menggunakan model transformer `cardiffnlp/twitter-roberta-base-sentiment-latest` yang dilatih pada jutaan teks media sosial.
2. **Context-Aware Sentiment Adjustment (Penajaman Kontekstual Diplomasi)**:
   - Menghindari kelemahan model AI umum yang sering melabeli desakan investigasi HAM, tuntutan referendum, atau kritik pelanggaran sebagai "Netral".
   - *Negatif (Kritis)*: Opini desakan investigasi pelanggaran HAM, tuduhan penjajahan/kolonialisme, kritik terhadap operasi militer, desakan referendum/kemerdekaan.
   - *Positif (Mendukung)*: Pembelaan terhadap kedaulatan NKRI, dukungan pembangunan infrastruktur & dana otonomi khusus (Otsus), persatuan kawasan, serta kritik terhadap kelompok bersenjata.
   - *Netral*: Pernyataan faktual umum, diskusi sejarah, atau doa perdamaian.
3. **Pemetaan Narasi Dominan (Entman Framing Theory)**:
   - **HAM & Pelanggaran Kemanusiaan**: Wacana pelanggaran hak asasi, desakan kunjungan komisioner PBB, kekerasan sipil, dan diskriminasi rasial.
   - **Identitas Melanesia & Solidaritas Pasifik**: Penegasan rumpun Melanesia ("We are Melanesian, not Melayu"), solidaritas Pasifik (Vanuatu, Solomon, Fiji), dan keanggotaan MSG (*Melanesian Spearhead Group*).
   - **Kedaulatan & Penentuan Nasib Sendiri**: Wacana referendum, *Pepera/Act of Free Choice 1969*, dekolonisasi, integritas wilayah NKRI, dan hukum internasional.
   - **Pembangunan & Stabilitas Keamanan**: Pembangunan jalan/sekolah/RS oleh pemerintah RI, stabilitas ekonomi, peranan TNI-Polri, dan eksploitasi SDA (Freeport/sawit).
4. **Analisis Komparasi per Kanal Berita & Blok Geopolitik**:
   - Menjawab **RQ2** secara presisi: Memetakan perbedaan respons audiens media Singapura (*CNA*), Malaysia (*Astro AWANI*), Australia (*ABC News*), Selandia Baru (*RNZ Pacific*), dan Mitra Global (*Al Jazeera*).

---

## 📁 2. Berkas dalam Folder Ini:

- [`process_nlp_yt_colab.ipynb`](file:///d:/portfolio/asean/9_sentiment_analysis_yt/process_nlp_yt_colab.ipynb): Notebook Google Colab interaktif (dukungan GPU T4, visualisasi grafik, dan unduh otomatis).
- [`process_nlp_yt_colab.py`](file:///d:/portfolio/asean/9_sentiment_analysis_yt/process_nlp_yt_colab.py): Skrip mandiri Python.
- [`requirements.txt`](file:///d:/portfolio/asean/9_sentiment_analysis_yt/requirements.txt): Daftar dependensi pustaka Python.

---

## 🚀 3. Cara Menjalankan di Google Colab:

1. Buka [Google Colab](https://colab.research.google.com) dan unggah file [`process_nlp_yt_colab.ipynb`](file:///d:/portfolio/asean/9_sentiment_analysis_yt/process_nlp_yt_colab.ipynb).
2. **Aktifkan Akselerator GPU** *(Sangat Disarankan agar proses inferensi cepat)*:
   - Klik menu **Runtime** -> **Change runtime type**.
   - Pada opsi *Hardware accelerator*, pilih **T4 GPU** -> Klik **Save**.
3. Jalankan **Sel 1** (`!pip install...`) untuk menginstal pustaka `transformers`, `torch`, `wordcloud`, dll.
4. Pada **Sel 2**, unggah file `youtube_papua_asean_comments.csv` hasil scraping Anda.
5. Jalankan **Sel 3**. Seluruh proses pengolahan akan berjalan otomatis, dan seluruh berkas luaran berikut akan **otomatis terunduh ke komputer Anda**:
   - `youtube_papua_sentiment_analyzed.csv` *(Dataset lengkap berisi label sentimen dan framing)*
   - `ringkasan_analisis_yt_fisip.txt` *(Rekapitulasi statistik persentase sentimen & framing)*
   - `yt_sentiment_distribution_pie.png` *(Pie chart sebaran sentimen keseluruhan)*
   - `yt_narrative_distribution_bar.png` *(Bar chart sebaran 4 narasi Entman framing)*
   - `yt_sentiment_by_bloc_bar.png` *(Grafik sentimen per Blok Geopolitik)*
   - `yt_sentiment_by_media_bar.png` *(Grafik sentimen per Kanal Media: CNA vs AWANI vs ABC vs RNZ vs Al Jazeera)*
   - `yt_wordcloud_comments.png` *(WordCloud kata kunci utama komentar wacana publik)*

---

## 📊 4. Skema Kolom CSV Hasil Analisis:
File `youtube_papua_sentiment_analyzed.csv` memuat atribut lengkap:
`platform`, `post_id`, `created_at`, `username`, `user_location`, `country_bloc`, `media_source`, `full_text`, `clean_text`, `sentiment_raw`, `sentiment`, `sentiment_score`, `dominant_narrative`, `like_count`, `url`.
