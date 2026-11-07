"""M1 golden regression — proves the refactored configuration produces ZERO semantic drift.

Rebuilds the full derived pipeline output in memory (via the authoritative builder
component functions, which only READ inputs) and compares every golden field for
all 1,540 retained records against docs/M0_GOLDEN_BASELINE_MANIFEST.json's
registered baseline (data/golden/m0/golden_baseline_m0.csv).

The golden baseline is NEVER modified by this test.
Run: python -m unittest discover -s tests -v  (from repo root)
"""

import json
import os
import sys
import unittest

import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

GOLDEN = os.path.join(ROOT, "data", "golden", "m0", "golden_baseline_m0.csv")
MANIFEST = os.path.join(ROOT, "docs", "M0_GOLDEN_BASELINE_MANIFEST.json")
MASTER = os.path.join(ROOT, "data", "processed", "master_triangulation_repaired.csv")
REGISTER = os.path.join(ROOT, "docs", "DATA_EXCLUSION_REGISTER.csv")

REQUIRED = [GOLDEN, MANIFEST, MASTER, REGISTER,
            os.path.join(ROOT, "archive", "legacy_pipelines", "7_hasil4_x", "asean_papua_sentiment_v2_analyzed.csv"),
            os.path.join(ROOT, "archive", "legacy_pipelines", "10_hasil5_yt", "youtube_papua_sentiment_analyzed.csv"),
            os.path.join(ROOT, "archive", "legacy_pipelines", "13_hasil_news", "news_papua_sentiment_analyzed.csv")]


@unittest.skipUnless(all(os.path.exists(p) for p in REQUIRED), "M0 golden artifacts or legacy inputs missing")
class TestM1GoldenRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(MANIFEST, encoding="utf-8") as f:
            cls.manifest = json.load(f)
        cls.fields = cls.manifest["golden_files"][0]["columns"]
        cls.golden = pd.read_csv(GOLDEN, encoding="utf-8", dtype={"post_id": str}).sort_values("post_id").reset_index(drop=True)

        # Retained population = master rows NOT excluded by the audit register.
        reg = pd.read_csv(REGISTER, encoding="utf-8")
        cls.excluded = set(reg[reg["dataset"] == "master_repaired"]["post_id"])
        cls.master = pd.read_csv(MASTER, encoding="utf-8-sig", dtype={"post_id": str})
        cls.retained_master = cls.master[~cls.master["post_id"].isin(cls.excluded)]

        # Rebuild the derived output in memory through the authoritative builder
        # functions (read-only with respect to every file), then restrict to the
        # same retained population.
        import build_master_repaired as bm
        x_df, _ = bm.build_x()
        yt_df, _ = bm.build_yt()
        news_df, _ = bm.build_news()
        merged = pd.concat([x_df, yt_df, news_df], ignore_index=True)
        merged = merged[~merged["post_id"].isin(cls.excluded)]
        cls.rebuilt = merged.sort_values("post_id").reset_index(drop=True)

    def test_01_population_size(self):
        self.assertEqual(len(self.golden), 1540)
        self.assertEqual(len(self.rebuilt), 1540)
        self.assertEqual(len(self.retained_master), 1540)

    def test_02_join_key_alignment(self):
        self.assertEqual(list(self.golden["post_id"]), list(self.rebuilt["post_id"]),
                         "post_id sequences diverge — record identity/order not preserved")

    def test_03_no_semantic_drift_all_golden_fields(self):
        def norm_object(s):
            # NaN and empty string are the same value at the CSV serialization
            # level (golden writes na_rep=""); normalize both to "".
            return s.astype("object").where(s.notna(), "").astype(str)

        diffs = []
        for field in self.fields:
            a, b = self.golden[field], self.rebuilt[field]
            if a.dtype == float or b.dtype == float:
                same = (a == b) | (a.isna() & b.isna())
            else:
                same = norm_object(a) == norm_object(b)
            n_diff = int((~same).sum())
            if n_diff:
                examples = self.golden.loc[~same, "post_id"].head(5).tolist()
                diffs.append(f"{field}: {n_diff} rows differ, e.g. {examples} "
                             f"(old={a[~same].head(3).tolist()!r} new={b[~same].head(3).tolist()!r})")
        self.assertEqual(diffs, [], "SEMANTIC DRIFT DETECTED:\n" + "\n".join(diffs))

    def test_04_master_dataset_untouched_and_consistent(self):
        # The production master must equal golden on all fields (it is the source
        # of the baseline) — proving no dataset mutation occurred during M1.
        m = self.retained_master.sort_values("post_id").reset_index(drop=True)
        for field in self.fields:
            self.assertTrue(
                (m[field].astype(str).fillna("§NA§").values ==
                 self.golden[field].astype(str).fillna("§NA§").values).all(),
                f"production master field '{field}' differs from golden baseline")

    def test_05_golden_file_hash_matches_manifest(self):
        import hashlib
        h = hashlib.sha256(open(GOLDEN, "rb").read()).hexdigest()
        self.assertEqual(h, self.manifest["golden_files"][0]["sha256"])


if __name__ == "__main__":
    unittest.main()
