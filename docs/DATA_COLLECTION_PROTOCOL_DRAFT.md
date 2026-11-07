# Data Collection Protocol — RQ1 (PROVISIONAL DRAFT)
**Status**: PROVISIONAL DRAFT for team discussion. **Not approved methodology. No scraping has been or will be performed under this document without team approval.**
**Authoritative planning references**: `docs/RQ_SPECIFIC_RESEARCH_DESIGN.md` (assignment, preserved formulations, decision register D1–D5) · `docs/GLOBAL_SAMPLING_FRAMEWORK.md` (strata S1–S3 + category T, M1–M8, attribution model) · companion artifacts: `docs/COUNTRY_SOURCE_REGISTER.csv`, `docs/LANGUAGE_COVERAGE_MATRIX.csv`.
**Constraint**: this protocol changes no existing dataset, notebook, or pipeline code; existing repaired pipeline (`src/`, `tests/`) is referenced as the processing standard, not modified.

---

## 1. Research scope and unresolved scope alternatives
The three RQ1 formulations (F1 ASEAN/social-only; F2 international; F3 international-across-poros) are preserved verbatim in the design document and **must not be restated differently here**. Their scope discrepancy (design doc §3) remains **D1 — PENDING TEAM APPROVAL**. This protocol is therefore written to be **scope-agnostic in collection** (it collects a frame that serves either reading) and **scope-explicit in analysis** (the analyzed subset is chosen only after D1):

- Collection frame: geographic strata **S1–S3** (M49-based) + transnational/multilateral **category T** (`GLOBAL_SAMPLING_FRAMEWORK.md` §3.1).
- Indonesia is **inside S1**; Indonesian-origin units carry `origin_country=ID` and are subject to the default analysis filter, inclusion being **D3/M5 — PENDING TEAM APPROVAL**.
- Timor-Leste is inside S1 as ASEAN's 11th member (26 October 2025, per team instruction); historical-intent caveat and TLS discovery expectations per **M1 — PENDING TEAM APPROVAL**.
- Platform set (social-only vs multi-platform; Reddit inclusion) — **M7 — PENDING TEAM APPROVAL**; temporal windows — **M6 — PENDING TEAM APPROVAL**; quotas/target N — **M8 — PENDING TEAM APPROVAL**.

## 2. Source discovery and eligibility criteria
**Two-tier discovery** (no scraping until approved):
1. **Tier A — pilot-evidenced sources** (`COUNTRY_SOURCE_REGISTER.csv`, `verification_status = pilot_verified_yield`): eligible by default, subject to per-outlet caps (single-outlet dominance evidence: one channel = 59.7% of the YouTube pillar **[V]**).
2. **Tier B — discovery**: candidate databases/directories with their documented limitations (GDELT, Media Cloud, Factiva/Nexis/NewsBank, Google News RSS, Asia News Network, PINA/Pacific directories — see framework §4). Directory hits are **leads, not sources**.

**Eligibility gate — a source enters the frame only with a complete registry row**: source name; publisher country (ISO-3 + M49); stratum/category; platform layer; observed/expected languages with basis; access route; evidence URL; verification status. A manual **access check** (one page/comment fetch by a human, logged) is required before `verification_status` may advance beyond `proposed_candidate`. Registered-but-zero-yield sources (e.g., NST, Malay Mail, BenarNews **[V]**) are re-tested, never silently dropped (`no_yield_observed` is a valid status).

## 3. Geographic and publisher attribution
Four-way attribution per unit, **plus community affiliation as a fifth, separate attribute** (framework §2):

| Attribute | Capture rule |
|---|---|
| Publisher country | From the registry row (documented evidence URL). Transnational outlets → **category T** + HQ country; never counted as a geographic stratum. |
| Country/region discussed | Word-boundary gazetteer matching on text (the repaired `topic_country_mentions` logic); multi-valued; never used to infer author origin. |
| Author location | **Self-reported platform fields only** (e.g., X profile location), recorded as `self-reported`; absent/unclassifiable → `unverified` (pilot: 267/375 **[V]**). Never imputed. |
| Community affiliation | Subreddit/channel/group membership recorded as its own attribute. **Affiliation is not evidence of author location** and must not be used to impute it. |
| Platform / media type | Registry-controlled vocabulary (`news_mainstream`, `public_broadcaster`, `wire`, `regional_news`, `social_x`, `social_youtube_comments`, `social_reddit`, `multilateral_ngo`). |

Word-boundary matching is mandatory; legacy substring geo-matching (the "Nederland→Laos" and "un"-substring defects, audited) is banned.

## 4. Language identification and translation handling
- **Identification**: platform API `lang` where present (X `in`→`id` normalization); otherwise deterministic detection (langdetect, seed=0) with the documented reliability threshold (<40 chars → `und`, never guessed). Detection long-tail on short units is treated as `und`.
- **Original text is always preserved**; any translated text is stored in a separate column with `original_text` untouched and a `is_translated` flag — mirroring the repaired dataset schema. Original-vs-translated provenance is never mixed.
- **Translation is a decision, not a default**: the pilot executed no translation **[V]**. If adopted: id→en via `opus-mt-id-en` (verified to exist); **no `opus-mt ms-en` checkpoint exists** (verified absent) — Malay routes would require NLLB-family models (literature-reported coverage, not locally verified); all routes require **random human spot-checks** before inference, and model language support must follow official model cards only (cardiffnlp `-latest` = English-only; `xlm-roberta` fine-tuned on 8 languages not including ms/id — verified). Route selection: **PENDING TEAM APPROVAL**.
- Non-English units are **never silently fed to an English-only model** (repaired-pipeline rule).

## 5. Collection metadata and provenance
Per unit (extends the repaired master schema): `platform, post_id, created_at (absolute, ISO-8601), username (hashed option — see §7), user_location, origin_country, origin_bloc, bloc_basis, community_affiliation, country_bloc, topic_country_mentions, media_source/outlet_id (registry FK), full_text, clean_text, language, language_source, url, collection_batch_id, collector_version`. **Absolute timestamps are mandatory** (pilot's YouTube relative strings and scrape-day date fallbacks are documented defects). Every batch produces a **manifest**: SHA-256 of all inputs/outputs, registry version, code version, configuration, row counts, and known-defect flags — the standard already used by `src/build_master_repaired.py`. Raw data is written once and never edited in place.

## 6. Deduplication and data cleaning
1. Exact dedup on platform-native IDs (post/comment/article ID); URL normalization dedup for news (pilot evidence: cross-source ID systems already handled by repaired builder).
2. Near-duplicate policy (same story syndicated across outlets): **retained per-outlet** (outlets are sampling units), flagged with a content-hash cluster id — aggregation decisions **PENDING TEAM APPROVAL** (M8-adjacent).
3. Cleaning: reuse the tested functions in `src/nlp_core.py` (`clean_for_lexicon`, `clean_for_model_card`) — no new silent transforms; emoji/URL-only units are kept with empty `clean_text` (documented pilot behavior).
4. **No silent inference fallbacks**: collection and inference failures must fail loudly and be logged, never converted to default labels (repaired-pipeline rule; audited defect).

## 7. Ethical and privacy considerations
- All target content is public; nevertheless: **usernames/locations are personal data** — apply data minimization (store hashed usernames by default; keep re-identification keys offline if needed), a documented **takedown/deletion channel**, and access controls on any non-anonymized extract. AoIR Internet Research Ethics 3.0 is the project's cited framework.
- **Platform ToS**: X session-cookie scraping (pilot method) carries documented ToS risk; prefer official/academic APIs where feasible; YouTube comment collection must use documented-quota API routes or clearly-disclosed alternatives; Google News RSS/`site:` scraping respects robots and rate limits (delays between requests, as piloted).
- Human-subjects implications for RQ2 stimulus use are **outside this protocol's scope** (RQ2 team; flagged D4).
- Final ethics sign-off: **PENDING TEAM APPROVAL**.

## 8. Sampling and stopping criteria
- **Stratified purposive** across S1–S3 + T, with per-stratum minimum outlet counts and **per-outlet caps** (cap values set after discovery; M8). Within an outlet: collection continues to the outlet cap or exhaustion, whichever first.
- **Temporal**: bounded window(s) required (pilot's 2008–2026 unstratified span and scrape-day-dated items are documented defects); window definition **M6 — PENDING TEAM APPROVAL**.
- **Stopping criteria** (all must hold): (a) approved quotas met for every *eligible* stratum; (b) registry exhausted for strata where quotas are unreachable — with the shortfall **reported as a coverage gap, not imputed**; (c) dedup threshold reached (new-unique rate below a logged threshold); (d) ethics/ToS constraints satisfied. Under no circumstance is coverage asserted for strata that discovery could not fill (e.g., TLS, ms/fr content — currently `unknown` in the language matrix).
- **No sample sizes are specified in this draft** — quotas are team decisions (M8) after discovery yields are known.

## 9. Quality assurance and audit trail
- Registry versioning: any change to `COUNTRY_SOURCE_REGISTER.csv` is a new version; batches reference the registry version they used.
- All processing through the tested, pinned pipeline (`src/` + `tests/`, 42 tests baseline); new collection code must meet the same standard (unit tests, loud failures, manifest).
- Post-collection audit: recompute strata/attributions from raw data; compare against registry; log every discrepancy (the recovery project's traceability standard: reproduced counts must match, mismatches must be explained or flagged).
- Human validation remains the outstanding gate: human reference annotation (codebook, then precision/recall/F1 as *measured* results) per `docs/METHODOLOGY_REPAIRED.md` §8 — **not yet conducted**; no metric may be reported until it is. Per the 2026-11-08 team decision, Cohen's κ is not a mandatory completion requirement: two independent annotators are the ideal option if resources allow; a single annotator yields only a limited reference; without annotation, results stay descriptive-exploratory.

## 10. Known limitations
1. **No coverage guarantees**: every non-pilot source/language is `unknown` or `expected_unverified`; three pilot outlets yielded zero articles **[V]**.
2. **Author location is rarely verifiable** (267/375 X rows **[V]**); community affiliation is not location.
3. **LID reliability** below ~40 characters (`und` handling).
4. **Platform constraints**: X ToS/access; YouTube quotas; Reddit non-inclusion in pilot corpus.
5. **Temporal coverage defects of the pilot** (relative timestamps; scrape-day date fallback) — corrected prospectively, not retroactively.
6. **Model constraints**: English-only primary model; domain shift to news unquantified; any multilingual route requires the quality checks in §4.
7. **Scope decisions open** (D1–D5, M1–M8): this protocol collects a frame compatible with all documented alternatives; it does not presuppose any of them.

---
*End of provisional draft. This document must be reviewed by the research team (and the RQ2 team where D4 applies) before any collection activity.*
