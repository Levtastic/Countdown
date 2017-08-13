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
        lword = Word(letters)

        return [word.value for word in self._words if word.fits_in(lword)]


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
        self._counter = self._counter or Counter(self.value)
        return self._counter

    def fits_in(self, other):
        return len(self.value) <= len(other.value) and all(
            other.counter[char] >= count for char, count in self.counter.items()
        )
