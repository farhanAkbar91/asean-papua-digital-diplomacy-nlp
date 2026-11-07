# Dataset Dictionary — RQ1 Handoff (PROVISIONAL DRAFT)
**Scope**: authoritative artifacts `data/processed/master_triangulation_repaired.csv` (1,540 retained records) and the fresh-inference artifact `data/processed/fresh_inference_en.csv`. Golden reference: `data/golden/m0/golden_baseline_m0.csv` (frozen).
**Read with**: `METHODOLOGY_REPAIRED.md` (semantics/limitations) and `RQ1_HANDOFF_REQUIREMENTS.md` (permitted/prohibited uses).

---

## 1. Master dataset columns (28)

### Identity & metadata
| Column | Type | Meaning |
|---|---|---|
| `post_id` | str, unique | **Join key.** Platform-native ID (tweet id / YouTube comment id / news hash) |
| `platform` | enum | `Platform X (Twitter)` · `YouTube Comments` · `Media Berita Online` |
| `created_at` | str | X: absolute (API) · News: date (4 items are scrape-day artifacts — flag in `created_at_note`) · YouTube: **relative string only** (no temporal resolution) |
| `created_at_note` | str | Known timestamp caveats |
| `username` | str | Public account name (PII: public social data — see handoff §ethics) |
| `user_location` | str | Self-reported profile field; empty for most X rows |
| `media_source` | str | Outlet (news) or channel cohort (YouTube) |
| `url` | str | Source URL |

### Geography (four-way attribution; never conflate)
| Column | Meaning |
|---|---|
| `language` | X: API `lang` normalized (`in`→`id`) · YT/News: langdetect seed=0. Values: en 1,013 · id 295 · und 213 · **19 others** (tl 4, lt 2; singletons ro, nl, et, so, ko, ru, lv, ja, da, fr, no, de, sw — 1 each; LID results on short/noisy texts, retained but outside EN-only inference scope) |
| `language_source` | `x_api_lang_normalized` · `langdetect_seed0` |
| `origin_country`, `origin_bloc` | Author/publisher origin from profile location (X) — empty where unknown (X: 260/364 unverified). YouTube/News: empty (attribution lives in `country_bloc`) |
| `bloc_basis` | Explicit basis of the bloc value: `profile_location_word_boundary` (X) · `video_channel_country (commenter origin unknown)` (YT) · `outlet_country` (news) |
| `topic_country_mentions` | Countries discussed (X; word-boundary gazetteer; multi-valued) — **never** an origin claim |
| `country_bloc` | Compat column = `origin_bloc` (X) or channel/outlet bloc (YT/News) |

### Text
| Column | Meaning |
|---|---|
| `full_text` | Original text (news: title + body; X/YT: post/comment) — **never modified** |
| `clean_text` | Lexicon-cleaned text (X/YT; empty `""` for news by schema). 2 emoji-only YT rows clean to `""` (excluded in the audit register) |
| `clean_text_matches_legacy` | Traceability flag vs legacy outputs |

### Sentiment (read with §provenance)
| Column | Meaning |
|---|---|
| `sentiment_model` | Raw 3-class label (`Positive`/`Neutral`/`Negative`) of the English-only Cardiff model — **EN rows only**. Empty for 133 X rows (rule-fired, historically unrecoverable) and all non-EN rows. **Historical** at handoff; fresh labels live in `fresh_inference_en.csv` until a team-approved merge |
| `sentiment_model_score` | Model probability of the predicted class; present iff label present |
| `inference_source` | `legacy_raw_recovered` (historical) · `requires_rerun` · `fresh_inference` (after an approved merge) |

### Stance rule layer (EXPERIMENTAL — not a validated stance model)
| Column | Meaning |
|---|---|
| `stance_target` | **Experimental metadata from the legacy pipeline** — the constant string `Indonesia's Sovereignty & Governance in Papua`. This is NOT a team-approved or validated final research construct; the stance rule layer that references it is experimental and distinct from any validated output (see `PENDING_DECISIONS_REGISTER.md` N2) |
| `stance_rule_variant` | `x_v2` · `youtube` · `news` (legacy keyword lists, per platform) |
| `stance_rule_adjusted` | Rule-layer output; never replaces `sentiment_model` |
| `stance_rule_evidence` | Matched keywords (`;`-joined) — empty when the layer did not fire |
| `stance_rule_fired` | bool |

### Framing (lexical topic salience — NOT Entman's four functions)
| Column | Meaning |
|---|---|
| `thematic_frame` | One of 5 coded categories or `Other/No-Frame` (704 honest residuals) |
| `framing_evidence` | Matched keywords (word-boundary); always non-empty for coded frames |

### Provenance
| Column | Meaning |
|---|---|
| `legacy_final_label` | Pre-repair label — **provenance only, never analyze** |

## 2. Fresh-inference artifact (`fresh_inference_en.csv`, 1,013 rows)

| Column | Meaning |
|---|---|
| `post_id` | Join key back to the master |
| `sentiment_model`, `sentiment_model_score` | **Fresh verified inference** (English rows only) |
| `inference_source` | Constant `fresh_inference` |
| `model_version` | Actual resolved Hugging Face revision at load time |
| `pipeline_version` | `2.0.0-m2` |
| `inferred_at_utc` | Execution timestamp |

Manifest: `fresh_inference_en.manifest.json` (environment versions, label distribution, determinism spot-check, hashes). **Merging into the master supersedes the M0 golden baseline and requires team approval.**

## 3. Reference values (measured, for sanity checks)

- Rows: 1,540 (X 364 · YT 864 · News 312). Language: en 1,013 · id 295 · und 213 · other 19.
- Framing: `Other/No-Frame` 704; every coded frame has non-empty evidence.
- Stance rule fired: 391/1,540.
- X origins: non-specific 260 · Mitra 52 · Pacific 48 · ASEAN 4.
- Integrity: golden SHA-256 `4e2cf764…`; see `build_manifest.json` for all input hashes.

## 4. Known data caveats (quote in any analysis)

1. YouTube `created_at` is relative — no temporal analysis possible for 864 rows.
2. 4 news items carry the scrape-day date (2026-09-04).
3. `und` (213) and the 19 long-tail language rows: no language claim, no EN inference.
4. `id` rows: no verified sentiment (295 rows empty after an approved fresh-EN merge) — historical labels for them were degenerate (278/282 Neutral) and must not be used.
5. Zero duplicates by construction; the 31 audit-excluded records are in `DATA_EXCLUSION_REGISTER.csv`.
