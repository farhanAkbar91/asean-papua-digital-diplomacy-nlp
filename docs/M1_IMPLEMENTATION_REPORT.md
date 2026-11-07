# M1 Implementation Report — Configuration Externalization
**Status: PASS** (all exit criteria met; evidence below)
**Date**: 2026-11-07 · **Branch**: `repo-restructuring` · **Baseline commit**: `9cc0deb` (code untouched before M1 — verified in pre-checks)
**Nature**: pure structural refactor, behavior-preserving. No label, keyword, threshold, taxonomy, model, or scope change.

---

## 1. Files created and modified

| File | Change |
|---|---|
| `configs/lexicon.yaml` (NEW, 119 lines) | Framing configuration, moved verbatim: 5 categories + keywords, `category_priority` (evaluation/tie-break order), `residual_label: Other/No-Frame` |
| `configs/rules.yaml` (NEW, 119 lines) | Stance rule layer, moved verbatim: `stance_target`, 3 variants (`x_v2`, `youtube`, `news`) with full `critical`/`supportive` lists and `passthrough` mappings, in legacy evaluation order |
| `configs/pipeline.yaml` (NEW, 7 lines) | Only parameters actually used by active code: `langdetect_seed: 0`, `language_detection.min_chars: 40`, `preprocessing.lead_max_words: 250` |
| `configs/models.yaml` (NEW, 17 lines) | Model registry metadata for the single model in use: `cardiffnlp/twitter-roberta-base-sentiment-latest`, task, `label_order` (index order per official model card), citation, preprocessing expectation, `language_guard: english_only`. Unknown metadata marked `unknown` — **no revision or historical execution version was invented** |
| `src/config_loader.py` (NEW, 138 lines) | Strict loader: deterministic `yaml.safe_load` (document order preserved), full schema/type validation, `ConfigError` on missing/invalid files, **no silent fallbacks** — invalid configuration can never produce default labels |
| `src/nlp_core.py` (MODIFIED, −107/+31 net) | Integration: `NARRATIVE_CATEGORIES`, `FRAME_RESIDUAL`, `STANCE_RULES`, `STANCE_TARGET`, LID threshold, langdetect seed, and lead-extraction default now load from `configs/` at import. Module attribute names preserved (all existing callers/tests unaffected). The in-code literals were **removed** — no second active config source remains |
| `src/run_inference.py` (MODIFIED, +12/−3) | `MODEL_NAME` and label mapping now load from `configs/models.yaml`. Includes one integration fix (see §5c) |
| `tests/test_m1_config.py` (NEW, 20 tests) | Verbatim-equivalence witnesses + loader strictness + active-code consumption + run_inference label-order checks |
| `tests/test_m1_golden_regression.py` (NEW, 5 tests) | Full golden regression: rebuilds the derived pipeline in memory via the authoritative builder functions and compares **all 19 golden fields** for all 1,540 retained records |
| `requirements.txt` (MODIFIED, +1) | `PyYAML==6.0.3` (already present in the environment; pinned) |

**Unchanged**: `src/build_master_repaired.py` (consumes `nlp_core` attributes — no edit needed), all 42 existing tests (unmodified), all datasets, `data/golden/m0/*`, `docs/M0_*`, archive.

## 2. Configuration moved (scope)

Externalized: framing lexicon (all categories/keywords/order/residual), stance rule layer (all lists/passthrough/target), pipeline parameters that exist in active code (LID threshold, langdetect seed, lead word cap), model identity/label metadata.
Deliberately **not** externalized (not in the M1-enumerated scope; no second source existed for them): geo gazetteer (`COUNTRY_KEYWORDS`/`BLOC_BY_COUNTRY`), selection filters (`SPAM_*`, `X_RELEVANCE_KEYWORDS`, `LEGACY_EXCLUDE_LOCATION_KEYWORDS`), `X_LANG_NORMALIZATION`, `MODEL_LABEL_MAP` in the builder. These remain single-source in code and are candidates for a later phase if the team wants them.

## 3. Evidence of old↔new configuration equivalence (three independent layers)

1. **Generation by import**: the YAML files were produced by a script that imported the *pre-change* `nlp_core`/`run_inference` modules and serialized their live constants (`yaml.safe_dump`, `sort_keys=False`) — the move is verbatim by construction, not transcription.
2. **Witness tests** (`test_m1_config.py`): the full expected values (all 104 framing keywords in order; all 3 rule variants with every keyword and passthrough mapping; target; parameters; model identity) are embedded as literals in the tests and compared exactly — plus per-list count witnesses (23/20/20/22/19 framing; 20/12, 18/15, 16/13 rules). Any future accidental edit to the YAML fails these tests.
3. **Golden regression** (§5): end-to-end output equality on all 1,540 retained records.

## 4. Test results

| Suite | Count | Result |
|---|---|---|
| Existing (unit 30 + integration 12) | 42 | **PASS** (unmodified) |
| M1 configuration tests | 20 | **PASS** |
| M1 golden regression | 5 | **PASS** |
| **Total** | **67** | **67/67 OK** (`python -m unittest discover -s tests`) |

## 5. Golden regression result & differences found/resolved

**Zero semantic drift on all 19 golden fields × 1,540 records.** Methodology: the regression harness was written and validated **before** integration (pre-change run: 5/5 OK — proving the harness itself is sound), then re-run after integration (5/5 OK). Golden file SHA-256 re-verified unchanged: `4e2cf764…` (matches the M0 manifest; the baseline was never updated).

Issues encountered during development and their resolution:
- **(a) Harness population bug (fixed in harness, not semantic)**: the first harness run compared 1,571 builder rows against the 1,540-record golden — the retained-population filter (audit register) was missing from the harness. Fixed in the test; dataset untouched.
- **(b) NaN vs empty-string comparison artifact (fixed in harness)**: golden CSV serializes NaN as `""`; pandas reads it back as NaN while the rebuilt in-memory frame holds `""`. At CSV level these are identical values; the comparison now normalizes both. Not a data or behavior difference.
- **(c) Latent crash bug in `src/run_inference.py` (integration fix — flagged, not silent)**: the pre-change `LABEL_MAP` was a **string-keyed** dict (`{"negative": ...}`) but indexed by **integer argmax** (`LABEL_MAP[idx]`) — guaranteed `KeyError` on the first prediction. The script has never executed successfully (no transformers environment exists here; the M0 report documents zero fresh inference), so no observed behavior existed to preserve. Externalizing the broken mapping verbatim would have enshrined a guaranteed runtime failure; the externalized `label_order` follows the official model card index order (0=negative, 1=neutral, 2=positive), and a regression test now pins it. The label **set** and semantics are unchanged. Golden baseline unaffected (run_inference output is not part of M0 golden).
- No unlabeled differences were accepted; no golden baseline update occurred.

## 6. Git status (scope discipline)

```
 M requirements.txt            (+1: PyYAML pin)
 M src/nlp_core.py             (config integration; literals removed)
 M src/run_inference.py        (config integration + documented LABELS fix)
?? configs/                    (4 YAML)
?? src/config_loader.py
?? tests/test_m1_config.py
?? tests/test_m1_golden_regression.py
?? data/golden/, docs/…        (pre-existing untracked M0/planning artifacts — preserved)
```
No commit or push was made. No force-push, no merge. All prior uncommitted work preserved. Datasets, raw data, golden baseline, legacy archive: untouched (SHA-256 verified post-M1: raw ×3, master, golden — all match M0 manifest values).

## 7. Intentionally not done (out of M1 scope)

Keyword additions/repairs · label/taxonomy changes · negation handling · multi-label framing · model replacement · stance model addition · translation · fastText LID upgrade · threshold changes · scraping · fine-tuning · geo-gazetteer and selection-filter externalization (deferred, see §2) · any commit/push · **M2**.

## 8. M1 exit criteria

- [x] All in-scope configuration externalized (lexicon, rules, pipeline, models)
- [x] No two active configuration sources can diverge (in-code literals removed; loader is the single path; witnesses live only in tests)
- [x] New configuration semantically identical to the old (generation-by-import + witness tests + end-to-end regression)
- [x] All 42 existing tests pass
- [x] All new tests pass (20 + 5)
- [x] Golden regression: zero semantic drift (harness validated pre-change, re-verified post-change)
- [x] Dataset and raw data unchanged (SHA-256 verified)
- [x] M0 golden baseline unchanged (SHA-256 matches manifest)
- [x] No changes outside M1 scope

**M1: PASS.** Stopping here — M2 (module split) requires explicit authorization.
