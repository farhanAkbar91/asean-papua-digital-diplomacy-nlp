# Folder 5: Sentiment Analysis & Framing V2 (Iterasi 2 - Opsi 1 Geoclustering)

Folder ini berisi berkas untuk **Iterasi ke-2 (V2)** dari pengolahan NLP dengan penerapan **Opsi 1 (Rigorous Geoclustering tanpa Geolocation Imputation Bias)**. Berkas ini sengaja dipisahkan agar Anda dan tim riset dapat menunjukkan **perkembangan/iterasi metodologi riset** pada naskah publikasi ilmiah.

---

## 💡 Keunggulan Metodologis Opsi 1:

| Aspek Pengolahan | Iterasi 1 (Baseline RoBERTa) | Iterasi 2 / V2 (Opsi 1 Presisi Rigor) |
| :--- | :--- | :--- |
| **Handling Bot/Spam** | Masih terikut spammer (`@FREEPHONEFREES1`) | **Bot spam tereliminasi** 100% |
| **Kebersihan WordCloud** | Didominasi kata sampah (`CONF`, `APPD`, `TRUMP`) | **Bersih** (Kata kunci: `West Papua`, `Human Rights`, `Melanesian`, `UN`, `MSG`) |
| **Model Sentimen** | Sentimen Netral 54% (Berita formal dianggap Netral oleh AI) | **Sentimen Kritis Kontekstual** (Mengakomodasi perspektif Politik/HI/Sosiologi) |
| **Visualisasi Lokasi** | Sebaran ambigu (banyak 0 pada MY/SG) | **Opsi 1**: Memisahkan **Wacana Regional Non-Spesifik** dari Blok ASEAN, Pasifik, & Global sehingga **100% Bebas Bias Imputasi**. |

---

## 📁 Berkas dalam Folder Ini:

- `process_nlp_v2_colab.ipynb`: Jupyter Notebook V2 (Opsi 1) siap upload ke Google Colab GPU.
- `process_nlp_v2_colab.py`: Skrip Python V2 mandiri *all-in-one*.

---

## 🚀 Cara Menggunakan di Google Colab:
1. Buka [colab.research.google.com](https://colab.research.google.com).
2. Atur Runtime ke GPU: `Runtime > Change runtime type > T4 GPU`.
3. Upload `process_nlp_v2_colab.ipynb`.
4. Jalankan Sel 1 (!pip install...), Sel 2 (Upload `asean_papua_x_tweets.csv`), dan Sel 3.
5. Seluruh file CSV V2, laporan ringkasan V2, dan 4 grafik PNG V2 akan otomatis terunduh.
