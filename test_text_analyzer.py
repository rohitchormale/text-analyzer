#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
This module implements unit test cases for `text_analyzer.py` module.


@author: Rohit Chormale
"""


import unittest
from text_analyzer import INSERT_COST, DROP_COST, SUBSTITUTE_COST, TRANSPOSE_COST, \
    calculate_damerau_levenshtein_distance, calculate_resemblance_score, get_match_with_score, analyze_word, analyze_paragraph


class TextAnalyzer2TestCase(unittest.TestCase):
    def setUp(self):
        self.input_dict = ["hello", "this", "is", "a", "test", "program", "which", "silly", "as", "well", "easy"]

    # tests for calculate_damerau_levenshtein_distance
    def _test_calculate_damerau_levenshtein_distance_max_value(self, s, t):
        max_dist = max(len(s), len(t)) * max(INSERT_COST, DROP_COST, SUBSTITUTE_COST, TRANSPOSE_COST)
        self.assertLessEqual(calculate_damerau_levenshtein_distance(s, t), max_dist)

    def test_calculate_levenshtein_distance_less_than_max_distance(self):
        self._test_calculate_damerau_levenshtein_distance_max_value('esay', 'easy')
        self._test_calculate_damerau_levenshtein_distance_max_value('esaay', 'easy')
        self._test_calculate_damerau_levenshtein_distance_max_value('si', 'is')

    def test_calculate_levenshtein_distance_with_empty_source(self):
        s = ""
        t = "easy"
        self.assertEqual(calculate_damerau_levenshtein_distance(s, t), len(t)*INSERT_COST)

    def test_calculate_levenshtein_distance_with_empty_target(self):
        s = "easy"
        t = ""
        self.assertEqual(calculate_damerau_levenshtein_distance(s, t), len(s)*DROP_COST)

    def test_calculate_levenshtein_distance_with_equal_source_target(self):
        s = "easy"
        t = "easy"
        self.assertEqual(calculate_damerau_levenshtein_distance(s, t), 0)


    # tests for calculate_resemblance_score
    def _test_calculate_resemblance_score_optimal_values(self, s, t):
        dist = calculate_damerau_levenshtein_distance(s, t)
        self.assertGreaterEqual(calculate_resemblance_score(s, t, dist), 0)
        self.assertLessEqual(calculate_resemblance_score(s, t, dist), 1)

    def test_calculate_resemblance_score_optimal_values(self):
        self._test_calculate_resemblance_score_optimal_values("easy", "easy")
        self._test_calculate_resemblance_score_optimal_values("easy", "")
        self._test_calculate_resemblance_score_optimal_values("", "easy")
        self._test_calculate_resemblance_score_optimal_values("esay", "easy")
        self._test_calculate_resemblance_score_optimal_values("esaay", "easy")
        self._test_calculate_resemblance_score_optimal_values("si", "is")

    def test_calculate_resemblance_score_with_equal_source_target(self):
        s = "easy"
        t = "easy"
        score = calculate_resemblance_score(s, t, calculate_damerau_levenshtein_distance(s, t))
        self.assertEqual(score, 1)

    # tests for get_match_with_score
    def test_get_match_with_score(self):
        self.assertEqual(len(get_match_with_score("easy", self.input_dict)), len(self.input_dict))
        self.assertEqual(len(get_match_with_score("", self.input_dict)), len(self.input_dict))

    def test_get_match_with_score_order(self):
        # as equal target string has hightest score, we are expecting it to appear first
        self.assertEqual(get_match_with_score("easy", self.input_dict)[0][0], "easy")

    def test_get_match_with_score_limit(self):
        self.assertEqual(len(get_match_with_score("easy", self.input_dict, 1)), 1)
        self.assertEqual(len(get_match_with_score("", self.input_dict)), len(self.input_dict))
        self.assertEqual(len(get_match_with_score("", self.input_dict, limit=len(self.input_dict)+1)), len(self.input_dict))

    # tests for analyze_word
    def test_analyze_word(self):
        self.assertEqual(analyze_word("eaasy", self.input_dict), ("eaasy", ["easy"]))
        self.assertEqual(analyze_word("si", self.input_dict), ("si", ["is"]))

    def test_analyze_word_with_empty_word(self):
        self.assertEqual(analyze_word('', self.input_dict), ('', [self.input_dict[0]]))

    def test_analyze_word_with_limit(self):
        self.assertEqual(len(analyze_word("eaasy", self.input_dict, limit=3)[1]), 3)
        self.assertEqual(len(analyze_word('si', self.input_dict, limit=1)[1]), 1)
        self.assertEqual(len(analyze_word('si', self.input_dict, limit=100)[1]), len(self.input_dict))

    def test_analyze_word_with_case(self):
        self.assertEqual(analyze_word('Si', self.input_dict), ('Si', ['is']))
        self.assertEqual(analyze_word('eaAsy', self.input_dict), ('eaAsy', ['easy']))

    def test_analyze_existing_word_from_dict(self):
        self.assertEqual(analyze_word("hello", self.input_dict), ("hello", ["hello"]))


    # tests for analyze paragraph
    def test_analyze_paragraph(self):
        result = analyze_paragraph("hello this si a test progam which is silly as well as eays", self.input_dict)
        # TODO - order of result can be changed. so better write test by matching exact words
        self.assertEqual(result, [('eays', ['easy']), ('si', ['is']), ('progam', ['program'])])


if __name__ == "__main__":
    unittest.main()
