# METHODOLOGY (REPAIRED) — RQ1 Computational Pipeline
**Status**: This document describes what the pipeline ACTUALLY does as of the 2026-11-07 integrity repair. It supersedes, for methodological purposes, all earlier planning documents (`BLUEPRINT_*`, `FIKSASI_*`, `JUSTIFIKASI_*`, `PENJELASAN_*`, `SIAP_COPY_PASTE_*`), which are retained as historical archives (originals in `archive/pre_repair_docs/`; bannered revisions in `docs/methodology_history/`).

**The single most important sentence in this project:**
> No human gold-standard validation has been conducted. No Cohen's Kappa, Precision, Recall, F1, or significance result exists for this project, and none may be reported until the validation protocol below has been executed.

---

## 1. Corpus (pilot, N = 1,571 — unchanged counts, repaired derivations)

| Platform | N | Source artifact | Notes |
|---|---|---|---|
| Platform X (Twitter) | 375 | `data/raw/asean_papua_x_tweets.csv` (427 raw → deterministic filter reproduction, verified 375/375 ID match vs `archive/legacy_pipelines/7_hasil4_x`) | language from API `lang` ('in'→'id'); profile locations largely missing |
| YouTube Comments | 884 | `data/raw/youtube_papua_asean_comments.csv` (884/884 ID match vs `archive/legacy_pipelines/10_hasil5_yt`) | `created_at` is a RELATIVE string ("7 years ago") — absolute dates unavailable; 59.7% of comments sit under one channel (Al Jazeera English); 2 emoji-only rows clean to empty text |
| Media Berita Online | 312 | `data/raw/news_papua_asean_articles.csv` (312/312 ID match vs `archive/legacy_pipelines/13_hasil_news`) | dates span 2008-08-14 → 2026-09-04; RSS date-parse failures were stamped with the scrape day (2026-09-04, 4 articles) — treat those rows with caution; corpus contains **no Malay and no French** articles |

**Measured language composition (repaired, `language` column)**: en ≈ 1018, id ≈ 300, und ≈ 231 (texts < 40 chars — below reliable detection), plus a small long tail from langdetect noise on short comments. The corpus is **English + Indonesian**, not the trilingual (EN/MS/FR) composition previously claimed.

**Provenance finding (verified):** the legacy master's X-row annotations were produced by an unshipped pipeline (news-vocabulary labels; the v2 rule/passthrough relationship fails for 237/237 no-fire rows). The repaired dataset therefore recovers X raw model labels deterministically from `archive/legacy_pipelines/7_hasil4_x` where the rule layer provably did not fire (237 rows) and marks the remaining 138 rows `inference_source='requires_rerun'` rather than inventing them.

## 2. Label taxonomy (what each column does and does not mean)

| Column | Meaning | Status |
|---|---|---|
| `sentiment_model` | Raw 3-class output of `cardiffnlp/twitter-roberta-base-sentiment-latest` (Negative/Neutral/Positive), **English rows only** | **Authoritative** primary measure |
| `sentiment_model_score` | Model probability of the predicted class; present iff `sentiment_model` present | Authoritative |
| `inference_source` | `legacy_raw_recovered` \| `requires_rerun` \| `fresh_inference` | Provenance flag |
| `stance_rule_adjusted`, `stance_rule_evidence`, `stance_rule_fired` | Experimental keyword calibration layer (legacy-equivalent logic, per-platform lists), with the keywords that fired | **Experimental — NOT for headline results** until human-validated |
| `stance_target` | Constant target string; documents the construct the stance layer aims at | Declarative only — the transformer is a generic sentiment model, not a target-aware stance model |
| `thematic_frame`, `framing_evidence` | Word-boundary lexical topic classification into 5 coded categories + `Other/No-Frame`; matched keywords stored | Topic salience, **not** a measurement of Entman's four framing functions |
| `origin_country`, `origin_bloc`, `bloc_basis`, `topic_country_mentions` | X: actor origin from profile location (word-boundary gazetteer); YouTube: video-channel cohort; News: outlet country | `bloc_basis` states exactly what each bloc value is based on |
| `language`, `language_source` | API `lang` (X, normalized) or langdetect seed=0 (YT/news); <40 chars → `und` | Measured, with documented reliability limit |
| `legacy_final_label` | Old (pre-repair) label, kept for audit comparability only | Do not analyze |

## 3. Model facts (verified against official Hugging Face model cards, 2026-11-07)

- `cardiffnlp/twitter-roberta-base-sentiment-latest`: RoBERTa-base pretrained on ~124M tweets (2018–2021), fine-tuned on TweetEval sentiment; labels 0=Negative, 1=Neutral, 2=Positive; **English-only** ("This model is suitable for English"); expected preprocessing = mentions→`@user`, links→`http` (implemented); correct citation: **Loureiro et al. (2022), TimeLMs, ACL 2022 Demo** (TweetEval/Barbieri et al. 2020 covers the *non*`-latest` model).
- `cardiffnlp/twitter-xlm-roberta-base-sentiment`: sentiment fine-tuning covers **8 languages (Ar, En, Fr, De, Hi, It, Sp, Pt)** — Malay/Indonesian are **not** among them; use on id/ms text requires prior testing.
- Translation checkpoints: `Helsinki-NLP/opus-mt-ms-en` **does not exist**; `opus-mt-id-en` exists. Any translation step must include random spot-checks of translation quality before inference (indirect MT can alter sentiment classification — Poncelas et al., 2020, AMTA).

## 4. What has and has not been executed

| Step | Status |
|---|---|
| Data collection (pilot) | ✅ done (legacy scrapers; ToS/ethics caveats in §6) |
| Selection reproduction (X 427→375) | ✅ done, verified exact (375/375 IDs) |
| Cleaning, language tagging, geo/bloc, framing, rule layer | ✅ done in `src/` + `tests/` (unit + integration tested, 42 tests) |
| Rule-layer traceability vs legacy outputs | ✅ verified: YT 884/884, News 312/312, X 237 recovered + 138 flagged |
| Transformer inference (raw labels) | ⚠️ partially recoverable from legacy artifacts; 138 X rows require re-run via `src/run_inference.py` (needs Colab) |
| Translation of non-English items | ❌ prepared, **not executed** |
| Human gold standard (N=100–150, 2 independent annotators) | ❌ **not conducted** |
| Cohen's Kappa / Precision / Recall / F1 | ❌ **not computed** (nothing to compute against) |
| Statistical significance / uncertainty estimates | ❌ not computed |
| "Operational Discursive Synthesis" (Entman 4 functions from Frame×Stance) | ❌ proposal only — not implemented, not validated |

## 5. Reproduction

```bash
pip install -r requirements.txt
python src/build_master_repaired.py             # -> data/processed/master_triangulation_repaired.csv + build_manifest.json
python -m unittest discover -s tests            # 42 tests
# in Colab (torch + transformers):
python src/run_inference.py --platform x       # then re-run the builder to merge
```

## 6. Known limitations (must be disclosed in any manuscript)

1. **No human validation** (§4) — all label distributions are unvalidated model/rule outputs.
2. **Rule-layer directional assumption**: any mention of "referendum"/"independence"/"human rights" flips a text to Critical even in pro-government sentences (pinned by test). The layer is experimental only.
3. **Framing = lexical topic salience**; no negation handling (e.g., "no evidence of genocide" still scores F1 — pinned by test); no measurement of Entman's cause/moral-judgement/remedy functions. The project's five frames are a domain-specific adaptation, **not** the Semetko & Valkenburg (2000) taxonomy.
4. **Cross-platform text heterogeneity** (tweets vs comments vs long articles) and **domain shift** of a tweet-trained model onto news leads — unquantified.
5. **Temporal mixing**: news items span 2008–2026 without stratification; 4 items carry scrape-day dates.
6. **YouTube blocs are channel cohorts**, not commenter geographies; timestamps are relative.
7. **Language detection** is heuristic and unreliable below ~40 characters (231 `und` rows).
8. **Platform ToS / research ethics**: X data collected via cookie-session scraping (twikit); YouTube comments via a non-API downloader; Google News RSS harvesting. AoIR-3.0 ethics guidance requires a documented data-minimization and takedown protocol before publication; usernames are currently stored in plain text.
9. **Corpus size** (N=1,571) is a pilot, below the previously stated 3,000–5,000 target.

## 7. Claims that must NOT be made from this dataset

- ❌ "Annotated/validated sentiment distribution is X%" — there is no annotation.
- ❌ Any κ / P / R / F1 value.
- ❌ "The corpus covers English, Malay and French."
- ❌ "Stance toward Indonesia's sovereignty is Y%" (the model measures generic sentiment; the stance layer is an unvalidated keyword rule).
- ❌ "Framing distribution proves ASEAN press compliance with Non-Interference."
- ❌ "Free of single-platform bias" (59.7% of the YouTube pillar is one channel).
- ❌ "BLEU ≥ 85 translation quality" (fabricated claim; removed).

## 8. Required next steps before any publication claim

1. Re-run inference in Colab for the 138 flagged X rows (and optionally re-verify YT/News) via `run_inference.py`.
2. Decide and implement the cross-lingual path (translate id→en with `opus-mt-id-en` + quality spot-checks, or test a multilingual model on id text) — then re-run.
3. Execute the human validation protocol: stratified random N=100–150, **two independent annotators** blind to model output, a written codebook, then Cohen's κ (target ≥ 0.75 as a *measured* result) and P/R/F1 for (a) model and (b) model+rule variants.
4. Only after (3): decide whether the rule layer is retained, and regenerate all descriptive statistics with uncertainty estimates.
