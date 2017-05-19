# -*- coding: utf-8
import pytest

from germalemma import GermaLemma

lemmatizer = GermaLemma()

test_table = (
    # known nouns
    ((u'US-Präsident', 'N'), u'US-Präsident'),
    ((u'US-Präsidenten', 'N'), u'US-Präsident'),
    ((u'EG-Staaten', 'N'), u'EG-Staat'),
    ((u'EG-Staaten', 'NP'), u'EG-Staat'),
    # unknown nouns
    ((u'US-Präsidentenhaus', 'N'), u'US-Präsidentenhaus'),
    ((u'US-Präsidentenhäuser', 'N'), u'US-Präsidentenhaus'),
    ((u'EU-Neu-Delegierte', 'N'), u'EU-Neu-Delegierter'),
    ((u'Feinstaubbelastungen', 'N'), u'Feinstaubbelastung'),
    # known adjectives
    ((u'fies', 'ADJ'), u'fies'),
    ((u'besser', 'ADJ'), u'gut'),
    ((u'schöne', 'ADJ'), u'schön'),
    # unknown adjectives
    ((u'unbeschreibliches', 'ADJ'), u'unbeschreiblich'),
    ((u'klagloser', 'ADJ'), u'klaglos'),
    # capitalize nouns
    ((u'xyz123', 'N'), u'Xyz123'),
    # nonsense
    ((u'-EU-Delegierte', 'N'), u'-EU-Delegierter'),
    ((u'EU-Delegierte-', 'N'), u'EU-Delegierte-'),
    ((u'Xyz123', 'N'), u'Xyz123'),
    ((u'', 'ADV'), u''),
)


def test_find_lemma():
    for test, expected in test_table:
        assert lemmatizer.find_lemma(*test) == expected


def test_find_lemma_exceptions():
    with pytest.raises(ValueError):
        lemmatizer.find_lemma(u'Der', 'DET')
