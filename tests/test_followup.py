#!/usr/bin/env python3

from .test_common import HTMLish, HumanTests


class FollupTests(HumanTests):
    documents = {
        'attendproc': HTMLish('Attendee Procedure for incident handling.md'),
        'codeconduct': HTMLish('code_of_conduct.md'),
        'staffproc': HTMLish('Staff Procedure for incident handling.md'),
    }

    def test_only_chair_makes_public_statements(self):

        givens = ['An Incident that has been reported to Staff.']

        outcomes = [
            'Staff has not addressed the public.',
            'Chair may have addressed the public.',
        ]

        supports = ['staffproc:publicresponse']

        self.assertImplements(givens, outcomes, supports)
