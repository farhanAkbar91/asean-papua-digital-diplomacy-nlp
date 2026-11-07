# ASEAN–Papua Digital Diplomacy NLP Pipeline
### Computational Social Science & Data Triangulation Architecture — Post-Recovery Release

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-118%2F118%20passing-brightgreen)](#5-reproducibility)
[![Pipeline](https://img.shields.io/badge/pipeline__version-2.0.0--m2-4c1d95)](#3-current-technical-status)
[![Status](https://img.shields.io/badge/Status-Engineering%20closed%2C%20research%20pending-orange)](#6-handoff-and-pending-decisions)

> ⚠️ **STATUS PENELITIAN (baca sebelum menggunakan dataset)**
> 1. Dataset ini adalah **korpus pilote eksploratif (N = 1.540)**. Tidak ada anotasi manusia, tidak ada Cohen's Kappa, precision, recall, atau F1 yang pernah dihitung. Tidak ada klaim validasi ilmiah atas label apa pun.
> 2. **Label otoritatif sentiment** = prediksi model pada baris berbahasa Inggris (`data/processed/fresh_inference_en.csv`); label historis di master dipertahankan sebagai provenance. Lapisan aturan kata-kunci ("stance") adalah **eksperimental** dan tidak boleh dipakai untuk temuan utama.
> 3. Klasifikasi tematik = **analisis topic salience leksikal**, bukan pengukuran empat fungsi framing Entman.
> 4. Korpus faktual berbahasa **Inggris + Indonesia** (en 1.013 · id 295 · und 213 · 19 baris bahasa lain). Bukan korpus tiga bahasa.
> 5. Keputusan metodologis (rumusan RQ1, cakupan data, strategi bahasa, stance/framing, anotasi, penggunaan untuk RQ2/RQ3) berada pada **tim penelitian** — lihat [`docs/PENDING_DECISIONS_REGISTER.md`](docs/PENDING_DECISIONS_REGISTER.md).

---

## 1. Project Overview

Proyek ini menganalisis **wacana digital internasional seputar isu Papua dan klaim identitas Melanesia Indonesia** menggunakan Natural Language Processing (NLP), sebagai pemenuhan **Research Question 1 (RQ1)** dalam kerangka riset kolaboratif multidisiplin (Teknologi Informasi, Sosiologi, Hubungan Internasional) yang menargetkan publikasi internasional bereputasi.

Korpus dibangun dengan triangulasi tiga platform: **Platform X/Twitter** (aktivisme transnasional), **komentar YouTube** pada kanal berita regional, dan **media berita daring** (agenda-setting institusional). Setiap record membawa atribusi geografis empat arah yang dipisahkan secara eksplisit: negara penerbit, negara yang dibahas, lokasi penulis (bila terverifikasi), dan platform.

**Posisi proyek**: ini adalah penelitian **eksploratif** berbasis korpus pilote terkurasi. Dataset TIDAK merepresentasikan seluruh opini internasional, seluruh negara ASEAN/Pasifik, atau seluruh masyarakat — lihat [Research and Data Limitations](#4-research-and-data-limitations).

## 2. Project Development Timeline

Perjalanan proyek dari kondisi awal hingga engineering closure:

| Fase | Tanggal | Apa yang terjadi |
|---|---|---|
| Kondisi awal | Sep 2026 | Pipeline iteratif (scraping X/YouTube/News → sentiment RoBERTa → rule layer → framing leksikon) dengan master dataset N=1.571; dokumentasi berisi klaim yang melampaui implementasi |
| **Audit forensik** | 2026-11-07 | Audit independen menemukan: 6 dari 27 referensi fabrikan; klaim "BLEU ≥ 85" tanpa dasar; metode yang diklaim di naskah (terjemahan NMT, deteksi bahasa, evidence spans, κ ≥ 0.75) **belum pernah dieksekusi**; lapisan aturan kata-kunci menghasilkan ±25% label final; 508 dari 569 baris "framing Diplomasi" sesungguhnya residual tanpa kecocokan leksikon; bug geolokasi substring ("Nederland" → "Laos"; "un" di dalam kata apa pun → "Mitra Global"); master dataset tidak dapat direproduksi dari kode yang tersedia |
| **Recovery & rekonstruksi** | 2026-11-07 | Pipeline diperbaiki tanpa mengubah data mentah: gazetteer geografis word-boundary, framing dengan residual eksplisit `Other/No-Frame`, lapisan aturan dipisahkan sebagai kolom eksperimen, fallback senyap inference dihapus, referensi fabrikan diganti referensi terverifikasi |
| **M0 — Golden baseline** | 2026-11-07 | 1.540 retained records dibekukan sebagai baseline regresi (19 field, SHA-256 termanifestasi); 83 record dikecualikan dengan alasan eksplisit; 31 record Reddit masuk daftar REVIEW |
| **M1 — Configuration externalization** | 2026-11-07 | Seluruh konfigurasi framing/stance/pipeline/model dipindahkan ke `configs/*.yaml` verbatim; loader ketat tanpa fallback; zero semantic drift terbukti via golden regression |
| **M2 — Module split** | 2026-11-07 | Pipeline dimodularisasi (`src/pipeline/`: preprocess, langid, translation seam, sentiment, stance, framing, orchestrator CLI dengan stage manifest); entry point lama tetap kompatibel |
| **M2.1 — Audit & reliability** | 2026-11-07/08 | Audit independen terhadap implementasi aktual; perbaikan keandalan (proteksi stale-output, kelengkapan manifest gagal, guard kosakata stance); stamping versi (`pipeline_version`, config content identifiers); koreksi dokumentasi |
| **T1 — Fresh inference** | 2026-11-08 | **Inferensi baru sungguhan** untuk 1.013 record berbahasa Inggris dengan model Cardiff pada lingkungan terverifikasi (Python 3.11, torch 2.15.0+cpu, transformers 5.22.2); revisi model aktual terekam |
| **Final closure & handoff** | 2026-11-08 | Dokumentasi penutupan, dataset dictionary, register keputusan, laporan akhir bahasa Indonesia (`docs/LAPORAN_AKHIR_PEMULIHAN_DAN_EVALUASI_PROYEK.pdf`), publikasi ke GitHub |

Rincian lengkap: [`docs/RECOVERY_LOG.md`](docs/RECOVERY_LOG.md) dan [`docs/FINAL_VALIDATION_REPORT.md`](docs/FINAL_VALIDATION_REPORT.md).

## 3. Current Technical Status

| Item | Nilai (terverifikasi) |
|---|---|
| Master dataset | `data/processed/master_triangulation_repaired.csv` — **1.540 baris retained** (X 364 · YouTube 864 · News 312) |
| Fresh inference (EN) | `data/processed/fresh_inference_en.csv` — **1.013 record berbahasa Inggris** |
| Hasil fresh inference | **Negative 348 · Neutral 537 · Positive 128** (determinism spot-check lulus) |
| Model | `cardiffnlp/twitter-roberta-base-sentiment-latest` (English-only, sesuai model card resmi) |
| Model revision | `3216a57f2a0d9c45a2e6c20157c20c49fb4bf9c7` (diresolusi dari snapshot cache Hugging Face saat eksekusi) |
| Pipeline version | `2.0.0-m2` |
| Automated tests | **118/118 passing** |
| Golden regression | **Zero drift** pada 19 field × 1.540 baris terhadap baseline M0 (SHA `4e2cf764…` tidak berubah) |
| Master & golden | **Tidak dimodifikasi** oleh fresh inference (artefak terpisah; penggabungan menunggu keputusan tim) |
| Bahasa korpus | en 1.013 · id 295 · und 213 · 19 baris bahasa lain (tl 4, lt 2, 13 singleton) — tanpa konten Melayu/Prancis terukur |

**Catatan penting**: 118 tes otomatis yang lulus membuktikan **perangkat lunak bekerja sesuai spesifikasinya** — bukan bahwa penelitian telah tervalidasi secara ilmiah, dan bukan ukuran akurasi model. Fresh inference adalah **eksekusi yang terverifikasi**, bukan pengukuran akurasi.

## 4. Research and Data Limitations

Ringkasan jujur (rincian: [`docs/METHODOLOGY_REPAIRED.md`](docs/METHODOLOGY_REPAIRED.md) §6, [`docs/DATA_QUALITY_AUDIT.md`](docs/DATA_QUALITY_AUDIT.md)):

1. **Tidak ada validasi manusia** — tidak ada κ/precision/recall/F1; tidak ada klaim akurasi model.
2. **Sentimen non-Inggris tidak tercakup** — 295 baris Indonesia + 213 baris `und` berada di luar inferensi; label historisnya tidak dapat dipertanggungjawabkan.
3. **Geografi X tidak terverifikasi** untuk 260/364 baris (lokasi profil kosong); blok YouTube = kohort kanal, bukan asal komentator.
4. **Waktu**: YouTube hanya punya timestamp relatif; 4 artikel bertanggal hari-scraping; rentang berita 2008–2026 tanpa stratifikasi.
5. **Sumber timpang**: 59,7% pilar YouTube berasal dari satu kanal; S1 (ASEAN) bertumpu pada MY/SG; penerbit Melanesia/Pasifik = nol; kategori transnasional didominasi satu outlet.
6. **Stance & framing**: rule layer bersifat eksperimental (asumsi arah terdokumentasi); framing = topic salience leksikal, bukan empat fungsi Entman.
7. **Generalisasi**: korpus pilote tidak mendukung klaim representatif atas negara, masyarakat, atau opini internasional, maupun inferensi sebab-akibat.

## 5. Reproducibility

```bash
# 1) environment (Python 3.11 disarankan untuk inference):
pip install -r requirements.txt

# 2) bangun master dataset + manifest:
python src/build_master_repaired.py

# 3) jalankan seluruh 118 tes:
python -m unittest discover -s tests

# 4) fresh inference EN (terpisah dari master/golden; butuh torch+transformers):
python src/run_fresh_inference.py

# 5) stage CLI (contoh):
python src/pipeline/run.py --stage framing --platform youtube \
  --input data/raw/youtube_papua_asean_comments.csv --output out/framing_yt.csv
```

Integritas: bandingkan SHA-256 master dengan `data/processed/build_manifest.json`; golden baseline harus tetap `4e2cf764f1800266eacf3a96763c901d2b2438fb54f0655207a2ba4a3372a370` (lihat [`docs/M0_GOLDEN_BASELINE_MANIFEST.json`](docs/M0_GOLDEN_BASELINE_MANIFEST.json)).

## 6. Handoff and Pending Decisions

**Engineering closure selesai** (pipeline, tes, manifest, dokumentasi). Keputusan metodologis dan penelitian berada pada tim:

- Rumusan final RQ1 (F1/F2/F3 — tiga formulasi masih terdokumentasi, belum diputuskan).
- Cakupan data (ASEAN-only vs curated-internasional — rekomendasi feasibility: curated internasional, lihat [`docs/RQ1_HANDOFF_REQUIREMENTS.md`](docs/RQ1_HANDOFF_REQUIREMENTS.md) §8), periode, kuota.
- Strategi bahasa (terjemahan id→en, model multibahasa, atau scope-out) dan master-refresh (menggabungkan fresh inference menimpa golden baseline — butuh persetujuan).
- Codebook stance (target/proposisi, unit analisis) dan framing; desain anotasi (2 anotator ideal / 1 anotator = referensi terbatas / tanpa anotasi = eksploratif-deskriptif; **Cohen's Kappa tidak diwajibkan** dalam proyek ini).
- Penggunaan keluaran RQ1 sebagai input RQ2/RQ3.

Register lengkap: [`docs/PENDING_DECISIONS_REGISTER.md`](docs/PENDING_DECISIONS_REGISTER.md). Kewajiban penerima: baca [`docs/RQ1_HANDOFF_REQUIREMENTS.md`](docs/RQ1_HANDOFF_REQUIREMENTS.md) (permitted/prohibited uses) sebelum menganalisis.

## 7. Repository Structure

```text
├── README.md                      <- dokumen ini
├── LICENSE (MIT) · requirements.txt · .gitignore
├── data/
│   ├── raw/                       <- data mentah X/YouTube/News (tidak diubah)
│   ├── processed/                 <- master_triangulation_repaired.csv + build_manifest.json
│   │                                 + fresh_inference_en.csv(.manifest.json)
│   └── golden/m0/                 <- golden baseline beku (regresi)
├── src/
│   ├── nlp_core.py · config_loader.py · build_master_repaired.py · run_inference.py
│   ├── run_fresh_inference.py     <- T1: fresh EN inference
│   └── pipeline/                  <- M2: config, preprocess, langid, translation (mati),
│                                    sentiment, stance, framing, run (CLI stage)
├── tests/                         <- 118 tes (unit + integrasi + regresi golden)
├── configs/                       <- lexicon.yaml, rules.yaml, pipeline.yaml, models.yaml
├── docs/                          <- METHODOLOGY_REPAIRED, RECOVERY_LOG, FINAL_VALIDATION_REPORT,
│                                    DATASET_DICTIONARY, PENDING_DECISIONS_REGISTER, RQ1_FINALIZATION_PLAN,
│                                    RQ1_HANDOFF_REQUIREMENTS, LAPORAN_AKHIR_PEMULIHAN_DAN_EVALUASI_PROYEK.pdf,
│                                    methodology_history/, manuscripts/
├── notebooks/                     <- notebook Colab historis (pra-perbaikan)
└── archive/                       <- pipeline legacy + dokumen pra-perbaikan (provenance)
```

Dokumen metodologi historis (M0–M2.1): [`docs/M0_PREFLIGHT_REPORT.md`](docs/M0_PREFLIGHT_REPORT.md) · [`docs/M1_IMPLEMENTATION_REPORT.md`](docs/M1_IMPLEMENTATION_REPORT.md) · [`docs/M2_IMPLEMENTATION_REPORT.md`](docs/M2_IMPLEMENTATION_REPORT.md) · [`docs/NLP_PIPELINE_REFACTOR_PLAN.md`](docs/NLP_PIPELINE_REFACTOR_PLAN.md) · [`docs/RQ_SPECIFIC_RESEARCH_DESIGN.md`](docs/RQ_SPECIFIC_RESEARCH_DESIGN.md) · [`docs/GLOBAL_SAMPLING_FRAMEWORK.md`](docs/GLOBAL_SAMPLING_FRAMEWORK.md) · [`docs/COUNTRY_SOURCE_REGISTER.csv`](docs/COUNTRY_SOURCE_REGISTER.csv) · [`docs/LANGUAGE_COVERAGE_MATRIX.csv`](docs/LANGUAGE_COVERAGE_MATRIX.csv) · [`docs/DATA_COLLECTION_PROTOCOL_DRAFT.md`](docs/DATA_COLLECTION_PROTOCOL_DRAFT.md) · [`docs/DATA_QUALITY_AUDIT.md`](docs/DATA_QUALITY_AUDIT.md) · [`docs/DATA_EXCLUSION_REGISTER.csv`](docs/DATA_EXCLUSION_REGISTER.csv) · [`docs/SUPPLEMENTARY_COLLECTION_PLAN.md`](docs/SUPPLEMENTARY_COLLECTION_PLAN.md).

## 8. License

Dataset dan kode didistribusikan di bawah [MIT License](LICENSE). Data sosial di dalam korpus adalah konten publik platform yang bersangkutan; lihat catatan etika pada [`docs/METHODOLOGY_REPAIRED.md`](docs/METHODOLOGY_REPAIRED.md) §6.
