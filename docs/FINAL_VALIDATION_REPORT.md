# Final Validation & Reproducibility Report — RQ1 Engineering Closure
**Date**: 2026-11-08 · **Branch**: `repo-restructuring` · **Baseline commit**: `9cc0deb` (pre-M1; all M0–M2.1 work is uncommitted on top, preserved)
**Purpose**: the verifiable evidence record for the final engineering closure (T1–T4) and the handoff package. Companion docs: `M2_IMPLEMENTATION_REPORT.md`, `M2.1` audit notes in `RQ1_FINALIZATION_PLAN.md`, `DATASET_DICTIONARY.md`, `PENDING_DECISIONS_REGISTER.md`, `RQ1_HANDOFF_REQUIREMENTS.md`.

---

## 1. Verified starting state (preflight)

- Branch `repo-restructuring` @ `9cc0deb`; 26 working-tree entries (3 tracked modifications from M1 + untracked M0–M2.1 artifacts) — all preserved; nothing overwritten.
- M0 golden SHA `4e2cf764…` **MATCH** manifest; production master SHA **MATCH**.
- Test baseline: **107/107 OK** before closure changes.

## 2. T2 — Pipeline reliability fixes (implemented + empirically verified)

| Fix | Empirical verification |
|---|---|
| Failed run no longer leaves a stale successful CSV at the output path (previous output + manifest are removed at run start) | Probe: successful `langid` run → failing `sentiment` run on the SAME output path → output file absent; regression test `test_failed_run_removes_previous_output` |
| Unremovable previous artifact (e.g., directory at output path) fails loudly with `StageError` | `test_stale_output_removal_failure_is_loud` |
| Failed manifests contain `finished_utc` | Probe + `test_failed_manifest_has_finished_utc` (manifest: `status="failed"`, `finished_utc` set, `error` set, `output=null`, no output file) |
| Stance stage base-label vocabulary guard (case-sensitive, variant passthrough keys) | Probes: unified `Negative`/`Neutral` base with variant `x_v2` → `StageError` naming the offending labels and allowed keys; native `Netral` base → OK; no base column → OK; `news` variant accepts lowercase `neutral` and rejects wrong-case `Neutral` (tests ×4) |

## 3. T3 — Version provenance (implemented + verified)

- `configs/pipeline.yaml`: `pipeline_version: "2.0.0-m2"` (actual pipeline state identifier; loader validates it).
- `config_loader.content_version()`: configuration content identifiers — `lexicon_version = 4a46b4f8eb65`, `rules_version = 69371a7893d2` (SHA-256 prefixes of the config files; deterministic, re-verified).
- Stage manifests carry a `versions` block (pipeline/lexicon/rules/model).
- Fresh-inference artifact columns: `inference_source="fresh_inference"`, `model_version`, `pipeline_version="2.0.0-m2"`, `inferred_at_utc`.
- Honesty rule maintained: the registry retains `revision: unknown (never pinned historically)` for the *legacy* runs — the historical predictions still carry no executable version claim. The fresh run's revision is the **actual** resolved value (below), captured from the local cache.

## 4. T1 — Fresh English inference: EXECUTED and VERIFIED (not merely "script completed")

| Evidence | Value |
|---|---|
| Execution environment | Dedicated Python **3.11.9** venv: torch **2.15.0+cpu**, transformers **5.22.2**, device **cpu** |
| Model | `cardiffnlp/twitter-roberta-base-sentiment-latest` (the approved model; identity unchanged) |
| **Actual model revision** | **`3216a57f2a0d9c45a2e6c20157c20c49fb4bf9c7`** — resolved from the local HF cache: `refs/main` → snapshot containing the loaded weights (`pytorch_model.bin`); cross-checked against the live HF API (same sha). `transformers 5.22.2` did not populate `config._commit_hash`, so the revision was captured post-download from the cache snapshot (method recorded in the manifest) |
| Target | **1,013 / 1,013** EN retained records (exact-target assertion; no silent reduction) |
| Predictions | 1,013; labels `Negative` 348 · `Neutral` 537 · `Positive` 128 (non-degenerate); scores within (0,1] |
| Determinism | Spot-check passed (first 10 records re-predicted identically) |
| Runtime | 607.2 s |
| Artifacts | `data/processed/fresh_inference_en.csv` (SHA-256 `5c774222…`) + `fresh_inference_en.csv.manifest.json` |
| Isolation | Production master and M0 golden baseline **untouched** (SHA re-verified after inference); merging fresh labels = team decision N6 |
| Honest note | `transformers 5.22.2` emitted one non-fatal loading notice ("UNEXPECTED … can be ignored when loading from different task/architecture") — weights loaded and predictions verified; recorded here for transparency |

## 5. Regression & suite state

- **118/118 tests OK** (= 67 pre-existing + 11 closure regression + 40 M2 + … breakdown: unit 30, integration 12, M1 config 20, M1 golden regression 5, M2 modules 19, M2 orchestrator 21, closure 11).
- Golden regression (19 fields × 1,540 records vs the original M0 baseline): **PASS, zero semantic drift** — the golden baseline was never updated.
- Datasets: raw ×3, production master — SHA-verified unchanged after all closure work.
- Builder `src/build_master_repaired.py`: **unchanged** (no justified change identified; the fresh-inference artifact is separate by design).

## 6. Documentation corrections applied (T4)

Plan LOC inventory (375/132 actual + pipeline 605 + loader 138) · `DATA_QUALITY_AUDIT.md` 1,409→1,407 (×2) · M2-report manifest wording → "auditable and reproducible (runtime timestamps; hashes are the deterministic anchors)" · 19 non-EN/ID/und records enumerated (tl 4, lt 2, 13 singletons) in `METHODOLOGY_REPAIRED.md` + `DATASET_DICTIONARY.md` · historical/missing/fresh distinction kept consistent across handoff docs · manifest filename reference corrected (`fresh_inference_en.csv.manifest.json`).

## 7. Reproduction commands (for the team)

```bash
# environment (any Python 3.11+ with wheels; the verified run used Python 3.11.9):
pip install pandas pyyaml langdetect torch transformers

# rebuild + test:
python src/build_master_repaired.py             # authoritative master + manifest
python -m unittest discover -s tests            # 118 tests must be green

# fresh English inference (writes a SEPARATE artifact; master/golden untouched):
python src/run_fresh_inference.py               # -> data/processed/fresh_inference_en.csv(.manifest.json)

# stage CLI examples:
python src/pipeline/run.py --stage framing --platform youtube --input data/raw/youtube_papua_asean_comments.csv --output out/framing_yt.csv
```

## 8. Remaining work (not engineering; see `PENDING_DECISIONS_REGISTER.md`)

Human annotation round (0/1/2-annotator scenarios with their claim ceilings) · team decisions D1–D5/M1–M8 + N1–N7 (scope, language strategy, stance targets/codebook, framing codebook, master-refresh approval N6, RQ2/RQ3 usage rights N5) · any additional collection (`SUPPLEMENTARY_COLLECTION_PLAN.md`).

---

*End of the engineering closure record. The engineering owner's obligations are fulfilled as of this report; theoretical and interpretive decisions remain with the research team.*
