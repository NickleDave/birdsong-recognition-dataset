![Build Status](https://github.com/NickleDave/birdsong-recognition-dataset/actions/workflows/ci.yml/badge.svg)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4584210.svg)](https://doi.org/10.5281/zenodo.4584210)
![PyPI version](https://badge.fury.io/py/birdsong-recognition-dataset.svg)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
# birdsong-recognition-dataset
Python utility for working with data from the following repository:  
Koumura, T. (2016). BirdsongRecognition (Version 1). figshare.  
<https://doi.org/10.6084/m9.figshare.3470165.v1>  
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
<https://github.com/cycentum/birdsong-recognition>

The original code was released under the GNU license:  
<https://github.com/cycentum/birdsong-recognition/blob/master/LICENSE>

The `birdsongrec` module is used with the [`crowsetta`](https://github.com/NickleDave/crowsetta)
 package to make the repository a dataset available in the
[`hybrid-vocal-classifier`](https://hybrid-vocal-classifier.readthedocs.io/en/latest/)
and [`vak`](https://github.com/NickleDave/vak) libraries.

### Installation
#### with `pip`

```console
$ pip install birdsong-recognition-dataset
```

#### with `conda`

```console
$ conda install birdsong-recognition-dataset -c conda-forge
```

### Usage

The main thing that `birdsongrec` gives you is easy access to the
annotation, without having to deal with the .xml file format.

This format is schematized in [this XML schema file](./doc/xsd/AnnotationSchema.xsd),
adapted [from the original](https://github.com/cycentum/birdsong-recognition/blob/master/xsd/AnnotationSchema.xsd) 
under the [GNU license](https://github.com/cycentum/birdsong-recognition/blob/master/LICENSE)
(file is unchanged except for formatting for readability).

To access the annotation in the `Annotation.xml` files for each bird,
use the `parse_xml` function.
```Python
>>> from birdsongrec import parse_xml
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

The `birdsongrec` package also provides a convenience function to load the annotation
for an individual song, `load_song_annot`. This is basically a wrapper
around `parse_xml` that filters out the songs you don't want.
```Python
>>> from birdsongrec import load_song_annot
>>> wav1 = load_song_annot(wav_file='1.wav')
>>> print(wav1)                                                                                                  
Sequence from 1.wav with position 32000 and length 214176  
```

### Getting Help
Please feel free to raise an issue here:  
https://github.com/NickleDave/birdsong-recognition-dataset/issues

### License
[BSD License](./LICENSE).

### Citation
If you use this package, please cite the DOI:  
[![DOI](https://zenodo.org/badge/159952839.svg)](https://zenodo.org/badge/latestdoi/159952839)
