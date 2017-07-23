#!/usr/bin/env python
# coding: utf-8

from collections import Counter


class Solver:
    def __init__(self):
        self._words = {}

    def load_words(self, filename):
        with open(filename) as file:
            words = [word.strip().lower() for word in file.readlines()]

        self._words = {word: Counter(word) for word in words}

    def get_matches(self, letters):
        if not letters:
            return []

        results = []
        letters = Counter(letters.strip().lower())

        for word, word_letters in self._words.items():
            if len(word) > len(letters):
                continue

            difference = Counter(letters)
            difference.subtract(word_letters)

            if any(val < 0 for val in difference.values()):
                continue
            
            yield word
