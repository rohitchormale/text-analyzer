#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
ASCII Text Analyzer

This module implements APIs to analyze text for possible errors and provide suggestions against input dictionary
using Damerau-Levenshtein Distance algorithm. Here, Damerau-Levenshtein Distance is calculated by using Iterative Matrix method.


usage:
text_analyzer.py [-h] [-t T] [-f F] [-d D]
optional arguments:
  -h, --help  show this help message and exit
  -t T        Input text to be analyzed
  -f F        Input file path containing text to be analyzed
  -d D        Input file path of dictionary to be used with analyzer. Each new
              word should be on new line.


References:
   https://en.wikipedia.org/wiki/Levenshtein_distance
   https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance

@author: Rohit Chormale
"""

import decimal
decimal.getcontext().prec = 6
from decimal import Decimal


INSERT_COST = 1
DROP_COST = 1
SUBSTITUTE_COST = 2
TRANSPOSE_COST = 1

# if `strict` flag applied, the words having resemblance-score below this threshold, will be dropped from suggestions.
# see func `get_match_with_score` and `analyze_word` for more info
RESEMBLANCE_THRESHOLD = 0.4
DEFAULT_ENGLISH_DICT = ["hello", "this", "is", "a", "test", "program", "which", "silly", "as", "well", "easy"]


def calculate_damerau_levenshtein_distance(s, t):
    """
    Calculate Damerau-Levenshtein distance using iterative matrix method.

    Args:
        s (string): source stringTrue
        t (string): target string

    Returns:
        Integer value
    """

    # increase matrix size null character
    rows = len(s) + 1
    cols = len(t) + 1

    # create required matrix space
    matrix = [[ 0 for j in range(cols)]for i in range(rows)]

    # calculate costs of first row (horizontal). Here 0/NULL indicates empty string.
    # As source string is empty, we can only perform insert operations to convert it in target
    for j in range(cols):
        matrix[0][j] = j * INSERT_COST

    # calculate costs of first column (vertical). Here, to convert source to null,
    # we can only perform drop operations.
    for i in range(rows):
        matrix[i][0] = i * DROP_COST

    # now calculate diagonal elements. here we will iterate cols by row to calculate how many operations we need
    # to convert source to target. This conversion will follow below rules,
    # - if source and target characters are same at given diagonal position, cost will be 0 i.e. cost upto previous characters
    # - if source and target characters are not same, then we have 3 options insert, drop and substitute.
    # We will choose operation with the lowest cost
    for j in range(1, cols):
        for i in range(1, rows):
            if s[i-1] == t[j-1]:
                DIAGONAL_COST = 0
            else:
                DIAGONAL_COST = SUBSTITUTE_COST
            matrix[i][j] = min(matrix[i][j-1] + INSERT_COST,
                               matrix[i-1][j] + DROP_COST,
                               matrix[i-1][j-1] + DIAGONAL_COST)
            # damerau lookup using transpose operations for frequent scenarios user rearranged chars during typing
            # we will choose lowest value in between old matrix and new one
            if i > 1 and j > 1 and s[i-1] == t[j-2] and s[i-2] == t[j-1]:
                matrix[i][j] = min(matrix[i][j],
                                   matrix[i-2][j-2]+TRANSPOSE_COST)

    return matrix[rows-1][cols-1]


def calculate_resemblance_score(s, t, distance):
    """
    Calculate resemblance score in range of 0 to 1, using max possible distance/cost. Higher score indicate more resemblance.
    If score == 1: both source and target strings are equal

    Args:
        source (string): source string
        target (string): target string
        distance (int): damerau-levenshtein distance between source and target string

    Returns:
        Decimal value in range of 0 to 1
    """
    max_possible_distance = max(len(s), len(t)) * max(INSERT_COST, DROP_COST, SUBSTITUTE_COST, TRANSPOSE_COST)
    return Decimal(1) - Decimal(distance)/Decimal(max_possible_distance)


def get_match_with_score(word, input_dict, limit=None, strict=False):
    """Returns possible matching words from input dictionary sorted by resemblance score.

    Args:
        word (string): word to find similar words
        input_dict (list): dictionary to match input word against
        limit (int): limiting output words
        strict (boolean): enable RESEMBLANCE_THRESHOLD to drop suggestions having score below threshold

    Returns:
        List of tuples of possible matching words with resemblance score
        e.g.[('foo', 0.9111), ('Bar', 0.6543), ('Baz', 0.333)]"""
    suggestions = []
    for i in input_dict:
        dist = calculate_damerau_levenshtein_distance(word.lower(), i)
        score = calculate_resemblance_score(word, i, dist)
        if not strict:
            suggestions.append((i, score))
        else:
            if score >= Decimal(0.4):
                suggestions.append((i, score))

    if limit is None or limit > len(suggestions):
        return sorted(suggestions, key=lambda x: x[1], reverse=True)
    return sorted(suggestions, key=lambda x: x[1], reverse=True)[:limit]


def analyze_word(word, input_dict, limit=1, strict=False):
    """
    Analyze given word against input dictionary to find possible matches

    Args:
        word (string): input word to find matches
        input_dict (list): input dictionary to match against word
        limit (int): max number of suggestions
        strict (boolean): remove words from suggestions which are below RESEMBLANCE_THRESHOLD

    Returns:
        word and list of possible suggestions.
        e.g. 'fo', ['foo', 'bar', 'baz']
    """
    match_with_scores = get_match_with_score(word, input_dict, limit, strict)
    suggestions = [i[0] for i in match_with_scores]
    return word, suggestions


def analyze_paragraph(text, input_dict):
    """
    Analyze given paragraph again input dictionary to find wrong words and return possible suggestions.

    Args:
        text (string): text to analyze
        input_dict (list): input dict to match against text paragraph

    Returns:
        list of tuples of word and possible matches.
    """
    result = []
    text_list = text.split()
    for word in set(text_list):
        # If word not present in dict, then only try to match suggestion
        if word.lower() not in input_dict:
            word, suggestions = analyze_word(word, input_dict, strict=True)
            if suggestions:
                result.append((word, suggestions))
    return result


def parse_text_file(filename):
    """Parse given text file and return content of file.

    Args:
        filename (string): filepath to read text from

    Returns:
        content of path"""
    with open(filename, 'r') as text_file:
        text = text_file.read()
    return text


def parse_dict_file(filename):
    """Parse given dictionary file and return list of words, assuming new line as delimiter.

    Args:
        filename (string): filepath to read dict from. Each word should be on new line

    Returns:
        List containing words
        """
    with open(filename, 'r') as dict_file:
        input_dict = [i.strip().lower() for i in dict_file.readlines()]
    return input_dict


if __name__ == "__main__":
    import argparse, sys, os
    ap = argparse.ArgumentParser(description="Text Analyzer")
    ap.add_argument("-t", help="Input text to be analyzed")
    ap.add_argument("-f", help="Input file path containing text to be analyzed")
    ap.add_argument("-d", help="Input file path of dictionary to be used with analyzer. Each new word should be on new line.")
    args = vars(ap.parse_args())
    text_path = args["f"]
    text = args["t"]
    dict_path = args["d"]

    # Give preference over text if both -t and -f present
    if not text:
        # if input text file not present, exit
        if not text_path or not os.path.isfile(text_path):
            print("Filepath is not valid\n")
            ap.print_help()
            sys.exit(1)

        # read content of input file
        text = parse_text_file(text_path)

    # if input dict file is present, load dict else use default dict
    if dict_path and os.path.isfile(dict_path):
        input_dict = parse_dict_file(dict_path)
    else:
        input_dict = DEFAULT_ENGLISH_DICT

    # finally pass text and input dict to analyzer
    result = analyze_paragraph(text, input_dict)
    for word, suggestions in result:
        print("%s => %s" %(word, ",".join(suggestions)))
