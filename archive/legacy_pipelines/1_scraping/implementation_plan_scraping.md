# Implementation Plan - Skrip Scraping Data X (Twitter) Wacana ASEAN (Isu Papua & Melanesia)

Rencana ini mencakup pembuatan skrip Python otomatis untuk mengambil (scrape) data tuitan dan komentar dari platform X (Twitter) terkait isu Papua dan identitas Melanesia di wilayah ASEAN (selain Indonesia), serta memfilternya agar siap diolah oleh modul NLP (Analisis Sentimen & Pemetaan Narasi).

## User Review Required

> [!IMPORTANT]
> **Metode Otentikasi X (Twitter)**: Karena X memperketat akses tanpa login, skrip ini akan menggunakan library **`twikit`** (metode paling stabil dan gratis saat ini). Library ini membutuhkan file *cookies* atau *login credentials* dari akun X (disarankan menggunakan **akun X sekunder/dummy**).

> [!WARNING]
> **Penanganan Kuota / Rate Limit X**: Untuk mencegah pemblokiran akun dummy, skrip akan dilengkapi *delay/sleep* acak antar permintaan data dan fitur simpan otomatis (*auto-save checkpoint*) secara periodik.

---

## Open Questions

> [!IMPORTANT]
> 1. **Penyimpanan Akun X Dummy**: Apakah Anda setuju menggunakan metode *cookies* (misal simpan `cookies.json`) dari akun X dummy?
> 2. **Format File Data Output**: Apakah Anda lebih memilih hasil akhir disimpan sebagai file **CSV**, **JSON**, atau **Excel (.xlsx)**?
> 3. **Daftar Negara ASEAN Target**: Apakah pencarian fokus pada **Malaysia & Singapura** dulu, atau langsung mencakup seluruh negara ASEAN (Thailand, Filipina, Vietnam, dll.)?

---

## Proposed Changes

### Scraping & Data Pipeline Component

#### [NEW] [requirements.txt](file:///d:/portfolio/asean/requirements.txt)
- Berisi dependensi Python yang dibutuhkan: `twikit`, `pandas`, `pydantic`, `python-dotenv`.

#### [NEW] [scrape_x_asean.py](file:///d:/portfolio/asean/scrape_x_asean.py)
- Skrip utama berbasis `asyncio` dan `twikit` yang melakukan:
  1. Otentikasi ke X menggunakan *cookies* / kredensial akun dummy.
  2. Pencarian tuitan berbasis kueri boolean multi-bahasa (`"West Papua" OR "Papua" OR "Melanesia" OR "MSG"`).
  3. Pemfilteran geografis pengguna (mengecualikan lokasi Indonesia seperti Jakarta, Indonesia, dll., dan memprioritaskan lokasi ASEAN).
  4. Ekstraksi atribut penting: `tweet_id`, `created_at`, `username`, `user_location`, `full_text`, `language`, `retweet_count`, `like_count`, `reply_count`.
  5. Penyimpanan otomatis (*checkpointing*) ke direktori `data/`.

#### [NEW] [config.py](file:///d:/portfolio/asean/config.py)
- Pengaturan kueri pencarian, daftar kata kunci inklusi/eksklusi, filter lokasi negara ASEAN, serta batas jumlah tuitan yang di-scrape.

#### [NEW] [.env.example](file:///d:/portfolio/asean/.env.example)
- Template variabel lingkungan untuk menyimpan kredensial dummy X secara aman.

---

## Verification Plan

### Automated Tests
- Menjalankan uji otentikasi akun X dummy (`python -m unittest` atau skrip verifikasi koneksi).
- Menjalankan skrip scraping skala kecil (*dry run* 10 tuitan) untuk mengecek apakah atribut data `full_text`, `user_location`, dan timestamp terekstrak dengan benar tanpa error.

### Manual Verification
- Memeriksa file output (`CSV`/`JSON`) di folder `data/` untuk memastikan:
  - Teks tuitan bersih dan lengkap.
  - Tidak ada data tuitan asal Indonesia yang terikut.
  - Struktur data siap dimasukkan ke pipeline Analisis Sentimen NLP.
