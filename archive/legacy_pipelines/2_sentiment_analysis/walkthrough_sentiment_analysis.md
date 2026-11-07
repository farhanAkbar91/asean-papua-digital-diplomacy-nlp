# Walkthrough - Pipeline NLP & Visualisasi Data untuk Tim FISIP

Pipeline pengolahan data teks NLP berbasis GPU di Google Colab telah selesai dibangun dan siap digunakan untuk mengolah file CSV hasil *scraping*.

## Berkas yang Dibuat

1. **[`process_nlp_colab.ipynb`](file:///d:/portfolio/asean/process_nlp_colab.ipynb)** *(Disarankan)*
   - Berkas Jupyter Notebook untuk Google Colab dengan GPU T4.
   - Terdiri dari 3 sel utama:
     - **Sel 1**: Install library `transformers`, `torch`, `matplotlib`, `seaborn`, `wordcloud`, `scikit-learn`.
     - **Sel 2**: Mengunggah berkas `asean_papua_x_tweets.csv`.
     - **Sel 3**: Eksekusi pembersihan teks, Sentiment Analysis (*CardiffNLP RoBERTa GPU*), Pemetaan Narasi *Entman Framing*, pembuatan 4 grafik PNG, dan otomatis mengunduh hasil ke komputer lokal.
2. **[`process_nlp_colab.py`](file:///d:/portfolio/asean/process_nlp_colab.py)**
   - Berkas skrip Python mandiri *all-in-one* yang dapat langsung di-*copy-paste* ke sel Colab.

---

## Luaran yang Akan Dihasilkan Otomatis di Colab:

- **`asean_papua_sentiment_analyzed.csv`**: File CSV lengkap yang sudah diperkaya dengan kolom `clean_text`, `sentiment` (Positif, Netral, Negatif), `sentiment_score`, dan `dominant_narrative`.
- **`ringkasan_analisis_fisip.txt`**: Berkas teks ringkasan eksekutif berisi persentase sentimen & narasi dominan yang siap langsung ditempelkan ke bab pembahasan draf skripsi FISIP.
- **Visualisasi Grafik (PNG)**:
  - `sentiment_distribution_pie.png`: Pie chart proporsi sentimen.
  - `narrative_distribution_bar.png`: Horizontal bar chart distribusi narasi Entman Framing.
  - `sentiment_by_country_bar.png`: Bar chart distribusi sentimen per negara ASEAN.
  - `wordcloud_asean_papua.png`: WordCloud kata yang paling sering muncul.

---

## Langkah Menjalankan di Google Colab:

1. Buka [colab.research.google.com](https://colab.research.google.com).
2. Pastikan Runtime menggunakan GPU (`Runtime > Change runtime type > T4 GPU`).
3. Upload file [`process_nlp_colab.ipynb`](file:///d:/portfolio/asean/process_nlp_colab.ipynb).
4. Jalankan **Sel 1** (!pip install...), **Sel 2** (Upload `asean_papua_x_tweets.csv`), dan **Sel 3** (Pipeline NLP).
