# Pending Decisions Register — Research Team (consolidated)
**Purpose**: single authoritative list of decisions that belong to the research team, with their current state and impact. Engineering work does NOT proceed on unapproved items. Updated: 2026-11-08.

| ID | Decision | Options / notes | Impact if unresolved | Status |
|---|---|---|---|---|
| D1 | Canonical RQ1 wording (F1 ASEAN/social-only · F2 international · F3 international-across-poros — preserved verbatim in `RQ_SPECIFIC_RESEARCH_DESIGN.md`) | F1 vs F2/F3 | Which subset is the RQ1 answer; which claims are in scope | **OPEN** |
| D2 | Role of non-ASEAN strata (S2–S3) and category T if F1 is chosen | excluded · control/comparator | Analysis frame | **OPEN** |
| D3/M5 | Indonesian-origin units (inside S1 structurally; analytic filter) | exclude (as piloted) · include as flagged subset | 295 id-language rows in/out of claims | **OPEN** |
| D4 | RQ2 stimulus coupling (the "493 ASEAN units" idea is **not supported as a validated subset** — measured composition differs) | joint decision with RQ2 team | Survey instrument design | **OPEN** |
| D5 | Construct vocabulary (sentiment/narrative vs stance/framing) | F1 vs F3 vocabulary | Manuscript terminology | **OPEN** |
| M1 | Timor-Leste (ASEAN 11th member, 26 Oct 2025): F1 scope interpretation + source discovery | — | S1 coverage | **OPEN** |
| M2 | AU/NZ placement (Pacific vs Western stratum) | — | Cross-bloc comparisons | **OPEN** |
| M3 | New Caledonia / French press inclusion | — | Melanesian-caucus coverage (fr = 0 measured) | **OPEN** |
| M4 | Category-T (transnational) handling in comparisons | — | AJE dominance treatment | **OPEN** |
| M6 | Temporal window for claims/collection | — | 2008–2026 span treatment | **OPEN** |
| M7 | Platform set (Reddit integration: 31 REVIEW records; Instagram never implemented) | — | Platform coverage | **OPEN** |
| M8 | Quotas / target N (1,540 pilot vs 3,000–5,000 aspiration) | — | Collection planning | **OPEN** |
| N1 | Cross-lingual path for id/und sentiment (translate id→en via `opus-mt-id-en` + spot-checks; or multilingual model; or scope out) | — | Whether non-EN rows enter sentiment claims | **OPEN** |
| N2 | Stance architecture (zero-shot NLI interim vs fine-tune after annotation) + stance target(s) from: Indonesian sovereignty over Papua · Papuan self-determination · human-rights protection · Indonesian government policy · international diplomatic intervention (**not interchangeable**; actor distinction: publisher/author/quoted actor/overall) | — | Whether any stance claim is possible | **OPEN — IR team owns** |
| N3 | Framing codebook: keep 5-category topic-salience taxonomy (approved text) and/or IR-team Entman codebook (unit of analysis, coding rules per function, qualitative procedure) | — | Whether framing outputs are claimable | **OPEN — IR team owns** |
| N4 | Annotation resources: annotator count (2 preferred / 1 with documented single-annotator reference limitation / 0 → descriptive-exploratory only), sample size (N=150 provisional pilot), protocol | — | Evaluation design | **OPEN** |
| N5 | Which validated RQ1 outputs may feed RQ2/RQ3 (after any validation round) | — | Handoff usage rights | **OPEN** |
| N6 | Master refresh approval: merge `fresh_inference_en.csv` labels into the master (supersedes the M0 golden baseline via a documented retirement procedure) | — | When sentiment claims rest on fresh labels | **OPEN** |
| N7 | Additional collection per `SUPPLEMENTARY_COLLECTION_PLAN.md` / scope feasibility (curated-international recommendation) | — | Coverage gaps | **OPEN** |

**Decided (recorded, no longer open)**: 2026-11-08 — Cohen's κ is **not** a mandatory completion requirement; single-annotator reference and descriptive-exploratory fallbacks are the documented alternatives (`METHODOLOGY_REPAIRED.md` §8).
