# Global Sampling Framework — RQ1 (Provisional, Geography-First)
**Status**: Provisional planning framework for team discussion. **Not an approved methodology. No scraping has been performed.**
**Companion to**: `docs/RQ_SPECIFIC_RESEARCH_DESIGN.md` (RQ1 assignment, preserved formulations, unresolved scope discrepancy D1).
**Evidence legend**: **[V]** verified against a cited project artifact · **[A]** assumption · **[R]** recommendation · **[PENDING TEAM APPROVAL]** unresolved decision.

---

## 1. Design principles

1. **Geography-first**: geographic strata are defined *before* source selection, so that source discovery fills a geographic frame rather than the frame emerging from whatever sources are easiest to scrape. **[R]**
2. **Language follows availability**: expected languages are derived from geography *and then validated against actual source availability*; no country is assumed representable (instruction: do not assume every country/language can be covered). **[R]**
3. **No coverage fabrication**: no outlet is claimed verified unless the project's own pilot data shows it produced content; no circulation/coverage statistics are asserted. **[V]**
4. **Compatibility with both RQ1 scopes** (documented discrepancy D1): strata are designed so an ASEAN-only analysis (F1) and an international analysis (F2/F3) draw from the same frame. **[R]**

---

## 2. Four-way attribution model (mandatory per-item metadata)

Every sampled unit must carry four independently recorded attributes. The pilot's audit showed these were historically conflated (e.g., YouTube comments geo-tagged by *channel*; X blocs inferred from *text mentions*); the model below keeps them separate. **[V]** for the limitations (see `docs/METHODOLOGY_REPAIRED.md` §6; `data/processed/build_manifest.json` `bloc_basis`).

| Attribute | Definition (operational) | How captured | Reliability note |
|---|---|---|---|
| **Publisher/source country** | Country where the publishing organization is headquartered/registered | Outlet registry entry (curated, with evidence URL) | High if registry is documented; transnational outlets (e.g., Al Jazeera) get HQ country *plus* a `transnational` flag |
| **Country/region discussed** | Countries/regions the document is about | Entity matching on text (gazetteer, word-boundary; the repaired `topic_country_mentions` logic) | Multi-valued; a unit may discuss several countries |
| **Author location** | Location of the individual author/poster, only where an explicit basis exists | Self-reported platform fields only (e.g., X profile location). These are **declarations, not verified facts** — even when present, the attribute is recorded as `self-reported`. | **Often absent** — pilot evidence: 267/375 X rows have no classifiable origin **[V]**. Units without a basis are labelled `unverified`, never imputed |
| **Community affiliation** | Membership of, or posting within, an online community (e.g., a subreddit) | Platform metadata (subreddit, channel, group) | **Not evidence of geographic location.** Affiliation may correlate with location but must be recorded as its own attribute and must never be used to impute author location |
| **Platform / media type** | Channel class | Registry: `news_mainstream`, `public_broadcaster`, `wire`, `social_x`, `social_youtube_comments`, `social_reddit`, `multilateral_ngo` | Deterministic |

Rule: **publisher country ≠ discussed country ≠ author location**. Cross-tabulations must state which attribute they use. **[R]**

---

## 3. UN M49 geographic reference (proposed mapping)

UN M49 is used as the neutral geographic vocabulary (numeric codes per the UN Statistics Division classification). The project's legacy bloc names are retained as *construct labels* so pilot comparability is preserved.

### 3.1 Proposed strata

| Stratum | M49 region(s) | Countries (M49 numeric / ISO-3) | Legacy construct label |
|---|---|---|---|
| **S1 — Southeast Asia (ASEAN member states)** | 035 South-eastern Asia | Brunei 096/BRN · Cambodia 116/KHM · **Indonesia 360/IDN** · Laos 418/LAO · Malaysia 458/MYS · Myanmar 104/MMR · Philippines 608/PHL · Singapore 702/SGP · Thailand 764/THA · **Timor-Leste 626/TLS** (11th ASEAN member, 26 Oct 2025 — see M1) · Viet Nam 704/VNM | "Blok ASEAN" |
| **S2a — Melanesia & Pacific** | 054 Melanesia | Fiji 242/FJI · New Caledonia 540/NCL · Papua New Guinea 598/PNG · Solomon Islands 090/SLB · Vanuatu 548/VUT | "Blok Pasifik & Melanesia" |
| **S2b — Australia & New Zealand** | 053 Australia and New Zealand | Australia 036/AUS · New Zealand 554/NZL | *(see mapping decision M2 — pilot placed AU/NZ inside "Blok Pasifik & Melanesia")* |
| **S3 — Western / Anglosphere & Europe** | 154 Northern Europe · 155 Western Europe · 021 Northern America | United Kingdom 826/GBR · United States 840/USA · Netherlands 528/NLD · France 250/FRA · Switzerland 756/CHE | Blueprint poros 3 "Barat/Anglosphere" (never implemented as a separate bloc) |

**Category T — transnational / multilateral sources (NOT a geographic stratum).** UN system bodies, international NGOs, and outlets without a single national editorial base (e.g., Al Jazeera English → HQ Qatar 634/QAT, M49 145; BenarNews → US-funded). Units from category T are labelled by the category plus their recorded HQ country; they are **never counted as a geographic stratum** and cannot substitute for a country stratum in any geographic comparison. Legacy label: "Mitra Global". (Replaces the former "S4" of the first draft; see decision M4.)

**Structural definition resolving the former S0/S1 overlap (Indonesia).** Indonesia **is part of S1** (M49 035; ASEAN member). The former draft's separate "S0" stratum is **abolished**: Indonesian origin is handled as an *author-location attribute value* (`origin_country = Indonesia`) with a documented default **analysis filter** — the pilot excluded Indonesia-origin X accounts (note "semua negara ASEAN jangan indonesia", `MABA SCOPUS.pdf` p.1) and registered no Indonesian news outlets. Whether Indonesian-origin units are analyzed is decision D3/M5 (**PENDING TEAM APPROVAL**) — this is an analytic filter, not a structural gap in the frame. **[R]**

### 3.2 Mapping decisions requiring the team (each is a documented ambiguity)

| ID | Issue | Status |
|---|---|---|
| M1 | **Timor-Leste (626/TLS)**: **current membership fact updated — ASEAN's 11th member since 26 October 2025** (per team instruction, 2026-11-07); M49 035 therefore coincides with current ASEAN membership, and S1 is defined on that basis. **Historical distinction**: the project documents were drafted without referencing accession, so the F1 formulation "negara-negara anggota ASEAN" may have been intended as the pre-accession ASEAN-10; the pilot registry contained **no Timor-Leste sources** (verified) **[V]**. | Membership fact: **resolved**. Interpretive scope (whether TLS units fall under F1 as written) and source-discovery expectations for TLS: **PENDING TEAM APPROVAL** — no coverage assumed |
| M2 | **Australia/NZ (S2b)**: M49 places them in Oceania but not Melanesia; the pilot data placed them under "Blok Pasifik & Melanesia" while the blueprint's 4-poros design (never implemented) put them in "Barat/Anglosphere" — a documented inconsistency. | **PENDING TEAM APPROVAL** — S2b in Pacific stratum, in S3, or separate |
| M3 | **New Caledonia (540)**: French overseas territory; M49 Melanesia; French-language press relevant to the Melanesian caucus claim. | Recommendation: keep in S2a; **PENDING TEAM APPROVAL** |
| M4 | **Transnational outlets** (Al Jazeera, BenarNews): publisher HQ ≠ editorial geography; such outlets belong to **category T**, not to any geographic stratum. | Recommendation: category T with HQ country recorded; **PENDING TEAM APPROVAL** |
| M5 | **Indonesian-origin units (analysis filter inside S1)**: pilot excluded Indonesia-origin X accounts (documented note "jangan indonesia" in `MABA SCOPUS.pdf` p.1) and registered no Indonesian news outlets; under F2/F3 international scope, Indonesian-language discourse is part of the measured corpus (id ≈ 300 units **[V]**). Structural question is resolved (S1 includes Indonesia; exclusion is a filter, not a stratum — see §3.1). | Analytic inclusion/exclusion: **PENDING TEAM APPROVAL** (overlaps design doc D3) |

---

## 4. Candidate country & source discovery framework (provisional)

**No scraping performed.** Two evidence tiers are distinguished.

### Tier A — outlets already exercised by the pilot (evidence: pilot article counts, `0_data`/`13_hasil_news` as preserved in `archive/legacy_pipelines/`) **[V]**

| Outlet | Publisher country (stratum) | Observed pilot yield (news articles) |
|---|---|---|
| RNZ Pacific | New Zealand (S2b/S3 — mapping M2) | 50 |
| ABC News Australia | Australia (S2b/S3 — mapping M2) | 50 |
| Al Jazeera English | Qatar HQ — transnational (category T) | 50 |
| CNA (Channel NewsAsia) | Singapore (S1) | 45 |
| Free Malaysia Today | Malaysia (S1) | 43 |
| The Straits Times | Singapore (S1) | 31 |
| The Star | Malaysia (S1) | 31 |
| Asia Pacific Report | New Zealand-based regional (S2b) | 11 |
| Astro AWANI | Malaysia (S1) | 1 |
| New Straits Times, Malay Mail, BenarNews | Malaysia/Malaysia/US-funded | **0 in pilot** (registered but no yield — do not assume availability) |

Pilot registry also mentioned but never tested (prose documents only): Fiji Times, Vanuatu Daily Post, Solomon Star, Reuters, The Guardian, BBC, The Diplomat — **UNVERIFIED candidates**. **[V]** that they are untested.

### Tier B — candidate discovery databases & directories (none queried yet; all **UNVERIFIED**)

| Candidate | Intended use | Coverage limitations (qualitative, to be verified in discovery) |
|---|---|---|
| Google News RSS (`site:` queries) | Initial per-outlet/per-country discovery — **already used by pilot** **[V]** | English-locale bias (pilot used `hl=en&gl=US`); index nondeterminism; date-parse fallback stamped scrape-day dates (documented) |
| GDELT 2.0 | Cross-country news indexing incl. Pacific/ASEAN languages; outlet discovery where registries are thin | Machine-extracted metadata; no full text; machine translation; precision on niche political topics unverified |
| Media Cloud | Outlet directory with country collections; attention data | Coverage depends on curated RSS lists; smaller Pacific outlets may be absent |
| Factiva / Nexis / NewsBank (subscription) | Archival breadth incl. major ASEAN titles; language coverage | Commercial licensing restricts redistribution of texts; institutional access required; title lists vary by license — must be checked against university subscriptions **[A]** |
| Asia News Network (member-paper directory) | ASEAN outlet discovery | Only member papers; list must be verified |
| PINA / Pacific media directories; Devpolicy (ANU) | Pacific/Melanesia outlet discovery | Small outlets; intermittent publishing; archives may be shallow — must be verified outlet-by-outlet |

**Discovery protocol** (what the later deliverables operationalize): for each stratum → enumerate candidate outlets via Tier-B directories → record evidence URL + language + access route in `COUNTRY_SOURCE_REGISTER.csv` → mark verified only after a manual access check. **[R]**

### Platform dimension (constraints documented from pilot experience) **[V]**
- **X**: pilot used session-cookie scraping (`twikit`) — platform-ToS risk documented; official academic access is restricted/paid. Author location verifiable only from profile fields (267/375 unclassifiable).
- **YouTube**: comments retrievable via registry of news-channel videos; pilot evidence: 884 comments from 22 videos, 59.7% from one channel (Al Jazeera) — single-outlet dominance must be capped in future sampling; timestamps were relative strings only.
- **Reddit**: pilot registered threads but Reddit data did **not** enter the master corpus; subreddits (`r/Malaysia`, `r/singapore`, `r/asean`, `r/pacific`, …) provide **community affiliation** — a separate attribute under §2, which may correlate with but does **not** prove an author's geographic location. Any Reddit-based geographic claim would require an independent, verifiable location basis. **[R]** (not a promise of data).

---

## 5. Multilingual considerations (from measured availability, not assumption)

| Language | Basis | Status |
|---|---|---|
| English | Measured dominant corpus language (en ≈ 1,018 units in repaired master **[V]**) | In scope |
| Indonesian | Measured (id ≈ 300 units; X API `in`→`id` 117/375 **[V]**) | In scope — but its *analytic* status depends on M5/D3 |
| Malay | Expected for S1 (Malaysia) by project documents **[A]**; pilot news corpus contained **0 Malay articles** (measured heuristic check **[V]**); no `opus-mt` ms→en checkpoint exists (verified against Hugging Face, `docs/METHODOLOGY_REPAIRED.md` §3) | Representation **not assumed**; discovery must establish whether Malay-language Papua coverage exists at usable volumes |
| French | Expected via New Caledonia/Melanesian caucus claim (project docs **[A]**); pilot found **no French content** **[V]** | Same — discovery-dependent; do not promise |
| Tetum/Portuguese (Timor-Leste), Burmese, Khmer, Lao, Thai, Vietnamese, Filipino | None in pilot; plausible small yields for this niche topic **[A]** | Explicitly out of guaranteed scope; only included if discovery proves availability |

Rule: the `LANGUAGE_COVERAGE_MATRIX.csv` deliverable will record **evidence-based** language availability per stratum; empty cells mean "not established", not zero. **[R]**

---

## 6. Provisional sampling strategy

| Dimension | Provisional rule | Status |
|---|---|---|
| **Geographic** | Stratified purposive over the geographic strata **S1–S3 plus transnational/multilateral source category T** (all in scope under F2/F3; S1 only under F1, with the roles of S2–S3 and T per D2 — noting T is a source category, not a geographic stratum). Per-stratum minimum outlet counts and per-outlet caps to prevent single-outlet dominance (pilot evidence: one channel = 59.7% of a platform pillar **[V]**) — caps set after discovery | Framework **[R]**; numbers **PENDING TEAM APPROVAL** |
| **Temporal** | Bounded window(s) required — pilot news span 2008-08-14 → 2026-09-04 unstratified, plus 4 scrape-day-dated items **[V]**. Candidate: fixed recent window and/or event-anchored windows (e.g., documented Papua protest/hostage episodes). | Window definition **PENDING TEAM APPROVAL** |
| **Source-level** | Outlet inclusion requires: documented registry entry (evidence URL, publisher country, platform type, language) + manual access check; registered-but-zero-yield outlets are not silently dropped — recorded as `no_yield_observed` | **[R]** |
| **Language** | Per-item language recorded (API field where present, deterministic detection otherwise, threshold-documented); units below detection threshold labelled `und` as in the repaired pipeline; no machine-translation step is *assumed* — if translation is adopted, it must follow `docs/METHODOLOGY_REPAIRED.md` §3 quality-check requirement | **[R]** |
| **Attribution** | Four-way metadata (§2) mandatory per unit; `unverified` author location is a valid value | **[R]** |
| **Platform** | Multi-platform under F2/F3; social-only under F1 (D1). Reddit recommended as pilot-adjacent addition for verifiable community geography | **PENDING TEAM APPROVAL** |
| **Sample sizes / quotas** | **None are stated anywhere in this framework** — target N and per-stratum quotas are team decisions after discovery yields are known | **PENDING TEAM APPROVAL** |

---

## 7. Consolidated decision register (carried into team discussion)

D1 canonical RQ1 scope (see design doc) · D2 role of non-ASEAN strata and of transnational/multilateral category T · D3/M5 Indonesian-origin units (analysis filter within S1) · D4 RQ2 stimulus dependency · D5 construct vocabulary · M1 Timor-Leste (membership fact updated; scope interpretation open) · M2 AU/NZ placement · M3 New Caledonia · M4 transnational outlets (category T) · M6 temporal window(s) · M7 platform set (incl. Reddit; affiliation ≠ location) · M8 quotas/target N.

All items: **PENDING TEAM APPROVAL**.

---

## 8. Evidence vs assumption vs recommendation (summary)

- **[V] Verified**: RQ assignment and all three formulations (cited); pilot outlet yields (10 outlets incl. three zero-yield); measured corpus composition (en/id dominance; 0 Malay/French in news; 267/375 X origins unclassifiable; AJE 59.7% of YouTube pillar; news dates 2008–2026); platform limitations (twikit session scraping; YouTube relative timestamps).
- **[A] Assumptions**: expected Malay/French/Tetum availability; subscription-database access via university licenses; ASEAN membership list as of the documents' date.
- **[R] Recommendations**: geography-first strata S1–S3 on M49 (Indonesia inside S1; transnational/multilateral sources as a separate category T, not a stratum); four-way attribution model with community affiliation kept distinct from author location; two-tier discovery; outlet caps; temporal bounds; registry-gated source inclusion.
- **Nothing here is approved methodology**; every open choice is in the §7 register, marked **PENDING TEAM APPROVAL**.
