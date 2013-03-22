#!/usr/bin/env python3

import os
import re
import unittest


class HTMLish(object):
    """HumanTests documents that have HTML-style <!-- clause:markers -->"""
    def __init__(self, filename):
        self.filename = filename

    def __repr__(self):
        return self.filename

    def clauses(self):
        """Return all of the clauses in the file"""
        clauses = re.compile(
            '<!-- clause:(.*?) -->(.*?)<!-- endclause:(.*?) -->', re.DOTALL)
        seen = set()
        with open(self.filename) as infile:
            for result in clauses.finditer(infile.read()):
                startname, content, endname = result.groups()
                assert startname == endname
                assert startname not in seen
                seen.add(startname)
                yield startname, content


class HumanTests(unittest.TestCase):
    """Tests that require human interpretation"""

    documents = {}

    _separator = '-' * 80

    def __init__(self, *args, **kwargs):
        super(HumanTests, self).__init__(*args, **kwargs)
        self.clausemap = {abbrev: dict(document.clauses())
                          for abbrev, document in self.documents.items()}

    def _getclauses(self, filename):
        clauses = re.compile(
            '<!-- clause:(.*?) -->(.*?)<!-- endclause:(.*?) -->', re.DOTALL)
        with open(filename) as infile:
            for result in clauses.finditer(infile.read()):
                startname, content, endname = result.groups()
                assert startname == endname
                yield startname, content

    def _renderclauselist(self, title, items):
        print(title)
        for index, item in enumerate(items):
            if not index:
                print(self._separator)
            abbrev, clausename = item.split(':')
            print('Document: %s' % self.documents[abbrev])
            print('Clause: %s' % clausename)
            print('')
            print(self.clausemap[abbrev][clausename].strip())
            print(self._separator)

    def _renderiolist(self, title, items):
        print('%s:\n' % title)
        for item in items:
            print(' - %s' % item)
        print('')

    def assertImplements(self, givens, outcomes, supports, opposes=None):

        self._renderiolist('Givens', givens)
        self._renderiolist('Outcomes', outcomes)

        self._renderclauselist('Clauses supporting these outcomes', supports)
        if opposes is not None:
            self._renderclauselist('Clauses opposing these outcomes', opposes)

        while True:
            result = input('On balance, do these clauses support the desired '
                           'outcomes to the given situation? ').upper()
            if result in ('Y', 'N'):
                break
            print('')
            print('Please answer "Y" or "N"')

        self.assertTrue(result == 'Y')
