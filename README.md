# koumura
Functions for working with data from the following repository:
<https://figshare.com/articles/BirdsongRecognition/3470165>  

The repository contains .wav files of Bengalese finch song from ten birds
and annotation for the songs in .xml files.

It's called `koumura` because that's the first author's last name, and 
because I am too lazy to type `PyBirdsongRecognition`.

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

The `koumura` module is used in the 
[`hybrid-vocal-classifier`](https://hybrid-vocal-classifier.readthedocs.io/en/latest/) 
and [`songdeck`](https://github.com/NickleDave/songdeck) libraries.

### Installation
`$ pip install koumura`

### Usage

The main thing that `koumura` gives you is easy access to the 
annotation, without having to deal with the .xml file format. 
Using `koumura` with that repository, you can load the `.cbin` audio files ...
```Python
>>> np.allclose(onsets, notmat_dict['onsets'])
True
```

### Getting Help
Please feel free to raise an issue here:  
https://github.com/NickleDave/koumura/issues

### License
[BSD License](./LICENSE).
