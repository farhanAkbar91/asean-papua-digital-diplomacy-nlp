"""M2 orchestrator tests — stage execution, validation, manifests, loud failures.

Uses small synthetic CSVs in temp directories plus one REAL environment
behavior test (sentiment stage fails loudly without transformers — no mocks,
no simulated success).
Run: python -m unittest discover -s tests -v  (from repo root)
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

from pipeline import run as run_mod  # noqa: E402
from pipeline.run import StageError, run_stage  # noqa: E402


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def write_csv(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


YT_ROWS = (
    "post_id,full_text,language\n"
    'yt_a,"Reports of human rights abuses in the highlands",en\n'
    'yt_b,"A meeting was held to discuss the agenda",en\n'
    'yt_c,"pemerintah menyatakan pembangunan papua berjalan",id\n'
)
X_ROWS = (
    "post_id,full_text,language\n"
    'x_a,"human rights violations reported",in\n'
    'x_b,"plain meeting text",en\n'
)
NEWS_ROWS = (
    "post_id,full_text\n"
    'n_a,"JAKARTA: ASEAN foreign ministers held a summit on regional ties."\n'
)


class OrchestratorTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def inp(self, name, content):
        return write_csv(os.path.join(self.tmp, name), content)

    def outp(self, name):
        return os.path.join(self.tmp, name)


class TestValidStages(OrchestratorTestBase):
    def test_langid_youtube(self):
        i = self.inp("in.csv", YT_ROWS)
        o = self.outp("out.csv")
        man = run_stage("langid", "youtube", i, o)
        self.assertEqual(man["status"], "ok")
        out = open(o, encoding="utf-8-sig").read()
        self.assertIn("langdetect_seed0", out)
        self.assertEqual(man["input"]["rows"], 3)
        self.assertEqual(man["output"]["rows"], 3)  # no silent record loss
        self.assertEqual(man["input"]["sha256"], sha(i))
        self.assertEqual(man["output"]["sha256"], sha(o))

    def test_langid_x_uses_api_column(self):
        i = self.inp("in.csv", X_ROWS)
        o = self.outp("out.csv")
        man = run_stage("langid", "x", i, o)
        out = open(o, encoding="utf-8-sig").read()
        self.assertIn("x_api_lang_normalized", out)
        self.assertIn("id", out)  # 'in' normalized to 'id'

    def test_framing_outputs_with_evidence(self):
        i = self.inp("in.csv", YT_ROWS)
        o = self.outp("out.csv")
        man = run_stage("framing", "youtube", i, o)
        self.assertEqual(man["status"], "ok")
        out = open(o, encoding="utf-8-sig").read()
        self.assertIn("thematic_frame", out)
        self.assertIn("Other/No-Frame", out)         # explicit residual
        self.assertIn("human rights", out)           # evidence preserved

    def test_stance_outputs_and_variant(self):
        i = self.inp("in.csv", YT_ROWS)
        o = self.outp("out.csv")
        man = run_stage("stance", "youtube", i, o)
        self.assertEqual(man["variant"], "youtube")
        out = open(o, encoding="utf-8-sig").read()
        self.assertIn("stance_rule_adjusted", out)
        self.assertIn("stance_rule_evidence", out)
        self.assertIn("stance_rule_fired", out)

    def test_stance_variant_override_and_rejection(self):
        i = self.inp("in.csv", NEWS_ROWS)
        o = self.outp("out.csv")
        man = run_stage("stance", "news", i, o, variant="news")
        self.assertEqual(man["variant"], "news")
        with self.assertRaises(StageError):
            run_stage("stance", "news", i, self.outp("o2.csv"), variant="bogus")

    def test_preprocess_adds_clean_text_and_news_lead(self):
        i = self.inp("in.csv", NEWS_ROWS)
        o = self.outp("out.csv")
        run_stage("preprocess", "news", i, o)
        out = open(o, encoding="utf-8-sig").read()
        self.assertIn("clean_text", out)
        self.assertIn("clean_lead", out)

    def test_input_unchanged_after_run(self):
        i = self.inp("in.csv", YT_ROWS)
        before = sha(i)
        run_stage("framing", "youtube", i, self.outp("out.csv"))
        self.assertEqual(sha(i), before)

    def test_manifest_fields_complete(self):
        i = self.inp("in.csv", YT_ROWS)
        o = self.outp("out.csv")
        run_stage("langid", "youtube", i, o)
        man = json.load(open(o + ".manifest.json", encoding="utf-8"))
        for key in ["schema", "stage", "platform", "input", "output", "status",
                    "error", "started_utc", "finished_utc", "code_commit"]:
            self.assertIn(key, man)
        self.assertEqual(man["schema"], "stage-manifest-v1")
        self.assertEqual(man["status"], "ok")
        self.assertIsNotNone(man["code_commit"])


class TestValidationFailures(OrchestratorTestBase):
    def test_invalid_stage_rejected(self):
        i = self.inp("in.csv", YT_ROWS)
        with self.assertRaises(StageError):
            run_stage("tokenize", "youtube", i, self.outp("o.csv"))

    def test_invalid_platform_rejected(self):
        i = self.inp("in.csv", YT_ROWS)
        with self.assertRaises(StageError):
            run_stage("langid", "instagram", i, self.outp("o.csv"))

    def test_missing_input_rejected(self):
        with self.assertRaises(StageError):
            run_stage("langid", "youtube", os.path.join(self.tmp, "nope.csv"),
                      self.outp("o.csv"))

    def test_missing_full_text_rejected(self):
        i = self.inp("in.csv", "post_id\na\n")
        with self.assertRaises(StageError):
            run_stage("framing", "youtube", i, self.outp("o.csv"))

    def test_missing_post_id_rejected(self):
        i = self.inp("in.csv", "full_text\nsome text\n")
        with self.assertRaises(StageError):
            run_stage("framing", "youtube", i, self.outp("o.csv"))

    def test_duplicate_post_id_rejected(self):
        i = self.inp("in.csv", YT_ROWS + 'yt_a,"another text",en\n')
        with self.assertRaises(StageError):
            run_stage("framing", "youtube", i, self.outp("o.csv"))

    def test_output_equals_input_rejected(self):
        i = self.inp("in.csv", YT_ROWS)
        with self.assertRaises(StageError):
            run_stage("framing", "youtube", i, i)

    def test_empty_input_rejected(self):
        i = self.inp("in.csv", "post_id,full_text\n")
        with self.assertRaises(StageError):
            run_stage("framing", "youtube", i, self.outp("o.csv"))

    def test_langid_x_requires_language_column(self):
        i = self.inp("in.csv", "post_id,full_text\nx_a,text here enough\n")
        with self.assertRaises(StageError):
            run_stage("langid", "x", i, self.outp("o.csv"))


class TestSentimentStageRealBehavior(OrchestratorTestBase):
    def test_sentiment_fails_loudly_without_model_environment(self):
        # REAL environment behavior (transformers absent): the stage must fail
        # loudly, write a FAILED manifest, and never fabricate labels.
        i = self.inp("in.csv", YT_ROWS)
        o = self.outp("out.csv")
        with self.assertRaises(Exception) as ctx:
            run_stage("sentiment", "youtube", i, o)
        man = json.load(open(o + ".manifest.json", encoding="utf-8"))
        self.assertEqual(man["status"], "failed")
        self.assertIn("torch/transformers unavailable", man["error"])
        self.assertIn("NO fallback inference is permitted", man["error"])
        self.assertFalse(os.path.exists(o))  # no output produced on failure


class TestCliEntryPoint(OrchestratorTestBase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, os.path.join(ROOT, "src", "pipeline", "run.py"), *args],
            capture_output=True, text=True, cwd=ROOT)

    def test_cli_valid_stage_exit_zero(self):
        i = self.inp("in.csv", YT_ROWS)
        o = self.outp("out.csv")
        r = self.run_cli("--stage", "framing", "--platform", "youtube",
                         "--input", i, "--output", o)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("[ok]", r.stdout)

    def test_cli_invalid_stage_exit_nonzero(self):
        i = self.inp("in.csv", YT_ROWS)
        r = self.run_cli("--stage", "nope", "--platform", "youtube",
                         "--input", i, "--output", self.outp("o.csv"))
        self.assertNotEqual(r.returncode, 0)

    def test_cli_missing_input_exit_nonzero(self):
        r = self.run_cli("--stage", "framing", "--platform", "youtube",
                         "--input", os.path.join(self.tmp, "nope.csv"),
                         "--output", self.outp("o.csv"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("[FATAL]", r.stderr)


if __name__ == "__main__":
    unittest.main()
