# notebooks/ — Historical Colab Notebooks (PRE-REPAIR)

These are the primary Google Colab notebooks from the legacy iteration
folders (`archive/legacy_pipelines/`), collected here for convenience.
They are **historical artifacts**: they implement the pre-repair logic
(substring geo matching, residual-as-frame relabeling, silent inference
fallback, model-label overwriting) and are **superseded by `src/`**.

Do not use them for new analysis. See `docs/METHODOLOGY_REPAIRED.md`.

| Notebook | Legacy origin |
|---|---|
| `scrape_x_asean_colab.ipynb` | 1_scraping |
| `process_nlp_colab.ipynb` | 2_sentiment_analysis (v1 baseline) |
| `process_nlp_v2_colab.ipynb` | 5_sentiment_analysis_v2 |
| `scrape_youtube_colab.ipynb` | 8_multiplatform_scraping |
| `scrape_reddit_colab.ipynb` | 8_multiplatform_scraping |
| `process_nlp_yt_colab.ipynb` | 9_sentiment_analysis_yt |
| `scrape_news_colab.ipynb` | 11_media_berita_scraping |
| `process_nlp_news_colab.ipynb` | 12_sentiment_analysis_news |

Notebooks with executed outputs (result snapshots, e.g. in
`3_hasil1_x/`) remain inside `archive/legacy_pipelines/` as provenance.
