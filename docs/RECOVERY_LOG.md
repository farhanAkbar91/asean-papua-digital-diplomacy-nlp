# RECOVERY LOG — Emergency Repair 2026-11-07

> **RESTRUCTURING ADDENDUM (same day):** after this recovery, the repository was
> restructured for publication. Paths in the Stage tables below are HISTORICAL
> (as they were at recovery time). Current locations:
> `recovery/nlp_core.py` → `src/nlp_core.py` · `recovery/build_master_repaired.py` → `src/build_master_repaired.py` ·
> `recovery/run_inference.py` → `src/run_inference.py` · `recovery/tests/` → `tests/` ·
> `recovery/output/` → `data/processed/` · `recovery/requirements.txt` → `requirements.txt` ·
> `recovery/archive_original_docs/` → `archive/pre_repair_docs/` · root methodology docs → `docs/methodology_history/` ·
> legacy folders `1_`–`14_` → `archive/legacy_pipelines/`. Full map: `docs/RESTRUCTURING_MANIFEST.md`.
> Post-restructure verification: 42/42 tests pass; builder reproduces identical outputs from the new paths.

Every significant change made by the emergency recovery, with rationale and traceability. Originals of all edited documents are archived verbatim in `recovery/archive_original_docs/`. No raw dataset or legacy per-platform output was modified anywhere in this recovery.

## Stage 1 — Literature & model integrity (audit AUD-01, AUD-05, AUD-12)

| File | Change |
|---|---|
| `JUSTIFIKASI_LITERATUR_DAN_METODOLOGI_NLP_RQ1.md` | Removed 5 fabricated/unverifiable references (Ammon 2001; Ku & Yiu 2012; Maclellan 2015-JPH; Halpern & Gibbs 2013-JCMC; Poncelas 2020-EAMT) with documented deletion notes; replaced with verified works (Crystal 2003; Maclellan 2016-AJIA; Halpern & Gibbs 2013-CHB; Poncelas et al. 2020-AMTA). Fixed Barberá author list, Mohammad 5th author (Cherry), Jungherr title, Milner year (2008). **Deleted the false "BLEU ≥ 85" claim** and replaced it with realistic guidance (SOTA ≈ 40–50 BLEU; spot-checks mandatory). Corrected `cardiffnlp/…-latest` citation to Loureiro et al. 2022 (TimeLMs) and documented English-only support. Fixed Barbier et al. 2012→2013 (Morgan & Claypool). Added explicit correction notes at each edit site. |
| `PENJELASAN_METODE_DAN_LANGKAH_KERJA_RQ1.txt` | Section VI reference list replaced with the verified list (+ deletion register). Track A model description now states English-only per official model card. Track B now says the 5 frames are an adaptation, not the S&V taxonomy. |
| `SIAP_COPY_PASTE_GDOCS_RQ1.txt` | Manuscript method text rewritten to describe **only executed steps** (language tagging; model-card preprocessing; rule layer as separate experimental column; framing with explicit `Other/No-Frame`; NMT marked "prepared, not executed"; validation marked "not conducted"). Gap-table κ claim changed from asserted to "not yet performed". Reference list replaced (same verified list). |
| `FIKSASI_PIPELINE_DAN_JUSTIFIKASI_TEORI_RQ1.md` | "Cardiff NLP (2022) model card" citation → Loureiro et al. (2022) with English-only note. S&V attribution corrected ("adapted from"; project frames ≠ S&V frames). |
| `FRAMEWORK_EKSPANSI_GLOBAL_DAN_BATASAN_NLP_RQ1.md` | Model facts corrected: `opus-mt-ms-en` does not exist (id-en does); `twitter-xlm-roberta-base-sentiment` fine-tuning languages enumerated (ms/id NOT included); translation spot-check requirement added. |

## Stage 2 — Pipeline & reproducibility (AUD-03, AUD-04, AUD-06, AUD-07, AUD-10)

| File | Purpose / key changes |
|---|---|
| `recovery/nlp_core.py` (new) | Deterministic shared core: legacy-identical cleaning; **model-card preprocessing**; langdetect (seed=0, <40 chars → `und`); X `lang` 'in'→'id'; **word-boundary country gazetteer** (replaces substring matching: NL≠Laos, "un" no longer collides); origin (location-only) vs topic-mentions separated; **unified word-boundary framing lexicon with explicit `Other/No-Frame` residual** and keyword evidence; legacy keyword rule layer preserved verbatim per platform, returned as a separate result with evidence; X raw-label recovery function; lead extraction; legacy selection filters reproduced verbatim. |
| `recovery/build_master_repaired.py` (new) | **Authoritative** builder → `recovery/output/master_triangulation_repaired.csv` + `build_manifest.json` (input SHA-256, provenance findings, all distributions, traceability stats). Reproduces the X selection exactly (375/375). Recovers X raw labels where provable (237), flags 138 `requires_rerun` instead of fabricating. Merges optional refreshed inference from `run_inference.py`. Records label-change accounting vs the legacy master. |
| `recovery/run_inference.py` (new) | Colab-ready inference for the English-only model with **loud failure** (verified: exits 1 with FATAL message when transformers missing; no silent "Neutral+0.85" fallback), model-card preprocessing, language guard (non-English rows → NaN, never inferred). |
| `recovery/requirements.txt` (new) | Pinned deps with honest verification status per environment. |
| `recovery/tests/test_nlp_core.py` (new) | 30 unit tests pinning repaired behaviour, incl. regression tests for the documented flaws: NL→Laos, "un"-substring bloc pollution, residual-as-Diplomasi, rule direction on "rejects the referendum push", negation limitation, passthrough semantics, 'in'→'id'. |
| `recovery/tests/test_build_master.py` (new) | 12 integration tests: row counts 1571 (375/884/312), no duplicate IDs, model-label/rule-layer separation, score-present-iff-label-present, requires_rerun flagged not fabricated, Diplomasi frame only with coded evidence, NL row ≠ Laos, language normalization, manifest traceability (YT 884/884 and News 312/312 rule reproduction), stance_target constant. |
| `recovery/output/*` (new) | Repaired master (1,571 rows) + manifest. Raw data untouched. |
| `README.md` | Added mandatory status banner (pilot corpus; no human validation; en/id corpus; authoritative pipeline); marked historical distributions as pre-repair artifacts with the residual/substring caveats; softened "ASEAN press compliance" claim; reproduction guide now points to `recovery/`. |

## Stage 3 — Documentation alignment
| File | Change |
|---|---|
| `METHODOLOGY_REPAIRED.md` (new) | Actual methodology; label taxonomy; verified model facts; executed-vs-not table; limitations; forbidden claims; validation next-steps. |
| `RECOVERY_LOG.md` (new) | This file. |
| Root historical docs | Status banners added (see below). |

## Test results
- `python -m unittest discover -s recovery/tests` → **42/42 OK** (final run; re-verified as `python -m unittest discover -s tests` after restructuring).
- Builder traceability: X selection 375/375 IDs identical; YT rule reproduction 884/884; News 312/312; clean-text reproduction X 375/375, YT 882/884 (2 emoji-only comments clean to empty — legacy stored NaN; understood and documented).
- `run_inference.py` loud-failure verified (exit code 1, FATAL message, no fallback).

## Key quantified findings surfaced by the repair
1. Legacy master X annotations are **not reproducible from any shipped artifact** (news-vocabulary pipeline; 237/237 no-fire passthrough violations) — repaired dataset flags provenance per row.
2. Deterministic rule re-computation fires on 138 X rows (legacy master implied 188) — further evidence the master's X labels came from an unshipped run.
3. Repaired framing: "Diplomasi & Hubungan Internasional" 569 → **78** (coded matches only); **725** rows now honestly "Other/No-Frame".
4. Repaired X origin blocs: 267/375 honest "Non-Spesifik" (location missing) vs the old text-inferred distribution.

## Unresolved (documented, not worked around)
- 138 X rows `requires_rerun` (needs Colab: `src/run_inference.py`).
- Translation step not executed; corpus remains en+id.
- No human gold standard → no κ/P/R/F1 (deliberately absent).
- YT absolute timestamps, news date-fallback rows, ToS/ethics protocol, corpus expansion to target N — all require fieldwork/scraping decisions.
- Blueprint's "4 poros" taxonomy still differs from the data's 3-bloc+residual scheme (reconciliation is a research-design decision, deliberately not imposed silently).
