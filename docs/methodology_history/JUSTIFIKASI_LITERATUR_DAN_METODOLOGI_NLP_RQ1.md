# 📚 JUSTIFIKASI LITERATUR & METODOLOGI KOMPUTASIONAL NLP (RQ1)
**Dokumen Pendukung Manuskrip Publikasi Scopus Q1/Q2**  
**Bidang Keilmuan**: Computational Social Science, Digital Diplomacy, & Natural Language Processing  
**Fokus Penelitian**: Research Question 1 (RQ1) - Wacana Digital Internasional Isu Papua & Identitas Melanesia  
**Tanggal Pembakuan**: 18 September 2026  
**Revisi Integritas**: 7 November 2026 — sitasi fabrikan dihapus/diganti, klaim BLEU ≥ 85 dihapus, atribusi Semetko & Valkenburg dikoreksi. Lihat `METHODOLOGY_REPAIRED.md` dan `RECOVERY_LOG.md`.

---

## 📌 1. Pengantar & Tujuan Dokumen

Dokumen ini disusun sebagai **repositori pembelaan metodologis (*methodological defense repository*)** yang memuat landasan teoretis, justifikasi komputasional, serta daftar referensi ilmiah baku untuk mempertahankan setiap keputusan teknis dalam perancangan pipeline NLP RQ1. Berkas ini disiapkan untuk diintegrasikan ke dalam Bab Metodologi (*Research Methods*) dan penanganan tanggapan reviewer (*Response to Reviewers*).

---

## 🏛️ 2. Tujuh Pilar Pembelaan Metodologis (*The 7 Methodological Pillars*)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   7 PILAR JUSTIFIKASI ILMIAH METODOLOGI NLP (RQ1)                      │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Trilingual Selection    │ 2. Translate-Test Pipeline │ 3. Triangulasi Multi-Platform│
│    (EN, MS, FR)            │    (NMT Normalization)     │    (News, YouTube, X)        │
├────────────────────────────┼────────────────────────────┼──────────────────────────────┤
│ 4. Inverted Pyramid Lead   │ 5. Purposive Niche Corpus  │ 6. Target-Specific Stance    │
│    (250 Words Truncation)  │    (N = 3.000 - 5.000)     │    (vs General Polarity)     │
├────────────────────────────┴────────────────────────────┴──────────────────────────────┤
│ 7. Operational Discursive Synthesis & Explainability (Entman Framing + Kappa ≥ 0.75)    │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 🌐 PILAR 1: Pemilihan Tiga Bahasa Strategis (Inggris, Melayu, Prancis)

#### Pertanyaan Kritis Reviewer:
> *"Mengapa korpus dibatasi pada Bahasa Inggris, Melayu, dan Prancis? Mengapa tidak menyertakan Bahasa Belanda atau Spanyol?"*

#### Argumentasi Ilmiah & Pembelaan:
1. **Bahasa Inggris ($\approx 85-90\%$) sebagai *Lingua Franca* Diplomasi Internasional**:
   * Bahasa kerja resmi Sidang Umum PBB, forum multilateral (*Pacific Islands Forum*), dan kawat berita global (*Reuters, AP, AFP*). Teks hukum internasional terkait hak asasi dan integritas teritorial hampir seluruhnya dirilis dalam Bahasa Inggris.
   * *Sitasi*: Crystal (2003). *(Catatan revisi: sitasi "Ammon (2001)" dan "Ku & Yiu (2012)" yang sebelumnya digunakan ternyata tidak dapat diverifikasi keberadaannya dan telah dihapus pada audit integritas 2026-11-07.)*
2. **Bahasa Melayu ($\approx 5-10\%$) untuk Konteks Regional ASEAN (Sasaran RQ2)**:
   * Relevan secara mutlak untuk menangkap wacana asli masyarakat dan media di Malaysia (*Astro Awani, Berita Harian*), yang menjadi target pengujian persepsi *attentive public* pada RQ2.
   * *Sitasi*: Collins (1998); Milner (2008).
3. **Bahasa Prancis ($\approx 3-5\%$) untuk Poros Diplomasi Melanesia Pasifik (Kaledonia Baru)**:
   * Salah satu aktor advokasi paling vokal dalam mendukung perjuangan kemerdekaan Papua di forum *Melanesian Spearhead Group* (MSG) adalah **Kaledonia Baru (Kanaky - Front de Libération Nationale Kanak et Socialiste / FLNKS)** yang berbahasa resmi Prancis. Selain itu, Republik Vanuatu adalah negara bilingual resmi Inggris-Prancis. Mengabaikan Bahasa Prancis berarti mendistorsi representasi resmi blok Pasifik.
   * *Sitasi*: Maclellan (2016); Lawson (2013).

---

### 🔄 PILAR 2: Pendekatan *Translate-Test Pipeline* vs Model Multilingual Asli

#### Pertanyaan Kritis Reviewer:
> *"Mengapa menggunakan Machine Translation untuk menstandarisasi teks ke Bahasa Inggris alih-alih langsung menggunakan model multilingual seperti XLM-RoBERTa atau mBERT?"*

#### Argumentasi Ilmiah & Pembelaan:
1. **Menghindari Penurunan Kapasitas Semantik (*The Curse of Multilinguality*)**:
   * Model multilingual seperti `XLM-RoBERTa` membagi kapasitas parameternya untuk $\ge 100$ bahasa sekaligus, yang secara empiris terbukti menurunkan performa pemahaman nuansa semantik halus (*fine-grained political sentiment*) pada teks informal media sosial dibandingkan model khusus bahasa tunggal seperti `Twitter-RoBERTa-base`.
   * *Sitasi*: Conneau et al. (2020); Barbieri et al. (2020).
2. **Konsistensi Ruang Leksikon Tunggal (*Single Vector Space for Deductive Framing*)**:
   * Menstandarisasi ke Bahasa Inggris memungkinkan buku kode leksikon (*codebook*) untuk 5 kategori Entman didefinisikan satu kali secara baku. Ini mencegah pergeseran makna (*semantic drift*) yang tak terhindarkan jika konsep hukum rumit (misal: *"self-determination"*, *"act of free choice"*) harus diterjemahkan ke kamus multi-bahasa.
3. **Kualitas Neural Machine Translation (NMT) Modern — dengan verifikasi wajib**:
   * Sistem NMT modern (mis. NLLB-200) menunjukkan kualitas terjemahan tinggi pada pasangan bahasa sumber daya-menengah; Namun, **tidak ada sistem NMT yang dilaporkan mencapai BLEU ≥ 85** pada pasangan berita terbuka apa pun (rentang realistis SOTA: ± 40–50 BLEU; klaim "BLEU ≥ 85" yang sebelumnya tertulis di dokumen ini telah **dihapus** karena tidak didukung literatur apa pun).
   * Konsekuensi metodologis: kualitas terjemahan **wajib diuji acak (spot-check)** pada sampel sebelum inferensi, karena literatur menunjukkan terjemahan machine dapat memengaruhi klasifikasi sentimen hilir (indirect translation).
   * *Sitasi*: NLLB Team (2022); Poncelas, Lohar, Hadley & Way (2020, AMTA). *(Catatan revisi: sitasi "Poncelas, Hadley & Way (2020, EAMT, hlm. 353–362)" sebelumnya tidak ditemukan pada indeks EAMT 2020 dan telah diganti dengan versi AMTA yang terverifikasi.)*

---

### 📐 PILAR 3: Triangulasi Tiga Platform (Media Berita, YouTube, X)

#### Pertanyaan Kritis Reviewer:
> *"Apa dasar pemilihan media berita, komentar YouTube, dan X? Mengapa tidak menggunakan platform tunggal?"*

#### Argumentasi Ilmiah & Pembelaan:
1. **Mitigasi Bias Algoritmik Platform Tunggal (*Cross-Platform Triangulation*)**:
   * Setiap platform memiliki bias demografi dan algoritma tersendiri. Menggabungkan 3 pilar ini menciptakan triangulasi wacana yang utuh dan representatif:
     * **Media Berita Resmi**: Mewakili *Institutional Agenda-Setting* (pandangan elit, kawat berita formal, kebijakan luar negeri resmi). (*Sitasi: McCombs & Shaw, 1972*).
     * **Platform X (Twitter)**: Mewakili *Elite & Transnational Activism* (diplomat, jurnalis investigasi, aktivis diaspora, seruan tagar PBB). (*Sitasi: Castells, 2015*).
     * **Komentar YouTube**: Mewakili *Deliberative / Dialectical Public Sphere* (reaksi spontan publik awam dan terdidik lintas negara atas video investigasi CNA, ABC, Al Jazeera). (*Sitasi: Halpern & Gibbs, 2013*).
2. **Keandalan Metodologis**:
   * *Sitasi*: Barbier, Feng, Gundecha & Liu (2013), *Provenance Data in Social Media* (Morgan & Claypool). *(Catatan revisi: entri "Barbier et al. (2012) — Cross-platform triangulation, SBP, hlm. 178–186" tidak ditemukan pada TOC SBP 2012/LNCS 7227 dan telah diganti dengan monograf 2013 yang terverifikasi.)*

---

### 📰 PILAR 4: Pemotongan Berita Model Piramida Terbalik (*Inverted Pyramid Lead - 250 Kata*)

#### Pertanyaan Kritis Reviewer:
> *"Mengapa teks artikel berita panjang hanya dianalisis pada judul dan 250 kata pertama? Apakah ini tidak menghilangkan konteks berita?"*

#### Argumentasi Ilmiah & Pembelaan:
1. **Kaidah Jurnalistik Internasional (*The Inverted Pyramid Principle*)**:
   * Berita kawat internasional (Reuters, AP, CNA, The Star) dirancang dengan struktur piramida terbalik: fakta kunci 5W+1H, *framing* utama, dan sikap editorial terkonsentrasi pada paragraf pembuka (*lead paragraph*). Paragraf-paragraf lanjutan umumnya bersifat penjelasan teknis atau pengulangan latar belakang masa lalu (*historical boilerplate*).
   * *Sitasi*: Pöttker (2003).
2. **Kesesuaian Token Transformer Tanpa Truncation Bias**:
   * Model Transformer berbasis BERT/RoBERTa memiliki batasan komputasi 512 subword tokens. Mengambil judul + lead paragraph memastikan seluruh unit analisis berada dalam batas representasi penuh model tanpa pemotongan acak di tengah kalimat.

---

### 🎯 PILAR 5: Skala Kuota Korpus Terkurasi ($N = 3.000 - 5.000$)

#### Pertanyaan Kritis Reviewer:
> *"Mengapa ukuran dataset berkisar ribuan data dan bukan 'Big Data' ratusan ribu atau jutaan baris?"*

#### Argumentasi Ilmiah & Pembelaan:
1. **Karakteristik Isu: *High-Stakes Niche Geopolitics***:
   * Berbeda dengan topik budaya pop viral atau pemilu nasional, wacana diplomasi Papua adalah topik kebijakan luar negeri yang spesifik (*niche*).
   * Menarik data dalam skala jutaan baris justru akan mengorbankan kualitas data dengan menyedot jutaan tuitan bot spam, promosi kripto dengan tagar acak, atau ambiguitas entitas (*Papua New Guinea, flora/fauna*).
2. **Prinsip Kualitas Korpus Domain Spesifik**:
   * Jurnal bereputasi mengutamakan kemurnian data (*curated domain corpus*) daripada kuantitas data mentah penuh kebisingan.
   * *Sitasi*: Jungherr (2015); Barberá et al. (2021).

---

### ⚖️ PILAR 6: *Target-Specific Diplomatic Stance* (Bukan Sentimen Emosional)

#### Pertanyaan Kritis Reviewer:
> *"Mengapa tidak menggunakan analisis sentimen standar positif/negatif biasa?"*

#### Argumentasi Ilmiah & Pembelaan:
1. **Bias Kesantunan Jurnalisme (*Civility Bias in Diplomatic Reporting*)**:
   * Berita kawat formal ditulis dengan bahasa gramatikal netral dan santun (*objective journalism*). Model sentimen umum akan mengklasifikasikan kalimat *"UN human rights commissioner requests unhindered access to Jayapura"* sebagai **Netral**, padahal secara geopolitik kalimat tersebut membawa muatan tekanan kritis terhadap kedaulatan RI.
2. **Kesesuaian Target Eksplisit**:
   * Dengan menetapkan target baku:  
     $$\text{Target} = \textbf{"Indonesia's Sovereignty \& Governance in Papua"}$$  
     kita mengukur secara presisi posisi wacana teks terhadap klaim politik Indonesia, sesuai dengan standar *SemEval Stance Detection*.
   * *Sitasi*: Mohammad et al. (2016); Küçük & Can (2020).

---

### 🧩 PILAR 7: Sintesis Diskursif Operasional Entman & Standar Reliabilitas ($\kappa \ge 0.75$)

#### Pertanyaan Kritis Reviewer:
> *"Bagaimana Anda membuktikan bahwa klasifikasi framing Anda memenuhi teori Entman (1993) dan bukan sekadar klasifikasi topik biasa? Bagaimana mengukur keandalannya?"*

#### Argumentasi Ilmiah & Pembelaan:
1. **Operational Discursive Synthesis**:
   * 4 Elemen Entman dijembatani secara operasional melalui perpaduan *Issue Salience* (Thematic Frame) dan *Target Orientation* (Diplomatic Stance), didukung ekstraksi *Evidence Spans* (Explainable NLP).
   * *Sitasi*: Entman (1993); Matthes & Kohring (2008).
2. **Metrik Kesepakatan Antar-Anotator (*Inter-Annotator Agreement*)**:
   * Menggunakan uji **Cohen's Kappa ($\kappa$)** pada sampel acak validasi ($N = 100 - 150$). Ambang batas $\kappa \ge 0.75$ menjamin kesepakatan tingkat *substantial to almost perfect*, membuktikan bahwa model AI bekerja selaras dengan pakar manusia.
   * *Sitasi*: Cohen (1960); Landis & Koch (1977).

---

## 📖 3. Daftar Referensi Baku (Dapat Langsung Disalin ke Naskah)
**Status: TERVERIFIKASI (audit integritas 2026-11-07).** Entri fabrikan telah dihapus; entri dengan kesalahan bibliografis telah dikoreksi. Detail verifikasi: `RECOVERY_LOG.md`.

```text
Barberá, P., Boydstun, A. E., Linn, S., McMahon, R., & Nagler, J. (2021). Automated text classification of news articles: A practical guide. Political Analysis, 29(1), 19-42. https://doi.org/10.1017/pan.2020.8

Barbier, G., Feng, Z., Gundecha, P., & Liu, H. (2013). Provenance Data in Social Media. Morgan & Claypool (Synthesis Lectures on Data Mining and Knowledge Discovery). https://doi.org/10.1007/978-3-031-01904-3

Barbieri, F., Camacho-Collados, J., Espinosa-Anke, L., & Neves, L. (2020). TweetEval: Unified benchmark and comparative evaluation for tweet classification. In Findings of the Association for Computational Linguistics: EMNLP 2020 (pp. 1644-1650). https://aclanthology.org/2020.findings-emnlp.148/

Castells, M. (2015). Networks of Outrage and Hope: Social Movements in the Internet Age (2nd ed.). Polity Press.

Cohen, J. (1960). A coefficient of agreement for nominal scales. Educational and Psychological Measurement, 20(1), 37-46. https://doi.org/10.1177/001316446002000104

Collins, J. T. (1998). Malay, World Language: A Short History. Dewan Bahasa dan Pustaka.

Conneau, A., Khandelwal, K., Goyal, N., Chaudhary, V., Wenzek, G., Guzmán, F., Grave, E., Ott, M., Zettlemoyer, L., & Stoyanov, V. (2020). Unsupervised cross-lingual representation learning at scale. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (pp. 8440-8451). https://aclanthology.org/2020.acl-main.747/

Crystal, D. (2003). English as a Global Language (2nd ed.). Cambridge University Press.

Entman, R. M. (1993). Framing: Toward clarification of a fractured paradigm. Journal of Communication, 43(4), 51-58. https://doi.org/10.1111/j.1460-2466.1993.tb01304.x

Franzke, A. S., Bechmann, A., Zimmer, M., Ess, C., & Association of Internet Researchers. (2020). Internet Research: Ethical Guidelines 3.0. https://aoir.org/reports/ethics3.pdf

Halpern, D., & Gibbs, J. (2013). Social media as a catalyst for online deliberation? Exploring the affordances of Facebook and YouTube for political expression. Computers in Human Behavior, 29(3), 1159-1168. https://doi.org/10.1016/j.chb.2012.10.008

Jungherr, A. (2015). Analyzing Political Communication with Digital Trace Data: The Role of Twitter Messages in Social Science Research. Springer. https://doi.org/10.1007/978-3-319-20319-5

Küçük, D., & Can, F. (2020). Stance detection: A survey. ACM Computing Surveys, 53(1), Article 12, 1-37. https://doi.org/10.1145/3369026

Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. Biometrics, 33(1), 159-174. https://doi.org/10.2307/2529310

Lawson, S. (2013). 'Melanesia': The history and politics of an idea. The Journal of Pacific History, 48(1), 1-22. https://doi.org/10.1080/00223344.2012.760839

Lazer, D., Pentland, A., Adamic, L., Aral, S., Barabási, A.-L., Brewer, D., Christakis, N., Contractor, N., Fowler, J., Gutmann, M., Jebara, T., King, G., Macy, M., Roy, D., & Van Alstyne, M. (2009). Computational social science. Science, 323(5915), 721-723. https://doi.org/10.1126/science.1168582

Loureiro, D., Barbieri, F., Neves, L., Espinosa-Anke, L., & Camacho-Collados, J. (2022). TimeLMs: Diachronic language models from Twitter. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics: System Demonstrations. https://aclanthology.org/2022.acl-demo.25/

Maclellan, N. (2016). West Papua, Indonesia and the Melanesian Spearhead Group: Competing logics in regional and international politics. Australian Journal of International Affairs, 70(5), 506-524. https://doi.org/10.1080/10357718.2015.1119231

Matthes, J., & Kohring, M. (2008). The content analysis of media frames: Toward improving reliability and validity. Journal of Communication, 58(2), 258-279. https://doi.org/10.1111/j.1460-2466.2008.00384.x

McCombs, M. E., & Shaw, D. L. (1972). The agenda-setting function of mass media. Public Opinion Quarterly, 36(2), 176-187. https://doi.org/10.1086/267990

Milner, A. (2008). The Malays. Wiley-Blackwell.

Mohammad, S. M., Kiritchenko, S., Sobhani, P., Zhu, X., & Cherry, C. (2016). SemEval-2016 Task 6: Detecting stance in tweets. In Proceedings of the 10th International Workshop on Semantic Evaluation (SemEval-2016) (pp. 31-41). https://aclanthology.org/S16-1003/

NLLB Team, Costa-jussà, M. R., Cross, J., Çelebi, O., Elbayad, M., Heafield, K., ... & Wang, J. (2022). No language left behind: Scaling human-centered machine translation. arXiv:2207.04672. https://arxiv.org/abs/2207.04672

Poncelas, A., Lohar, P., Hadley, J., & Way, A. (2020). The impact of indirect machine translation on sentiment classification. In Proceedings of the 14th Conference of the Association for Machine Translation in the Americas (AMTA 2020), Research Track (pp. 78-88). https://aclanthology.org/2020.amta-research.7/

Pöttker, H. (2003). News and its communicative quality: The inverted pyramid—when and why did it appear? Journalism Studies, 4(4), 501-511. https://doi.org/10.1080/1461670032000136596

Semetko, H. A., & Valkenburg, P. M. (2000). Framing European politics: A content analysis of press and television news. Journal of Communication, 50(2), 93-109. https://doi.org/10.1093/joc/50.2.93

Wendt, A. (1999). Social Theory of International Politics. Cambridge University Press.
```

**Catatan penghapusan permanen (terverifikasi fabrikan pada audit 2026-11-07):**
- ~~Ammon, U. (2001). The dominance of English as a language of diplomacy...~~ (bab tidak ada dalam TOC buku)
- ~~Ku, G., & Yiu, L. (2012). The Lingua Franca of International Organizations...~~ (tidak ada di IJAL 22(1))
- ~~Maclellan, N. (2015). The Melanesian Spearhead Group and regional diplomacy: Kanaky and the Pacific, JPH 50(4), 441-455~~ (tidak ada di edisi tersebut; diganti Maclellan 2016, AJIA 70(5))
- ~~Poncelas, Hadley & Way (2020, EAMT)~~ (judul/venue/halaman salah; diganti versi AMTA)
- ~~Halpern & Gibbs (2013, JCMC 18(4), 459-474)~~ (judul/venue/halaman salah; diganti versi CHB)
