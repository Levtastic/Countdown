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
        letters = letters.strip().lower()

        if not letters:
            return []

        lcount = Counter(letters)

        for word, wcount in self._words.items():
            if len(word) > len(letters):
                continue

            if all(lcount[char] >= count for char, count in wcount.items()):
                yield word
