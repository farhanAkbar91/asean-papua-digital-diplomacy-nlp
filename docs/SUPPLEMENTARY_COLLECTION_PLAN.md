# Supplementary Collection Plan — RQ1 (PROVISIONAL DRAFT)
**Status**: PROVISIONAL DRAFT. **No scraping has been performed or scheduled**; every item below requires team approval and the ethics/ToS gate before execution.
**Inputs**: gap analysis in `docs/DATA_QUALITY_AUDIT.md` (all gap statements are measured, not assumed); source candidates from `docs/COUNTRY_SOURCE_REGISTER.csv` (verification status carried over verbatim); scope decisions D1–D5 / M1–M8 from the planning documents remain **PENDING TEAM APPROVAL**.

**Principle**: collection is proposed only where the audit shows a *measured* gap; no quotas or target N are set here (M8 — PENDING TEAM APPROVAL); items are ordered by evidence strength × effort.

---

## P0 — Complete the existing dataset before any new collection

| Item | Detail |
|---|---|
| **Gap addressed** | 133 retained X records have no `sentiment_model` prediction (of the 138 originally flagged `requires_rerun`; 5 were excluded as duplicates) — audit Phase 3. |
| **Action** | Re-run inference for X: `python src/run_inference.py --platform x` in a torch/transformers environment (e.g., Colab), then `python src/build_master_repaired.py` to merge. English-only guard applies; non-English rows stay `NaN` by design. |
| **Source / verification** | Existing data only — no collection. |
| **Period / language** | Existing X records; en only for inference. |
| **Constraints** | Requires HF model download (~500 MB) + GPU/CPU runtime. No fabrication of predictions is permitted; failures must stay loud. |
| **Status** | Ready to execute; **PENDING TEAM APPROVAL** not required (it is recovery of existing scope), but runtime access is. |

## P1 — YouTube metadata refresh (absolute timestamps)

| Item | Detail |
|---|---|
| **Gap addressed** | 864 retained YouTube records (56% of corpus) have **no temporal resolution** (relative strings only) — audit Phase 4.4. |
| **Action** | Re-pull video/comment **metadata** (publish timestamps, video registry status) for the 22 registry videos via the official YouTube Data API v3; join by `post_id`/video to the existing corpus. Comment text is not re-collected. |
| **Source / verification** | Existing registry channels (CNA, Astro AWANI, ABC News In-depth, RNZ Pacific, Al Jazeera English, FMT, Straits Times, The Star, BenarNews) — `pilot_verified_yield` / `registered_zero_yield` per register. |
| **Period / language** | Existing comments (2019–2026 span implied by relative strings — exact dates unknown until pulled); en + id. |
| **Constraints** | API quota; comments may have been deleted/turned off since collection (expect partial joins — report join rate honestly); no ToS issue (official API). |
| **Status** | Recommendation; **PENDING TEAM APPROVAL** (M7-adjacent). |

## P2 — Reddit layer decision and integration (data already exists)

| Item | Detail |
|---|---|
| **Gap addressed** | 31 REVIEW records (r/newzealand 16, r/PapuaNewGuinea 7, r/Malaysia 6, r/singapore 2) collected but never integrated; would add a platform where **community affiliation** is explicit (never treated as author location). |
| **Action** | Team decision (M7): integrate the existing 31 records through the repaired pipeline, and/or collect the pilot-config threads that yielded nothing (r/asean, r/pacific, r/fiji, r/australia listed in the legacy config but absent from data). |
| **Source / verification** | Existing pilot scrape (`pilot_scraped_not_in_master`); further collection via official Reddit API (PRAW). |
| **Period / language** | Existing threads; en. |
| **Constraints** | Community affiliation ≠ author location (framework §2 rule); API terms apply; small volumes. |
| **Status** | **PENDING TEAM APPROVAL** (M7). |

## P3 — Malaysian Malay-language news (largest measured language gap)

| Item | Detail |
|---|---|
| **Gap addressed** | **ms = 0 in the corpus** (0/312 news items contained Malay; S1 depends on two English-language windows into Malaysia) — audit Phase 4.3. |
| **Action** | Discovery + collection from Malay-language Malaysian outlets: **Astro AWANI** (Bahasa Malaysia portal — `pilot_verified_yield` for its English side only; ms content untested), **Berita Harian** (named in project documents; `documented_untested`). Google News RSS with Malay locale/queries (`hl=ms`) as the discovery route. |
| **Source / verification** | As above — both require the registry eligibility gate (§2 of the protocol draft) before any bulk collection. |
| **Period / language** | Per M6 window once defined — **PENDING TEAM APPROVAL**; ms. |
| **Constraints** | **No `opus-mt ms-en` checkpoint exists** (verified absent); translation would require NLLB-family models (literature-reported coverage, not locally verified) — route decision **PENDING TEAM APPROVAL**; original text preserved regardless. Google News Malay-locale indexing depth unverified. |
| **Status** | **PENDING TEAM APPROVAL** (route + window). |

## P4 — Category T: institutional/multilateral sources

| Item | Detail |
|---|---|
| **Gap addressed** | Category T rests on one outlet (Al Jazeera: 50 news + 514 comments) — audit Phase 4.2; UN/INGO institutional material (UN OHCHR, Amnesty, HRW — named in project planning docs, `documented_untested`) is absent. |
| **Action** | Collect official public documents/press releases (OHCHR Papua reports and statements; Amnesty/HRW Papua publications) via official sites — structured pages, not search-scraping. |
| **Source / verification** | Register row B10 — `documented_untested`; institutional pages are stable and citable (evidence URL per document). |
| **Period / language** | Per M6 window; en (some id/fr institutional material exists — verify per document). |
| **Constraints** | Genre differs from news/social text (report language) — must be flagged as a distinct source type in analysis; copyright limits redistribution (store URLs + excerpts per license). |
| **Status** | **PENDING TEAM APPROVAL** (M4-adjacent). |

## P5 — Melanesian-island publishers (S2a) and French-language press

| Item | Detail |
|---|---|
| **Gap addressed** | **Zero S2a-publisher content** (Fiji/Vanuatu/Solomon/New Caledonia never tested); **fr = 0** despite the Melanesian-caucus rationale in the planning documents — audit Phase 4.2/4.3. |
| **Action** | Discovery-first (per protocol §2): Fiji Times, Vanuatu Daily Post, Solomon Star (all `documented_untested`); New Caledonia: Les Nouvelles Calédoniennes, NC la 1ère (`proposed_candidate`, M3); then targeted collection only where the access check passes. |
| **Source / verification** | As listed — none verified; availability explicitly unknown. |
| **Period / language** | Per M6; en (Fiji/Solomon/Vanuatu), fr (New Caledonia); Bislama possible for Vanuatu — record if encountered. |
| **Constraints** | Small outlets: intermittent publishing, thin archives; fr→en translation route unverified locally; M3 placement decision pending. |
| **Status** | **PENDING TEAM APPROVAL** (M3 + translation route). |

## P6 — Timor-Leste (newest ASEAN member)

| Item | Detail |
|---|---|
| **Gap addressed** | S1 covers 2 of 11 member states; Timor-Leste (ASEAN's 11th member since 26 Oct 2025) has **no sources registered and no content** — audit Phase 4.2; M1 leaves its F1-scope interpretation open. |
| **Action** | Discovery scan of TLS outlets (e.g., Tatoli/Portal Timor Lorosa'e, Primatika? — **none are in the register yet; candidates must be identified and evidence-verified during discovery** — no source is named here as available). |
| **Source / verification** | None existing — discovery required before anything enters the register. |
| **Period / language** | Per M6; tet/pt (coverage unknown — language matrix L5/L6). |
| **Constraints** | Language support/translation routes unknown; low expected volume on this niche topic **[A]**; M1 interpretation pending. |
| **Status** | **PENDING TEAM APPROVAL** (M1). |

## P7 — X supplementation (highest-constraint platform)

| Item | Detail |
|---|---|
| **Gap addressed** | X retained records are 52% concentrated in the 2026-08/09 scrape window; 2015–2025 coverage thin; author origins 71% unverified — audit Phase 4.4/4.2. |
| **Action** | If the team accepts the ToS/ethics trade-off: targeted collection over defined event windows (documented Papua episodes) with the repaired gazetteer-based attribution; otherwise treat X as a convenience layer and rebalance toward news/YouTube. |
| **Source / verification** | X platform (register P1) — `pilot_verified_yield` with documented ToS risk (session scraping) and restricted official academic access. |
| **Period / language** | Per M6 windows; en + id. |
| **Constraints** | Platform ToS (documented); author-location verification remains poor regardless of volume; bot/coordination content requires the duplicate screen (audit Phase 2). |
| **Status** | **PENDING TEAM APPROVAL** (M6 + ethics gate) — lowest priority of the collection items. |

---

## Sequencing summary (recommendation, no decision made)

**P0 (complete existing) → P1 (metadata refresh, low risk) → P2 (Reddit decision, data exists) → P3 (ms gap) → P4 (T institutions) → P5 (S2a/fr) → P6 (TLS) → P7 (X).**

Every item: **PENDING TEAM APPROVAL** where a scope decision (D1, D3/M5, M1–M8) or the ethics/ToS gate is a precondition. No collection occurs until (a) the relevant pending decisions are taken, (b) sources pass the registry eligibility gate, and (c) the ethics sign-off is recorded.
