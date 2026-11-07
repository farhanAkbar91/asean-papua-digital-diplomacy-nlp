> ⚠️ **STATUS (2026-11-07)**: Dokumen perencanaan historis. Skema kolom dan protokol validasi di sini TIDAK identik dengan dataset yang terimplementasi — ikuti `docs/METHODOLOGY_REPAIRED.md` dan `src/build_master_repaired.py` sebagai acuan otoritatif. Entri validasi (kappa/F1) berstatus BELUM DILAKSANAKAN.

# 🚀 BLUEPRINT FINAL: PIPELINE NLP & METODOLOGI KOMPUTASIONAL (RQ1)
**Status Dokumen**: FINAL & TERKUNCI (*LOCKED ARCHITECTURE*)  
**Peran**: Natural Language Processing (NLP) Engineer  
**Fokus Penelitian**: Research Question 1 (Wacana Digital Internasional Isu Papua & Melanesia)  
**Target Publikasi**: Jurnal Internasional Bereputasi Tinggi (Scopus Q1/Q2 FISIP)  
**Tenggat Waktu**: 10 November 2026  

---

## 💡 1. Penambahan Kunci: "Operational Discursive Synthesis" (Solusi Teori Entman)

Satu elemen krusial yang kita sempurnakan adalah **Sintesis Diskursif Operasional (*Operational Discursive Synthesis*) antara *Diplomatic Stance* dan *Thematic Framing***.

Dalam tradisi *Computational Social Science*, kita tidak mengklaim *stance* secara mekanistik identik dengan kausalitas murni. Sebaliknya, kita memposisikannya sebagai **inferensi operasional (*operational inference*)**:
* **Target Stance Eksplisit (`stance_target`)**: Ditetapkan secara baku:  
  $$\text{Target} = \textbf{"Indonesia's Sovereignty \& Diplomatic Position in Papua"}$$
* **Sintesis 4 Elemen Entman (1993)**:
  1. **Define Problem (Masalah Utama)**: Ditentukan oleh **Thematic Frame** (isu apa yang memperoleh *salience*: HAM, kedaulatan, identitas Melanesia, stabilitas pembangunan, atau diplomasi).
  2. **Diagnose Cause & Make Moral Judgement (Aktor & Nilai Etis)**: Diinferensikan secara operasional melalui **Diplomatic Stance terhadap Target** (apakah narasi membebankan atribusi negatif/kritis kepada otoritas RI atau membebankan atribusi negatif kepada kelompok separatis bersenjata/OPM).
  3. **Suggest Remedies / Treatment (Rekomendasi Solusi)**: Dihasilkan dari **Sintesis Frame × Stance** (misal: Frame HAM + Stance Kritis secara operasional mengarah pada rekomendasi intervensi/investigasi PBB).
* **Explainability (Evidence Span Extraction)**: Model NLP mengekstrak bukti leksikal spesifik (`stance_evidence_span` dan `framing_evidence_span`) sebagai *rationale* transparan keputusan AI.

```
                  ┌────────────────────────────────────────┐
                  │          TEKS WACANA DIGITAL           │
                  └──────────────────┬─────────────────────┘
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
    [ THEMATIC FRAME CATEGORY ]             [ DIPLOMATIC STANCE ]
    1. Define Problem                       Target: RI Sovereignty in Papua
       (Issue Salience)                     2. Diagnose Cause (Operational)
       Evidence: framing_evidence_span      3. Make Moral Judgement
                 │                          Evidence: stance_evidence_span
                 │                                       │
                 └───────────────────┬───────────────────┘
                                     ▼
                  ┌─────────────────────────────────────┐
                  │    OPERATIONAL DISCURSIVE SYNTHESIS │
                  │   4. Suggest Remedies / Treatment   │
                  │      (Rekomendasi Tindakan/Solusi)  │
                  │   Contoh: HAM + Stance Kritis       │
                  │   -> Inferensi: Desakan Akses PBB   │
                  └─────────────────────────────────────┘
```

Dengan formulasi inferensi operasional ini, metodologi kita **secara elegan dan defensif menjembatani teori Robert Entman (1993)** tanpa klaim deterministik yang rentan didebat reviewer!

---

## 🔄 2. Diagram Alur Pipeline End-to-End (5 Tahap Kerja Final)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TAHAP 1: AKUISISI DATA SKALA GLOBAL TERSTRATIFIKASI                                   │
│ • 4 Poros: 1) Pasifik/Melanesia, 2) ASEAN, 3) Anglosphere/Barat, 4) Multilateral/PBB   │
│ • 3 Platform: Media Berita Resmi, Komentar Berita YouTube, Platform X                  │
│ • 3 Bahasa Input: Bahasa Inggris (~85%), Bahasa Melayu (~10%), Bahasa Prancis (~5%)   │
│ • Filter: Query Boolean Anti-Ambiguitas (Eliminasi noise non-politik & rugby/flora)    │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TAHAP 2: PIPELINE TRANSLASI & STANDARISASI DATA (LINGUA FRANCA NORMALIZATION)          │
│ • Deteksi Bahasa Otomatis (Language Identification)                                    │
│ • Machine Translation: Translasi teks Melayu & Prancis ke Bahasa Inggris               │
│ • Pembersihan Teks: Regex noise, custom stopwords jurnalistik, & lead paragraph parser  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TAHAP 3: DUAL-TRACK NLP INFERENCE (PEMODELAN INTI)                                     │
│ ┌──────────────────────────────────────┐     ┌───────────────────────────────────────┐ │
│ │ Track A: Diplomatic Stance (RoBERTa) │     │ Track B: Codebook-Guided Framing      │ │
│ │ • Pretrained Twitter-RoBERTa         │     │ • 5 Dimensi Operasionalisasi Entman   │ │
│ │ • Stance Calibration Rules (SemEval) │     │ • A Priori Deductive Lexicon Codebook │ │
│ │ Output: Positif / Kritis / Netral    │     │ Output: 5 Kategori Bingkai Narasi     │ │
│ └──────────────────┬───────────────────┘     └───────────────────┬───────────────────┘ │
└────────────────────┼─────────────────────────────────────────────┼─────────────────────┘
                     └──────────────────────┬──────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TAHAP 4: SINTESIS ENTMAN & STRATIFIKASI GEOPOLITIK                                    │
│ • Matriks Silang Stance × Framing (Memetakan Cause, Moral Judgement, & Remedy)         │
│ • Komparasi Sebaran Wacana: Poros ASEAN vs Pasifik vs Barat vs Multilateral            │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TAHAP 5: PROTOKOL VALIDASI ILMIAH (STANDAR SCOPUS Q1/Q2)                               │
│ • Sampling Gold Standard Acak Terstratifikasi (N = 100 - 150 data)                     │
│ • Anotasi Ganda Independen (AI Model vs Human Expert)                                  │
│ • Pelaporan Metrik Reliabilitas: Cohen's Kappa (κ ≥ 0.75), Precision, Recall, Macro-F1 │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 3. Matriks Operasionalisasi 5 Kategori Bingkai Tematik dalam Kerangka Entman
*(Thematic Frame Categories Operationalized within Entman's Framework)*

Berikut matriks resmi yang akan dicantumkan di naskah publikasi untuk membuktikan bahwa pembingkaian tematik kita valid secara ilmiah dalam kerangka teori Entman (1993):

| Kode Frame | Kategori Bingkai Tematik (*Thematic Frame*) | Definisi Masalah (*Problem*) & Solusi (*Remedy*) | Inferensi Kausal (*Cause*) Berdasarkan Stance |
| :---: | :--- | :--- | :--- |
| **F1** | **HAM & Pelanggaran Kemanusiaan** | Masalah: Kekerasan terhadap warga sipil.<br>Remedy: Akses PBB & investigasi independen. | • *Kritis*: Otoritas keamanan / Pemerintah RI.<br>• *Positif*: Teror KKB/separatis terhadap guru/nakes. |
| **F2** | **Identitas Melanesia & Rasial** | Masalah: Solidaritas adat, ras Melanesia, & budaya.<br>Remedy: Keanggotaan penuh di MSG & aliansi Pasifik. | • *Kritis*: Kolonialisme & marjinalisasi ras Melanesia.<br>• *Positif*: Indonesia rumah bagi 13 juta ras Melanesia. |
| **F3** | **Kedaulatan & Dekolonisasi** | Masalah: Legalitas status politik & Pepera 1969.<br>Remedy: Hak penentuan nasib sendiri (*Self-Determination*). | • *Kritis*: Pendudukan ilegal / aneksasi teritorial.<br>• *Positif*: Integritas wilayah NKRI sah diakui PBB. |
| **F4** | **Pembangunan & Stabilitas** | Masalah: Stabilitas ekonomi, infrastruktur, & sandera.<br>Remedy: Penegakan hukum terukur & percepatan Otsus. | • *Kritis*: Eksploitasi tambang (Freeport) & deforestasi.<br>• *Positif*: Pemerataan Trans-Papua & pembebasan sandera. |
| **F5** | **Diplomasi Regional & Bilateral** | Masalah: Hubungan diplomatik antarnegara di forum dunia.<br>Remedy: Kepatuhan pada prinsip *ASEAN Non-Interference*. | • *Kritis*: Desakan negara Pasifik di forum PBB.<br>• *Positif*: Kemitraan bilateral erat RI-Malaysia-Singapura. |

---

## 🗃️ 4. Struktur Standar Dataset Master Akhir (`master_dataset_global_rq1.csv`)

Setiap baris data yang diproses oleh pipeline final ini memiliki struktur kolom standar yang transparan dan dapat diaudit (*explainable & auditable*):

1. `item_id`: Pengidentifikasi unik data wacana.
2. `platform`: Sumber platform (`News_Media`, `YouTube_Comment`, `X_Twitter`).
3. `geopolitical_bloc`: 4 Poros (`Pacific_Melanesia`, `ASEAN_Bloc`, `Western_Anglosphere`, `Multilateral_Global`).
4. `source_entity`: Nama media / kanal (misal: `CNA_Singapore`, `RNZ_Pacific`, `ABC_Australia`, `TheStar_Malaysia`).
5. `raw_language`: Bahasa asli sebelum translasi (`en`, `ms`, `fr`).
6. `original_text`: Teks mentah asli dari sumber.
7. `english_text`: Teks yang telah distandarisasi ke Bahasa Inggris via machine translation.
8. `stance_target`: Target acuan sikap baku (`"Indonesia's Sovereignty & Governance in Papua"`).
9. `diplomatic_stance`: Sikap terhadap target (`Positive_Supportive`, `Critical_Oppositional`, `Neutral_Factual`).
10. `stance_confidence`: Skor probabilitas model Transformer (0.0 - 1.0).
11. `stance_evidence_span`: Rationale/frasa kunci pemicu sikap (misal: `["rights abuses", "illegal occupation"]`).
12. `thematic_frame`: Kategori bingkai tematik (`F1_HAM`, `F2_Melanesian_Identity`, `F3_Sovereignty`, `F4_Development_Security`, `F5_Regional_Diplomacy`).
13. `framing_evidence_span`: Rationale/leksikon kunci pemicu bingkai (misal: `["human rights", "un commissioner", "torture"]`).
14. `operational_synthesis`: Label sintesis operasional wacana Entman (misal: `HAM_Critical_Abuse_Allegation` atau `Sovereignty_Supportive_Territorial`).

---

## 🎯 5. Status Kesiapan Menuju 10 November 2026

Dengan dokumen cetak biru yang telah diperbarui ini:
1. **Pipeline sudah 100% terkunci** secara arsitektur, metodologi, dan skema data.
2. **Justifikasi teoretis sepenuhnya defensif**:
   * Stance detection memiliki target formal yang eksplisit (`stance_target`).
   * Hubungan Stance dan Framing diposisikan secara akademis sebagai *operational discursive synthesis*.
   * Nomenklatur pembingkaian dibakukan menjadi *thematic frame categories operationalized within Entman's framework*.
   * Prinsip *Explainable NLP (XAI)* terpenuhi melalui *evidence span extraction*.
3. **Pekerjaan NLP Engineer menjadi sangat jelas dan terukur**: kita tinggal menjalankan eksekusi teknis langkah demi langkah sesuai jadwal 5 fase menuju 10 November 2026.
