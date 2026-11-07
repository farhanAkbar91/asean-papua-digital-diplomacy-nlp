# RQ-Specific Research Design — RQ1 (Provisional)
**Status**: Planning document for team discussion. **Not an approved methodology.**
**Scope**: RQ1 only. This document creates no RQs, modifies none, and makes no methodological decisions for RQ2 or RQ3.
**Date**: 2026-11-07 · **Prepared for**: research team review
**Evidence legend**: **[V]** verified against a cited project artifact · **[A]** assumption · **[R]** recommendation · **[PENDING TEAM APPROVAL]** unresolved decision requiring the team.

---

## 1. Documented RQ assignment

The project documents assign RQ1 to the computational/NLP role (the owner of this task) and RQ2/RQ3 to other team members. This is stated, not inferred:

| Item | Evidence (verbatim, source) |
|---|---|
| RQ1 owner | "Penyusun / Penanggung Jawab RQ1 : Farhan Akbar (NLP Engineer & Komputasi)" — `docs/methodology_history/PENJELASAN_METODE_DAN_LANGKAH_KERJA_RQ1.txt`, header block **[V]** |
| RQ1 scope of work | "Sebagai **NLP Engineer**, ruang lingkup kerja kita dibatasi secara tegas untuk menyelesaikan **RQ1**" — `docs/methodology_history/FIKSASI_PIPELINE_DAN_JUSTIFIKASI_TEORI_RQ1.md` §1 **[V]** |
| RQ2 owner (other member) | "Pengelolaan survei persepsi 100 responden panel di Malaysia/Singapura via Populix/Dynata (**Tanggung jawab tim Sosiologi - RQ2**)" — same file §1 **[V]** |
| RQ3 owner (other member) | "Evaluasi efektivitas diplomasi luar negeri … (**Tanggung jawab tim Hubungan Internasional - RQ3**)" — same file §1 **[V]** |
| Deliverable boundary | RQ1 deliverables per FIKSASI §1: annotated corpus, inference models, validation metrics (pending), method text. This design document supports those; it does not alter them. **[V]** |

---

## 2. Original RQ formulations (preserved verbatim — not modified)

Three project documents state RQ1 formulations. They are reproduced exactly as written, including their inconsistencies:

| # | Source (current path) | Formulation (verbatim) |
|---|---|---|
| F1 | `docs/manuscripts/MABA SCOPUS.pdf`, p.1 (internal planning doc) | "RQ 1: Bagaimana sentimen (positif, negatif, netral) dan pemetaan konstruksi narasi dominan (seperti isu HAM, kedaulatan, dan diplomasi) dalam wacana digital negara-negara anggota ASEAN di Media Sosial terkait klaim identitas kemelanesiaan Indonesia dan isu Papua?" |
| F2 | `docs/manuscripts/DRAFT FIX.pdf`, p.4 (manuscript draft) | "RQ 1: Bagaimana framing media mengenai isu Papua dikonstruksikan dalam wacana digital internasional?" |
| F3 | `docs/methodology_history/FIKSASI_PIPELINE_DAN_JUSTIFIKASI_TEORI_RQ1.md` §1 (NLP-engineer scope doc) | "RQ1: *"Bagaimana sentimen/stance diplomatik dan konstruksi narasi dominan (framing) mengenai isu Papua dan identitas Melanesia dikonstruksikan dalam wacana digital internasional lintas poros geopolitik?"*" |

Supporting planning notes also present in the documents (not reproduced as RQs): the sampling note "Instagram, X (semua negara ASEAN jangan indonesia)" and sampling criteria documents in `MABA SCOPUS.pdf` p.1 **[V]**; the 4-poros stratification proposal in `FRAMEWORK_EKSPANSI_GLOBAL_DAN_BATASAN_NLP_RQ1.md` **[V]**.

---

## 3. Documented formulation discrepancy (explicit, not resolved)

The three formulations differ on two design dimensions:

| Dimension | F1 (MABA SCOPUS) | F2 (DRAFT FIX) | F3 (FIKSASI) |
|---|---|---|---|
| Geographic scope | "negara-negara anggota ASEAN" — **ASEAN member states only** | "wacana digital internasional" — **international discourse** | "wacana digital internasional lintas poros geopolitik" — **international, across geopolitical axes** |
| Platform scope | "di Media Sosial" — **social media** | "wacana digital" — **unspecified (broader)** | multi-platform (news, YouTube, X) per the same document's pipeline sections **[V]** |
| Constructs | sentiment + dominant narrative mapping | media framing | sentiment/diplomatic stance + framing |

### How the project itself has treated this discrepancy (documented history)
1. **In-project expansion decision**: `FRAMEWORK_EKSPANSI_GLOBAL_DAN_BATASAN_NLP_RQ1.md` records the NLP engineer's conditional agreement ("**SETUJU BERSYARAT**") to move from the regional-ASEAN design to a global stratified design, explicitly justified by the F2 formulation and RQ2 linkage. **[V]** — this is the team's own documented movement toward F2/F3, recorded before the pilot was built.
2. **Implemented pilot**: the collected pilot corpus (N = 1,571) follows the **international** scope: 3 platforms; legacy bloc composition "Mitra Global 750 / Blok ASEAN 493 / Blok Pasifik & Melanesia 287 / Non-Spesifik 41" (`docs/methodology_history/LAPORAN_PROGRESS_DAN_EVALUASI_RISET_FISIP.md`; `data/processed/build_manifest.json`). **[V]**
3. **Known tension in the implemented data**: under an F1 (ASEAN-only) reading, the pilot's largest bloc is non-ASEAN — this exact concern was documented by the project's own self-audit ("Apakah dataset ini benar-benar menjawab persepsi kawasan ASEAN…?" — `CELAH_METODOLOGIS…` Celah 4) **[V]** — and the repaired origin-based re-classification shows X-account origins are mostly unclassifiable (267/375 "Non-Spesifik") with only 4 origin-classified as ASEAN (`data/processed/build_manifest.json`). **[V]**
4. **Downstream dependency**: RQ2's documented stimulus plan uses "493 unit wacana Blok ASEAN" from this corpus (14_laporan README, now in archive). Any scope decision for RQ1 therefore **propagates to RQ2 materials** — flagged here; the decision belongs to the team, not to this document. **[PENDING TEAM APPROVAL]**

### Explicit non-resolution
This document does **not** decide between F1 and F2/F3. Both readings are carried forward (see §4). The discrepancy is listed in the decision register (§5, item D1) as the first item requiring team approval.

---

## 4. Design compatibility strategy (works under either reading)

**[R]** Rather than re-collect data per scope, the sampling framework (`GLOBAL_SAMPLING_FRAMEWORK.md`) defines one geography-first frame whose **geographic strata (S1–S3) and transnational/multilateral source category (T) are separable**:

- Under **F1 (ASEAN-only)**: analysis restricts to the ASEAN stratum (S1, now including Timor-Leste as ASEAN's 11th member since 26 October 2025) and treats S2–S3 and category T as out-of-scope (or, if the team prefers, as contextual comparators — sub-decision D2; note T is a source category, not a geographic stratum).
- Under **F2/F3 (international)**: all geographic strata S1–S3 and category T are in scope, with legacy bloc labels mapped per stratum/category.

Both readings share the same attribution model (publisher country / discussed country / author location / platform), the same country-source register, and the same collection protocol — so the scope decision changes *which subset is analyzed*, not *what is collected*. This keeps the discrepancy unresolved without blocking preparation. **[R]**

Note that F1 also restricts *platform* to social media while the pilot and F3 include news media; under F1 the news stratum would be excluded from analysis. Flagged as part of D1. **[PENDING TEAM APPROVAL]**

---

## 5. Decision register (consolidated; nothing decided here)

| ID | Decision | Options on the table | Status |
|---|---|---|---|
| D1 | Canonical RQ1 formulation (geography × platform scope) | F1 ASEAN/social-only · F2/F3 international/multi-platform | **PENDING TEAM APPROVAL** |
| D2 | Role of non-ASEAN strata (S2–S3) and of transnational/multilateral category T if F1 is chosen | excluded · control/comparator (the "Grup Kontrol" idea already suggested in `CELAH…` §3) | **PENDING TEAM APPROVAL** |
| D3 | Indonesian-origin discourse inclusion/exclusion (pilot excluded Indonesia-location X accounts; note documented in `MABA SCOPUS.pdf` p.1). *Structural note: the sampling framework now fixes Indonesia **inside** stratum S1; this decision concerns only the analytic filter, not the frame structure.* | exclude (as piloted) · include as flagged subset within S1 | **PENDING TEAM APPROVAL** |
| D4 | Whether RQ1 scope decisions affecting RQ2 stimulus materials are taken jointly | RQ1-only decision · joint RQ1+RQ2 decision | **PENDING TEAM APPROVAL** — affects another member's RQ; flagged per task restrictions |
| D5 | Constructs label for RQ1 output (sentiment/narrative per F1 vs stance/framing per F3) | follow F1 vocabulary · follow F3 vocabulary (validation-status caveats in `docs/METHODOLOGY_REPAIRED.md` apply either way) | **PENDING TEAM APPROVAL** |

---

## 6. Boundaries of this document
- No RQ text was created, added, rewritten, or replaced (§2 preserves originals verbatim).
- No scraping was performed; no datasets or pipeline code were modified.
- All candidate sources/registers named in the companion framework are marked verified/unverified; no coverage statistics are asserted beyond those observable in the project's own pilot data.
- The discrepancy (§3) is documented as found and left open for the team (D1–D5).
