# Folder 1: Scraping Data X (Twitter) ASEAN

Folder ini berisi berkas untuk mengumpulkan data tuitan dari platform X (Twitter) terkait isu Papua & Identitas Melanesia di wilayah ASEAN (non-Indonesia).

---

## 📁 Berkas dalam Folder Ini:

- `scrape_x_asean_colab.ipynb`: Notebook Jupyter untuk Google Colab.
- `scrape_x_asean_colab.py`: Skrip Python Colab mandiri.
- `scrape_x_asean.py`: Skrip Python eksekusi lokal.
- `config.py`: Konfigurasi query pencarian boolean & filter lokasi ASEAN.
- `.env.example`: Template cookie X (`auth_token` & `ct0`).
- `requirements.txt`: Dependensi library Python lokal.

---

## 🚀 Cara Menggunakan (Colab):
1. Buka [colab.research.google.com](https://colab.research.google.com).
2. Upload berkas `scrape_x_asean_colab.ipynb`.
3. Jalankan Sel 1 dan Sel 2. Masukkan `auth_token` dan `ct0` dari cookie X akun dummy Anda.
4. File CSV hasil scraping (`asean_papua_x_tweets.csv`) akan otomatis terunduh.
