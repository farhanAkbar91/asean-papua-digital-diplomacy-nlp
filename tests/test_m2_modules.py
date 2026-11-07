"""M2 module tests — independent imports, delegation equivalence, guards.

No mocked inference output is used as evidence of model behavior: the
sentiment loud-failure test exercises the REAL environment (transformers is
absent here), and predict() is not faked anywhere.
Run: python -m unittest discover -s tests -v  (from repo root)
"""

import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

import nlp_core as nc  # noqa: E402


class TestImportsAndStructure(unittest.TestCase):
    def test_independent_imports(self):
        from pipeline import config, preprocess, langid, translation, sentiment, stance, framing, run  # noqa: F401
        self.assertTrue(True)

    def test_no_circular_import(self):
        # nlp_core must NOT import anything from pipeline (acyclic dependency:
        # config_loader <- nlp_core <- pipeline.* <- run)
        import src  # noqa: F401  (namespace sanity)
        srcdir = os.path.join(ROOT, "src")
        with open(os.path.join(srcdir, "nlp_core.py"), encoding="utf-8") as f:
            core_src = f.read()
        self.assertNotIn("from pipeline", core_src)
        self.assertNotIn("import pipeline", core_src)

    def test_config_facade_is_the_m1_loader(self):
        from pipeline import config as pcfg
        import config_loader as cl
        self.assertIs(pcfg.load_framing_config, cl.load_framing_config)
        self.assertIs(pcfg.load_rules_config, cl.load_rules_config)
        self.assertIs(pcfg.load_pipeline_config, cl.load_pipeline_config)
        self.assertIs(pcfg.load_models_config, cl.load_models_config)
        self.assertIs(pcfg.ConfigError, cl.ConfigError)


class TestPreprocessModule(unittest.TestCase):
    def test_delegation_matches_nlp_core(self):
        from pipeline import preprocess as pp
        samples = [
            "Check https://t.co/abc @user now! #FreeWestPapua",
            "JAKARTA: The government built infrastructure in Papua.",
            "",
        ]
        for s in samples:
            self.assertEqual(pp.clean_for_lexicon(s), nc.clean_for_lexicon(s))
            self.assertEqual(pp.clean_for_model_card(s), nc.clean_for_model_card(s))
            self.assertEqual(pp.clean_news_text(s), nc.clean_news_text(s))
        self.assertEqual(pp.lead_max_words(), 250)
        body = "JAKARTA: " + " ".join(f"w{i}" for i in range(400))
        self.assertEqual(len(pp.extract_lead_text(body).split()), 250)

    def test_stage_text_semantics(self):
        # framing/stance input: news -> full_text; x/youtube -> clean_text
        import pandas as pd
        from pipeline.run import _stage_text
        df = pd.DataFrame({"full_text": ["raw one", "raw two"],
                           "clean_text": ["clean one", "clean two"]})
        self.assertEqual(list(_stage_text(df, "news")), ["raw one", "raw two"])
        self.assertEqual(list(_stage_text(df, "x")), ["clean one", "clean two"])
        df2 = pd.DataFrame({"full_text": ["Check https://t.co/x now"]})
        self.assertEqual(list(_stage_text(df2, "youtube")), ["Check now"])  # computed via existing cleaning


class TestLangidModule(unittest.TestCase):
    def test_x_normalization(self):
        from pipeline import langid as li
        self.assertEqual(li.normalize_x_language("in"), "id")
        self.assertEqual(li.normalize_x_language("en"), "en")
        self.assertEqual(li.normalize_x_language(""), "und")

    def test_threshold_and_seed_from_config(self):
        from pipeline import langid as li
        self.assertEqual(li.lid_min_chars(), 40)
        self.assertEqual(li.langdetect_seed(), 0)
        self.assertEqual(li.detect_language("x" * 39), "und")
        if nc._LANGDETECT_AVAILABLE:
            long_en = "The government of Indonesia stated that development in Papua continues."
            self.assertEqual(li.detect_language(long_en), li.detect_language(long_en))  # deterministic

    def test_active_backend_is_langdetect_only(self):
        from pipeline import langid as li
        self.assertEqual(li.ACTIVE_BACKEND, "langdetect")


class TestTranslationModule(unittest.TestCase):
    def test_disabled_by_default(self):
        from pipeline import translation as tr
        self.assertEqual(tr.DEFAULT_BACKEND, "none")
        self.assertEqual(tr.available_backends(), ["none"])
        self.assertEqual(tr.approved_routes(), [])
        self.assertFalse(tr.is_enabled())
        self.assertFalse(tr.is_enabled("opus_mt"))

    def test_translate_never_executes(self):
        from pipeline import translation as tr
        with self.assertRaises(tr.TranslationError):
            tr.translate(["apa kabar papua"], "id", "en")
        with self.assertRaises(tr.TranslationError):
            tr.translate(["apa kabar papua"], "id", "en", backend="opus_mt")


class TestSentimentModule(unittest.TestCase):
    def test_identity_and_labels_from_config(self):
        from pipeline import sentiment as sm
        self.assertEqual(sm.MODEL_NAME, "cardiffnlp/twitter-roberta-base-sentiment-latest")
        self.assertEqual(sm.LABELS, ["Negative", "Neutral", "Positive"])
        self.assertEqual(sm.LANGUAGE_GUARD, "english_only")

    def test_english_only_guard_is_strict(self):
        from pipeline import sentiment as sm
        mask = sm.english_only_mask(["en", "id", "und", "en", "fr"])
        self.assertEqual(mask, [True, False, False, True, False])

    def test_loud_failure_real_environment(self):
        # transformers is NOT installed in this environment: load_model must
        # raise SentimentError (no fallback, no default labels). This is a REAL
        # failure-path test, not a mock.
        from pipeline import sentiment as sm
        with self.assertRaises(sm.SentimentError) as ctx:
            sm.load_model()
        self.assertIn("NO fallback inference is permitted", str(ctx.exception))

    def test_model_card_preprocess(self):
        from pipeline import sentiment as sm
        self.assertEqual(sm.model_card_preprocess("hi @you https://t.co/x"),
                         "hi @user http")


class TestStanceModule(unittest.TestCase):
    def test_equivalence_with_nlp_core(self):
        from pipeline import stance as st
        cases = [
            ("Reports of human rights abuses in the highlands", "Netral", "x_v2"),
            ("A meeting was held to discuss the agenda", "Netral", "x_v2"),
            ("nkri harga mati", "Netral", "youtube"),
            ("Indonesia firmly rejects the referendum push", "Netral", "news"),
        ]
        for text, base, variant in cases:
            self.assertEqual(st.apply_stance_rule(text, base, variant),
                             nc.apply_stance_rule(text, base, variant))

    def test_variants_order_and_target(self):
        from pipeline import stance as st
        self.assertEqual(st.VARIANTS, ["x_v2", "youtube", "news"])
        self.assertEqual(st.STANCE_TARGET,
                         "Indonesia's Sovereignty & Governance in Papua")
        self.assertIn("experimental", st.LAYER_STATUS)

    def test_unknown_variant_rejected(self):
        from pipeline import stance as st
        with self.assertRaises(ValueError):
            st.apply_stance_rule("text", "Netral", "nonexistent")


class TestFramingModule(unittest.TestCase):
    def test_equivalence_with_nlp_core(self):
        from pipeline import framing as fr
        cases = [
            "UN commissioner requested access amid allegations of torture",
            "the weather in jayapura was cloudy today",
            "ASEAN foreign ministers will hold a summit on regional ties",
            "There is no evidence of genocide in Papua",  # pinned limitation
        ]
        for text in cases:
            self.assertEqual(fr.classify_framing(text), nc.classify_framing(text))

    def test_categories_priority_and_residual(self):
        from pipeline import framing as fr
        self.assertEqual(fr.CATEGORY_PRIORITY, list(nc.NARRATIVE_CATEGORIES.keys()))
        self.assertEqual(fr.FRAME_RESIDUAL, "Other/No-Frame")
        frame, scores, ev = fr.classify_framing("no keywords here at all")
        self.assertEqual(frame, "Other/No-Frame")
        self.assertEqual(ev, [])


if __name__ == "__main__":
    unittest.main()
