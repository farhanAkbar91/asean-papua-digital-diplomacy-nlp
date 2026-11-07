# RQ1 Handoff Requirements — What RQ2/RQ3 Members Must Receive (PROVISIONAL DRAFT)
**Purpose**: define exactly what the other team members must receive, and how they may — and may not — use RQ1 outputs responsibly.
**Status**: PROVISIONAL DRAFT for team approval. **Headline fact: the RQ1 dataset contains NO human-validated labels and NO measured reliability metrics yet.** Everything below is written around that fact.

---

## 1. Deliverable package (what must be handed over)

| # | Item | File / source | Notes |
|---|---|---|---|
| 1 | Annotated master dataset (refreshed: fresh EN inference + version stamps) | `data/processed/master_triangulation_repaired.csv` (post T1/T3 of the finalization plan) | 1,540 retained records; per-record provenance columns |
| 2 | Golden baseline + manifest | `data/golden/m0/` + `docs/M0_GOLDEN_BASELINE_MANIFEST.json` | regression reference; receivers can verify integrity |
| 3 | Build manifest | `data/processed/build_manifest.json` | input hashes, provenance findings, distributions |
| 4 | Dataset dictionary | (to be produced — finalization task §8) | every column, allowed values, semantics, provenance |
| 5 | Validation report | (to be produced — after human annotation) | codebooks, sample design, κ, per-class P/R/F1, adjudication log |
| 6 | Methodology + limitations | `docs/METHODOLOGY_REPAIRED.md` (updated) + `docs/DATA_QUALITY_AUDIT.md` | includes the explicit "no human validation" statement until §5 is complete |
| 7 | Reproduction & verification commands | this document §5 | one-command rebuild + integrity checks |
| 8 | Pending-decision register | `docs/RQ_SPECIFIC_RESEARCH_DESIGN.md` (D1–D5) + `docs/GLOBAL_SAMPLING_FRAMEWORK.md` (M1–M8) | decisions that change interpretation |
| 9 | Exclusion register | `docs/DATA_EXCLUSION_REGISTER.csv` | 83 EXCLUDE + 31 REVIEW records with reasons |

## 2. Label taxonomy the receivers must understand

| Column | Meaning | Status at handoff |
|---|---|---|
| `sentiment_model` (+`_score`) | Raw 3-class output of the English-only Cardiff model on **EN rows only** (after T1: *fresh verified inference*; before T1: historical, unverified) | Authoritative sentiment measure for EN rows; **non-EN rows are empty by design** |
| `inference_source` | `legacy_raw_recovered` (historical) / `requires_rerun` / `fresh_inference` | Never treat historical as fresh |
| `stance_rule_*` | Keyword rule layer (experimental) with evidence + `stance_rule_fired` | **Not a stance model.** Usable only as an exploratory signal until validated |
| `thematic_frame`, `framing_evidence` | Lexical topic-salience classification (5 categories + `Other/No-Frame`) with matched keywords | Topic salience, **not** a measurement of Entman's four functions; validation pending |
| `origin_country/bloc`, `bloc_basis`, `country_bloc` | Geographic attribution with explicit basis | X origins 71% unverified; YouTube blocs are **channel cohorts** (not commenter geography) |
| `language`, `language_source` | API-normalized (X) or langdetect (YT/News); `und` = short/unreliable | `und` rows must not be assigned a language claim |
| `legacy_final_label` | Pre-repair label | **Provenance only — never analyze** |

## 3. Permitted uses (after T1–T3 and the approved validation round)

1. Descriptive distributions **restricted to the decided scope** (D1) with limitations quoted verbatim from the handoff limitations section.
2. Stimulus development for RQ2 **only from validated labels** (post-annotation), and only after D4 is settled jointly — note the planning documents' "493 ASEAN-bloc units" idea is **not supported as-is** by the measured data (ASEAN attribution rests on 4 X-origin rows + channel-cohort YouTube + 151 news items).
3. Cross-bloc comparisons **stated with attribution basis** (`bloc_basis`) and category-T outlets never presented as a geographic stratum.
4. Reproduction/verification of every number from the manifests.

## 4. Prohibited uses (hard rules)

1. **No reliability or performance claims** (κ/accuracy/F1/"tervalidasi") until the validation report exists — quoting any number not from that report is a research-integrity violation.
2. No presentation of the corpus as trilingual, ASEAN-representative, temporally balanced, or free of single-outlet dominance (measured facts contradict each of these).
3. No use of `legacy_final_label`, of `id`/`und` sentiment values (they are empty after T1 / historically degenerate), or of YouTube timestamps for temporal claims.
4. No causal or effectiveness language on behalf of RQ3 ("diplomasi berhasil/gagal") from RQ1 distributions.
5. No re-scoring/relabeling of the handed-over dataset locally; changes go through the versioned pipeline.

## 5. Reproduction & integrity verification (receivers' one-pager)

```bash
pip install -r requirements.txt
python src/build_master_repaired.py            # rebuilds data/processed master + manifest
python -m unittest discover -s tests           # full test suite must be green
```
Integrity: compare SHA-256 of the received master against the handed-over manifest; golden baseline hash must equal `4e2cf764f1800266eacf3a96763c901d2b2438fb54f0655207a2ba4a3372a370` (per `M0_GOLDEN_BASELINE_MANIFEST.json`).

## 6. Known limitations the receivers must quote (measured, not assumed)

en 1,013 / id 295 / und 213 (no ms/fr/tet content) · X author origins 71% unverified · YouTube = channel-cohort geography + no absolute timestamps · news spans 2008–2026 with 4 scrape-day-dated items · T dominated by one outlet · S2a publishers absent · X concentrated in the 2026-08/09 scrape window · author location self-reported only · Reddit layer unintegrated (31 REVIEW records).

## 7. Open decisions that change interpretation (register pointer)

D1 scope · D2 non-ASEAN role · D3/M5 Indonesian-origin inclusion · D4 RQ2 stimulus coupling · D5 construct vocabulary · M1 Timor-Leste · M2 AU/NZ · M3 New Caledonia · M4 category T · M6 temporal window · M7 platforms · M8 quotas · stance architecture · translation route. Receivers must not assume any of these; they must ask.

---

*This document is part of the handoff package and must be delivered together with the dataset. It supersedes informal claims in earlier progress documents.*


---

## 8. Research scope: collection feasibility (PROPOSAL — not approved)

Three scope options, assessed against measured evidence (`COUNTRY_SOURCE_REGISTER.csv`, `LANGUAGE_COVERAGE_MATRIX.csv`, `DATA_QUALITY_AUDIT.md`):

| Option | Feasibility | Assessment |
|---|---|---|
| **ASEAN-only (F1)** | Feasible but thin | Measured S1 coverage = MY/SG only (151 news + 313 YT-channel-cohort + 4 X-origin records); ms = 0; no Indonesian-origin X data collected (documented rule); TL untested. Would require the ms-language collection items (P3) to be defensible. |
| **Curated international (F2/F3)** | **Recommended as the feasibility option** — matches the implemented pilot design (S1–S3 + T) and the existing evidence base | Requires no new strata concept; gaps are enumerable (S2a absent, T single-outlet, id/und language policy); collection items P3–P6 address them incrementally. |
| **Globally representative** | **Not feasible at current resources** | No sampling frame for global representativeness; niche-topic yields are unmeasured outside the curated outlet list; quotas would be arbitrary. Not recommended. |

**Required distinctions when reporting scope** (these were historically conflated):
- **Collection scope ≠ analytical scope**: what was gathered (frame) vs what is analyzed/claimed (D1 + D2 + M-decisions).
- **Publisher country ≠ author location ≠ discussed country**: use `bloc_basis`, `origin_country`, `topic_country_mentions` respectively.
- **Geographic strata (S1–S3) ≠ transnational category T** (never a stratum).
- **Core analytical data ≠ exploratory data ≠ excluded/pending-review data**: retained 1,540 (core) · Reddit 31 REVIEW + `Other/No-Frame` residuals and rule-layer columns (exploratory) · 83 EXCLUDE + unintegrated sources (excluded/pending — see the register).

**Insufficient-coverage register** (do NOT fill with irrelevant records; no forced regional quotas): languages ms/fr/tet/pt = 0 measured; S2a publishers = 0; TL = 0; X author origins 71% unverified; YouTube timestamps absent; T concentrated in one outlet. Any collection to address these follows `SUPPLEMENTARY_COLLECTION_PLAN.md` P3–P7 with team approval (M1–M8).

## 9. Intended RQ1 outputs (specification — claims only after validation)

1. **Descriptive sentiment distribution** for eligible records = EN rows with **fresh verified inference** (`fresh_inference_en.csv`, 1,013 records) — with `model_version` quoted. Historical labels are not a basis for claims; id/und rows are out of sentiment scope pending N1.
2. **Thematic/narrative category distribution** (5 categories + `Other/No-Frame`) — supported by the lexicon config (`configs/lexicon.yaml`) and, before any publication claim, by the team-approved codebook + validation round (§10). Presented as **topic salience**, never as Entman's four framing functions.
3. **Cross-platform / cross-source comparisons** only where coverage and per-cell sample sizes justify them (e.g., news by outlet with n≥11; YouTube by channel with the AJE 59.7% dominance caveat; X cross-bloc comparisons are NOT justifiable with 71% unverified origins).
4. **Representative anonymized examples + qualitative interpretation** — usernames hashed/out anonymized in any publication; examples selected with the evidence columns, interpreted qualitatively by the IR team.
5. **Curated dataset + dataset dictionary + codebook + methodology + validation report + reproducibility documentation** (`DATASET_DICTIONARY.md`, `FINAL_VALIDATION_REPORT.md`, this package).

## 10. Annotation & evaluation design (updated per the 2026-11-08 team decision)

**Cohen's κ is NOT a mandatory completion requirement.** Three annotation scenarios, each with its own claim ceiling:

| Scenario | What is produced | Permitted claims |
|---|---|---|
| **2 independent annotators** (preferred) | Double-annotated sample; κ as measured; adjudicated gold set | κ + model precision/recall/F1 (macro & per-class) + confusion matrix vs gold |
| **1 annotator** | Labels documented as a **single-annotator reference** | Model P/R/F1 + confusion matrix **with the explicit single-annotator limitation**; NO inter-annotator reliability claim. **F1 does not replace inter-annotator reliability.** |
| **No annotation** | — | **Descriptive exploratory analysis only**; no validated model performance claims of any kind |

- **N=150 is a provisional pilot proposal**, not a statistically guaranteed sufficient sample; before finalizing size, set stratification (platform × language × rule-fired) and ensure minimum class coverage (including `mixed/unclear` and `Other/No-Frame` validation).
- Separate the two evaluation questions: **inter-annotator reliability** (agreement between humans) and **model performance vs the human reference** (P/R/F1/confusion). Never mix them; never fabricate either.
- Do not report any metric that was not actually computed from the actual annotation round.

## 11. Ownership & handoff table (assign before use)

| Responsibility | Owner |
|---|---|
| Pipeline implementation, tests, manifests, reproducibility, known limitations | NLP engineering owner (delivered) |
| Approving research scope (D1, D2, M-decisions) | Research team |
| Recruiting annotators; conducting annotation & adjudication | Research team (NOT the engineering owner) |
| Theoretical constructs: framing codebook, stance targets, interpretation rules | IR team |
| Sociological / IR interpretation of results | Sociology / IR teams |
| Deciding additional data collection beyond the recommended plan | Research team |
| Post-handoff research changes and future pipeline extensions | Whomever the team assigns (handoff package is the baseline) |
| Recording unresolved theoretical decisions as blockers | Research team (engineering owner flags, does not resolve) |

**Unresolved theoretical decisions are team-owned blockers, not engineering defects.** The engineering owner's closure obligation is exactly the package in §1 plus the honest-limitations statements in §4/§6.
