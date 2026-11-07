# NLP Pipeline Refactor Plan — Audit & Migration Readiness (PROVISIONAL DRAFT)
**Status**: PROVISIONAL DRAFT for team review. This document changes **no code, no dataset, no configuration**. It is the technical map agreed before any larger change.
**Constraints honored**: no dataset modification · no scraping · no fine-tuning · no unilateral codebook or scope decisions (see §8 non-decisions register).
**Scope of audit**: active code only at audit time (`src/` 1,023 LOC + `tests/` 365 LOC; 42/42 tests). Inventory updated post-M2.1: production 1,675 LOC (incl. `config_loader` 138, `pipeline/` 605, `run_fresh_inference` ~140) + tests 1,280 LOC, 118/118 tests passing. Legacy scripts in `archive/legacy_pipelines/` are deprecated and out of scope except as historical reference. **[V]** = verified by inspection/computation · **[R]** recommendation · **PENDING TEAM APPROVAL** items marked.

---

## 1. Current code inventory (verified) **[V]**

| File | LOC | Role |
|---|---|---|
| `src/nlp_core.py` | 375 | Pure functions: cleaning, language handling, geo gazetteer, framing lexicon (now loaded from configs), stance rule layer (from configs), lead extraction, legacy selection filters |
| `src/build_master_repaired.py` | 420 | Authoritative master builder (selection reproduction, label recovery, derived columns, manifest, refresh merge) |
| `src/run_inference.py` | 132 | Transformer inference entry point (delegates model loading/prediction to `pipeline.sentiment`; loud failure, model-card preprocessing, language guard) |
| `src/config_loader.py` | 138 | M1 strict configuration loader (+ `content_version` configuration identifiers) |
| `src/pipeline/` (9 modules) | 605 | M2 stage modules + orchestrator (config facade, preprocess, langid, translation seam, sentiment, stance, framing, run CLI) |
| `tests/test_nlp_core.py` | 240 | 30 unit tests |
| `tests/test_build_master.py` | 125 | 12 integration tests |
| `tests/test_m1_config.py` + `test_m1_golden_regression.py` | 365 | 25 M1 tests |
| `tests/test_m2_modules.py` + `test_m2_orchestrator.py` | 420 | 40 M2 tests |
| `tests/test_final_closure.py` | 130 | 11 M2.1 closure regression tests |
| **Baseline** | | **42/42 tests OK** (re-verified at audit time) |

---

## 2. Component map: preprocessing / language / sentiment / stance / framing / output

Status legend: **VALID** (keep as-is) · **FIX** (keep, targeted fix) · **REPLACE** (retire after successor exists) · **NEW** (does not exist yet).

| # | Component | Implementation today | Status | Rationale / action |
|---|---|---|---|---|
| 2.1 | Lexicon cleaning | `clean_for_lexicon()` — legacy-identical regex | **VALID** | Tested; required for traceability vs legacy outputs. Keep verbatim. |
| 2.2 | Model-input cleaning | `clean_for_model_card()` — mention→`@user`, URL→`http` per official card | **VALID** | Matches cardiffnlp preprocessing requirement. |
| 2.3 | News lead processing | `clean_news_text()` + `extract_lead_text(max_words=250)` | **VALID (flag)** | Word-boundary clean, deterministic. Limitation: 250-word inverted-pyramid assumption is empirically unvalidated for this corpus (documented) — keep behavior; sensitivity check is a later, team-visible analysis. |
| 2.4 | Language detection — X | API `lang` + `normalize_x_language()` (`in`→`id`) | **VALID** | Ground-truth-ish source; tested. |
| 2.5 | Language detection — YT/News | `detect_language()` = langdetect (seed=0) + 40-char `und` threshold | **VALID baseline / FIX candidate** | Works, but heuristic: 213/1,540 retained rows `und`, long-tail noise on short comments (audit). FIX = optional fastText LID backend behind the same interface, evaluated on a human-checked sample before any switch (§5.2). |
| 2.6 | Translation | — none | **NEW (blocked)** | Route decision (id→en `opus-mt-id-en` verified; ms→en absent; NLLB literature-reported) is **PENDING TEAM APPROVAL**. Architecture must provide a disabled adapter slot (§4). |
| 2.7 | Sentiment inference | `cardiffnlp/twitter-roberta-base-sentiment-latest` (English-only, TimeLMs citation) via `run_inference.py` | **VALID / FIX** | Model choice defensible for EN. FIX: per-text predict loop (no batching) → batched inference; add model/lexicon **version stamping**; domain-shift check on news leads is an open analysis (not a code change). |
| 2.8 | Inference failure handling | `die()` loud failure; no silent fallback; non-English guard | **VALID** | Audited defect (legacy 0.85 fallback) already removed; keep as hard rule. |
| 2.9 | Stance — model | none (constant `STANCE_TARGET` only) | **NEW (blocked)** | True target-aware stance needs either a zero-shot NLI backend (interim, technically assessable) or fine-tuning on human annotations (blocked: no gold standard exists — standing integrity gate). Selection **PENDING TEAM APPROVAL**. |
| 2.10 | Stance — rule layer | `apply_stance_rule()` + verbatim legacy lists + evidence | **VALID as experimental layer** | Directional assumption documented and test-pinned; stays a SEPARATE column, never replaces model output. Whether it survives into results = team decision (post-validation). |
| 2.11 | Framing | `classify_framing()` — unified word-boundary lexicon, 5 coded categories + `Other/No-Frame`, evidence keywords | **VALID baseline / FIX** | Honest residual, evidence preserved. FIX: **externalize lexicon to `configs/lexicon.yaml`** (content unchanged) so any codebook revision is a data change reviewed by the team, not a code edit. Negation handling and multi-label are candidate upgrades — **PENDING TEAM APPROVAL** (codebook decisions). |
| 2.12 | Geo / strata | `COUNTRY_KEYWORDS` gazetteer + word-boundary `match_country`, origin vs topic separation | **VALID** | Replaces audited substring defects; tested (NL≠Laos, "un" no-collision). Extensible via config; Timor-Leste sources/language pending M1. |
| 2.13 | Output management | `build_master_repaired.py` + `build_manifest.json` (SHA-256, provenance flags, refresh merge) | **VALID** | Authoritative and tested. FIX (additive): stamp `model_version`, `lexicon_version`, `pipeline_version` columns; add optional translation columns (`is_translated`, `translated_text`) as schema slots — empty until a route is approved. |
| 2.14 | Legacy pipeline scripts | `archive/legacy_pipelines/` (4 NLP scripts, 3 scrapers) | **REPLACE (done)** | Already archived; superseded by `src/`. Kept for provenance only. |
| 2.15 | Orchestrator/CLI | none (builder is monolithic per-platform functions) | **NEW** | `src/pipeline/run.py` stage-based CLI (§4) so preprocessing/langid/sentiment/stance/framing can run and be tested independently. |

---

## 3. Compatibility with the 1,540 retained records **[V]**

| Check | Result |
|---|---|
| All 1,540 retained records pass current pipeline | Yes — they are its output; refactor must reproduce outputs **exactly** (golden-file regression, §7). |
| 133 X rows `requires_rerun` | Handled by existing `inference_source` mechanism + refresh merge; refactor must preserve the flag semantics and never fabricate labels. |
| 213 `und` language rows | Inference guard skips them (by design); refactor keeps the guard; fastText-LID upgrade may resolve some — only after evaluation (§5.2). |
| 295 `id` rows | Current English-only sentiment cannot serve them honestly (legacy labels exist for YT rows; X `id` rows mostly `Neutral` garbage from legacy — provenance-flagged). Refactor routes them to the translation adapter (disabled) or multilingual backend (**PENDING TEAM APPROVAL**) — never silently through the EN model. |
| 704 `Other/No-Frame` + 391 rule-fired rows | Preserved verbatim under externalized config (behavior-preserving refactor). |
| 2 excluded emoji-only rows | Already EXCLUDE in the audit register; no pipeline change needed. |
| Schema columns consumed/produced | Full column list verified against `build_master_repaired.py`; refactor adds only additive version/translation columns. |

---

## 4. Target modular architecture (behavior-preserving)

> **Implementation status (2026-11-07):** M1 (configuration externalization) and M2 (module split: `src/pipeline/{config,preprocess,langid,translation,sentiment,stance,framing,run}.py` + stage CLI) are **implemented and verified** against the M0 golden baseline (zero semantic drift). The M2 CLI is minimal by design: no batching, no version stamping, no backends beyond the disabled translation seam — those remain M3+ scope. See `docs/M1_IMPLEMENTATION_REPORT.md` and `docs/M2_IMPLEMENTATION_REPORT.md`.

```text
src/
├── nlp_core.py            # unchanged pure functions (cleaning, geo) during M1–M2
├── pipeline/
│   ├── config.py          # loads configs/*.yaml; validates schema; exposes versions
│   ├── preprocess.py      # cleaning + lead extraction (wraps nlp_core)
│   ├── langid.py          # LangIDBackend interface: api_lang | langdetect | fasttext (opt-in)
│   ├── translation.py     # TranslationBackend interface: none (default) | opus_mt | nllb  [disabled]
│   ├── sentiment.py       # SentimentBackend: HF sequence classification, BATCHED, card preprocessing,
│   │                      #   language guard, model_version stamp, loud failure
│   ├── stance.py          # StanceBackend: rule_layer (default, verbatim) | zero_shot_nli [off] | finetuned [blocked]
│   ├── framing.py         # FramingBackend: lexicon (reads configs/lexicon.yaml) | multi_label [off]
│   └── run.py             # CLI orchestrator: --stage {preprocess,langid,sentiment,stance,framing,all}
│                          #   --platform {x,yt,news} --input --output; writes per-stage manifests
├── build_master_repaired.py   # unchanged until M5; then consumes pipeline outputs
└── io_utils.py            # hashing, manifest schema, atomic writes
configs/
├── lexicon.yaml           # framing categories/keywords — moved verbatim from code
├── rules.yaml             # stance rule lists + passthrough maps — moved verbatim
├── models.yaml            # model registry: name, revision, task, language, citation
└── pipeline.yaml          # thresholds (40-char LID), batching size, flags
tests/                     # existing 42 + new (§7)
```

Design rules (all audited-defect-driven): pure/pure-adapter separation · every backend returns `(labels, scores, evidence, backend_version)` · **no silent fallbacks** (backend failure = loud stage failure with partial-results quarantine) · deterministic seeds · post_id preserved as join key end-to-end · all config content moved **verbatim** in M1 (zero semantic drift, proven by golden regression).

What deliberately does **not** change in this refactor: label vocabularies, rule logic, lexicon content, residual semantics, 40-char threshold, target constant — any change to those is a codebook/scope decision (**PENDING TEAM APPROVAL**).

---

## 5. Model candidates & inference needs

### 5.1 Sentiment (EN)
- **Keep**: `cardiffnlp/twitter-roberta-base-sentiment-latest` (English-only per card; cite Loureiro et al. 2022 TimeLMs). No evidence justifies switching the EN backend.
- Alternatives evaluated and **not** recommended now: `twitter-roberta-base-sentiment` (older TweetEval head, `LABEL_0..2` mapping — no gain); XLM-T multilingual variant (fine-tuning languages exclude ms/id — no benefit for our gap).
- Inference needs: batching (current loop is per-text); corpus 1,540 texts (plus 133 rerun) is small — CPU-feasible in principle; **exact runtime to be measured during M3, not asserted here**.

### 5.2 Language ID
- Current langdetect (seed=0) is deterministic but weak on short texts (213 `und`, 13-singleton noise).
- **Candidate**: fastText `lid.176.bin` (standard, strong on short text) behind the same interface. Evaluation gate before any switch: human-checked sample (~100 short units; human effort required), report accuracy vs langdetect on identical sample; switch only if clearly better **and** team informed. No unilateral change.

### 5.3 Stance
- Interim technical option: **zero-shot NLI** backend (e.g., `facebook/bart-large-mnli` or a DeBERTa-v3 MNLI checkpoint) conditioned on the existing `STANCE_TARGET` string — assessable without annotations; hypothesis-verbatim must be reviewed by the team since it operationalizes the construct (D5-adjacent). **PENDING TEAM APPROVAL**.
- Definitive option: **fine-tuned stance model on the human gold standard** (2 annotators, κ measured) — blocked by the standing integrity gate (B7); fine-tuning is explicitly out of scope for this refactor.

### 5.4 Framing
- Baseline: externalized lexicon (verbatim).
- Candidate upgrades (all **PENDING TEAM APPROVAL** because they presuppose codebook text): zero-shot NLI multi-label over team-approved frame descriptions; supervised multi-label after annotations; topic-model discovery (BERTopic-class tools) strictly as an *exploratory aid*, never as frame assignment.

### 5.5 Translation adapter (slot only)
- Backends prepared, **disabled**: `opus-mt-id-en` (verified to exist), NLLB-family for ms (ms→en checkpoint absence verified). Enable only after route + quality-check protocol approval. Translated text always stored beside preserved originals with `is_translated` flag.

---

## 6. Migration plan

| Phase | Content | Exit criteria | Rollback |
|---|---|---|---|
| **M0 — Baseline freeze** | Tag current state; export golden outputs for all 1,540 retained records: join key `post_id`; identity fields (`platform`, `language`, `language_source`); geographic attribution (`origin_country`, `origin_bloc`, `bloc_basis`, `country_bloc`); sentiment (`sentiment_model`, `sentiment_model_score`, `inference_source`); stance layer (`stance_target`, `stance_rule_variant`, `stance_rule_adjusted`, `stance_rule_evidence`, `stance_rule_fired`); framing (`thematic_frame`, `framing_evidence`); provenance (`legacy_final_label`). Full schema + hashes in `docs/M0_GOLDEN_BASELINE_MANIFEST.json`; artifacts in `data/golden/m0/` (separate from production `data/processed/`). | Golden files + hashes committed on a refactor branch; 42/42 tests green. | n/a |
| **M1 — Config externalization** | Move lexicon/rules/thresholds verbatim to `configs/*.yaml`; `nlp_core` reads config with code-fallback removed after verification. | 42/42 tests pass **and** golden regression = byte-identical outputs. | Git revert (no data touched). |
| **M2 — Module split** | Create `src/pipeline/*` with backend interfaces; orchestrator CLI; keep old entry points working. | New unit tests per module; golden regression identical; CLI smoke tests. | Git revert. |
| **M3 — Inference improvements** | Batched HF inference; model registry + version stamping; optional fastText LID evaluation harness (no switch without the §5.2 gate). | Batched vs per-text outputs identical on 1,540 (determinism check); measured runtime recorded; LID evaluation report delivered to team. | Feature flags off. |
| **M4 — Optional backends (off)** | Translation adapter + zero-shot stance/framing backends implemented behind flags, default OFF. | Flags-off run = golden regression identical; flags-on smoke tests on ≤20 records marked experimental. | Flags off. |
| **M5 — Re-run & version stamping** | Re-run all stages on the 1,540 retained records; produce `master_v2` with `pipeline_version`/`model_version`/`lexicon_version`; diff report vs golden. | Diff = zero semantic drift (or every difference explained & team-reviewed); manifest complete; human-validation gate untouched. | Keep v1 master intact; v2 is additive. |

Cross-phase rules: no fine-tuning at any phase (blocked until annotations + approval); no scraping; datasets untouched (v2 is a new file); every phase ends with the full test suite green.

---

## 7. Test plan

| Suite | Content | Baseline |
|---|---|---|
| Existing | 42 tests (unit 30 + integration 12) | **Must stay green at every phase** |
| Golden regression (NEW) | Full-output equality vs M0 golden files on all 1,540 retained records, per stage | Exact match required in M1–M2; in M3–M5 any diff must be explained item-by-item |
| Backend contracts (NEW) | Each backend: failure → loud exception (no default labels); score-present-iff-label-present; evidence non-empty for coded frames; `model_version` present | Per module |
| Determinism (NEW) | Same input → same output across runs; batched == per-text sentiment outputs | M3 |
| Config integrity (NEW) | YAML schema validation; verbatim equivalence vs in-code lists (checksum) | M1 |
| CLI tests (NEW) | Stage orchestration, partial-results quarantine on injected failure | M2 |
| LID evaluation harness (NEW) | fastText vs langdetect on the human-checked short-text sample; report only | M3 gate |
| Language guard (NEW) | Non-English/`und` rows never reach the EN model; `id` rows route to disabled adapter until approved | Existing + extended |

Coverage target (recommendation): all `src/pipeline/*` modules unit-tested; no target % asserted as a vanity number.

---

## 8. Non-decisions register (explicitly NOT decided by this plan)

| Item | Why pending |
|---|---|
| Framing codebook content (categories, keywords, negation/multi-label policy) | Codebook = team decision (design doc D5; framework §5.4) |
| Stance construct verbalization (NLI hypothesis text; whether stance layer reaches results) | D5 + validation gate |
| Rule-layer status after human validation (retain/drop) | Standing integrity gate B7 |
| Translation adoption + route (id→en; ms via NLLB; fr→en) | Route/quality decisions; B4 |
| Scope decisions D1, D3/M5, M2, M6, M7, M8 | Team register (unchanged) |
| Any fine-tuning | Blocked: no annotations exist; explicitly out of refactor scope |
| Any scraping / dataset modification | Out of scope per instructions |

## 9. Risks

1. **Behavior drift during refactor** — mitigated by golden regression + verbatim config moves (M1 exit criteria).
2. **pandas 3 / Python 3.14 wheel constraints** — inference still requires a Colab-style environment; keep `run_inference.py` compatible with both paths.
3. **Hidden coupling** — builder currently computes everything inline; M2 split must keep the builder runnable until M5 switches it to pipeline outputs (both paths tested in parallel).
4. **Expectation creep** — this refactor deliberately does **not** improve labels; it makes the pipeline modular, versioned, and testable. Label improvements come only from the approved decisions + human validation.

---

*End of provisional plan. Execution starts only after team review; M0 can begin immediately since it changes nothing.*
