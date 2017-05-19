# -*- coding: utf-8

# https://datascience.blog.wzb.eu/2016/07/13/accurate-part-of-speech-tagging-of-german-texts-with-nltk/
# http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger.html

import codecs
import pickle
from collections import defaultdict

from pyphen import Pyphen

VALID_POS_PREFIXES = ('N', 'V', 'ADJ', 'ADV')

ADJ_SUFFIXES_BASE = (
    'bar',
    'haft',
    'ig',
    'isch',
    'lich',
    'los',
    'sam',
    'en',
    'end',
    'ern'
)

ADJ_SUFFIXES_FLEX = (
    'e',
    'er',
    'es',
    'en',
    'em',
    'ere',
    'erer',
    'eres',
    'eren',
    'erem',
    'ste',
    'ster',
    'stes',
    'sten',
    'stem',
)

ADJ_SUFFIXES_DICT = {}

for suffix in ADJ_SUFFIXES_BASE:
    for flex in ADJ_SUFFIXES_FLEX:
        ADJ_SUFFIXES_DICT[suffix + flex] = suffix


class GermaLemma(object):
    pyphen_dic = Pyphen(lang='de')

    def __init__(self, **kwargs):
        if 'lemmata' in kwargs:
            self.lemmata = kwargs['lemmata']
            if 'lemmata_lower' in kwargs:
                self.lemmata_lower = kwargs['lemmata_lower']
            else:
                self.lemmata_lower = {pos: {token.lower(): lemma for token, lemma in pos_lemmata}
                                      for pos, pos_lemmata in self.lemmata.items()}
        elif 'tiger_corpus' in kwargs:
            self.lemmata, self.lemmata_lower = self.load_corpus_lemmata(kwargs['tiger_corpus'])
        elif 'pickle' in kwargs:
            self.load_from_pickle(kwargs['pickle'])
        else:
            self.load_from_pickle('data/lemmata.pickle')

    def find_lemma(self, w, pos):
        if pos.startswith('N') or pos.startswith('V'):
            pos = pos[0]
        elif pos.startswith('ADJ') or pos.startswith('ADV'):
            pos = pos[:3]

        if pos not in VALID_POS_PREFIXES:
            raise ValueError("POS tag `pos` must be one of %s" % str(VALID_POS_PREFIXES))

        if not w:   # do not process empty strings
            return w

        # look if we can directly find `w` in the lemmata dictionary
        res = self.dict_search(w, pos)
        if res:
            return res

        if pos == 'N':
            res = self._composita_lemma(w) or w
        else:
            res = w

        if pos == 'ADJ':
            res = self._adj_lemma(res)

        if pos == 'N':
            if len(res) > 1:
                res = res[0] + res[1:]
        else:
            res = res.lower()

        return res

    def dict_search(self, w, pos, use_lower=False):
        pos_lemmata = self.lemmata_lower[pos] if use_lower else self.lemmata[pos]

        return pos_lemmata.get(w, None)

    def _adj_lemma(self, w):
        for full, reduced in ADJ_SUFFIXES_DICT.items():
            if w.endswith(full):
                return w[:-len(full)] + reduced

        return w

    def _composita_lemma(self, w):
        # now split `w` by hyphenation step by step

        try:
            split_positions = [w.rfind('-') + 1]
        except ValueError:
            split_positions = []

        split_positions.extend([p for p in self.pyphen_dic.positions(w) if p not in split_positions])

        for hy_pos in split_positions:
            # split in left and right parts (start and end of the strings)
            left, right = w[:hy_pos], w[hy_pos:]

            # look if the right part can be found in the lemmata dictionary
            # if we have a noun, a lower case match will also be accepted
            if left and right and not right.endswith('innen'):
                res = self.dict_search(right, 'N', use_lower=right[0].islower())
                if res:
                    # concatenate the left side with the found partial lemma
                    if left[-1] == '-':
                        res = left + res.capitalize()
                    else:
                        res = left + res.lower()

                    if w.isupper():
                        return res.upper()
                    else:
                        return res

        return None

    @classmethod
    def load_corpus_lemmata(cls, corpus_file):
        lemmata = defaultdict(dict)
        lemmata_lower = defaultdict(dict)

        with codecs.open(corpus_file, encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                if len(parts) == 15:
                    token, lemma = parts[1:3]
                    pos = parts[4]
                    cls.add_to_lemmata_dicts(lemmata, lemmata_lower, token, lemma, pos)

        return lemmata, lemmata_lower

    @staticmethod
    def add_to_lemmata_dicts(lemmata, lemmata_lower, token, lemma, pos):
        for pos_prefix in VALID_POS_PREFIXES:
            if pos.startswith(pos_prefix):
                if token not in lemmata[pos_prefix]:
                    lemmata[pos_prefix][token] = lemma
                if lemma not in lemmata[pos_prefix]:  # for quicker lookup
                    lemmata[pos_prefix][lemma] = lemma

                if pos_prefix == 'N':
                    token_lower = token.lower()
                    if token_lower not in lemmata_lower[pos_prefix]:
                        lemmata_lower[pos_prefix][token_lower] = lemma
                    lemma_lower = lemma.lower()
                    if lemma_lower not in lemmata_lower[pos_prefix]:
                        lemmata_lower[pos_prefix][lemma_lower] = lemma

                return

    def save_to_pickle(self, pickle_file):
        with open(pickle_file, 'wb') as f:
            pickle.dump((self.lemmata, self.lemmata_lower), f, protocol=2)

    def load_from_pickle(self, pickle_file):
        with open(pickle_file, 'rb') as f:
            self.lemmata, self.lemmata_lower = pickle.load(f)
