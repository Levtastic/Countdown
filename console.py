#!/usr/bin/env python
# coding: utf-8

import os, sys
import time

from countdown import Solver


class App():
    def __init__(self):
        self.solver = Solver()
        self.start_time = None
        self.end_time = None

    @staticmethod
    def _resource_path(relative):
        if getattr(sys, 'frozen', False):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(__file__)

        return os.path.join(basedir, relative)

    def run(self):
        self.start_time = time.time()

        letters = self._get_letters()
        if not letters:
            print('Please include a list of letters as a command line parameter.')
            return False

        self.solver.load_words(self._resource_path('words.txt'))
        results = self.solver.get_matches(letters)

        self.end_time = time.time()

        self._display(results)

    def _get_letters(self):
        letters = ''.join(sys.argv[1:])
        letters = ''.join(c for c in letters if c.isalpha())

        return letters

    def _display(self, results):
        results.sort(key=len)

        print('{} words found in {:.5f} seconds:'.format(
            len(results),
            self.end_time - self.start_time
        ))
        print('\n'.join('({}) {}'.format(len(word), word) for word in results))


if __name__ == '__main__':
    app = App()
    app.run()
