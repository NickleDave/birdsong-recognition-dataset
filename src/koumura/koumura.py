"""
Python functions to facilitate interacting with the dataset from Koumura and
Okanoya 2016 [1].

The original code was released under the GNU license:
https://github.com/takuya-koumura/birdsong-recognition/blob/master/LICENSE

The Resequencer class implements the following: 
https://github.com/cycentum/birdsong-recognition/blob/master/
birdsong-recognition/src/computation/ViterbiSequencer.java

(The Python implementation is not a direct translation of the Java code)

data: https://figshare.com/articles/BirdsongRecognition/3470165

[1] Koumura T, Okanoya K (2016) Automatic Recognition of Element Classes and
Boundaries in the Birdsong with Variable Sequences. PLoS ONE 11(7): e0159188.
doi:10.1371/journal.pone.0159188
"""
import os
import glob
import xml.etree.ElementTree as ET

import numpy as np


class Syllable:
    """Object that represents a syllable.

    Attributes
    ----------
    position : int
        starting sample number ("frame") within .wav file
        *** relative to start of sequence! ***
    length : int
        duration given as number of samples
    label : str
        text representation of syllable as classified by a human
        or a machine learning algorithm
    """
    def __init__(self, position, length, label):
        if type(position) != int:
            raise TypeError(f'position must be an int, not type {type(position)}')
        if type(length) != int:
            raise TypeError(f'length must be an int, not type {type(length)}')
        if type(label) != str:
            raise TypeError(f'label must be a string, not type {type(label)}')
        self.position = position
        self.length = length
        self.label = label

    def __repr__(self):
        rep_str = "Syllable labeled {} at position {} with length {}".format(
                   self.label,self.position,self.length) 
        return rep_str


class Sequence:
    """Object that represents a sequence of syllables.

    Attributes
    ----------
    wav_file : string
        file name of .wav file in which sequence occurs
    position : int
        starting sample number within .wav file
    length : int
        duration given as number of samples
    syls : list
        list of syllable objects that make up sequence
    seq_spect : spectrogram object
    """
    def __init__(self, wav_file, position, length, syl_list):
        if type(wav_file) != str:
            raise TypeError(f'wav_file must be a string, not type {type(wav_file)}')
        if type(position) != int:
            raise TypeError(f'position must be an int, not type {type(position)}')
        if type(length) != int:
            raise TypeError(f'length must be an int, not type {type(length)}')
        if type(syl_list) != list:
            raise TypeError(f'syl_list must be a list, not type {type(syl_list)}')
        if not all([type(syl) == Syllable for syl in syl_list]):
            raise TypeError('not all elements in syl list are of type Syllable: '
                            f'{syl_list}')
        self.wav_file = wav_file
        self.position = position
        self.length = length
        self.num_syls = len(syl_list)
        self.syls = syl_list

    def __repr__(self):
        rep_str = "Sequence from {} with position {} and length {}".format(
                  self.wav_file, self.position, self.length)
        return rep_str


def parse_xml(xml_file, concat_seqs_into_songs=False, return_wav_abspath=False,
              wav_abspath=None):
    """parses Annotation.xml files.

    Parameters
    ----------
    xml_file : str
        filename of .xml file, e.g. 'Annotation.xml'
    concat_seqs_into_songs : bool
        if True, concatenate sequences into songs, where each .wav file is a
        song. Default is False.
    return_wav_abspath : bool
        if True, change value for the wav_file field of sequences to absolute path,
        instead of just the .wav file name (without a path). This option is
        useful if you need to specify the path to data on your system.
        Default is False, in which the .wav file name is returned as written in the
        Annotation.xml file.
    wav_abspath : str
        Path to directory in which .wav files are found. Specify this if you have changed
        the structure of the repository so that the .wav files are no longer in a 
        directory named Wave that's in the same parent directory as the Annotation.xml
        file. Default is None, in which case the structure just described is assumed.

    (The last two parameters are used by the conbirt library.)

    Returns
    -------
    seq_list : list of Sequence objects
        if concat_seqs_into_songs is True, then each sequence will correspond to one song,
        i.e., the annotation for one .wav file

    Examples
    --------
    >>> seq_list = parse_xml(xml_file='./Bird0/Annotation.xml', concat_seqs_into_songs=False)
    >>> seq_list[0]
    Sequence from 0.wav with position 32000 and length 43168
    """
    if return_wav_abspath:
        if wav_abspath:
            if not os.path.isdir(wav_abspath):
                raise NotADirectoryError(f'return_wav_abspath is True but {wav_abspath} '
                                         'is not a valid directory.')
    tree = ET.ElementTree(file=xml_file)
    seq_list = []
    for seq in tree.iter(tag='Sequence'):
        wav_file = seq.find('WaveFileName').text
        if return_wav_abspath:
            if wav_abspath:
                wav_file = os.path.join(wav_abspath, wav_file)
            else:
                # assume .wav file is in Wave directory that's a child to wherever
                # Annotation.xml file is kept (since this is how the repository is
                # structured)
                xml_dirname = os.path.dirname(xml_file)
                wav_file = os.path.join(xml_dirname, 'Wave', wav_file)
            if not os.path.isfile(wav_file):
                raise FileNotFoundError('File {wav_file} is not found')

        position = int(seq.find('Position').text)
        length = int(seq.find('Length').text)
        syl_list = []
        for syl in seq.iter(tag='Note'):
            syl_position = int(syl.find('Position').text)
            syl_length = int(syl.find('Length').text)
            label = syl.find('Label').text

            syl_obj = Syllable(position=syl_position,
                               length=syl_length,
                               label=label)
            syl_list.append(syl_obj)
        seq_obj = Sequence(wav_file=wav_file,
                           position=position,
                           length=length,
                           syl_list=syl_list)
        seq_list.append(seq_obj)

    if concat_seqs_into_songs:
        song_list = []
        curr_wav_file = seq_list[0].wav_file
        new_seq_obj = seq_list[0]
        for syl in new_seq_obj.syls:
            syl.position += new_seq_obj.position

        for seq in seq_list[1:]:
            if seq.wav_file == curr_wav_file:
                new_seq_obj.length += seq.length
                new_seq_obj.num_syls += seq.num_syls
                for syl in seq.syls:
                    syl.position += seq.position
                new_seq_obj.syls += seq.syls

            else:
                song_list.append(new_seq_obj)
                curr_wav_file = seq.wav_file
                new_seq_obj = seq
                for syl in new_seq_obj.syls:
                    syl.position += new_seq_obj.position

        song_list.append(new_seq_obj)  # to append last song

        return song_list

    else:
        return seq_list


def load_song_annot(wav_file, xml_file=None, concat_seqs=True):
    """load annotation for specific song from Koumura dataset

    Parameters
    ----------
    wav_file : str
        filename of .wav file from Koumura dataset
    xml_file : str
        absolute path to Annotation.xml file that
        contains annotation for `wav_file`.
        Default is None, in which case the function
        searches for Annotation.xml in the parent directory
        of `wav_file` (if a full path is given) or the
        parent of the current working directory.
    concat_seqs : bool
        if True, concatenate sequences from the .wav file into one single Sequence.
        Default is True.

    Returns
    -------
    seq_list : list
        of Sequence objects. If concat_seqs is True, a single Sequence object will be
        returned.

    Examples
    --------
    >>> from koumura import load_song_annot
    >>> wav1 = load_song_annot(wav_file='1.wav')
    >>> print(wav1)
    Sequence from 1.wav with position 32000 and length 214176
    """
    dirname, wav_file = os.path.split(wav_file)
    if xml_file is None:
        if dirname == '':
            xml_file = glob.glob('../Annotation.xml')
        else:
            xml_file = glob.glob(os.path.join(dirname, '../Annotation.xml'))

        if len(xml_file) < 1:
            raise ValueError(f'Can\'t open {wav_file}, Annotation.xml file not found in '
                             f'parent directory {dirname}')
        elif len(xml_file) > 1:
            raise ValueError('Can\'t open {}, found more than one Annotation.xml file '
                             'in parent of current directory'.
                             format(wav_file))
        else:
            xml_file = xml_file[0]

    seq_list = parse_xml(xml_file, concat_seqs_into_songs=concat_seqs)
    seq_list = [seq for seq in seq_list if seq.wav_file == wav_file]
    if len(seq_list) == 1:
        seq_list = seq_list[0]
    return seq_list


def determine_unique_labels(annotation_file):
    """given an annotation.xml file
    from a bird in BirdsongRecognition dataset,
    determine unique set of labels applied to syllables from that bird"""
    annotation = parse_xml(annotation_file,
                           concat_seqs_into_songs=True)
    lbls = [syl.label
            for seq in annotation
            for syl in seq.syls]
    unique_lbls = np.unique(lbls).tolist()
    unique_lbls = ''.join(unique_lbls)  # convert from list to string
    return unique_lbls


class Resequencer:
    """Computes most likely sequence of labels given observation probabilities
    at each time step in sequence and a second-order transition probability
    matrix taken from training data.

    Uses a Viterbi-like dynamic programming algorithm. (Viterbi-like because
    the observation probabilities are not strictly speaking the emission
    probabilities from hidden states but instead are outputs from some machine
    learning model, e.g., the softmax layer of a DCNN that assigns a probability
    to each label at each time step.)

    This is a Python implementation of the algorithm from Koumura Okanoya 2016.
    See "compLabelSequence" in:
        https://github.com/cycentum/birdsong-recognition/blob/master/
        birdsong-recognition/src/computation/ViterbiSequencer.java

    Parameters
    ----------
    sequences : list of strings
        Each string represents a sequence of syllables
    observation_prob : ndarray
        n x m x p matrix, n sequences of m estimated probabilities for p classes
    transition_prob : ndarray
        second-order transition matrix, n x m x p matrix where the value at
        [n,m,p] is the probability of transitioning to labels[p] at time step
        t given that labels[m] was observed at t-1 and labels[n] was observed
        at t-2
    labels : list of chars
        Contains all unique labels used to label songs being resequenced

    Returns
    -------
    resequenced : list of strings
        Each string represents the sequence of syllables after resequencing. So
        e.g. resequenced[0] is sequences[0] after running through the algorithm.
    """

    def __init__(self,transition_probs,labels):
        self.transition_probs = transition_probs
        self.labels = labels
        self.num_labels = len(labels)
        self.destination_label_ind = range(0,self.num_labels)

        #num_states calculation: +1 for 'e' state at beginning of initial states
        #number of labels (now without 'e') and + 1 for the final 'tail' state
        self.num_states = (self.num_labels + 1) * self.num_labels + 1
        # create dict of lists used to determine 'destination' state
        # given source state (key) and emitted label (index into each list)
        # i..e if source state is 5, destination_state{5} will return a list as
        # long as the number of labels, indexing into that list w/ e.g. index 4
        # will return some state number that then becomes the destination state
        # so len(destination_states.keys()) == num_states
        self.destination_states = {}
        dst_state_ctr = 0
        for label_one in range(0,self.num_labels+1):  # +1 for 'e' state
            for label_two in range(0,self.num_labels):  # now without e
                dest_label_one = label_two
                dest_state_list = []
                for dest_label_two in range(0,self.num_labels):
                    dest_state_list.append(
                        dest_label_one * self.num_labels + dest_label_two)
                self.destination_states[dst_state_ctr] = dest_state_list
                dst_state_ctr += 1
        # + 1 for the final tail states
        dest_label_one = self.num_labels
        dest_state_list = []
        for dest_label_two in range(0,self.num_labels):
            dest_state_list.append(
                dest_label_one * self.num_labels + dest_label_two)
        self.destination_states[dst_state_ctr] = dest_state_list
        # number of tail states = num_states because any state can transition to
        # a tail state and the tail state is non-emitting
        self.tail_states = list(range(0,self.num_states))

        self.head_state = self.num_states - 1  # last state in list is head 
        #prob. of tranisitioning from head state 'e' to any state
        #'e1)','e2',...'e(N-1)' where N is number of labels is equal for all
        #initial states.
        self.initial_transition_prob = 1.0 / self.num_labels

    def resequence(self,observation_probs):
        num_time_steps = observation_probs.shape[0] - 1
        source_states = []
        for time_step in range(num_time_steps):
            source_states.append(np.zeros((self.num_states,),dtype=int))

        # initial inductive step of Viterbi
        current_score = np.ones((self.num_states,)) * -np.inf

        #use dest_labl_id to index into observation_prob array
        for dest_labl_id in self.destination_label_ind:
            # need destination state to assign it a score in the
            # next_score array
            dest_state = self.destination_states[self.head_state][dest_labl_id]
            obsv_prob = observation_probs[0,dest_labl_id]  # row 0 = 1st t step
            current_score[dest_state] = \
                np.log(self.initial_transition_prob) + np.log(obsv_prob)

        # main loop for Viterbi
        for time_step in range(num_time_steps):
            next_score = np.ones((self.num_states,)) * -np.inf
            for source_state in range(self.num_states):
                for dest_label_ind in self.destination_label_ind:
                    # need destination state to assign it a score in the
                    # next_score array
                    dest_state = \
                        self.destination_states[source_state][dest_label_ind]

                    label_one = source_state // self.num_labels  # floor div
                    if label_one == self.num_labels \
                        or source_state == self.head_state:
                        trans_prob = self.initial_transition_prob
                    else:
                        label_two = source_state % self.num_labels
                        trans_prob = self.transition_probs[label_one,
                                                           label_two,
                                                           dest_label_ind]
                    ob_prob = observation_probs[time_step+1][dest_label_ind]
                    tmp_next_score = current_score[source_state] + \
                                     np.log(trans_prob) + \
                                     np.log(ob_prob)
                    if tmp_next_score >= next_score[dest_state]:
                        next_score[dest_state] = tmp_next_score
                        source_states[time_step][dest_state] = source_state    
            tmp = current_score
            current_score = next_score
            next_score = tmp

        # retrieve best state sequence in reverse using scores directly
        current_state = -1

        # initial step to get best state
        for state in self.tail_states:
            if current_state == -1 \
                or current_score[state] > current_score[current_state]:
                current_state = state
        resequenced = []
        # loop through len-2 because we already figured out last element at -1
        for time_step in range((len(observation_probs)-2),-1,-1):
            previous_state = source_states[time_step][current_state]
            source_label = -1

            possible_dest_states = self.destination_states[previous_state]
            for d in range(len(possible_dest_states)):
                if possible_dest_states[d] == current_state:
                    source_label_ind = self.destination_label_ind[d]
                    source_label = self.labels[source_label_ind]
                    break
            resequenced.append(source_label)
            current_state = previous_state

        previous_state = self.head_state
        source_label = -1
        possible_dest_states = self.destination_states[previous_state]
        for d in range(len(possible_dest_states)):
            if possible_dest_states[d] == current_state:
                source_label_ind = self.destination_label_ind[d]
                source_label = self.labels[source_label_ind]
                break
        resequenced.append(source_label)
        resequenced.reverse()
        return resequenced


def get_trans_mat(seqs,smoothing_constant=1e-4):
    """calculate second-order transition matrix given sequences of syllable labels

    Parameters
    ----------
    seqs : list of Sequence objects

    smoothing_constant : float
        default is 1e-4. Added to all probabilities so that none are zero.
        Mathematically convenient for computing Viterbi algorithm with
        exponential.

    Returns
    -------
    labels : 1-d array of ints
        set of unique labels across all Sequences.

    trans_mat : 3-d array
        Shape is n * n * n where n is the number of labels.
        trans_mat[i,j,k] is the probability of transitioning to labels[k]
        at time step t, given that label at time step t-1 was labels[k]
        and the label at time step t-2 was labels[i].
    """

    all_syls = [syl.label for seq in seqs for syl in seq.syls]
    labels = np.unique(all_syls)

    all_label_seqs = []
    for seq in seqs:
        all_label_seqs.append([syl.label for syl in seq.syls])

    num_labels = labels.shape[0]
    counts = np.zeros((num_labels,num_labels,num_labels))
    for label_seq in all_label_seqs:
        for ind in range(2,len(label_seq)):
            k = np.where(labels==label_seq[ind])
            j = np.where(labels==label_seq[ind-1])
            i = np.where(labels==label_seq[ind-2])
            counts[i,j,k] += 1
    trans_mat = np.zeros(counts.shape)
    for i in range(num_labels):
        for j in range(num_labels):
            num_ij_occurences = np.sum(counts[i,j,:])
            if num_ij_occurences > 0:
                for k in range(num_labels):
                    trans_mat[i,j,k] = counts[i,j,k] / num_ij_occurences

    if smoothing_constant:
        for i in range(num_labels):
            for j in range(num_labels):
                trans_mat[i,j,:] += smoothing_constant
                trans_mat[i,j,:] /= np.sum(trans_mat[i,j,:])

    return trans_mat
