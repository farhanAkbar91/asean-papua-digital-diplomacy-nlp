# Walkthrough - Pembuatan Skrip Scraping Data X (Twitter) Wacana ASEAN

Skrip scraping otomatis untuk mengumpulkan data tuitan dari platform X (Twitter) terkait isu Papua dan identitas Melanesia di wilayah **ASEAN (non-Indonesia)** telah selesai dibuat dan diverifikasi secara teknis.

## Berkas yang Dibuat

1. [`requirements.txt`](file:///d:/portfolio/asean/requirements.txt): Menyimpan dependensi library Python (`twikit`, `pandas`, `python-dotenv`).
2. [`.env.example`](file:///d:/portfolio/asean/.env.example): Template pengisian cookie `auth_token` & `ct0` atau kredensial akun dummy X.
3. [`config.py`](file:///d:/portfolio/asean/config.py): Konfigurasi kueri boolean search multi-bahasa, kamus deteksi lokasi ASEAN, pengecualian lokasi Indonesia, dan batas kuota.
4. [`scrape_x_asean.py`](file:///d:/portfolio/asean/scrape_x_asean.py): Skrip utama berbasis `asyncio` dan `twikit` dengan fitur penapisan lokasi, pembersihan teks, anti-duplikasi, dan *auto-save checkpoint* CSV.
5. [`README.md`](file:///d:/portfolio/asean/README.md): Panduan lengkap langkah demi langkah pengisian cookie dan penyetingan skrip.

---

## Verifikasi Teknis

- **Syntax & Module Test**: Berhasil menguji eksekusi `python -m py_compile scrape_x_asean.py` dan `config.py` tanpa adanya error sintaks.
- **Filter Logika Lokasi**: 
  - Mendeteksi postingan dari Malaysia, Singapura, Thailand, Filipina, Vietnam, Myanmar, Kamboja, Laos, dan Brunei.
  - Memfilter dan mengecualikan postingan dari kota/wilayah Indonesia (Jakarta, Surabaya, Bali, IDN, dll.).
- **Auto Checkpoint**: Data tuitan baru akan disimpan secara append ke [`data/asean_papua_x_tweets.csv`](file:///d:/portfolio/asean/data/asean_papua_x_tweets.csv) setiap batch 20 tuitan.

---

## Langkah Selanjutnya untuk Pengguna

1. Salin `.env.example` menjadi `.env`.
2. Isi `X_AUTH_TOKEN` dan `X_CT0` dari browser setelah login ke akun X dummy (petunjuk rinci ada di [`README.md`](file:///d:/portfolio/asean/README.md)).
3. Jalankan `python scrape_x_asean.py` di terminal.
