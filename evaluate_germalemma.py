# -*- coding: utf-8
import codecs
from random import shuffle
from statistics import mean
from collections import defaultdict

from germalemma import GermaLemma, VALID_POS_PREFIXES

tiger_corpus="data/tiger_release_aug07.corrected.16012013.conll09"

def load_tokens(corpus_file):
    known_tokens = set()
    tokens = []
    with codecs.open(corpus_file, encoding='utf8') as f:
        for line in f:
            parts = line.split()
            if len(parts) == 15:
                token, lemma = parts[1:3]
                pos = parts[4]

                if any(pos.startswith(x) for x in VALID_POS_PREFIXES) and token not in known_tokens:
                    tokens.append((token, lemma, pos))
                    known_tokens |= {token}

    return tokens

all_tokens = load_tokens(tiger_corpus)

pct_success_all_trials = []
incorrect_lemmata = []
known_incorrect_lemmata_tokens = set()
for _ in range(10):
    shuffle(all_tokens)

    n_split = int(len(all_tokens) * 0.75)
    tokens_a, tokens_b = all_tokens[:n_split], all_tokens[n_split:]

    # build lemmatizer with tokens_a

    lemmata = defaultdict(dict)
    lemmata_lower = defaultdict(dict)
    for token, lemma, pos in tokens_a:
        GermaLemma.add_to_lemmata_dicts(lemmata, lemmata_lower, token, lemma, pos)

    lemmatizer = GermaLemma(lemmata=lemmata, lemmata_lower=lemmata_lower)

    # test lemmatizer with tokens_b

    n_success = 0
    for token, true_lemma, pos in tokens_b:
        found_lemma = lemmatizer.find_lemma(token, pos)
        if found_lemma == true_lemma:
            n_success += 1
        elif found_lemma != token and token not in known_incorrect_lemmata_tokens:
            incorrect_lemmata.append((token, found_lemma, true_lemma))
            known_incorrect_lemmata_tokens |= {token}

    n_all = len(tokens_b)
    pct_success = round(n_success / n_all * 100, 2)
    print('%d / %d = %.2f%%' % (n_success, n_all, pct_success))

    pct_success_all_trials.append(pct_success)

print()
print(mean(pct_success_all_trials))
#print()
#print(incorrect_lemmata)
