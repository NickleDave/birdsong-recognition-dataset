![Build Status](https://github.com/NickleDave/koumura/actions/workflows/ci.yml/badge.svg)
![DOI](https://zenodo.org/badge/159952839.svg)
![PyPI version](https://badge.fury.io/py/koumura.svg)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
# koumura
Functions for working with data from the following repository:
<https://figshare.com/articles/BirdsongRecognition/3470165>  

The repository contains .wav files of Bengalese finch song from ten birds
and annotation for the songs in .xml files.

This repository provides a great resource, and was used to benchmark
a sliding window-based neural network for segmenting and labeling
the elements of birdsong, as described in the following paper:  
Koumura, Takuya, and Kazuo Okanoya.  
"Automatic recognition of element classes and boundaries in the birdsong
with variable sequences."  
PloS one 11.7 (2016): e0159188.  
<https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0159188>  

The code for the network can be found here:  
<https://github.com/takuya-koumura/birdsong-recognition>

The original code was released under the GNU license:  
<https://github.com/takuya-koumura/birdsong-recognition/blob/master/LICENSE>

The `koumura` module is used with the [`crowsetta`](https://github.com/NickleDave/crowsetta)
 package to make the repository a dataset available in the
[`hybrid-vocal-classifier`](https://hybrid-vocal-classifier.readthedocs.io/en/latest/)
and [`vak`](https://github.com/NickleDave/vak) libraries.

It's called `koumura` because that's the last name of the first author
on the paper, and because I am too lazy to type `PyBirdsongRecognition`.

### Installation
`$ pip install koumura`

### Usage

The main thing that `koumura` gives you is easy access to the
annotation, without having to deal with the .xml file format.

To access the annotation in the `Annotation.xml` files for each bird,
use the `parse_xml` function.
```Python
>>> from koumura import parse_xml
>>> seq_list = parse_xml(xml_file='./Bird0/Annotation.xml', concat_seqs_into_songs=False)
>>> seq_list[0]
Sequence from 0.wav with position 32000 and length 43168
>>> seq_list[0].syls[:3]
[Syllable labeled 0 at position 2240 with length 2688, Syllable labeled 0 at position 8256 with length 2784, Syllable labeled 0 at position 14944 with length 2816]  
```

Notice that this package preserves the abstraction of the original code,
where syllables and sequences of syllables are represented as objects.
This can be helpful if you are trying to replicate functionality from
that code.  
**Importantly, each song is broken up into a number of "sequences".**
You can set the flag `concat_seqs_into_songs` to `True` if you want
`parse_xml` to concatenate sequences by song (.wav file), so that each
Sequence is actually all the sequences from one song.  
If you are using the annotation to work with the dataset for
some other purpose, you may find it more convenient to work with some
other format. For that, please check out the
[`crowsetta`](https://github.com/NickleDave/crowsetta)
tool, that helps with building datasets of annotated vocalizations
in a way that's annotation-format agnostic.

The `koumura` package also provides a convenience function to load the annotation
for an individual song, `load_song_annot`. This is basically a wrapper
around `parse_xml` that filters out the songs you don't want.
```Python
>>> from koumura import load_song_annot
>>> wav1 = load_song_annot(wav_file='1.wav')
>>> print(wav1)                                                                                                  
Sequence from 1.wav with position 32000 and length 214176  
```

### Getting Help
Please feel free to raise an issue here:  
https://github.com/NickleDave/koumura/issues

### License
[BSD License](./LICENSE).

### Citation
If you use this package, please cite the DOI:
[![DOI](https://zenodo.org/badge/159952839.svg)](https://zenodo.org/badge/latestdoi/159952839)
