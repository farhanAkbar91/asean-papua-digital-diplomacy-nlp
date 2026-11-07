"""Unit tests for src/nlp_core.py — the repaired pipeline core.

These tests pin the REPAIRED behaviour that fixes audit issues AUD-03..AUD-07:
word-boundary geo matching, explicit framing residual, separated rule layer,
model-card preprocessing, and language normalization.
Run: python -m unittest discover -s tests -v  (from repo root)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import nlp_core as nc  # noqa: E402


class TestCleaning(unittest.TestCase):
    def test_clean_for_lexicon_removes_urls_mentions_punct(self):
        t = "Check https://t.co/abc @user now! #FreeWestPapua"
        out = nc.clean_for_lexicon(t)
        self.assertNotIn("https", out)
        self.assertNotIn("@user", out)
        self.assertIn("FreeWestPapua", out)

    def test_clean_for_model_card_follows_official_card(self):
        # Model card preprocessing: mentions -> '@user', links -> 'http'
        t = "thanks @bennywenda see https://t.co/xyz"
        out = nc.clean_for_model_card(t)
        self.assertIn("@user", out)
        self.assertIn("http", out)
        self.assertNotIn("bennywenda", out)
        self.assertNotIn("t.co", out)


class TestLanguage(unittest.TestCase):
    def test_x_lang_in_maps_to_id(self):
        self.assertEqual(nc.normalize_x_language("in"), "id")
        self.assertEqual(nc.normalize_x_language("en"), "en")
        self.assertEqual(nc.normalize_x_language("xx-not-real"), "xx-not-real")
        self.assertEqual(nc.normalize_x_language(""), "und")
        self.assertEqual(nc.normalize_x_language(None), "und")

    def test_detect_language_short_text_is_und(self):
        self.assertEqual(nc.detect_language("papua"), "und")
        # 40-char reliability threshold (documented limitation)
        self.assertEqual(nc.detect_language("x" * 39), "und")

    def test_detect_language_indonesian(self):
        out = nc.detect_language(
            "Pemerintah Indonesia menyatakan bahwa pembangunan di Papua "
            "terus berjalan dan masyarakat mendapat banyak manfaat nyata."
        )
        if nc._LANGDETECT_AVAILABLE:
            self.assertEqual(out, "id")
        else:
            self.assertEqual(out, "und")  # documented degradation without lib


class TestGeoOrigin(unittest.TestCase):
    """AUD-06: word-boundary gazetteer replaces substring matching."""

    def test_netherlands_is_not_laos(self):
        # Legacy bug: 'la' substring in "Nederland" -> "Laos"
        country, bloc = nc.origin_from_location("Den Haag, Nederland")
        self.assertEqual(country, "Netherlands")
        self.assertEqual(bloc, "Mitra Global")

    def test_switzerland_and_geneva(self):
        self.assertEqual(nc.origin_from_location("Geneva, Switzerland")[0],
                         "Switzerland")

    def test_port_vila_is_vanuatu(self):
        self.assertEqual(nc.origin_from_location("Port Vila, Vanuatu")[0],
                         "Vanuatu")
        self.assertEqual(nc.origin_from_location("Port Vila, Vanuatu")[1],
                         "Blok Pasifik & Melanesia")

    def test_new_zealand(self):
        self.assertEqual(nc.origin_from_location("Wellington, New Zealand")[0],
                         "New Zealand")

    def test_empty_location_unknown(self):
        country, bloc = nc.origin_from_location("")
        self.assertIsNone(country)
        self.assertEqual(bloc, nc.BLOC_UNKNOWN)

    def test_nonsense_location_unknown(self):
        country, bloc = nc.origin_from_location("somewhere on earth")
        self.assertIsNone(country)
        self.assertEqual(bloc, nc.BLOC_UNKNOWN)

    def test_indonesia_flagged_for_exclusion(self):
        self.assertTrue(nc.is_indonesia_origin("Jayapura, Indonesia"))
        self.assertFalse(nc.is_indonesia_origin("Kuala Lumpur, Malaysia"))

    def test_substring_collision_banned(self):
        # 'un' inside words must NOT match anything (legacy Mitra Global bug)
        self.assertIsNone(nc.match_country("Puncak Jaya highlands"))
        self.assertIsNone(nc.match_country("gunung tertinggi"))
        # 'la' inside words must map to the CORRECT country, never Laos:
        self.assertEqual(nc.match_country("Nederland"), "Netherlands")
        self.assertEqual(nc.match_country("Switzerland"), "Switzerland")
        self.assertEqual(nc.match_country("New Zealand"), "New Zealand")

    def test_topic_mentions_separate_from_origin(self):
        # Origin is derived ONLY from the location string; text mentions are a
        # separate variable. A tweet from an unknown location mentioning
        # Vanuatu has origin=None and a topic mention of Vanuatu.
        self.assertIsNone(nc.match_country("solidarity with West Papua people"))
        self.assertEqual(nc.origin_from_location("")[0], None)
        self.assertIn("Vanuatu", nc.topic_country_mentions(
            "Pacific leaders in Vanuatu and Fiji discuss Papua"))
        # 'un' as part of "under" must not appear as a mention of anything
        self.assertEqual(nc.topic_country_mentions("living under pressure"),
                         [])


class TestFraming(unittest.TestCase):
    def test_no_match_is_explicit_residual(self):
        # AUD-04/R4: zero-match must be 'Other/No-Frame', never 'Diplomasi...'
        frame, scores, ev = nc.classify_framing(
            "the weather in jayapura was cloudy today")
        self.assertEqual(frame, nc.FRAME_RESIDUAL)
        self.assertEqual(ev, [])
        self.assertEqual(sum(scores.values()), 0)

    def test_f5_requires_coded_keyword(self):
        frame, _, ev = nc.classify_framing(
            "ASEAN foreign ministers will hold a summit on regional ties")
        self.assertEqual(frame, "Diplomasi & Hubungan Internasional")
        self.assertIn("asean", ev)

    def test_f1_match_with_evidence(self):
        frame, _, ev = nc.classify_framing(
            "UN commissioner requested access amid allegations of torture")
        self.assertEqual(frame, "HAM & Pelanggaran Kemanusiaan")
        self.assertIn("torture", ev)

    def test_word_boundary_not_substring(self):
        # 'ras' (race) must not match inside 'grass'; 'un' not inside 'under'
        frame, scores, _ = nc.classify_framing(
            "green grass grows under the papuan sun")
        self.assertEqual(frame, nc.FRAME_RESIDUAL)

    def test_negation_limitation_is_documented_behaviour(self):
        # KNOWN LIMITATION (AUD-07, self-identified in CELAH doc): negation is
        # not handled; this test PINS the current behaviour so any future
        # negation handling must consciously change it.
        frame, _, ev = nc.classify_framing(
            "There is no evidence of genocide in Papua")
        self.assertEqual(frame, "HAM & Pelanggaran Kemanusiaan")
        self.assertIn("genocide", ev)


class TestStanceRuleLayer(unittest.TestCase):
    def test_rule_fires_and_records_evidence(self):
        label, ev, fired = nc.apply_stance_rule(
            "Reports of human rights abuses in the highlands", "Netral", "x_v2")
        self.assertTrue(fired)
        self.assertEqual(label, "Negatif (Kritis)")
        self.assertIn("human rights", ev)

    def test_no_fire_passes_model_label_through(self):
        label, ev, fired = nc.apply_stance_rule(
            "A meeting was held to discuss the agenda", "Netral", "x_v2")
        self.assertFalse(fired)
        self.assertEqual(label, "Netral")
        self.assertEqual(ev, [])

    def test_passthrough_mapping_variants(self):
        self.assertEqual(
            nc.apply_stance_rule("plain factual text", "Positif", "x_v2")[0],
            "Positif (Mendukung)")
        self.assertEqual(
            nc.apply_stance_rule("plain factual text", "Negatif", "youtube")[0],
            "Negatif (Kritis terhadap Diplomasi RI)")
        self.assertEqual(
            nc.apply_stance_rule("plain factual text", "neutral", "news")[0],
            "Netral (Liputan Faktual/Berimbang)")

    def test_directional_assumption_is_pinned(self):
        # AUD-09: the rule layer flips ANY mention of 'referendum' to Critical,
        # even in a pro-government sentence. This test pins the behaviour as a
        # documented limitation; the layer is experimental and must be
        # validated by human annotators before any headline use.
        label, ev, fired = nc.apply_stance_rule(
            "Indonesia firmly rejects the referendum push by separatists",
            "Netral", "x_v2")
        self.assertTrue(fired)
        self.assertEqual(label, "Negatif (Kritis)")
        self.assertIn("referendum", ev)

    def test_supportive_beats_critical_when_strictly_greater(self):
        label, _, fired = nc.apply_stance_rule(
            "otsus program brings development and special autonomy funds; "
            "one minor protest happened", "Netral", "x_v2")
        self.assertTrue(fired)
        self.assertEqual(label, "Positif (Mendukung)")

    def test_recover_x_base_label(self):
        # No-fire row: base recoverable from legacy adjusted label.
        self.assertEqual(
            nc.recover_x_base_label("plain factual text", "Netral"), "Netral")
        self.assertEqual(
            nc.recover_x_base_label("plain factual text", "Positif (Mendukung)"),
            "Positif")
        # Fired row: raw model label unrecoverable.
        self.assertIsNone(
            nc.recover_x_base_label("calls for independence referendum", "Negatif (Kritis)"))


class TestLeadExtraction(unittest.TestCase):
    def test_lead_is_first_250_words(self):
        body = "JAKARTA: " + " ".join(f"word{i}" for i in range(400))
        lead = nc.extract_lead_text(body)
        self.assertEqual(len(lead.split()), 250)
        self.assertFalse(lead.startswith("JAKARTA:"))

    def test_short_text_unchanged(self):
        self.assertEqual(nc.extract_lead_text("short article"), "short article")


class TestXSelectionFilters(unittest.TestCase):
    def test_spam_detection(self):
        self.assertTrue(nc.is_spam("FREEPHONEFREES1", "anything"))
        self.assertTrue(nc.is_spam("normaluser", "win prizes now conf & appd"))
        self.assertFalse(nc.is_spam("normaluser", "papua discourse"))

    def test_legacy_indonesia_location(self):
        self.assertTrue(nc.legacy_is_indonesia_location("Jakarta, Indonesia"))
        self.assertFalse(nc.legacy_is_indonesia_location("Oxford, UK"))

    def test_relevance(self):
        self.assertTrue(nc.is_relevant_x("West Papua human rights"))
        self.assertFalse(nc.is_relevant_x("completely unrelated football"))


if __name__ == "__main__":
    unittest.main()
