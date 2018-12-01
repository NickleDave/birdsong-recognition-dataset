# koumura
Functions for working with data from the following repository:
<https://figshare.com/articles/BirdsongRecognition/3470165>
The repository contains .wav files of Bengalese finch song from ten birds
and annotation for the songs in .xml files.
It's called `koumura` because that's the first author's last name, and 
because I am too lazy to type `PyBirdsongRecognition`.

This repository provides a great benchmark, and was used to that effect 
with a sliding window-based neural network for segmenting and labeling 
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

### Installation
`$ pip install koumura`

### Usage

The main that that `koumura` gives you is easy access to the annotation, 
without having to deal with the .xml file format. 
Using `koumura` with that repository, you can load the `.cbin` audio files ...
```Python
>>> import evfuncs

>>> rawsong, samp_freq = evfuncs.load_cbin('gy6or6_baseline_230312_0808.138.cbin')
```

... and the annotation in the `.not.mat` files ...
```Python
>>> notmat_dict = evfuncs.load_notmat('gy6or6_baseline_230312_0808.138.cbin')
```
(or, using the `.not.mat` filename directly)
```Python
>>> notmat_dict = evfuncs.load_notmat('gy6or6_baseline_230312_0808.138.not.mat')
```

...and you should be able to reproduce the segmentation of the raw audio files of birdsong
into syllables and silent periods, using the segmenting parameters from a .not.mat file and 
the simple algorithm applied by the SegmentNotes.m function.

```Python
>>> smooth = evfuncs.smooth_data(rawsong, samp_freq)
>>> threshold = notmat_dict['threshold']
>>> min_syl_dur = notmat_dict['min_dur'] / 1000
>>> min_silent_dur = notmat_dict['min_int'] / 1000
>>> onsets, offsets = evfuncs.segment_song(smooth, samp_freq, threshold, min_syl_dur, min_silent_dur)
>>> import numpy as np
>>> np.allclose(onsets, notmat_dict['onsets'])
True
```
(*Note that this test would return `False` if the onsets and offsets in the .not.mat 
annotation file had been modified, e.g., a user of the evsonganaly GUI had edited them,
after they were originally computed by the SegmentNotes.m function.*)

The `koumura` module is used in the 
[`hybrid-vocal-classifier`](https://hybrid-vocal-classifier.readthedocs.io/en/latest/) 
and [`songdeck`](https://github.com/NickleDave/songdeck) libraries.

### Getting Help
Please feel free to raise an issue here:  
https://github.com/NickleDave/koumura/issues

### License
[BSD License](./LICENSE).
