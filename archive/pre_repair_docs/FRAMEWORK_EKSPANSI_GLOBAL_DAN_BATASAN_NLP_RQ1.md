# 🌐 FRAMEWORK EKSPANSI DATA SKALA GLOBAL & BATASAN REALISTIS NLP (RQ1)
**Peran**: Natural Language Processing (NLP) Engineer  
**Konteks Riset**: Naskah Publikasi Scopus FISIP (Kolaborasi multidisiplin HI, Sosiologi, dan IT)  
**Tujuan Dokumen**: Menyusun batasan operasional (*operational boundaries*), stratifikasi korpus, dan mitigasi teknis pemodelan NLP atas permintaan ekspansi data dari skala regional ASEAN ke skala global internasional.

---

## 🧭 1. Pandangan NLP Engineer: Apakah Kita Setuju?

**Jawaban: SETUJU BERSYARAT (Conditional Agreement).**

### Mengapa Langkah Ini Logis Secara Teoretis?
1. **Penyelarasan dengan Dokumen Inti (`DRAFT FIX.pdf`)**:
   * Rumusan asli RQ1 di `DRAFT FIX.pdf` berbunyi: *"Bagaimana framing media mengenai isu Papua dikonstruksikan dalam **wacana digital internasional**?"*
   * Ekspansi global justru mengembalikan RQ1 ke desain besarnya, yaitu menangkap ekosistem wacana dunia.
2. **Keterhubungan Kausal yang Kuat dengan RQ2**:
   * RQ2 berfokus mengukur persepsi *attentive public* di Malaysia dan Singapura.
   * Publik terdidik di Malaysia & Singapura tidak hanya membaca media lokal mereka, melainkan sangat terpapar oleh media global (*CNA, BBC, Reuters, Al Jazeera, ABC Australia*). Dengan memiliki data global, kita punya variabel independen yang valid untuk menjelaskan dari mana persepsi publik terbentuk.

### Mengapa Harus Diberi "Batasan Ketat"?
Jika kita membuka pintu scraping ke "seluruh dunia tanpa filter":
* **Risiko Ledakan Noise**: Kata *"Papua"* di tingkat dunia sangat ambigu (bisa merujuk pada negara merdeka *Papua New Guinea*, satwa endemik, tim olahraga rugby, atau pariwisata).
* **Language Breakdown**: Model yang saat ini kita gunakan (`twitter-roberta-base-sentiment-latest`) adalah **monolingual Bahasa Inggris**. Memasukkan teks multi-bahasa tanpa adaptasi arsitektur akan menghasilkan inferensi sampah (*garbage in, garbage out*).

---

## 🧱 2. Empat Batasan Realistis (*Realistic Boundaries*)

Untuk menjaga agar ekspansi ini tetap ilmiah, terukur, dan tidak membuat proyek gagal eksekusi, kita tetapkan 4 pilar batasan:

```
                      ┌────────────────────────────────────────┐
                      │    KORPUS GLOBAL TERSTRATIFIKASI       │
                      └────────────────────────────────────────┘
                                           │
         ┌──────────────────┬──────────────┴─────┬──────────────────┐
         ▼                  ▼                    ▼                  ▼
   [ POROS 1: PASIFIK ] [ POROS 2: ASEAN ]  [ POROS 3: BARAT ] [ POROS 4: MULTILATERAL ]
   (Melanesia & MSG)    (MY, SG, TH, PH)    (US, UK, AU, NZ)   (UN, Amnesty, HRW)
```

### 📌 Batasan I: Stratifikasi 4 Poros Geopolitik (Bukan Sembarang Negara)
Data global tidak boleh dicampuradukkan menjadi satu gumpalan acak, melainkan harus dikelompokkan ke dalam 4 poros diplomasi resmi:

| Poros Geopolitik | Negara / Entitas Utama | Karakteristik Narasi yang Diharapkan | Sumber Target |
| :--- | :--- | :--- | :--- |
| **1. Pasifik & Melanesia** | Vanuatu, Fiji, Solomon Islands, PNG, Kaledonia Baru (FLNKS) | Solidaritas ras Melanesia, desakan keanggotaan penuh MSG, kritik dekolonisasi. | *RNZ Pacific, Solomon Star, Fiji Times, Vanuatu Daily Post*. |
| **2. Blok ASEAN** | Malaysia, Singapura, Thailand, Filipina | Prinsip *ASEAN Non-Interference*, stabilitas kawasan, pemberitaan faktual kawat berita. | *CNA, The Straits Times, The Star, Astro Awani, Bangkok Post*. |
| **3. Negara Barat / Anglosphere** | Australia, Selandia Baru, Inggris, Amerika Serikat, Belanda | Isu kebebasan pers, investigasi pelanggaran HAM, pembebasan sandera, investasi SDA. | *ABC News Australia, The Guardian, BBC, Reuters, The Diplomat*. |
| **4. Lembaga Multilateral Global** | PBB (UN OHCHR), Kaukus Parlemen Internasional (IPWP), LSM HAM | Desakan akses kunjungan Komisioner PBB, resolusi hukum internasional. | Rilis resmi OHCHR, *Amnesty International, Human Rights Watch, Al Jazeera English*. |

---

### 📌 Batasan II: Cakupan Bahasa & Solusi Arsitektur NLP
Kita tidak bisa menerima semua bahasa di dunia. Kita batasi secara fungsional diplomasi:

1. **Bahasa Utama: Bahasa Inggris (Bobot $\approx 85 - 90\%$)**
   * **Justifikasi**: Bahasa Inggris adalah *lingua franca* diplomasi internasional, resolusi PBB, dan media arus utama global.
   * **Model**: Kompatibel langsung dengan `twitter-roberta-base-sentiment-latest`.

2. **Bahasa Regional Tambahan: Bahasa Melayu / Indonesia (Bobot $\approx 5 - 10\%$)**
   * **Justifikasi**: Esensial untuk menangkap sentimen asli netizen Malaysia (media lokal Astro Awani / Twitter Malaysia).

3. **Bahasa Melanesia Pasifik: Bahasa Prancis (Bobot $\approx 3 - 5\%$)**
   * **Justifikasi**: Kaledonia Baru (Kanaky) adalah anggota inti MSG yang berbahasa Prancis dan sangat vokal menyuarakan solidaritas Melanesia Papua.

#### ⚠️ Konsekuensi Teknis untuk NLP Engineer:
Jika kita memasukkan Bahasa Melayu dan Prancis, kita punya dua opsi solusi arsitektur:
* **Opsi A (Machine Translation Pipeline - Direkomendasikan)**:  
  Seluruh teks non-Inggris diterjemahkan secara terstandarisasi ke Bahasa Inggris menggunakan `Helsinki-NLP/opus-mt` atau library translasi sebelum masuk ke RoBERTa. Keunggulan: *Pipeline inferensi sentimen dan framing tetap seragam dalam satu ruang vektor*.
* **Opsi B (Multilingual Model)**:  
  Mengganti model dasar ke `cardiffnlp/twitter-xlm-roberta-base-sentiment` (mendukung multi-bahasa). Kelemahan: Kemampuan nuansa leksikon politiknya sedikit lebih rendah dibanding RoBERTa bahasa Inggris murni.

---

### 📌 Batasan III: Formula Query Pencarian (Disambiguasi Entitas Ketat)
Untuk mencegah tersedotnya data sampah non-politik, query scraping wajib menggunakan parameter boolean kontekstual:

```text
QUERY FORMULA (Inggris):
("West Papua" OR "Papua issue" OR "Papuan independence" OR "Papuan human rights") 
AND 
("Indonesia" OR "Jakarta" OR "Melanesian" OR "MSG" OR "sovereignty" OR "TNI" OR "OPM" OR "UN visit" OR "referendum")

EXCLUDE TERMS (Anti-Noise):
- "New Guinea" (jika berdiri sendiri tanpa konteks Indonesia)
- "rugby"
- "football"
- "recipe"
- "bird of paradise"
- "travel vlog"
```

---

### 📌 Batasan IV: Kuota Volume Data Realistis ($N = 3.000 - 5.000$)
Kita tidak perlu mengambil jutaan data yang justru akan memunculkan bias spammer/bot:
* Target yang sangat defensif dan prestisius untuk publikasi jurnal Scopus di bidang komunikasi politik komputasional adalah **$N = 3.000$ hingga $5.000$ data bersih terverifikasi**.
* Alokasi kuota yang seimbang:
  * **Media Berita Internasional Terkurasi**: 800 – 1.200 artikel penuh.
  * **YouTube Comments (Kanal Berita Global/Regional)**: 2.000 – 2.500 komentar.
  * **Platform X / Reddit Diskusi Internasional**: 1.000 – 1.500 postingan.

---

## 📋 3. Kesimpulan Sikap untuk Rapat Tim Selanjutnya

Dalam rapat tim berikutnya, Anda sebagai NLP Engineer dapat menyampaikan posisi dengan percaya diri:

> *"Sisi NLP siap dan sangat mendukung ekspansi data ke skala global, karena hal ini memperkuat fondasi RQ1 (Wacana Digital Internasional) dan memperkaya variabel pengujian RQ2. Namun, secara metodologi komputasional, ekspansi global kita wajib dibatasi pada **4 Poros Geopolitik**, menggunakan **bahasa Inggris sebagai korpus utama** dengan pipeline translasi terstandarisasi untuk teks Melayu/Prancis, serta menerapkan **filter disambiguasi entitas ketat** agar dataset tidak tercemar oleh jutaan data sampah non-diplomatik."*
