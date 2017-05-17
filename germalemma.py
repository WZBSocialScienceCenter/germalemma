# https://datascience.blog.wzb.eu/2016/07/13/accurate-part-of-speech-tagging-of-german-texts-with-nltk/
# http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger.html

from collections import defaultdict

from pyphen import Pyphen

VALID_POS_PREFIXES = ('N', 'V', 'ADJ', 'ADV')


class GermaLemma(object):
    pyphen_dic = Pyphen(lang='de')

    def __init__(self, tiger_corpus_file):
        self.lemmata, self.lemmata_lower = self._load_corpus_lemmata(tiger_corpus_file)

    def find_lemma(self, w, pos):
        if pos not in VALID_POS_PREFIXES:
            raise ValueError("POS tag `pos` must be one of %s" % str(VALID_POS_PREFIXES))

        if not w:   # do not process empty strings
            return w

        # look if we can directly find `w` in the lemmata dictionary
        res = self.dict_search(w, pos)
        if res:
            return res

        # now split `w` by hyphenation step by step
        for hy_pos in self.pyphen_dic.positions(w):
            # split in left and right parts (start and end of the strings)
            left, right = w[:hy_pos], w[hy_pos:]

            # look if the right part can be found in the lemmata dictionary
            # if we have a noun, a lower case match will also be accepted
            res = self.dict_search(right, pos, use_lower=(pos == 'N' and right[0].islower()))
            if res:
                # concatenate the left side with the found partial lemma
                return left + res.lower()

        # no (partial) lemma found -> return the input word
        return w

    @staticmethod
    def _load_corpus_lemmata(corpus_file):
        lemmata = defaultdict(dict)
        lemmata_lower = defaultdict(dict)

        with open(corpus_file) as f:
            for line in f:
                parts = line.split()
                if len(parts) == 15:
                    token, lemma = parts[1:3]
                    token_lower = token.lower()
                    pos = parts[4]

                    for pos_prefix in VALID_POS_PREFIXES:
                        if pos.startswith(pos_prefix):
                            if token not in lemmata[pos_prefix]:
                                lemmata[pos_prefix][token] = lemma
                            if lemma not in lemmata[pos_prefix]:    # for quicker lookup
                                lemmata[pos_prefix][lemma] = lemma

                            if pos_prefix == 'N':
                                if token_lower not in lemmata_lower[pos_prefix]:
                                    lemmata_lower[pos_prefix][token_lower] = lemma
                                lemma_lower = lemma.lower()
                                if lemma_lower not in lemmata_lower[pos_prefix]:
                                    lemmata_lower[pos_prefix][lemma_lower] = lemma

        return lemmata, lemmata_lower

    def dict_search(self, w, pos, use_lower=False):
        pos_lemmata = self.lemmata_lower[pos] if use_lower else self.lemmata[pos]

        return pos_lemmata.get(w, None)


# def load_sentences(corpus_file):
#     sents = []
#     cur_sent = []
#     with open(corpus_file) as f:
#         for line in f:
#             parts = line.split()
#             if len(parts) == 15:
#                 token, lemma = parts[1:3]
#                 pos = parts[4]
#                 cur_sent.append((token, lemma, pos))
#             else:
#                 sents.append(cur_sent)
#                 cur_sent = []
#
#     return sents
