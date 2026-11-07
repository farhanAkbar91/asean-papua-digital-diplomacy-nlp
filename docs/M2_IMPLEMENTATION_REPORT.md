# M2 Implementation Report — NLP Pipeline Module Split
**Status: PASS** (all exit criteria met; evidence below)
**Date**: 2026-11-07 · **Branch**: `repo-restructuring` · **Pre-M2 verified state**: M1 PASS, 67/67 tests, golden SHA `4e2cf764…` (verified at pre-check)
**Nature**: structural refactor only. No model, label, keyword, threshold, taxonomy, scope, or dataset change.

---

## 1. Pre-implementation state and hashes

- `git status` audited before any change: only known untracked M0/M1/planning artifacts + the 3 M1-modified tracked files (`requirements.txt`, `src/nlp_core.py`, `src/run_inference.py`). No unexplained working-tree changes.
- Golden baseline SHA-256 verified against `M0_GOLDEN_BASELINE_MANIFEST.json`: **MATCH** (`4e2cf764…`); production master SHA also matched.
- All 67 tests re-run: **67/67 OK** before M2 work began.
- Dependency boundaries inspected: acyclic (`config_loader ← nlp_core ← {build_master_repaired, run_inference}`); hidden couplings identified: (a) `nlp_core` loads M1 config at import; (b) tests pin `nlp_core` module attributes; (c) `run_inference` must keep `MODEL_NAME`/`LABELS` module attributes (pinned by `test_m1_config`); (d) the builder consumes `nlp_core` functions only.

## 2. Final module architecture (as implemented)

```text
src/pipeline/
├── __init__.py     # package doc
├── config.py       # facade re-exporting the M1 loader (NO duplicated parsing)
├── preprocess.py   # clean_for_lexicon / clean_for_model_card / clean_news_text / extract_lead_text (delegates)
├── langid.py       # normalize_x_language / detect_language / detect_languages (langdetect backend ONLY; fastText excluded)
├── translation.py  # DISABLED seam: default backend 'none'; translate() always raises TranslationError
├── sentiment.py    # MODEL_NAME/LABELS (models.yaml), model_card_preprocess, english_only_mask,
│                   #   load_model (loud SentimentError), predict (per-text loop; batching = M3)
├── stance.py       # apply_stance_rule / recover_x_base_label / VARIANTS / STANCE_TARGET (experimental layer)
├── framing.py      # classify_framing / classify_label / CATEGORIES / CATEGORY_PRIORITY / FRAME_RESIDUAL
└── run.py          # stage CLI: preprocess|langid|sentiment|stance|framing; manifests; atomic writes
```

All stage modules **delegate** to the audited pure functions in `src/nlp_core.py` — there is exactly one implementation of every transformation. Dependency direction stays acyclic: `config_loader ← nlp_core ← pipeline.* ← run.py` (a test asserts `nlp_core` never imports `pipeline`).

## 3. Function migration mapping

| Existing function (single implementation stays in `src/nlp_core.py`) | Exposed by | Notes |
|---|---|---|
| `clean_for_lexicon`, `clean_for_model_card`, `clean_news_text`, `extract_lead_text` | `pipeline.preprocess` | verbatim delegation; lead default from `configs/pipeline.yaml` |
| `normalize_x_language`, `detect_language` | `pipeline.langid` | `in`→`id`, seed 0, 40-char `und` — unchanged; fastText explicitly excluded (M2 scope) |
| — (new seam) | `pipeline.translation` | `translate()` raises `TranslationError` for every backend; `approved_routes() == []` |
| model loading/prediction (`run_inference.load_model/predict`) | `pipeline.sentiment` | identical messages/semantics; `run_inference` now delegates (loud `die()` path preserved, exit 1) |
| `apply_stance_rule`, `recover_x_base_label`, `STANCE_RULES`, `STANCE_TARGET` | `pipeline.stance` | experimental rule layer, unchanged; unknown variant → `ValueError` |
| `classify_framing`, `NARRATIVE_CATEGORIES`, `FRAME_RESIDUAL` | `pipeline.framing` | identical semantics incl. residual + evidence |
| `config_loader.*` | `pipeline.config` | facade only (no duplication) |
| — (new) | `pipeline.run` | orchestrator; no new transformations (§5) |

## 4. Compatibility decisions

- `src/build_master_repaired.py`: **untouched** (verified by diff scope); remains the authoritative builder; not migrated to the orchestrator (M2 rule).
- `src/run_inference.py`: CLI behavior preserved (same flags, messages, exit 1 on failure; verified: exit code 1 with `[FATAL]` in this environment). Module attributes `MODEL_NAME`/`LABELS` retained (now sourced from `pipeline.sentiment` → `configs/models.yaml`), keeping `test_m1_config` green.
- The English-only guard in `run_inference` now uses the tested `english_only_mask` helper (behavior-identical refactor of two inline comprehensions).
- No circular imports; pipeline modules never imported by `nlp_core`/builder.

## 5. CLI usage examples

```bash
# framing over the real YouTube raw input (validated end-to-end: 884 rows):
python src/pipeline/run.py --stage framing --platform youtube \
  --input data/raw/youtube_papua_asean_comments.csv --output out/framing_yt.csv

# language identification (X: API 'lang' normalized; others: langdetect):
python src/pipeline/run.py --stage langid --platform x \
  --input data/raw/asean_papua_x_tweets.csv --output out/langid_x.csv

# stance rule layer (platform default variant, override with --variant):
python src/pipeline/run.py --stage stance --platform news \
  --input data/raw/news_papua_asean_articles.csv --output out/stance_news.csv

# sentiment requires torch/transformers; elsewhere it fails loudly:
python src/pipeline/run.py --stage sentiment --platform youtube \
  --input data/raw/youtube_papua_asean_comments.csv --output out/sent.csv
#   -> exit 1, manifest status="failed", error contains
#      "torch/transformers unavailable ... NO fallback inference is permitted"
```

Stage semantics mirror the authoritative builder exactly: framing/stance input = `full_text` for news, `clean_text` for x/youtube (computed via the existing cleaning when absent); langid = API `lang` (X, normalized) or langdetect (others); sentiment = English-only guard (non-`en` rows are skipped with `sentiment_guard="skipped_non_english"`, never labeled).

## 6. Stage manifest format (`<output>.manifest.json`, schema `stage-manifest-v1`)

```json
{
  "schema": "stage-manifest-v1",
  "stage": "framing", "platform": "youtube", "variant": null,
  "input":  {"path": "...", "sha256": "...", "rows": 884},
  "output": {"path": "...", "sha256": "...", "rows": 884},
  "status": "ok", "error": null,
  "started_utc": "2026-11-07T…Z", "finished_utc": "2026-11-07T…Z",
  "code_commit": "<git sha>"
}
```
Failed runs record `status="failed"` + `error` (never a misleading success); outputs are written atomically (`*.tmp` → `os.replace`); inputs are never overwritten (input≠output enforced); record count in == out is asserted (silent loss forbidden); duplicate `post_id` inputs are rejected (data contract: unique join key).

## 7. Tests added and results

| Suite | Tests | Result |
|---|---|---|
| Existing (42) + M1 (25) | 67 | **PASS** (unmodified, incl. golden regression vs M0) |
| `tests/test_m2_modules.py` | 19 | **PASS** — independent imports; no-circular-import assertion; config facade identity; preprocess delegation equality; langid threshold/seed/backend; translation disabled (`translate` raises); sentiment guard strictness + **real** loud-failure test (no transformers present → `SentimentError`; no mocked inference evidence anywhere); stance/framing equivalence vs `nlp_core` incl. the pinned negation limitation; unknown-variant rejection |
| `tests/test_m2_orchestrator.py` | 21 | **PASS** — valid stages (langid x/youtube, framing, stance incl. variant override/rejection, preprocess w/ news lead); input-unchanged hash proof; complete manifest fields; 9 validation-failure cases (invalid stage/platform, missing input/`full_text`/`post_id`, duplicate `post_id`, output==input, empty input, X-langid without `language`); sentiment stage REAL loud failure (failed manifest, no output file); CLI subprocess tests (exit 0 with `[ok]`, non-zero on invalid stage, exit 1 + `[FATAL]` on missing input) |
| **Total** | **107** | **107/107 OK** |

## 8. Golden regression results

- The M1 golden regression (all 19 fields × 1,540 records vs the **original M0 baseline**) passes inside the full suite — the golden file was **never** modified: SHA-256 re-verified `4e2cf764…` == manifest after M2.
- Additionally verified after M2: production master and all three raw datasets unchanged (SHA-256 vs manifest).
- Two test-authoring fixes occurred during development (neither is semantic drift): `available_backends()` was added to `translation.py` (the test called a function that existed only as a constant), and one orchestrator-test expectation was corrected (`clean_for_lexicon("raw A")` is `"raw A"` — no noise to remove). Both were test/design mismatches, not pipeline behavior changes.

## 9. Limitations and blocked stages

- **Sentiment stage cannot run in this environment** (no transformers wheel for Python 3.14): it fails loudly with an auditable failed manifest — by design, not simulated. Run it in Colab; batching remains M3.
- The sentiment stage writes `sentiment_guard` ("en_inferred"/"skipped_non_english") as output metadata; historical predictions in the master remain historical (`inference_source` untouched).
- Reddit/Instagram are not orchestrator platforms (data contract: x/youtube/news only), matching the planning documents (M7 pending).
- M3+ items intentionally absent: batching, version stamping, fastText, translation execution, zero-shot NLI, master v2.

## 10. Git status and complete changed-file list (no commit made)

```
 M requirements.txt                  (M1: PyYAML pin — pre-existing M1 change)
 M src/nlp_core.py                   (M1 change — untouched by M2)
 M src/run_inference.py              (M1 changes + M2 delegation to pipeline.sentiment)
?? configs/                          (M1)
?? data/golden/                      (M0 — untouched)
?? docs/…                            (M0/M1/planning docs + NEW docs/M2_IMPLEMENTATION_REPORT.md)
?? src/config_loader.py              (M1)
?? src/pipeline/                     (NEW: __init__, config, preprocess, langid, translation,
?? tests/test_m1_config.py            sentiment, stance, framing, run)
?? tests/test_m1_golden_regression.py
?? tests/test_m2_modules.py          (NEW)
?? tests/test_m2_orchestrator.py     (NEW)
```
Datasets (raw + processed), golden baseline, legacy archive: untouched (hash-verified).

## 11. Explicit confirmation

**M3 was not started.** No batched inference, no version-stamping migration, no master v2, no new backends, no research-scope or codebook decisions were made. All PENDING TEAM APPROVAL markers elsewhere remain in force.

## M2 exit criteria

- [x] All modules have clear, independent responsibilities (no empty placeholder modules)
- [x] Existing entry points compatible (builder untouched; run_inference delegates with identical CLI behavior)
- [x] No circular imports (asserted by test)
- [x] Existing 67 tests pass
- [x] New M2 tests pass (40)
- [x] Golden regression: zero semantic drift vs the original M0 baseline (1,540 × 19 fields)
- [x] CLI stages work per documented capabilities (validated on real inputs: framing 884 rows; loud sentiment failure)
- [x] Stage manifests auditable and reproducible (schema v1, input/output SHA-256 hashes, row counts, code commit, version identifiers; they also carry runtime timestamps, so they are not byte-deterministic — the hashes are the deterministic anchors)
- [x] No data or golden baseline changes (hash-verified)
- [x] No M3 functionality introduced
- [x] Documentation reflects the actual implementation

**M2: PASS.** Stopping here — M3 requires explicit authorization.
