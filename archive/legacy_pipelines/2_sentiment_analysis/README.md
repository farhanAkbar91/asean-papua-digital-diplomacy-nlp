# Folder 2: Sentiment Analysis & Topic Modeling (Google Colab GPU)

Folder ini berisi berkas untuk melakukan **Analisis Sentimen (Transformer RoBERTa GPU)**, **Pemetaan Narasi Entman Framing**, dan **Pembuatan Grafik Visualisasi Hasil Analisis untuk Tim FISIP**.

---

## 📁 Berkas dalam Folder Ini:

- `process_nlp_colab.ipynb`: Jupyter Notebook siap upload ke Google Colab.
- `process_nlp_colab.py`: Skrip Python mandiri *all-in-one* jika ingin copy-paste langsung ke sel Colab.

---

## 🛠️ Langkah-Langkah Menggunakan di Google Colab:

1. Buka [colab.research.google.com](https://colab.research.google.com).
2. Pastikan Jenis Runtime adalah GPU:
   - Pilih **Runtime > Change runtime type > T4 GPU**.
3. Upload berkas `process_nlp_colab.ipynb` (atau copy-paste isi `process_nlp_colab.py`).
4. **Jalankan Sel 1** (!pip install...).
5. **Jalankan Sel 2**, lalu upload file CSV hasil scraping (`asean_papua_x_tweets.csv`).
6. **Jalankan Sel 3**.

---

## 📊 Hasil yang Akan Otomatis Terunduh:

- `asean_papua_sentiment_analyzed.csv` (CSV lengkap berlabel sentimen & narasi).
- `ringkasan_analisis_fisip.txt` (Laporan eksekutif persentase temuan untuk draf skripsi FISIP).
- `sentiment_distribution_pie.png` (Pie chart sentimen).
- `narrative_distribution_bar.png` (Bar chart narasi Entman Framing).
- `sentiment_by_country_bar.png` (Bar chart sentimen per negara ASEAN).
- `wordcloud_asean_papua.png` (WordCloud kata terbanyak).
