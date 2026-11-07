"""Modular NLP pipeline (M2).

Stage modules with a single implementation each, delegating to the audited
pure functions in src/nlp_core.py. No stage introduces new transformations;
behavior is preserved against the M0 golden baseline (see
tests/test_m1_golden_regression.py and tests/test_m2_*.py).
"""
