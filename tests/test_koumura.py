"""
test koumura module
"""
import os
from glob import glob
import unittest

import numpy as np

import koumura


class TestEvfuncs(unittest.TestCase):

    def setUp(self):
        self.test_data_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '.', 'test_data',
            'Bird0',
        )

    def test_parsexml(self):
        assert False

    def test_Syllable(self):
        assert False

    def test_Sequence(self):
        assert False
