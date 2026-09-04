# Modul 11: Scraping Media Berita Online Regional (Riset FISIP - Scopus)

Modul ini bertanggung jawab mengumpulkan korpus teks artikel berita resmi dari portal media massa arus utama di **Singapura**, **Malaysia**, **Kawasan Pasifik & Melanesia**, serta **Media Global**.

Modul ini merupakan pilar ketiga yang melengkapi **"Segitiga Emas" (*Golden Triangle*) Triangulasi Data** penelitian:
1. **Platform X / Twitter** (`7_hasil4_x/`): Wacana aktivisme digital & solidaritas transnasional.
2. **YouTube Media Regional** (`10_hasil5_yt/`): Ruang perdebatan dialektis publik awam & terdidik atas liputan audiovisual.
3. **Media Berita Online** (`11_media_berita_scraping/`): Agenda setting institusional & pembingkaian narasi formal yang memapar kelompok *attentive public* regional.

---

## 🎯 Relevansi dengan Dokumen Referensi (`MABA SCOPUS.pdf`)

1. **Menjawab Rumusan Masalah 1 (RQ1)**:
   * Menangkap konstruksi narasi formal media (*Entman Framing Theory*: HAM, Kedaulatan, Diplomasi RI, dan Pembangunan) di negara-negara ASEAN non-Indonesia terkait Papua dan klaim identitas kemelanesiaan.
2. **Menjawab Rumusan Masalah 2 (RQ2)**:
   * Menyediakan basis data wacana institusional yang dikonsumsi secara rutin oleh **kelompok *attentive public*** (kelompok terdidik, mahasiswa HI/Politik, jurnalis, dan analis kebijakan) di **Singapura dan Malaysia**.
3. **Menjawab Rumusan Masalah 3 (RQ3 - Sintesis)**:
   * Mengukur sejauh mana narasi diplomasi publik luar negeri Indonesia berhasil menembus dan memengaruhi bingkai pemberitaan media tetangga ASEAN.

---

## 🏛️ Daftar Media Sasaran (Purposive Sampling)

### A. Blok ASEAN (Fokus Utama RQ2)
* **Singapura**:
  * *CNA (Channel NewsAsia)*: Media rujukan diplomasi & regionalisme terdepan di Asia Tenggara.
  * *The Straits Times*: Surat kabar arus utama tertua dan paling berpengaruh di Singapura.
* **Malaysia**:
  * *The Star*: Harian berbahasa Inggris sirkulasi terbesar di Malaysia.
  * *Free Malaysia Today (FMT)*: Portal berita independen terkemuka dengan liputan kritis regional.
  * *New Straits Times (NST)*: Harian nasional arus utama Malaysia.
  * *Astro AWANI*: Portal berita televisi berita 24 jam terdepan Malaysia.
  * *Malay Mail*: Portal berita harian independen Malaysia.

### B. Blok Pasifik & Melanesia (Pembanding Kawasan)
* *RNZ Pacific (Radio New Zealand)*: Sumber rujukan utama isu geopolitik Pasifik & Melanesia.
* *ABC News Australia (The Pacific)*: Jurnalisme investigasi Australia terkait isu kawasan.
* *Asia Pacific Report*: Media independen dari *Pacific Media Centre* Auckland yang intensif mengawal isu West Papua & MSG.

### C. Mitra Global
* *Al Jazeera English*: Liputan investigasi independen global (e.g., 101 East).
* *BenarNews*: Afiliasi jurnalisme regional Asia Pasifik.

---

## 📋 Skema Kolom Terpadu (Unified Schema)

Data hasil scraping disimpan dalam format CSV dengan skema yang 100% kompatibel dengan pipeline NLP multi-platform:

| Kolom | Tipe Data | Keterangan |
| :--- | :--- | :--- |
| `platform` | String | Bernilai tetap: `"News Media"` |
| `post_id` | String | Hash unik ID artikel berbasis URL kanonikal |
| `created_at` | String (Date) | Tanggal publikasi artikel (`YYYY-MM-DD`) |
| `username` | String | Desk berita / News agency (e.g. `CNA Desk`, `Reuters`) |
| `user_location` | String | Lokasi kantor pusat media (e.g. `Singapore`, `Kuala Lumpur`) |
| `country_bloc` | String | `Blok ASEAN`, `Blok Pasifik & Melanesia`, `Mitra Global` |
| `media_source` | String | Nama portal media resmi |
| `full_text` | String | Judul + Ringkasan + Teks lengkap artikel berita |
| `like_count` | Integer | `0` (standar metrik media berita) |
| `url` | String | URL kanonikal artikel asli di portal media |

---

## 🚀 Cara Menjalankan di Google Colab

1. Buka file [`scrape_news_colab.ipynb`](file:///d:/portfolio/asean/11_media_berita_scraping/scrape_news_colab.ipynb) di Google Colab.
2. Jalankan sel **Langkah 1**: Menginstall dependensi (`googlenewsdecoder`, `beautifulsoup4`, `requests`, `pandas`, `tqdm`).
3. Jalankan sel **Langkah 2 & 3**: Memuat konfigurasi media target dan fungsi pembersihan/validasi teks.
4. Jalankan sel **Langkah 4**: Memulai scraping otomatis dengan *rate-limiting* sopan dan *progress bar*.
5. Jalankan sel **Langkah 5 & 6**: Melihat ringkasan distribusi data per blok geopolitik dan mendownload file `news_papua_asean_articles.csv`.
