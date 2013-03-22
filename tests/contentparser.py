#!/usr/bin/env python

import os
import re

testfiles = {
    'codeconduct': 'code_of_conduct.md',
    'attendproc': 'Attendee Procedure for incident handling.md',
    'staffproc': 'Staff procedure for incident handling.md',
}


def getsections(filename):
    sections = re.compile('<!-- clause:(.*?) -->(.*?)<!-- endclause:(.*?) -->',
                          re.DOTALL)
    with open(filename) as infile:
        for result in sections.finditer(infile.read()):
            startname, content, endname = result.groups()
            assert startname == endname
            yield startname, content

sectionmap = {}
for abbrev, filename in testfiles.items():
    abbrevsections = sectionmap[abbrev] = {}
    for sectionname, content in getsections(os.path.join('..', filename)):
        assert sectionname not in abbrevsections
        abbrevsections[sectionname] = content
