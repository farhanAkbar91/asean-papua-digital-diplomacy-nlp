# 🏛️ FIKSASI PIPELINE KOMPUTASIONAL & JUSTIFIKASI TEORETIS (RQ1)
**Fokus Peran**: Natural Language Processing (NLP) Engineer  
**Lingkup Tugas**: Penyelesaian Mandiri Research Question 1 (RQ1)  
**Target Deadline**: 10 November 2026 (Publikasi Scopus Q1/Q2 FISIP)  
**Tanggal Pembakuan**: 18 September 2026  

---

## 🎯 1. Batasan Peran & Ruang Lingkup Kerja

Sebagai **NLP Engineer**, ruang lingkup kerja kita dibatasi secara tegas untuk menyelesaikan **RQ1**:
> **RQ1**: *"Bagaimana sentimen/stance diplomatik dan konstruksi narasi dominan (framing) mengenai isu Papua dan identitas Melanesia dikonstruksikan dalam wacana digital internasional lintas poros geopolitik?"*

* **Di Luar Lingkup NLP Engineer**:
  * Pengelolaan survei persepsi 100 responden panel di Malaysia/Singapura via Populix/Dynata (**Tanggung jawab tim Sosiologi - RQ2**).
  * Evaluasi efektivitas diplomasi luar negeri dan kebijakan bilateral Kemlu RI (**Tanggung jawab tim Hubungan Internasional - RQ3**).
* **Deliverable Akhir NLP Engineer**:
  1. Korpus data bersih teranotasi ($N \approx 3.000 - 5.000$ data terstratifikasi).
  2. Model inferensi *Diplomatic Stance* dan *Codebook-Guided Framing*.
  3. Metrik validasi ilmiah (*Ground Truth*, Precision, Recall, Macro-F1, dan *Cohen’s Kappa*).
  4. Visualisasi analitis resolusi tinggi (300 DPI) & draf bab metode komputasional untuk naskah jurnal.

---

## 🗓️ 2. Peta Jalan Waktu Menuju 10 November 2026 (53 Hari)

```
[18-24 Sep]          [25 Sep - 8 Okt]        [9 - 20 Okt]         [21 - 31 Okt]        [1 - 10 Nov]
   FASE 1                 FASE 2                FASE 3               FASE 4               FASE 5
Fiksasi Teori &      Ekspansi Scraping     Inferensi NLP &      Validasi Empiris &    Finalisasi Naskah
Desain Pipeline       Multi-Poros Data     Pemodelan Final      Cohen's Kappa (Human) & Serah Terima
```

* **Fase 1 (18–24 Sep)**: Pembakuan teori, perumusan query global, dan pembuatan codebook leksikon.
* **Fase 2 (25 Sep – 8 Okt)**: Penarikan data terstratifikasi (X, YouTube, News) + translasi otomatis teks Melayu/Prancis.
* **Fase 3 (9–20 Okt)**: Eksekusi komputasi NLP (*Stance Calibration* & *Entman Framing Classification*).
* **Fase 4 (21–31 Okt)**: Uji validitas ilmiah terhadap sampel anotasi manusia ($N = 100 - 150$) untuk menghitung $\kappa \ge 0.75$.
* **Fase 5 (1–10 Nov)**: Penyusunan tabel statistik, grafik publikasi, dan teks metodologi untuk manuskrip Scopus.

---

## 🧠 3. Justifikasi Teoretis Inti Pipeline NLP

Untuk menjawab setiap keraguan reviewer jurnal internasional, pipeline kita didasarkan pada dua pilar teori komputasional sosial:

### Pilar I: Target-Specific Diplomatic Stance (Bukan Sentimen Emosi Biasa)
1. **Masalah Model NLP Standar**:
   * Model NLP umum (seperti RoBERTa Twitter) dirancang untuk mendeteksi emosi (*affective polarity*: senang vs sedih).
   * Pada teks diplomasi, jurnalisme formal mematuhi asas objektivitas (kata-kata terkesan netral), namun substansi agendanya dapat berupa **tekanan diplomatik terhadap kedaulatan negara**.
2. **Landasan Teoretis**:
   * Mengadopsi kerangka **Target-Specific Stance Detection** (Mohammad et al., SemEval): Mengukur sikap teks terhadap entitas target tertentu (*Target*: **Kedaulatan & Diplomasi RI di Papua**).
3. **Taksonomi 3 Kelas**:
   * **Positif (Mendukung Posisi/Kedaulatan RI)**: Mengakui status legal NKRI, mendukung otonomi khusus, menyoroti pembangunan/keamanan sipil, atau pembebasan sandera.
   * **Kritis/Negatif (Menentang/Menekan Posisi RI)**: Menyoroti pelanggaran HAM, tuntutan referendum/penentuan nasib sendiri, tuduhan militerisme ilegal, atau pemadaman internet.
   * **Netral (Faktual/Berimbang)**: Laporan kawat berita murni tanpa pemihakan moral atau wacana prosedural umum.

---

### Pilar II: Deductive Codebook-Guided Framing (Operasionalisasi Teori Entman)
1. **Masalah Topic Modeling Biasa**:
   * Metode unsupervised (seperti LDA / BERTopic murni) sering menghasilkan topik kata yang acak, ambigu, dan sulit dikaitkan dengan teori komunikasi politik.
2. **Landasan Teoretis**:
   * Mengacu pada teori framing **Robert M. Entman (1993)** dan pendekatan deduktif **Semetko & Valkenburg (2000)**.
   * Framing adalah pemilihan dan penonjolan aspek realitas untuk mendefinisikan masalah, mendiagnosis penyebab, memberikan evaluasi moral, dan menyarankan solusi.
3. **Operasionalisasi 5 Dimensi Narasi (A Priori Framing Codebook)**:
   * **Frame 1: HAM & Pelanggaran Kemanusiaan** (*Problem Definition: Human rights crisis*).
   * **Frame 2: Identitas Melanesia & Solidaritas Pasifik** (*Moral Evaluation: Ethnic & indigenous solidarity*).
   * **Frame 3: Kedaulatan & Penentuan Nasib Sendiri** (*Causal Diagnosis: Historical sovereignty dispute*).
   * **Frame 4: Pembangunan & Stabilitas Keamanan** (*Causal & Solution: Economic growth vs armed group terror*).
   * **Frame 5: Diplomasi Bilateral & Non-Interferensi** (*Treatment Recommendation: Bilateral dialogue & ASEAN Way*).

---

## 🛡️ 4. Protokol Validasi Ilmiah Standar Scopus (Kunci Kelulusan Reviewer)

Untuk menjamin temuan komputasional tidak disanggah sebagai *"AI halusinasi"*, kita akan menyertakan protokol validasi berikut:

1. **Pengambilan Sampel Emas (*Gold Standard Sub-Sample*)**:
   * Mengambil sampel acak berstrata ($N = 100 - 150$ baris) yang mencakup ketiga platform (X, YouTube, Berita).
2. **Validasi Anotasi Manusia (*Human-in-the-Loop*)**:
   * Dilakukan anotasi ganda secara independen antara sistem AI dan penilai manusia berdasarkan *Codebook* resmi.
3. **Metrik Keandalan yang Dilaporkan di Manuskrip**:
   * **Inter-Annotator Agreement**: Menghitung **Cohen’s Kappa ($\kappa$)** dengan target $\kappa \ge 0.75$ (*substantial to almost perfect agreement*).
   * **Kinerja Klasifikasi**: Melaporkan nilai **Precision, Recall, dan Macro F1-score** secara transparan pada bab metodologi.

---

## 📚 5. Daftar Rujukan Teori Awal (Untuk Sitasi Naskah Jurnal)

1. **Entman, R. M. (1993)**. *Framing: Toward clarification of a fractured paradigm*. Journal of Communication, 43(4), 51-58.
2. **Semetko, H. A., & Valkenburg, P. M. (2000)**. *Framing European politics: A content analysis of press and television news*. Journal of Communication, 50(2), 93-109.
3. **Mohammad, S. M., Kiritchenko, S., Sobhani, P., Zhu, X., & Salameh, M. (2016)**. *SemEval-2016 Task 6: Detecting Stance in Tweets*. Proceedings of the 10th International Workshop on Semantic Evaluation.
4. **Wendt, A. (1999)**. *Social Theory of International Politics*. Cambridge University Press (Teori Makro Konstruktivisme).
5. **Cardiff NLP (2022)**. *Twitter-RoBERTa-base for Sentiment Analysis*. Hugging Face Model Hub.
6. **Lazer, D., et al. (2009)**. *Computational Social Science*. Science, 323(5915), 721-723.
