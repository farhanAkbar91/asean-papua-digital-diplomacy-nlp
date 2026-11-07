# DATA QUALITY AUDIT — RQ1 Pilot Corpus (PROVISIONAL DRAFT)
**Status**: PROVISIONAL DRAFT for team discussion. **Read-only audit** — no raw dataset, processed file, pipeline code, notebook, or planning document was modified. Row-level classifications are recorded in `docs/DATA_EXCLUSION_REGISTER.csv`; the datasets themselves are untouched.
**Audit date**: 2026-11-07 · **Evaluation universe**: 1,654 records = 427 X raw + 884 YouTube + 312 news + 31 Reddit.
**Evidence legend**: **[V]** verified by computation in this audit · **[A]** assumption · **[R]** recommendation · **PENDING TEAM APPROVAL** items preserved from the planning documents (D1–D5, M1–M8).

---

## Phase 1 — Raw Data Integrity

### 1.1 Original raw datasets identified

| Dataset | Path | Rows | Role |
|---|---|---|---|
| X/Twitter raw | `data/raw/asean_papua_x_tweets.csv` | 427 | Scrape output; 375 selected into master, 52 not selected |
| YouTube comments raw | `data/raw/youtube_papua_asean_comments.csv` | 884 | Scrape output; all 884 in master |
| News articles raw | `data/raw/news_papua_asean_articles.csv` | 312 | Scrape output; all 312 in master |
| Reddit posts (pilot-era) | `archive/legacy_pipelines/8_multiplatform_scraping/reddit_papua_asean_posts.csv` | 31 | Collected in pilot; **never entered any master corpus** |
| Reddit variant (quarantined) | `archive/data-sampah_quarantine/reddit_papua_asean_posts.csv` | 29 | Different snapshot (different SHA-256, 29 rows); quarantined junk folder — **not part of the audit universe** |
| Legacy master (superseded) | `archive/legacy_pipelines/14_laporan_dan_master_dataset/master_triangulation_asean_papua.csv` | 1,571 | Processed artifact (provenance-flagged in the recovery); retained for traceability only |

### 1.2 File integrity (SHA-256, computed 2026-11-07)

| Dataset | SHA-256 (first 16 hex) | Bytes | Manifest cross-check |
|---|---|---|---|
| X raw | `5bc0307633797625` | 596,499 | **MATCH** vs `data/processed/build_manifest.json` **[V]** |
| YouTube raw | `c05b561461b96fc7` | 304,255 | **MATCH** **[V]** |
| News raw | `77050bb62c07d24d` | 1,299,677 | **MATCH** **[V]** |
| Reddit (pilot-era) | `cf46306194b6206b` | 254,705 | n/a (not a builder input) |
| Reddit (quarantined variant) | `ad6750b960a301d0` | 288,580 | n/a |

No raw file was modified, overwritten, or deleted. **[V]**

### 1.3 Provenance and fields

| Dataset | Collection method (documented) | Fields |
|---|---|---|
| X raw | `twikit` session-cookie scraping (ToS risk documented); legacy keyword queries; `detected_country` by substring matching (defective — audited) | tweet_id, created_at, username, user_name, user_location, detected_country, full_text, language, retweet_count, like_count, reply_count, tweet_url |
| YouTube raw | News-channel video registry + comment collection via non-API downloader; **relative timestamps only** | platform, post_id, created_at, username, user_location, country_bloc, media_source, full_text, like_count, url |
| News raw | Google News RSS (`site:` queries, `hl=en&gl=US`) → URL decode → BeautifulSoup extraction; date-parse fallback to scrape day | platform, post_id, created_at, username, user_location, country_bloc, media_source, full_text, like_count, url |
| Reddit | Hard-coded verified-thread list; subreddits r/newzealand(16), r/PapuaNewGuinea(7), r/Malaysia(6), r/singapore(2) **[V]** | platform, subreddit, created_at, username, user_location, full_text, like_count, url |

---

## Phase 2 — Row-Level Quality Assessment

### 2.1 Status criteria (applied uniformly; no record excluded for difficult sentiment/stance/framing)

- **RETAIN** — passes all quality criteria and belongs to the operational corpus.
- **EXCLUDE** — definite quality/validity defect, with a specific reason code.
- **REVIEW** — valid record whose inclusion depends on a **PENDING TEAM APPROVAL** decision or an integration step.

Exclusion codes: `EXCL_TEXT_UNUSABLE` (cleaned text empty — emoji/URL/mention-only), `EXCL_DUPLICATE_CONTENT` (exact duplicate of normalized text within platform; first occurrence retained deterministically by post_id), `EXCL_SPAM` (spam username/phrase; X only — the tweet-spam phrase list is not a valid test on long news text), `EXCL_OFF_TOPIC` (fails the legacy relevance/mandatory-subject gate as operationalized; linked to D1).

Explicitly **not** exclusion grounds (per audit constraints): unusual or hard-to-classify sentiment/stance/framing; `Other/No-Frame` results; low model confidence; language `und`; missing author location (flagged, not excluded).

### 2.2 Results

| Status | Count | Breakdown |
|---|---|---|
| **RETAIN** | **1,540** | X 364 · YouTube 864 · News 312 **[V]** |
| **EXCLUDE** | **83** | master: 11 X duplicate + 18 YouTube duplicate + 2 YouTube unusable-text = 31; raw-X non-selected: 36 spam + 16 off-topic = 52 **[V]** |
| **REVIEW** | **31** | all Reddit records (pending M7 platform decision + pipeline integration) **[V]** |
| **Total** | **1,654** | 1,540 + 83 + 31 ✓ |

Every EXCLUDE record has a row in `docs/DATA_EXCLUSION_REGISTER.csv` (114 rows = 83 EXCLUDE + 31 REVIEW) with dataset, platform, post_id, reason code, specific reason detail (including the matched spam phrase / failed gate), linked decision, and flags.

### 2.3 Criterion-by-criterion findings **[V]**

| Criterion | Finding |
|---|---|
| Empty/unusable text | 2 YouTube comments clean to empty (emoji/URL-only) → EXCLUDE. All other retained records carry usable text. |
| Duplicate content | 29 exact-text duplicates in master (11 X — coordinated/bot campaign texts, e.g., one autonomy-campaign text ×4; 18 YouTube — e.g., "free west papua" ×15). 0 in news (URL/title uniqueness verified in build). 0 in Reddit. Near-duplicate (syndication/paraphrase) detection was **not** applied — policy **PENDING TEAM APPROVAL**. |
| Spam/irrelevance | Master: 0 spam, 0 off-topic (legacy selection already removed them). Raw-X non-selected: 36 spam + 16 off-topic → EXCLUDE. |
| Topic relevance (operational scope) | X: all 364 retained pass the legacy keyword gate; News: all 312 pass the mandatory core-subject gate; YouTube: 424/864 retained comments contain no explicit topic keyword — **flagged, not excluded** (their relevance derives from the news-video context of the channel registry). Scope itself is D1 — PENDING. |
| Language identification | Retained: en 1,013 · id 295 · und 213 · tl 4 · lt 2 · 13 singleton detections (LID noise on short texts). `und` = short texts below the 40-char reliability threshold — flagged, not excluded. |
| Missing/unreliable metadata | Author location absent/unclassifiable for 260/364 retained X rows **[V]**; YouTube `user_location` is the *channel* cohort, not the commenter (documented). Reddit offers community affiliation only — never treated as location. |
| Timestamp validity | YouTube: all 864 retained rows carry **relative strings only** ("7 years ago") — unusable for temporal analysis (flagged; re-collection option in the supplementary plan). News: 4 rows stamped 2026-09-04 (scrape-day fallback) — flagged `date_fallback_suspected`. X: 364/364 parse to valid absolute timestamps. Reddit: mixed/relative strings — flagged. |
| Source attribution reliability | Publisher attribution reliable for news (registry-based) and YouTube *channel* cohorts; X origins largely unverified (by design, never imputed). Transnational outlets are category T (not a stratum). |
| Processing compatibility | All 1,540 retained records already pass through the repaired pipeline (see Phase 3). No record was excluded for processing difficulty. |

---

## Phase 3 — Existing Pipeline Integrity

Verified on the 1,540 retained records **[V]**:

| Output layer | Present | Missing | Notes |
|---|---|---|---|
| `sentiment_model` (transformer) | **1,407** (X 231 · YT 864 · News 312) | **133** | All 133 are X rows flagged `inference_source='requires_rerun'` — **explicitly tracked, not fabricated**. Provenance: of the 138 originally flagged, **133 are retained and still require re-inference; 5 were excluded as exact duplicates**. Completion route: `python src/run_inference.py --platform x` in a torch/transformers environment, then rebuild. |
| `sentiment_model_score` | 1,407 | 0 (where label present) | Score-present-iff-label-present verified `True`; no misattributed confidence. |
| `stance_rule_adjusted` (experimental layer) | **1,540** (100%) | 0 | Keyword-rule layer with evidence; 391 retained rows have `stance_rule_fired=True`. Experimental only — never a substitute for model output (planning rule). |
| `thematic_frame` (framing) | **1,540** (100%) | 0 | 704 `Other/No-Frame` (honest residual); **0 coded frames lack `framing_evidence`** — every coded classification carries its matched keywords. |

No inference failure was silently converted into a label; no neutral substitution occurred. The three output layers (sentiment / stance-rule / framing) are tracked separately, matching the repaired schema.

---

## Phase 4 — Dataset Gap Analysis (retained records only; no quotas imposed)

### 4.1 By platform **[V]**
YouTube 864 (56.1%) · X 364 (23.6%) · News 312 (20.3%).

### 4.2 By publisher country / geographic stratum **[V]** (attribution basis stated per the framework)

| Stratum/category | News (outlet cohort) | YouTube (channel cohort) | X (author origin — mostly unverified) |
|---|---|---|---|
| S1 ASEAN (MYS/SGP) | 151 | 313 | 4 |
| S2a Melanesia & Pacific | — | — | — |
| S2b AU/NZ (placement per M2) | 111 (RNZ+ABC+APR) | 37 (ABC+RNZ) | 48 |
| S3 West | — | — | 52 (incl. NL/CH/UK/US origins) |
| T transnational | 50 (Al Jazeera) | 514 (Al Jazeera channel) | — |
| Unverified / non-specific | 0 | 0 | 260 |

Genuine geographic gaps: **no S2a-publisher content at all** (Fiji/Vanuatu/Solomon/New Caledonia outlets: zero tested); S1 rests almost entirely on two countries (MYS/SGP); X author origins are 71% unclassifiable; category T is dominated by a single outlet (AJE: 50 news + 514 comments).

### 4.3 By language **[V]**
en 1,013 · id 295 · und 213 · tl 4 · lt 2 · 13 singletons. **Gaps: ms = 0, fr = 0, tet/pt = 0** — the Malaysian Malay and French/Melanesian expectations from the planning documents are entirely unrepresented (measured, not assumed).

### 4.4 By year and month **[V]**

| Year | X | News | | Year | X | News |
|---|---|---|---|---|---|---|
| 2008–2014 | 0 | 30 | | 2018 | 1 | 11 |
| 2015 | 5 | 20 | | 2019 | 12 | 42 |
| 2016 | 7 | 6 | | 2020 | 21 | 13 |
| 2017 | 8 | 7 | | 2021 | 13 | 8 |
| | | | | 2022 | 25 | 11 |
| | | | | 2023 | 34 | 35 |
| | | | | 2024 | 15 | 35 |
| | | | | 2025 | 15 | 31 |
| | | | | 2026 | **208** | 63 |

- **YouTube: no year/month computable** (relative timestamps) — the largest platform layer has **no temporal resolution at all**.
- **X is concentrated in the scrape window**: 2026-08 = 118 and 2026-09 = 71 of 364 rows (52% in two months); coverage 2015–2025 is thin (≤34/year, many single-digit months).
- **News peaks**: 2019 (42; 2019-09 = 12 — protest wave), 2023 (35), 2024 (35), 2026 (63; 2026-07 = 15). 2008–2014 is sparse (30 items across 7 years). Monthly detail is computable from `created_at`; 4 items carry the suspected scrape-day date (2026-09-04) and should be treated cautiously in any monthly claim.
- Any temporal window decision (M6) will determine how much of this distribution is in scope — **PENDING TEAM APPROVAL**.

### 4.5 Excluded and REVIEW records
83 EXCLUDE (reasons in the register: 52 spam/off-topic from raw-X non-selected; 29 exact duplicates; 2 unusable text) · 31 REVIEW (Reddit; pending M7 + integration).

### 4.6 Genuine coverage gaps (evidence-based summary; no quotas set)
1. **Sentiment completion**: 133 retained X rows without model predictions.
2. **Temporal resolution for YouTube** (56% of the corpus): zero.
3. **Language**: ms/fr/tet/pt entirely absent; id content's analytic status pending D3/M5.
4. **Geography**: no S2a (Melanesian-island) publisher sources; S1 = 2 of 11 member countries; X origins 71% unverified; T dominated by one outlet.
5. **Platform**: Reddit layer collected but unintegrated (31 records); no Instagram despite early planning mentions (never implemented).
6. **Temporal balance**: pre-2019 thin; X dominated by the scrape window.

---

## Blockers (remaining)

| # | Blocker | Type |
|---|---|---|
| B1 | 133 X rows require transformer re-inference (needs torch/transformers environment — `src/run_inference.py`) | Technical |
| B2 | YouTube absolute timestamps irrecoverable from current data; re-pull of the 22 registry videos via YouTube Data API would fix metadata only (comment text unchanged) | Technical + approval |
| B3 | Scope decisions D1, D3/M5, M2, M6, M7, M8 govern how gaps translate into collection needs | Team decision |
| B4 | Translation-route decision for id/ms/fr content (quality-check requirement) | Team decision |
| B5 | Ethics/ToS sign-off for any new collection (X session scraping risk documented) | Governance |
| B6 | Near-duplicate (syndication) policy undefined | Team decision |
| B7 | Human gold-standard validation still not conducted (standing integrity gate) | Research integrity |

---

*This audit documents the dataset as it exists. The classification statuses are advisory (recorded in the register); no data was altered. Supplementary collection priorities: `docs/SUPPLEMENTARY_COLLECTION_PLAN.md`.*
