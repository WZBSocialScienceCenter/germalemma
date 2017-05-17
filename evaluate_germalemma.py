# -*- coding: utf-8
import codecs

from germalemma import GermaLemma

tiger_corpus="data/tiger_release_aug07.corrected.16012013.conll09"

lemmatizer = GermaLemma(tiger_corpus=tiger_corpus)


def load_tokens(corpus_file):
    known_tokens = set()
    tokens = []
    with codecs.open(corpus_file, encoding='utf8') as f:
        for line in f:
            parts = line.split()
            if len(parts) == 15:
                token, lemma = parts[1:3]

                if token not in known_tokens:
                    pos = parts[4]

                    tokens.append((token, lemma, pos))
                    known_tokens |= {token}

    return tokens


# from collections import defaultdict
# lemmata = defaultdict(dict)
# with open("data/tiger_release_aug07.corrected.16012013.conll09") as f:
#     for line in f:
#         parts = line.split()
#         if len(parts) == 15:
#             token, lemma = parts[1:3]
#             token_lower = token.lower()
#             pos = parts[4]
#
#             for pos_prefix in ('N', 'V', 'ADJ', 'ADV'):
#                 if pos.startswith(pos_prefix):
#                     if token not in lemmata[pos_prefix]:
#                         lemmata[pos_prefix][token] = lemma
#                     if lemma not in lemmata[pos_prefix]:  # for quicker lookup
#                         lemmata[pos_prefix][lemma] = lemma