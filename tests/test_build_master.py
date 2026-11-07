"""Integration tests for the repaired master build.

Pins the invariants of data/processed/master_triangulation_repaired.csv and
build_manifest.json. Run the builder first:
    python src/build_master_repaired.py
    python -m unittest discover -s tests -v
"""

import json
import os
import sys
import unittest

import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_CSV = os.path.join(ROOT, "data", "processed", "master_triangulation_repaired.csv")
OUT_MANIFEST = os.path.join(ROOT, "data", "processed", "build_manifest.json")


@unittest.skipUnless(os.path.exists(OUT_CSV), "run build_master_repaired.py first")
class TestRepairedMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv(OUT_CSV, encoding="utf-8-sig", dtype={"post_id": str})
        with open(OUT_MANIFEST, encoding="utf-8") as f:
            cls.manifest = json.load(f)

    def test_row_counts_match_legacy_claims(self):
        self.assertEqual(len(self.df), 1571)
        counts = self.df["platform"].value_counts().to_dict()
        self.assertEqual(counts["Platform X (Twitter)"], 375)
        self.assertEqual(counts["YouTube Comments"], 884)
        self.assertEqual(counts["Media Berita Online"], 312)

    def test_no_duplicate_ids(self):
        self.assertEqual(self.df["post_id"].duplicated().sum(), 0)

    # --- AUD-03: model label authoritative; rule layer separate & evidenced ---
    def test_rule_layer_never_replaces_model_label(self):
        # sentiment_model must exist independently of stance_rule_adjusted
        self.assertIn("sentiment_model", self.df.columns)
        self.assertIn("stance_rule_adjusted", self.df.columns)
        # evidence must be non-empty exactly when the rule fired
        fired = self.df["stance_rule_fired"].astype(bool)
        ev_empty = self.df["stance_rule_evidence"].isna() | (
            self.df["stance_rule_evidence"].astype(str).str.strip() == "")
        self.assertTrue((fired == ~ev_empty).all())

    def test_model_score_semantics(self):
        # score present iff model label present (no misattributed confidence)
        has_label = self.df["sentiment_model"].notna()
        has_score = self.df["sentiment_model_score"].notna()
        self.assertTrue((has_label == has_score).all())

    def test_x_rows_requiring_rerun_are_flagged_not_fabricated(self):
        x = self.df[self.df["platform"] == "Platform X (Twitter)"]
        srcs = set(x["inference_source"].unique())
        self.assertTrue(srcs <= {"legacy_raw_recovered", "requires_rerun"})
        n_rerun = int((x["inference_source"] == "requires_rerun").sum())
        self.assertEqual(n_rerun, self.manifest["stats"]["x"]["n_requires_rerun"])
        # rows requiring rerun must have NO model label
        self.assertTrue(x.loc[x["inference_source"] == "requires_rerun",
                              "sentiment_model"].isna().all())

    # --- AUD-04: framing residual explicit; Diplomasi only from coded matches ---
    def test_residual_frame_is_explicit(self):
        self.assertIn("Other/No-Frame", set(self.df["thematic_frame"].unique()))

    def test_diplomasi_only_from_coded_evidence(self):
        dip = self.df[self.df["thematic_frame"] == "Diplomasi & Hubungan Internasional"]
        self.assertGreater(len(dip), 0)
        empty_ev = dip["framing_evidence"].isna() | (
            dip["framing_evidence"].astype(str).str.strip() == "")
        self.assertEqual(int(empty_ev.sum()), 0)

    # --- AUD-06: X origin from profile location only; topic mentions separate ---
    def test_x_origin_and_topic_separated(self):
        x = self.df[self.df["platform"] == "Platform X (Twitter)"]
        unknown = x["origin_bloc"] == "Wacana Regional Non-Spesifik"
        self.assertGreater(int(unknown.sum()), 0)  # honest about unknown origins
        with_mentions = x["topic_country_mentions"].astype(str).str.len() > 0
        self.assertGreater(int(with_mentions.sum()), 0)

    def test_nl_row_is_not_laos(self):
        # regression test for the legacy 'Nederland' -> 'Laos' bug
        x = self.df[self.df["platform"] == "Platform X (Twitter)"]
        nl = x[x["user_location"].astype(str).str.contains("Nederland", case=False,
                                                           na=False)]
        if len(nl):
            self.assertTrue((nl["origin_country"] == "Netherlands").all())
            self.assertFalse((nl["origin_country"] == "Laos").any())

    # --- AUD-05: language normalized; X api 'in' -> 'id' ---
    def test_language_normalization(self):
        x = self.df[self.df["platform"] == "Platform X (Twitter)"]
        self.assertNotIn("in", set(x["language"].unique()))
        self.assertIn("id", set(x["language"].unique()))
        # overall corpus must be reported as measured (en+id dominant)
        langs = self.df["language"].value_counts().to_dict()
        self.assertGreater(langs.get("en", 0) + langs.get("id", 0),
                           langs.get("und", 0))
        self.assertGreater(langs.get("en", 0), 800)
        self.assertGreater(langs.get("id", 0), 200)

    # --- traceability ---
    def test_manifest_traceability(self):
        st = self.manifest["stats"]
        self.assertEqual(st["x"]["legacy_ids_not_reproduced"], [])
        self.assertEqual(st["x"]["repaired_ids_not_in_legacy"], [])
        self.assertEqual(st["youtube"]["id_mismatch_vs_legacy"], [])
        self.assertEqual(st["news"]["id_mismatch_vs_legacy"], [])
        # rule-layer reproduction of legacy labels must be exact
        self.assertEqual(st["youtube"]["rule_traceability_matches"], 884)
        self.assertEqual(st["news"]["rule_traceability_matches"], 312)
        # input integrity
        self.assertEqual(len(self.manifest["input_sha256"]), 7)

    def test_stance_target_constant(self):
        self.assertTrue((self.df["stance_target"] ==
                         "Indonesia's Sovereignty & Governance in Papua").all())


if __name__ == "__main__":
    unittest.main()
