# M0 Preflight Report — Golden Baseline Freeze (PROVISIONAL DRAFT)
**Status**: M0 preflight complete; golden baseline exported. **M1 not started** (per instruction — awaiting explicit authorization).
**Constraints honored**: read-only w.r.t. datasets and pipeline code · no scraping · no fine-tuning · no model changes · no label correction/deletion · historical predictions never presented as verified fresh inference.
**Artifacts**: `data/golden/m0/golden_baseline_m0.csv` (immutable baseline) · `docs/M0_GOLDEN_BASELINE_MANIFEST.json` (deterministic manifest) · this report.
**Test baseline**: **42/42 tests OK** (re-run at preflight; suite unchanged).

---

## A1 — LOC inventory reconciliation

Verified by `wc -l` and cross-checked against `docs/NLP_PIPELINE_REFACTOR_PLAN.md` §1 — **identical, no correction required**:

| File | LOC | Class |
|---|---|---|
| `src/nlp_core.py` | 455 | production |
| `src/build_master_repaired.py` | 420 | production |
| `src/run_inference.py` | 148 | production |
| **Production subtotal** | **1,023** | |
| `tests/test_nlp_core.py` | 240 | test |
| `tests/test_build_master.py` | 125 | test |
| **Test subtotal** | **365** | |
| **Total** | **1,388** | |

Code cleanliness: `git status -- src tests` is empty → production and test code are byte-identical to commit `9cc0deb` (branch `repo-restructuring`). All documentation files are untracked working-tree additions and do not affect the code baseline.

---

## A2 — Sentiment provenance audit (1,540 retained records)

### A2.1 Presence cross-tabulation **[V]**

| Platform | retained | `sentiment_model` present | missing (`requires_rerun`) | score-iff-label |
|---|---|---|---|---|
| Platform X (Twitter) | 364 | 231 | 133 | ✓ |
| YouTube Comments | 864 | 864 | 0 | ✓ |
| Media Berita Online | 312 | 312 | 0 | ✓ |
| **Total** | **1,540** | **1,407** | **133** | verified `True` globally |

`inference_source` corresponds perfectly: `legacy_raw_recovered` = 1,407 (all present) · `requires_rerun` = 133 (all absent). **Zero records carry a verified fresh-model prediction** — nothing has been re-inferred since the repair.

### A2.2 Language × platform × presence (the "1,409 despite English-only model" question) **[V]**

| Bucket | present | missing | Detail |
|---|---|---|---|
| `en` | 894 | 119 | missing are all X `requires_rerun` rows |
| `id` | 282 | 13 | X 99 present / 13 missing; YT 183 present |
| `und` | 213 | 0 | YT 212 present; X 1 present |
| `other` (long-tail) | 19 | 1 | incl. **1 news article detected non-English** with a historical label |
| **Total** | **1,407** | **133** | |

**Why predictions exist despite the English-only model**: every one of the 1,407 is a **historical prediction preserved from legacy runs** — the legacy pipelines ran the English-only model over *all* rows without any language guard, and the repaired builder preserved those outputs as provenance-tagged labels (`legacy_raw_recovered`) instead of re-running anything. The repaired guard exists only in `src/run_inference.py`, which has **never been executed** — therefore no verified fresh inference exists in the dataset.

**Guard consistency**: the language guard was **not enforced historically** — 495 `id`/`und` rows (X 99+1, YT 183+212) carry historical predictions produced by feeding untranslated non-English/short text to the English-only model. Corroborating quality signal: historical labels on `id` rows are 278 `Neutral` / 4 `Negative` (the documented degenerate-Neutral pattern); `und` rows 166/24/23. The 13 `id` X rows *without* predictions are missing because the rule layer fired for them (rule-based `requires_rerun`), not because of any language guard.

**Origin of the historical predictions**:
- YouTube (864) and News (312): legacy shipped pipelines (`archive/legacy_pipelines/9_sentiment_analysis_yt`, `12_sentiment_analysis_news`) whose code names `cardiffnlp/twitter-roberta-base-sentiment-latest`; execution metadata (library versions, model revision, run date) was **never recorded**.
- X (231): recovered deterministically from `archive/legacy_pipelines/7_hasil4_x` via the rule-passthrough relation — and the legacy master's X layer additionally passed through a **partially unshipped pipeline** (recovery provenance finding). Double historical indirection.
- Conclusion: **historical prediction ≠ verified Cardiff inference**. The distinction is encoded in `inference_source` and is now frozen in the golden baseline. No label was overwritten, removed, or reinterpreted.

### A2.3 Erratum found in `docs/DATA_QUALITY_AUDIT.md` **[V]**
The audit report states "1,409 present (X 231 · YT 864 · News 312)". 231+864+312 = **1,407**; the 1,409 figure was computed on the pre-fix 1,542-row retained set (YT 866). Per the read-only constraint on existing documents, the erratum is recorded here **without editing the audit file**; recommended one-line correction at the next documentation revision.

---

## A3 — Golden regression populations (reconciled)

| Population | Count | Definition | Comparison rule |
|---|---|---|---|
| **P1 — existing predictions** | 1,407 | `sentiment_model` present (historical, provenance-tagged) | M1–M2 refactor: outputs must equal golden **exactly** (same code semantics). M3 batching: batched-vs-single-loop **determinism** on these records; fresh-model output is **not** regressed against historical labels as ground truth — differences are expected (unknown legacy execution metadata) and must be reported item-by-item, never silently absorbed. |
| **P2 — requires rerun** | 133 | `inference_source == 'requires_rerun'` (X) | **New-inference population**: no golden label exists; regression not applicable. Outputs recorded as `fresh_inference` + `model_version`. |
| **P3 — non-English** | 527 | `language != 'en'` (id 295 + und 213 + other 19) | EN sentiment model guard **must skip**; routing verification only. Any future prediction requires an approved route (translation adapter or multilingual backend) — **PENDING TEAM APPROVAL**. |
| **P4 — undetermined** | 213 | `language == 'und'` (short texts, <40-char LID threshold) | Same guard rule as P3; fastText-LID evaluation may reclassify some — decision gate per refactor plan §5.2, no unilateral switch. |

Note P2 ⊂ P3∪P1 overlap avoided: populations are defined for their respective checks (P1/P2 partition by label presence; P3/P4 are language-side views used for guard verification).

---

## A4 — M0 field inventory corrected **[V]**

`docs/NLP_PIPELINE_REFACTOR_PLAN.md` M0 row contained `thematic_frame` twice and an incomplete list. **Corrected** to the complete 19-field baseline schema (join key; identity; geographic attribution; sentiment + inference source; stance layer incl. construct declaration; framing + evidence; provenance), with the authoritative enumeration recorded in `M0_GOLDEN_BASELINE_MANIFEST.json → field_list`. Text columns are intentionally excluded from the golden file (joined via `post_id`) to keep the baseline a label/provenance artifact.

---

## Phase B — Golden baseline artifacts **[V]**

| Artifact | Value |
|---|---|
| File | `data/golden/m0/golden_baseline_m0.csv` — **outside** the production path (`data/processed/`) |
| Rows / columns | 1,540 / 19, sorted by `post_id` ascending (string), UTF-8, LF, empty-string NA |
| SHA-256 | `4e2cf764f1800266eacf3a96763c901d2b2438fb54f0655207a2ba4a3372a370` |
| Join key | `post_id` (unique — verified) |
| Manifest | `docs/M0_GOLDEN_BASELINE_MANIFEST.json` (schema `golden-schema-v1`, deterministic key-sorted JSON) |
| Manifest records | source dataset SHA-256 + row count; exclusion register SHA-256 (population definition); raw-input hashes; repo branch/commit (`repo-restructuring` @ `9cc0deb`); export timestamp; export procedure (sort/encoding/NA/line-terminator) for byte-identical reproduction; populations P1–P4; provenance notes |
| Determinism | re-running the documented export against the same source dataset + register reproduces a byte-identical CSV (hash re-verified post-write) |

Golden separation: the production master was **not** touched; the golden CSV is a derived, immutable reference for M1–M5 regression only.

---

## Test results & remaining open items

- **Tests: 42/42 OK** (`python -m unittest discover -s tests`; run twice during preflight).
- Open items preserved (none resolved silently):
  1. 133 P2 records require fresh inference (Colab/torch) — pending environment access.
  2. All 1,407 predictions remain *historical*; fresh verified inference does not exist yet.
  3. Translation-route and LID-upgrade decisions — **PENDING TEAM APPROVAL**.
  4. Audit-MD erratum (1,409 → 1,407) — recorded, not edited (read-only constraint).
  5. Golden artifacts are **uncommitted** working-tree files; committing them (M0 closure per the plan's exit criterion) awaits authorization.
  6. Codebook/scope decisions D1–D5, M1–M8 remain with the team.

**M0 status: COMPLETE (artifacts + documentation). Stop here — M1 requires explicit authorization.**
