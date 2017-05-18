# -*- coding: utf-8

from germalemma import GermaLemma, VALID_POS_PREFIXES

lemmatizer = GermaLemma(tiger_corpus="data/tiger_release_aug07.corrected.16012013.conll09")

test_table = (
    # known nouns
    ((u'US-Präsident', 'N'), u'US-Präsident'),
    ((u'US-Präsidenten', 'N'), u'US-Präsident'),
    ((u'EG-Staaten', 'N'), u'EG-Staat'),
    # unknown nouns
    ((u'US-Präsidentenhaus', 'N'), u'US-Präsidentenhaus'),
    ((u'US-Präsidentenhäuser', 'N'), u'US-Präsidentenhaus'),
    ((u'EU-Neu-Delegierte', 'N'), u'EU-Neu-Delegierter'),
    # known adjectives
    ((u'fies', 'ADJ'), u'fies'),
    ((u'besser', 'ADJ'), u'gut'),
    ((u'schöne', 'ADJ'), u'schön'),
    # unknown adjectives
    ((u'unbeschreibliches', 'ADJ'), u'unbeschreiblich'),
    ((u'klagloser', 'ADJ'), u'klaglos'),
    # nonsense
    ((u'-EU-Delegierte', 'N'), u'-EU-Delegierter'),
    ((u'EU-Delegierte-', 'N'), u'EU-Delegierte-'),
    ((u'xyz123', 'N'), u'xyz123'),
    ((u'', 'ADV'), u''),
)


def test_find_lemma():
    for test, expected in test_table:
        assert lemmatizer.find_lemma(*test) == expected


def test_pickle():
    lemmatizer.save_to_pickle('data/lemmata.pickle')
    lemmatizer_from_pickle = GermaLemma(pickle='data/lemmata.pickle')

    for pos in VALID_POS_PREFIXES:
        assert len(lemmatizer.lemmata[pos]) == len(lemmatizer_from_pickle.lemmata[pos])
        assert len(lemmatizer.lemmata_lower[pos]) == len(lemmatizer_from_pickle.lemmata_lower[pos])
