# RESTRUCTURING MANIFEST — 2026-11-07
Every file movement, archival, and deletion performed during repository restructuring, with rationale. Raw datasets were hash-verified before and after (see `data/processed/build_manifest.json` `input_sha256`, and the post-restructure verification log in `docs/RECOVERY_LOG.md`).

## 1. Moves — active implementation

| From | To | Rationale |
|---|---|---|
| `recovery/nlp_core.py` | `src/nlp_core.py` | Repaired core library is the active implementation |
| `recovery/build_master_repaired.py` | `src/build_master_repaired.py` | Authoritative builder; internal paths updated (data/raw, archive/legacy_pipelines, data/processed) |
| `recovery/run_inference.py` | `src/run_inference.py` | Inference script; paths updated |
| `recovery/tests/test_nlp_core.py` | `tests/test_nlp_core.py` | Test suite relocated; import path updated to `../src` |
| `recovery/tests/test_build_master.py` | `tests/test_build_master.py` | Same |
| `recovery/requirements.txt` | `requirements.txt` | Single root dependency file; comments updated |
| `recovery/output/master_triangulation_repaired.csv` | `data/processed/master_triangulation_repaired.csv` | Processed output lives with data |
| `recovery/output/build_manifest.json` | `data/processed/build_manifest.json` | Same |

## 2. Moves — data

| From | To | Rationale |
|---|---|---|
| `0_data/asean_papua_x_tweets.csv` | `data/raw/asean_papua_x_tweets.csv` | Raw data; SHA-256 verified unchanged after move |
| `0_data/youtube_papua_asean_comments.csv` | `data/raw/youtube_papua_asean_comments.csv` | Same |
| `0_data/news_papua_asean_articles.csv` | `data/raw/news_papua_asean_articles.csv` | Same |

## 3. Moves — documentation

| From | To | Rationale |
|---|---|---|
| `METHODOLOGY_REPAIRED.md` | `docs/METHODOLOGY_REPAIRED.md` | Active methodology = current documentation |
| `RECOVERY_LOG.md` | `docs/RECOVERY_LOG.md` | Active change log (restructuring addendum added) |
| `BLUEPRINT_FINAL_PIPELINE_DAN_METODOLOGI_RQ1.md` | `docs/methodology_history/` | Historical planning doc (status banner inside) |
| `CELAH_METODOLOGIS_DAN_STRATEGI_VALIDASI_RQ1.md` | `docs/methodology_history/` | Historical self-audit |
| `FIKSASI_PIPELINE_DAN_JUSTIFIKASI_TEORI_RQ1.md` | `docs/methodology_history/` | Historical plan |
| `FRAMEWORK_EKSPANSI_GLOBAL_DAN_BATASAN_NLP_RQ1.md` | `docs/methodology_history/` | Historical plan (model facts corrected in place) |
| `JUSTIFIKASI_LITERATUR_DAN_METODOLOGI_NLP_RQ1.md` | `docs/methodology_history/` | Historical justification (references repaired in place) |
| `LAPORAN_PROGRESS_DAN_EVALUASI_RISET_FISIP.md` | `docs/methodology_history/` | Historical progress report (git-tracked move) |
| `PENJELASAN_METODE_DAN_LANGKAH_KERJA_RQ1.txt` | `docs/methodology_history/` | Historical method text (reference list repaired in place) |
| `SIAP_COPY_PASTE_GDOCS_RQ1.txt` | `docs/methodology_history/` | Historical manuscript insert (repaired in place) |
| `DRAFT FIX.pdf` | `docs/manuscripts/DRAFT FIX.pdf` | Active manuscript draft |
| `MABA SCOPUS.pdf` | `docs/manuscripts/MABA SCOPUS.pdf` | Project planning manuscript |
| `archive/legacy_pipelines/14_laporan_dan_master_dataset/Laporan_Teknis_RQ1_Data_NLP_Papua_ASEAN.docx` | `docs/manuscripts/` | Technical handover report (pre-repair figures; historical) |
| `archive/legacy_pipelines/14_laporan_dan_master_dataset/Laporan_Teknis_RQ1_Data_NLP_Papua_ASEAN.pdf` | `docs/manuscripts/` | Same |
| `recovery/archive_original_docs/*` (9 files) | `archive/pre_repair_docs/` | Verbatim pre-repair snapshots of edited documents |

## 4. Moves — legacy experiments & notebooks

| From | To | Rationale |
|---|---|---|
| `1_scraping/` … `14_laporan_dan_master_dataset/` (14 folders, intact) | `archive/legacy_pipelines/<name>/` | Deprecated code/outputs preserved for provenance; NOT for analysis |
| `1_scraping/scrape_x_asean_colab.ipynb` | `notebooks/` | Primary notebook collected; pre-repair logic (see notebooks/README.md) |
| `2_sentiment_analysis/process_nlp_colab.ipynb` | `notebooks/` | Same |
| `5_sentiment_analysis_v2/process_nlp_v2_colab.ipynb` | `notebooks/` | Same |
| `8_multiplatform_scraping/scrape_youtube_colab.ipynb` | `notebooks/` | Same |
| `8_multiplatform_scraping/scrape_reddit_colab.ipynb` | `notebooks/` | Same |
| `9_sentiment_analysis_yt/process_nlp_yt_colab.ipynb` | `notebooks/` | Same |
| `11_media_berita_scraping/scrape_news_colab.ipynb` | `notebooks/` | Same |
| `12_sentiment_analysis_news/process_nlp_news_colab.ipynb` | `notebooks/` | Same |
| `data-sampah/` | `archive/data-sampah_quarantine/` | Junk folder; 2 files are NOT duplicates (older scrape snapshot + summary) — preserved, folder excluded from publication via `.gitignore` |

## 5. New files

| File | Purpose |
|---|---|
| `LICENSE` | MIT — resolves the broken `LICENSE` link in README (holder: project contributors; REVIEW if a different holder/license is required) |
| `notebooks/README.md` | Explains historical status of collected notebooks |
| `docs/RESTRUCTURING_MANIFEST.md` | This manifest |

## 6. Deletions (with justification)

| Deleted | Justification |
|---|---|
| `__pycache__/` directories (7 locations, ~20 `.pyc` files) | Regenerable bytecode caches; already `.gitignore`d; never tracked |
| `recovery/` residual empty directories | After content redistribution |

**No research artifact, dataset, code file, or document was deleted.** All content is either in active locations or `archive/`.

## 7. Verified duplicates (retained, not merged)

| Files (identical by SHA-256) | Action |
|---|---|
| `2_sentiment_analysis/asean_papua_x_tweets.csv` == `5_sentiment_analysis_v2/asean_papua_x_tweets.csv` (13-row local test snapshot) | Retained — both inside intact archived folders; merging would break folder provenance |
| `archive/data-sampah_quarantine/asean_papua_sentiment_v2_analyzed.csv` == `archive/legacy_pipelines/7_hasil4_x/...` (+ 2 PNGs) | Retained inside quarantined folder (not published) |
| `6_hasil3_x` vs `7_hasil4_x` narrative chart PNG | Retained — distinct folder provenance |

## 8. Reference updates applied

- `src/build_master_repaired.py`, `src/run_inference.py`: all input/output paths.
- `tests/test_nlp_core.py` (import path), `tests/test_build_master.py` (output paths).
- `requirements.txt`, `README.md` (banner, tree, commands), `docs/METHODOLOGY_REPAIRED.md` (§1, §4, §5, §8), `docs/RECOVERY_LOG.md` (addendum + 2 lines), `docs/methodology_history/BLUEPRINT_*.md` (banner pointer), `.gitignore` (quarantine path).
