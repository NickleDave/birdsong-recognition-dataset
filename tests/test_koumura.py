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
        with self.assertRaises(TypeError):
            # position should be an int
            syl = koumura.Syllable(position=1.5, length=3200, label='0')
        with self.assertRaises(TypeError):
            # length should be an int
            syl = koumura.Syllable(position=32500, length=2709.3, label='0')
        with self.assertRaises(TypeError):
            # length should bde an int
            syl = koumura.Syllable(position=32500, length=2709.3, label='0')

    def test_Sequence(self):
        syl1 = koumura.Syllable(position=32000, length=3200, label='0')
        syl2 = koumura.Syllable(position=64000, length=3200, label='0')
        syl3 = koumura.Syllable(position=96000, length=3200, label='0')
        syl_list = [syl1, syl2, syl3]
        wav_file = 'imaginary.wav'
        seq = koumura.Sequence(wav_file=wav_file, position=16000, length=120000,
                               syl_list=syl_list)
        for attr in ['wav_file', 'position', 'length', 'num_syls', 'syls']:
            self.assertTrue(hasattr(seq, attr))

        with self.assertRaises(TypeError):
            # position should be an int
            seq = koumura.Sequence(wav_file=wav_file, position=1.5, length=3200,
                                   syl_list=syl_list)
        with self.assertRaises(TypeError):
            # length should be an int
            seq = koumura.Sequence(wav_file=wav_file, position=32500, length=2709.3,
                                   syl_list=syl_list)
        with self.assertRaises(TypeError):
            # length should bde an int
            seq = koumura.Sequence(position=32500, length=2709.3, label='0')

    def test_parsexml(self):
        xml_file = os.path.join(self.test_data_dir, 'Annotation.xml')
        seq_list_no_concat = koumura.parse_xml(xml_file, concat_seqs_into_songs=False)
        self.assertTrue(all([type(seq) == koumura.Sequence 
                             for seq in seq_list_no_concat]))
        seq_list_concat = koumura.parse_xml(xml_file, concat_seqs_into_songs=True)
        self.assertTrue(all([type(seq) == koumura.Sequence 
                        for seq in seq_list_concat]))
        self.assertTrue(seq_list_no_concat != seq_list_concat)

    def test_load_song_annot(self):
        assert False
