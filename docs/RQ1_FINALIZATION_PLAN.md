# RQ1 Finalization Plan — Independent Audit & Minimum Closure Path (PROVISIONAL DRAFT)
**Status**: planning document for team review. Read-only audit basis; nothing was fixed, re-inferred, or decided here.
**Date**: 2026-11-07 · **Branch**: `repo-restructuring` · **Verified during this audit**: 107/107 tests · golden/master hashes MATCH · **objective: close RQ1 with minimum necessary work, not more architecture.**

> **EXECUTION STATUS (2026-11-08, final closure task)**:
> - **T2 reliability fixes: EXECUTED** (stale-output removal, failed-manifest `finished_utc`, stance vocabulary guard) — 11 regression tests in `tests/test_final_closure.py`.
> - **T3 version provenance: EXECUTED** (`pipeline_version: 2.0.0-m2`, config content identifiers, manifest `versions` block, inference provenance columns).
> - **T4 documentation corrections: EXECUTED** (plan LOC, 1,409→1,407, manifest wording, 19 non-EN/ID/und records enumerated).
> - **T1 fresh EN inference: EXECUTED** via a dedicated Python 3.11 venv (torch 2.15.0+cpu, transformers 5.22.2) — artifact `data/processed/fresh_inference_en.csv` + manifest with the resolved HF revision. Master/golden frozen; merge = decision N6.
> - Remaining for RQ1 closure: team decisions (§3) + human annotation/evaluation (§7) + final documentation (§8) — see `PENDING_DECISIONS_REGISTER.md`.
> - Test baseline after closure: 118/118.

---

## 1. Current engineering readiness (Part A — implementation inspected, not reports)

| # | Check | Verdict | Evidence / detail |
|---|---|---|---|
| A1 | M0 golden + manifest integrity | **PASS** | SHA re-verified: golden & master match manifest |
| A2 | M1 configuration loading / behavior preservation | **PASS** | 107/107 tests incl. witness + golden regression; single config source verified (no in-code duplicates) |
| A3 | M2 module boundaries / import compatibility | **PASS** | acyclic (`config_loader ← nlp_core ← pipeline.* ← run.py`); assertion test present; builder untouched (420 LOC) |
| A4 | All 107 tests | **PASS** | re-run during this audit: 107/107 OK |
| A5 | CLI behavior | **PASS** | exit codes 0/1/2 verified (M2 tests + re-audit) |
| A6 | Every stage performs its documented transformation | **PASS** | framing stage re-run on real input (884 rows, residual + evidence present); per-platform text semantics match builder |
| A7 | Failed stages leaving misleading artifacts | **MINOR ISSUE ×2** | (i) a failed run to a previously-used output path **leaves the stale successful output file** in place while the manifest honestly says `failed` — reading the CSV without the manifest misleads; (ii) failed manifests lack `finished_utc` (written before the `finally` block re-runs; the final rewrite is skipped when the exception propagates) |
| A8 | Manifest reproducibility/auditability | **PASS (note)** | input/output hashes + commit + row counts present; manifests contain timestamps → auditable, not byte-deterministic (wording in M2 report slightly overstates "deterministic") |
| A9 | Sentiment entry point executable in a supported environment | **PASS with caveat** | code path reviewed correct (int-indexed labels per model card, guard, loud failure); **actual execution remains unverified** until a Colab run happens — no transformers here |
| A10 | Historical vs fresh inference distinction | **PASS** | `inference_source` + golden provenance notes; nothing relabeled |
| A11 | Documentation currency | **MINOR ISSUE** | refactor plan §1 LOC stale (says 455/148; actual 375/132 after M1/M2); audit-MD erratum 1,409→1,407 still unfixed |

**Engineering readiness: sufficient to close RQ1.** The two MINOR issues and two doc staleness items are small, listed as tasks T2/T5 below; none blocks closure conceptually.

## 2. Current academic readiness (Part B — condensed)

- **Scope (B1)**: three RQ1 formulations remain unresolved (F1 ASEAN/social-only · F2 international · F3 international-across-poros); decision D1 gates what the dataset is *for*; D2–D5, M1–M8 remain with the team. Pipeline decisions that depend on them: analyzed subset (S1-only vs S1–S3+T), platform set (social-only vs multi), Indonesian-origin inclusion (D3/M5), temporal window (M6).
- **Dataset validity (B2)**: 1,540 retained records. Measured coverage: language en 1,013 / id 295 / und 213; X author origins 71% unclassifiable; YouTube (56% of corpus) has **no temporal resolution**; news spans 2008–2026 with scrape-day-dated outliers; S1 rests on MY/SG only; zero S2a publishers; category T dominated by one outlet; YouTube blocs are channel cohorts. **Documentable** (limitation text suffices): all of the above. **Requires new data**: any claim about Malaysia-language/French/Melanesian-island/Timor-Leste discourse, commenter-level geography, or pre-2026 X temporal dynamics.
- **Sentiment (B3)**: Cardiff EN-only model is **retained for EN rows only** (1,013 records; 894 with historical labels + 119 of the 133 requires-rerun). Historical predictions are **not** valid simply because they exist: X labels come via a partially unshipped pipeline; legacy runs recorded no execution metadata; `id` rows show the degenerate-Neutral pattern (278/282 Neutral); `und` rows were labeled despite being below reliable LID. Minimum defensible strategy: **fresh verified inference for all 1,013 EN rows** (mechanical, covers the 133), treat historical labels as superseded provenance, report `id`/`und` rows as out-of-sentiment-scope pending D3/M5 and a translation decision.
- **Stance (B4)**: the rule layer is an unvalidated keyword heuristic with a documented directional flaw (any "referendum"/"human rights" mention flips to Critical); it cannot support stance claims. A defensible stance construct needs a team-approved **codebook**: target(s) (e.g., RI sovereignty/governance; optionally OPM/armed groups as a second target — the "multiple-target" idea in the blueprint), 3-class orientation per target, an explicit `mixed/unclear` option, and human annotation. Model approach: zero-shot NLI as an assessable interim vs fine-tuning after annotation — **architecture decision PENDING**; do not commit now.
- **Framing (B5)**: the 5-category taxonomy is a domain-specific topic-salience adaptation of Entman (correctly no longer attributed to Semetko & Valkenburg). It is defensible **as lexical topic salience**, not as a measurement of Entman's four functions. Evidence extraction makes it auditable. Required: team sign-off on the codebook text (incl. residual semantics) + human validation of frame assignment.
- **Evaluation (B6)**: minimum defensible design (no results exist; none may be fabricated): written codebook + guidelines with worked examples; **stratified random sample N=150** (per the planning documents' 100–150) across platforms/languages; human reference annotation — per the 2026-11-08 team decision Cohen's κ is not mandatory: **2 independent annotators** (blind to model outputs) are the ideal option, with κ per label set (stance, framing) reported as a *measured* value if that scenario is resourced; **1 annotator** yields a single-annotator reference (no κ claim); precision/recall/F1 **macro + per-class** + confusion matrix for model-vs-reference and rules-vs-reference; explicit `mixed/unclear` label + adjudication protocol for ambiguous/multi-target items; report all numbers as measured, including failures.

## 3. Unresolved team decisions (gate the plan)

D1 canonical scope · D2 non-ASEAN strata role · D3/M5 Indonesian-origin inclusion · D4 RQ2 stimulus dependency · D5 construct vocabulary · M1 Timor-Leste interpretation · M2 AU/NZ placement · M3 New Caledonia · M4 category-T handling · M6 temporal window · M7 platform set (incl. Reddit) · M8 quotas · **new**: historical-label policy (supersede vs retain) · stance architecture (NLI interim vs fine-tune) · translation route.

## 4. Critical blockers (ranked)

1. **BLK-1 — Human annotation & evaluation do not exist.** No κ/P/R/F1 can be reported; without this, no sentiment/stance/framing claim is publishable. (Highest priority; longest lead time.)
2. **BLK-2 — No verified fresh inference.** All 1,407 existing predictions are historical (documented provenance weaknesses); sentiment claims currently rest on unverified outputs.
3. **BLK-3 — Scope decision D1** (plus D3/M5, M6) — determines which subset constitutes the RQ1 answer.
4. **BLK-4 — Stance construct/codebook** — the rule layer cannot be presented as stance evidence.
5. *(non-blocking)* A7 minor artifacts, A11 doc staleness, translation route, additional data collection — see §5–§6.

## 5. Minimum implementation tasks (code; all small)

| ID | Task | Priority | Why | Dependencies | Expected output | Team approval | Code change |
|---|---|---|---|---|---|---|---|
| T1 | **Fresh EN inference** for the 1,013 EN retained rows (includes the 133 `requires_rerun`) via `run_inference.py`/pipeline in Colab; merge through the builder's refresh mechanism | **P0** | Converts sentiment claims to verified inference; retires the historical-output risk | Colab/torch environment | refreshed master with `inference_source='fresh_inference'` + model version noted | No (mechanical completion of existing scope) | No new code (existing entry points) |
| T2 | **Fix A7 minor issues** in orchestrator: quarantine/delete stale output at same path on failure; write `finished_utc` in failed manifests; validate stance base-label vocabulary against variant passthrough keys (fail loudly on mismatch) | **P1** | Auditability of failed runs; prevents mixed-vocabulary stance outputs | none | patched `run.py` + 3–4 tests | No | Yes (small) |
| T3 | **Version/provenance stamping (minimal)**: stamp `pipeline_version`, `model_version`, `lexicon_version` columns during the T1 refresh | **P1** | Handoff consumers must know which labels are fresh vs historical | T1 | stamped master (this constitutes the "master v2" — no separate effort) | No | Yes (small) |
| T4 | **Documentation currency**: fix plan LOC inventory, audit-MD erratum (1,409→1,407), M2-report "deterministic" wording | **P2** | Report-vs-code trust | none | corrected docs | No | No (docs only) |
| T5 | Batched inference | **OPTIONAL** | Speed only; 1,013 texts are small | — | — | — | — |
| T6 | fastText LID upgrade | **OPTIONAL** (only if `und`/`id` rows enter sentiment scope) | Short-text LID quality | translation decision | evaluation report | Yes | Yes |

## 6. Minimum data tasks

| ID | Task | Priority | Condition |
|---|---|---|---|
| D-a | **None mandatory**: the 1,540-record corpus can close RQ1 as a *pilot* with documented limits | — | — |
| D-b | Additional collection (S2a/ms/TLS/institutional sources; see `SUPPLEMENTARY_COLLECTION_PLAN.md`) | **REQUIRED only if** the team approves scope claims beyond the measured coverage (D1 + M-decisions) | PENDING TEAM APPROVAL |
| D-c | YouTube timestamp re-pull | **REQUIRED only if** temporal claims about the YouTube layer are wanted | PENDING TEAM APPROVAL |
| D-d | Reddit integration | OPTIONAL (M7) | PENDING TEAM APPROVAL |

## 7. Human annotation & evaluation requirements (minimum defensible)

1. **Codebooks** (team-approved): stance (target[s], 3 classes + `mixed/unclear`, worked examples, edge cases incl. rejection-of-referendum sentences) and framing (5 categories + residual, decision rules, evidence expectations).
2. **Sample**: N=150 stratified across platform × language × stance-rule-fired, drawn from the refreshed master; plus a 20-item pilot round to calibrate the codebook.
3. **Annotators**: **2 independent**, trained on the codebook, **blind to model outputs** (never shown model labels).
4. **Agreement (per the 2026-11-08 team decision, κ is not mandatory)**: with two annotators available, report κ on the double-annotated sample; with one annotator, document a single-annotator reference (no κ claim); disagreements adjudicated by discussion (documented), with adjudicated labels forming the gold set where annotation happens.
5. **Metrics**: for each task (sentiment, stance-rule-layer, framing): precision/recall/F1 **macro and per-class**, confusion matrices, and coverage of `und`/non-EN exclusions. Report κ and per-class results **as measured** — including poor classes; no metric may be invented or omitted selectively.
6. **Handling ambiguity**: `mixed/unclear` is a valid gold label; multi-target stance items are annotated per target if the multiple-target design is approved.

## 8. Required final documentation

Updated `METHODOLOGY_REPAIRED.md` (post-T1/T3 state), a **validation report** (codebook, sample, κ, per-class metrics, adjudication log), an updated **limitations** section (all B2 items), the final **dataset dictionary** for the refreshed master, and this plan marked executed.

## 9. Handoff checklist (see companion `RQ1_HANDOFF_REQUIREMENTS.md`)

refreshed master + manifest + dataset dictionary · validation report · codebooks · limitations · reproduction commands · pending-decision register · explicit permitted/prohibited uses (incl. the RQ2-stimulus warning) · integrity verification steps for the receivers.

## 10. Definition of DONE (RQ1 closure)

RQ1 is DONE when **all** of the following hold:
1. Every sentiment claim rests on fresh, version-stamped inference over EN rows; historical labels are explicitly superseded.
2. Stance and framing labels used in any claim are supported by the human reference that the team actually produced (per-class P/R/F1 against an adjudicated or single-annotator gold set; κ only in the two-annotator scenario) from the approved codebook; the rule layer is either validated or explicitly excluded from claims.
3. D1/D3–D5/M6 are decided and the analyzed subset matches them.
4. All limitations in §2-B2 are documented in the handoff package.
5. Reproduction is one-command (`build_master_repaired.py` + tests green) and the receivers can verify integrity from the manifests.
6. The handoff document is delivered to the RQ2/RQ3 members with the permitted/prohibited-use list.

**Phases**: **P-A engineering closure** (T1–T4; days; no team decisions) → **P-B team decisions** (one meeting; D1, language strategy, stance approach, codebook, M6) → **P-C annotation & evaluation** (weeks; critical path; human effort) → **P-D handoff** (days). Avoid inventing milestones beyond these four.

---

*Nothing in this plan was implemented; no model was run; no decision was taken on the team's behalf.*
