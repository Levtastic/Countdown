#!/usr/bin/env python
# coding: utf-8

from collections import Counter


class Solver:
    def __init__(self):
        self._words = []

    def load_words(self, filename):
        with open(filename) as file:
            self._words = [Word(word) for word in file.readlines()]

    def get_matches(self, letters):
        letters = letters.strip().lower()

        if not letters:
            return []

        lcount = Counter(letters)

        for word in self._words:
            if len(word.value) > len(letters):
                continue

            if all(lcount[char] >= count for char, count in word.counter.items()):
                yield word.value


class Word:
    __slots__ = ('_value', '_counter')

    def __init__(self, value):
        self._value = value.strip().lower()
        self._counter = None

    @property
    def value(self):
        return self._value

    @property
    def counter(self):
        if self._counter is None:
            self._counter = Counter(self._value)

        return self._counter
