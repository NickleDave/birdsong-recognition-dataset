"""
test koumura module
"""
import os
from glob import glob
import unittest

import numpy as np

import koumura


class TestKoumura(unittest.TestCase):

    def setUp(self):
        self.test_data_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '.', 'test_data',
            'Bird0',
        )

    def test_Syllable(self):
        syl = koumura.Syllable(position=32000, length=3200, label='0')
        for attr in ['position', 'length', 'label']:
            self.assertTrue(hasattr(syl, attr))
        with self.assertRaises(ValueError):
            # position should be an int
            syl = koumura.Syllable(position=1.5, length=3200, label='0')
        with self.assertRaises(ValueError):
            # length should be an int
            syl = koumura.Syllable(position=32500, length=2709.3, label='0')
        with self.assertRaises(ValueError):
            # length should bde an int
            syl = koumura.Syllable(position=32500, length=2709.3, label='0')

    def test_Sequence(self):
        assert False


    def test_parsexml(self):
        assert False
    
    def test_load_song_annot(self):
        assert False
