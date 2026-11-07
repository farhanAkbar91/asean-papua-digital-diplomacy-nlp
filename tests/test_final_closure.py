"""Final-closure regression tests (M2.1): T2 reliability fixes + T3 provenance.

Empirical tests for the audited defects: stale output on failure, missing
finished_utc in failed manifests, stance base-vocabulary leakage — plus the
version-identifier scheme (actual config hashes; no invented versions).
Run: python -m unittest discover -s tests -v  (from repo root)
"""

import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

import pandas as pd  # noqa: E402

from pipeline.run import StageError, run_stage  # noqa: E402
from config_loader import content_version, load_pipeline_config, load_models_config  # noqa: E402

ROWS = (
    "post_id,full_text,language\n"
    'a,"Reports of human rights abuses in the highlands",en\n'
    'b,"A plain factual sentence with enough words",en\n'
)
ROWS_NATIVE_BASE = (
    "post_id,full_text,sentiment_model,language\n"
    'a,"Reports of human rights abuses in the highlands",Netral,en\n'
    'b,"A plain factual sentence with enough words",Netral,en\n'
)
ROWS_UNIFIED_BASE = (
    "post_id,full_text,sentiment_model,language\n"
    'a,"Reports of human rights abuses in the highlands",Negative,en\n'
    'b,"A plain factual sentence with enough words",Neutral,en\n'
)


class ClosureTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def inp(self, name, content):
        path = os.path.join(self.tmp, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def outp(self, name):
        return os.path.join(self.tmp, name)


class TestT2StaleOutputProtection(ClosureTestBase):
    def test_failed_run_removes_previous_output(self):
        i = self.inp("in.csv", ROWS)
        o = self.outp("out.csv")
        run_stage("langid", "youtube", i, o)          # successful run writes output
        self.assertTrue(os.path.exists(o))
        with self.assertRaises(Exception):
            run_stage("sentiment", "youtube", i, o)   # failing run, same path
        self.assertFalse(os.path.exists(o),
                         "stale successful output survived a failed run")

    def test_stale_output_removal_failure_is_loud(self):
        i = self.inp("in.csv", ROWS)
        o = self.outp("out.csv")
        run_stage("langid", "youtube", i, o)
        os.remove(o)    # replace the file with a directory at the same path
        os.makedirs(o)  # -> removal of the "previous artifact" is impossible
        with self.assertRaises(StageError) as ctx:
            run_stage("langid", "youtube", i, o)
        self.assertIn("cannot remove previous artifact", str(ctx.exception))


class TestT2FailedManifestCompleteness(ClosureTestBase):
    def test_failed_manifest_has_finished_utc(self):
        i = self.inp("in.csv", ROWS)
        o = self.outp("out.csv")
        with self.assertRaises(Exception):
            run_stage("sentiment", "youtube", i, o)
        man = json.load(open(o + ".manifest.json", encoding="utf-8"))
        self.assertEqual(man["status"], "failed")
        self.assertIsNotNone(man["finished_utc"],
                             "failed manifest missing finished_utc")
        self.assertIsNotNone(man["error"])
        self.assertIsNone(man["output"])


class TestT2StanceVocabularyGuard(ClosureTestBase):
    def test_unified_english_base_rejected_for_x_v2(self):
        i = self.inp("in.csv", ROWS_UNIFIED_BASE)
        with self.assertRaises(StageError) as ctx:
            run_stage("stance", "x", i, self.outp("o.csv"))
        self.assertIn("base-label vocabulary incompatible", str(ctx.exception))
        self.assertIn("Negative", str(ctx.exception))
        self.assertIn("Positif", str(ctx.exception))  # actionable: allowed keys shown
        self.assertFalse(os.path.exists(self.outp("o.csv")))

    def test_native_base_accepted(self):
        i = self.inp("in.csv", ROWS_NATIVE_BASE)
        o = self.outp("o.csv")
        man = run_stage("stance", "x", i, o)
        self.assertEqual(man["status"], "ok")
        df = pd.read_csv(o, encoding="utf-8-sig")
        self.assertIn("Netral", set(df["stance_rule_adjusted"].astype(str)))

    def test_no_base_column_allowed(self):
        i = self.inp("in.csv", ROWS)
        o = self.outp("o.csv")
        man = run_stage("stance", "x", i, o)
        self.assertEqual(man["status"], "ok")

    def test_news_variant_uses_lowercase_vocabulary(self):
        # news passthrough keys are LOWERCASE ('negative'/'neutral'/'positive');
        # the guard is case-sensitive because the passthrough lookup is.
        i = self.inp("in.csv",
                     "post_id,full_text,sentiment_model,language\n"
                     'a,"a plain factual sentence with enough words",neutral,en\n')
        o = self.outp("o.csv")
        man = run_stage("stance", "news", i, o)
        self.assertEqual(man["status"], "ok")  # compatible vocabulary passes
        with self.assertRaises(StageError):
            run_stage("stance", "news",
                      self.inp("in2.csv",
                               "post_id,full_text,sentiment_model,language\n"
                               'a,"a plain factual sentence with enough words",Neutral,en\n'),
                      self.outp("o2.csv"))  # wrong case is rejected


class TestT3VersionProvenance(ClosureTestBase):
    def test_pipeline_version_is_actual_identifier(self):
        self.assertEqual(load_pipeline_config()["pipeline_version"], "2.0.0-m2")

    def test_config_content_versions_are_real_hashes(self):
        import hashlib
        for name in ["lexicon.yaml", "rules.yaml"]:
            expected = hashlib.sha256(
                open(os.path.join(ROOT, "configs", name), "rb").read()).hexdigest()[:12]
            self.assertEqual(content_version(name), expected)
        self.assertEqual(content_version("lexicon.yaml"), content_version("lexicon.yaml"))

    def test_manifest_carries_versions(self):
        i = self.inp("in.csv", ROWS)
        o = self.outp("o.csv")
        run_stage("langid", "youtube", i, o)
        man = json.load(open(o + ".manifest.json", encoding="utf-8"))
        self.assertEqual(man["versions"]["pipeline_version"], "2.0.0-m2")
        self.assertEqual(man["versions"]["lexicon_version"], content_version("lexicon.yaml"))
        self.assertEqual(man["versions"]["rules_version"], content_version("rules.yaml"))
        self.assertEqual(man["versions"]["model_version"],
                         load_models_config()["sentiment"]["revision"])

    def test_model_version_defaults_to_honest_unknown(self):
        rev = load_models_config()["sentiment"]["revision"]
        self.assertIn("unknown", rev)  # no execution has pinned a revision yet


if __name__ == "__main__":
    unittest.main()
