"""
test birdsongrec module
"""
import os
from glob import glob
import unittest

import numpy as np

import birdsongrec


class TestKoumura(unittest.TestCase):

    def setUp(self):
        self.test_data_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '.', 'test_data',
            'Bird0',
        )

    def test_Syllable(self):
        syl = birdsongrec.Syllable(position=32000, length=3200, label='0')
        for attr in ['position', 'length', 'label']:
            self.assertTrue(hasattr(syl, attr))
        with self.assertRaises(TypeError):
            # position should be an int
            syl = birdsongrec.Syllable(position=1.5, length=3200, label='0')
        with self.assertRaises(TypeError):
            # length should be an int
            syl = birdsongrec.Syllable(position=32500, length=2709.3, label='0')
        with self.assertRaises(TypeError):
            # length should bde an int
            syl = birdsongrec.Syllable(position=32500, length=2709.3, label='0')

    def test_Sequence(self):
        syl1 = birdsongrec.Syllable(position=32000, length=3200, label='0')
        syl2 = birdsongrec.Syllable(position=64000, length=3200, label='0')
        syl3 = birdsongrec.Syllable(position=96000, length=3200, label='0')
        syl_list = [syl1, syl2, syl3]
        wav_file = os.path.join(self.test_data_dir, 'Wave', '0.wav')
        seq = birdsongrec.Sequence(wav_file=wav_file, position=16000, length=120000,
                                   syl_list=syl_list)
        for attr in ['wav_file', 'position', 'length', 'num_syls', 'syls']:
            self.assertTrue(hasattr(seq, attr))

        with self.assertRaises(TypeError):
            # position should be an int
            seq = birdsongrec.Sequence(wav_file=wav_file, position=1.5, length=3200,
                                       syl_list=syl_list)
        with self.assertRaises(TypeError):
            # length should be an int
            seq = birdsongrec.Sequence(wav_file=wav_file, position=32500, length=2709.3,
                                       syl_list=syl_list)
        with self.assertRaises(TypeError):
            # length should bde an int
            seq = birdsongrec.Sequence(position=32500, length=2709.3, label='0')

    def test_parsexml(self):
        xml_file = os.path.join(self.test_data_dir, 'Annotation.xml')
        seq_list_no_concat = birdsongrec.parse_xml(xml_file, concat_seqs_into_songs=False,
                                                   return_wav_abspath=False, wav_abspath=None)
        self.assertTrue(all([type(seq) == birdsongrec.Sequence
                             for seq in seq_list_no_concat]))
        seq_list_concat = birdsongrec.parse_xml(xml_file, concat_seqs_into_songs=True,
                                                return_wav_abspath=False, wav_abspath=None)
        self.assertTrue(all([type(seq) == birdsongrec.Sequence
                             for seq in seq_list_concat]))
        self.assertTrue(seq_list_no_concat != seq_list_concat)

        # test return_wav_abspath works with wav_abpsath=None
        seq_list_abspath = birdsongrec.parse_xml(xml_file, concat_seqs_into_songs=True,
                                                 return_wav_abspath=True, wav_abspath=None)
        for seq in seq_list_abspath:
            self.assertTrue(os.path.isfile(seq.wav_file))

        # test return_wav_abspath works with wav_abpsath specified
        wav_abpath = os.path.join(self.test_data_dir, 'Wave')
        seq_list_abspath = birdsongrec.parse_xml(xml_file, concat_seqs_into_songs=True,
                                                 return_wav_abspath=True,
                                                 wav_abspath=wav_abpath)
        for seq in seq_list_abspath:
            self.assertTrue(os.path.isfile(seq.wav_file))

    def test_load_song_annot(self):
        xml_file = os.path.join(self.test_data_dir, 'Annotation.xml')
        seq_list = birdsongrec.parse_xml(xml_file, concat_seqs_into_songs=True)

        wav_files = glob(os.path.join(self.test_data_dir,
                                      'Wave', '*.wav'))
        for wav_file in wav_files:
            seq = birdsongrec.load_song_annot(wav_file, xml_file=xml_file, concat_seqs=True)
            self.assertTrue(type(seq) == birdsongrec.Sequence)
            wav_file_without_path = os.path.split(wav_file)[1]
            wav_ind = np.asarray([wav_file_without_path == seq.wav_file 
                                  for seq in seq_list])

