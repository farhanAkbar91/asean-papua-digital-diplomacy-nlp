# ASEAN-Papua Digital Diplomacy NLP Pipeline
### Multi-Platform Computational Social Science & Data Triangulation Architecture

> ## ⚠️ STATUS PENELITIAN (WAJIB DIBACA — revisi integritas 2026-11-07)
> 1. **Dataset di repositori ini adalah korpus PILOTE (N = 1.571) yang BELUM divalidasi manusia.** Tidak ada Cohen's Kappa, Precision, Recall, atau F1 yang pernah dihitung. Jangan melaporkan metrik reliabilitas apa pun dari data ini.
> 2. **Label otoritatif = prediksi mentah model** (`sentiment_model`). Lapisan "context-aware adjustment" berbasis kata-kunci kini dilaporkan sebagai kolom eksperimen TERPISAH (`stance_rule_adjusted` + bukti kata-kunci) dan TIDAK boleh dipakai untuk temuan utama sampai tervalidasi.
> 3. **Korpus faktual berkomposisi Bahasa Inggris + Indonesia (en/id)** — BUKAN tiga bahasa (Inggris/Melayu/Prancis) seperti yang pernah diklaim. Model sentimen bersifat monolingual-Inggris sesuai model card resmi.
> 4. **Pipeline otoritatif yang diperbaiki**: `src/` + `tests/` — `src/build_master_repaired.py` (menghasilkan `data/processed/master_triangulation_repaired.csv` + manifest), `src/run_inference.py` (inferensi Colab, tanpa fallback senyap), `tests/` (42 tes otomatis). Dokumen metodologi aktual + batasan: [`docs/METHODOLOGY_REPAIRED.md`](docs/METHODOLOGY_REPAIRED.md). Log perubahan: [`docs/RECOVERY_LOG.md`](docs/RECOVERY_LOG.md). Manifest restrukturisasi: [`docs/RESTRUCTURING_MANIFEST.md`](docs/RESTRUCTURING_MANIFEST.md).
> 5. Distribusi statistik di bawah (bagian "Ringkasan Temuan Awal") adalah angka historis pra-reparasi yang **sebagian di antaranya telah terbukti merupakan artefak** (kategori residual dipetakan ke bingkai "Diplomasi"; blok geopolitik X berbasis substring "un"/"uk"). Gunakan angka dari `data/processed/` untuk analisis apa pun ke depan.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c?logo=pytorch)](https://pytorch.org/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-ffcc00?logo=huggingface)](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)
[![Scopus Target](https://img.shields.io/badge/Research-Scopus%20Indexed%20FISIP-4c1d95)](file:///d:/portfolio/asean/MABA%20SCOPUS.pdf)
[![Triangulation](https://img.shields.io/badge/Data%20Triangulation-X%20%7C%20YouTube%20%7C%20News-059669)](#-the-golden-triangle-triangulasi-data-n--1571)
[![License](https://img.shields.io/badge/License-MIT-gray)](LICENSE)

Repositori ini berisi **pipeline komputasional, rekayasa data (*data engineering*), dan pemodelan Natural Language Processing (NLP)** untuk menganalisis wacana digital, framing media, dan sentimen publik internasional terkait **Isu Papua dan Klaim Identitas Kemelanesiaan di Kawasan ASEAN dan Pasifik**.

Riset ini dirancang sebagai pemenuhan **Research Question 1 (RQ1)** dalam kerangka riset kolaboratif multidisiplin (Teknologi Informasi, Sosiologi, dan Hubungan Internasional) untuk target publikasi jurnal internasional bereputasi tinggi (**Scopus Q1/Q2**).

---

## 📐 The Golden Triangle: Triangulasi Data ($N = 1.571$)

Riset ini mengadopsi pendekatan **triangulasi multi-platform** untuk mengatasi bias algoritma tunggal media sosial:

```
                      [ MEDIA MASSA RESMI ]
                 (Agenda Setting Institusional)
                       N = 312 Artikel
                             / \
                            /   \
                           /     \
                          /       \
                         /  RISET  \
                        /   PAPUA   \
                       /   KOMPUTASI \
                      /_______________\
      [ PLATFORM X (TWITTER) ]      [ KOMENTAR YOUTUBE ]
       (Aktivisme Transnasional)    (Debat Dialektis Publik)
             N = 375 Tuitan              N = 884 Komentar
```

| Pilar Platform | Sumber Data | Jumlah Korpus | Karakteristik Wacana Ilmiah |
| :--- | :--- | :---: | :--- |
| **1. Platform X (Twitter)** | Postingan Publik Akun Kawasan | **375** tuitan | **Aktivisme Digital**: Kampanye hashtag satu arah, seruan kunjungan PBB, dan solidaritas diaspora Pasifik. |
| **2. YouTube Comments** | Komentar Video Berita Arus Utama | **884** komentar | **Debat Dialektis Publik**: Respon publik awam dan terdidik terhadap liputan audiovisual (CNA, Awani, ABC, Al Jazeera). |
| **3. Media Berita Online** | Portal Pers Resmi Singapura, Malaysia, Pasifik | **312** artikel utuh | **Agenda Setting Institusional**: Pemberitaan formal kawat berita, hukum internasional, dan kebijakan resmi negara. |
| **TOTAL MASTER KORPUS** | **3 Pilar Terintegrasi** | **1.571 data** | **Basis empiris utuh bebas bias platform tunggal**. |

---

## 🧠 Metodologi Komputasional & Arsitektur NLP

```
┌─────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│ Web Crawlers &  │ ───► │  Data Sanitation &      │ ───► │ Deep Learning Model:    │
│ Platform Scraper│      │  Anti-Noise Filtering   │      │ Twitter-RoBERTa (base)  │
└─────────────────┘      └─────────────────────────┘      └─────────────────────────┘
                                                                       │
                                                                       ▼
┌─────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│ Master Dataset  │ ◄─── │ Entman Framing Lexicon: │ ◄─── │ Context-Aware Diplomatic│
│ (1.571 Records) │      │ 5 Dominant Narratives   │      │ Rule-Based Adjustment   │
└─────────────────┘      └─────────────────────────┘      └─────────────────────────┘
```

1. **Model Transformer**: Menggunakan Pretrained Model `cardiffnlp/twitter-roberta-base-sentiment-latest` via Hugging Face Transformers & PyTorch.
2. **Inverted Pyramid Lead Processing**: Menganalisis judul + *lead paragraph* (250 kata pertama) untuk inferensi sentimen artikel berita panjang, dan teks utuh untuk anotasi framing.
3. **Penajaman Kontekstual Hubungan Internasional**: Rule-based adjustment yang menyelaraskan prediksi semantik umum dengan dinamika diplomasi kedaulatan vs isu pelanggaran HAM.
4. **Operasionalisasi Bingkai Tematik (5 kategori leksikon + residual "Other/No-Frame")**:
   *(Revisi 2026-11-07: ini adalah klasifikasi topik leksikal word-boundary — bukan pengukuran penuh 4 fungsi framing Entman. Unit tanpa kecocokan leksikon dilaporkan sebagai "Other/No-Frame", tidak lagi dipetakan ke bingkai "Diplomasi". Bukti kata-kunci tiap klasifikasi disimpan di kolom `framing_evidence`.)*
   * **HAM & Pelanggaran Kemanusiaan**: Desakan akses PBB, investigasi independen, perlindungan sipil.
   * **Identitas Melanesia & Solidaritas Pasifik**: Kekerabatan ras, forum MSG (*Melanesian Spearhead Group*), ikatan budaya Pasifik.
   * **Kedaulatan & Penentuan Nasib Sendiri**: Tuntutan referendum, dekolonisasi, status Pepera 1969 vs integritas teritorial NKRI.
   * **Pembangunan & Stabilitas Keamanan**: Kasus sandera pilot, penegakan hukum aparat, investasi strategis energi/SDA.
   * **Diplomasi & Hubungan Internasional**: Hubungan bilateral, norma *ASEAN Non-Interference*, kaukus internasional.

---

## 📊 Ringkasan Temuan Awal Komputasional
> ⚠️ **Angka di bawah ini adalah hasil historis pra-reparasi dan TIDAK VALID untuk publikasi**: (a) label "teranotasi" adalah keluaran model + lapisan aturan kata-kunci (bukan anotasi manusia); (b) label bingkai "Diplomasi & Hubungan Internasional" (569 data) termasuk 508 unit yang faktualnya TANPA kecocokan leksikon (residual); (c) blok geopolitik X saat itu ditentukan oleh substring teks (mis. "un" di dalam kata apa pun). Angka yang dapat dipertanggungjawabkan hanya dari `data/processed/master_triangulation_repaired.csv`.

* **Distribusi Label Historis (model + aturan; PRA-reparasi, tidak divalidasi)**:
  * **Netral (Faktual/Diskusi Umum)**: `757 data` (**48.19%**)
  * **Negatif (Kritis terhadap Posisi RI)**: `650 data` (**41.37%**)
  * **Positif (Mendukung Kedaulatan/Pembangunan RI)**: `164 data` (**10.44%**)
* **Distribusi Blok Geopolitik Historis (pra-reparasi; lihat catatan di atas)**:
  * **Mitra Global**: `750 data` (**47.74%**)
  * **Blok ASEAN (Singapura & Malaysia)**: `493 data` (**31.38%**)
  * **Blok Pasifik & Melanesia**: `287 data` (**18.27%**)
  * **Wacana Regional Non-Spesifik**: `41 data` (**2.61%**)
* **Catatan atas "Temuan Pers ASEAN"**: angka ~69% netral+positif media SG/MY diperoleh dari label pra-reparasi yang 25% di antaranya diproduksi aturan kata-kunci (termasuk Astro AWANI dengan n=1). Klaim "mencerminkan kepatuhan kuat terhadap ASEAN Way" TIDAK dapat dipertahankan dari data ini dan harus dihapus/direvisi pada manuskrip sampai validasi manusia dilakukan.

---

## 🗂️ Struktur Direktori Proyek

Proyek ini disusun secara berurutan dan transparan untuk mendokumentasikan setiap iterasi rekayasa data:

```text
asean-papua-digital-diplomacy-nlp/
├── README.md                      <-- Ringkasan proyek + status integritas (BACA DULU)
├── LICENSE                        <-- MIT
├── requirements.txt               <-- Dependensi pipeline aktif (pinned, status verifikasi jujur)
├── data/
│   ├── raw/                       <-- Data mentah X, YouTube, Berita (TIDAK diubah)
│   └── processed/                 <-- OUTPUT pipeline aktif: master_triangulation_repaired.csv + build_manifest.json
├── src/                           <-- Pipeline otoritatif hasil reparasi
│   ├── nlp_core.py
│   ├── build_master_repaired.py
│   └── run_inference.py
├── tests/                         <-- 42 tes otomatis (unit + integrasi)
├── notebooks/                     <-- Notebook Colab historis (pra-reparasi, bukan pipeline aktif)
├── docs/
│   ├── METHODOLOGY_REPAIRED.md    <-- METODOLOGI AKTUAL + batasan (sumber kebenaran)
│   ├── RECOVERY_LOG.md            <-- Log perubahan reparasi & restrukturisasi
│   ├── RESTRUCTURING_MANIFEST.md  <-- Manifest pemindahan/arsip file
│   ├── methodology_history/       <-- Dokumen perencanaan historis (berbanner status)
│   └── manuscripts/               <-- DRAFT FIX.pdf, MABA SCOPUS.pdf, Laporan Teknis
└── archive/
    ├── legacy_pipelines/          <-- 1_..14_ folder eksperimen historis (utuh, untuk provenance)
    ├── pre_repair_docs/           <-- Snapshot dokumen sebelum revisi integritas
    └── data-sampah_quarantine/    <-- Folder "sampah" lama (di-quarantine, tidak dipublikasikan)
```

---

## 🚀 Cara Menjalankan Pipeline (Reproduction Guide)
> **Pipeline OTORITATIF (repaired):**
> ```bash
> pip install -r requirements.txt
> python src/build_master_repaired.py           # membangun master + manifest (tanpa GPU)
> python -m unittest discover -s tests          # 42 tes otomatis
> # inferensi transformer (butuh Colab/torch+transformers):
> python src/run_inference.py --platform x
> python src/build_master_repaired.py           # gabungkan label inferensi baru
> ```
> Folder iterasi historis kini berada di `archive/legacy_pipelines/` — dipertahankan untuk provenance, TIDAK untuk dipakai analisis ke depan.

Seluruh modul komputasional dirancang kompatibel untuk dijalankan pada mesin lokal maupun **Google Colab (CPU/GPU)**:

### 1. Kloning Repositori
```bash
git clone https://github.com/USERNAME/asean-papua-digital-diplomacy-nlp.git
cd asean-papua-digital-diplomacy-nlp
```

### 2. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Pipeline NLP
* **Data X / Twitter**: Buka [`5_sentiment_analysis_v2/process_nlp_v2_colab.ipynb`](5_sentiment_analysis_v2/process_nlp_v2_colab.ipynb)
* **Komentar YouTube**: Buka [`9_sentiment_analysis_yt/process_nlp_yt_colab.ipynb`](9_sentiment_analysis_yt/process_nlp_yt_colab.ipynb)
* **Media Berita Online**: Buka [`12_sentiment_analysis_news/process_nlp_news_colab.ipynb`](12_sentiment_analysis_news/process_nlp_news_colab.ipynb)

---

## 👥 Tim Peneliti & Kolaborasi Multidisiplin

Riset ini merupakan bagian dari kolaborasi akademik antarbidang studi:
* **Bidang Teknologi Informasi / Computer Science**: Rekayasa data digital, web scraping multi-platform, pemodelan NLP Transformer RoBERTa, dan komputasi framing Entman (**Research Question 1**).
* **Bidang Sosiologi**: Analisis survei lapangan panel *attentive public* di Malaysia dan Singapura (**Research Question 2**).
* **Bidang Hubungan Internasional**: Sintesis evaluasi efektivitas diplomasi publik luar negeri Indonesia (**Research Question 3**).

---

## 📄 Lisensi
Dataset dan kode sumber ini didistribusikan di bawah lisensi [MIT License](LICENSE) untuk tujuan penelitian dan keterbukaan sains (*Open Science*).
