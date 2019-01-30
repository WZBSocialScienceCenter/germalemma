"""
Tests for germalemma module.

Markus Konrad <markus.konrad@wzb.eu>, Wissenschaftszentrum Berlin für Sozialforschung
January 2019
"""

import pytest

from germalemma import GermaLemma

lemmatizer = GermaLemma()

test_table = (
    # known nouns
    (('US-Präsident', 'N'), 'US-Präsident'),
    (('US-Präsidenten', 'N'), 'US-Präsident'),
    (('EG-Staaten', 'N'), 'EG-Staat'),
    (('EG-Staaten', 'NP'), 'EG-Staat'),
    # unknown nouns
    (('US-Präsidentenhaus', 'N'), 'US-Präsidentenhaus'),
    (('US-Präsidentenhäuser', 'N'), 'US-Präsidentenhaus'),
    (('EU-Neu-Delegierte', 'N'), 'EU-Neu-Delegierter'),
    (('Feinstaubbelastungen', 'N'), 'Feinstaubbelastung'),
    # known adjectives
    (('fies', 'ADJ'), 'fies'),
    (('besser', 'ADJ'), 'gut'),
    (('schöne', 'ADJ'), 'schön'),
    # unknown adjectives
    (('unbeschreibliches', 'ADJ'), 'unbeschreiblich'),
    (('klagloser', 'ADJ'), 'klaglos'),
    # capitalize nouns
    (('Abgeordneten', 'NN'), 'Abgeordneter'),
    (('xyz123', 'N'), 'Xyz123'),
    # nonsense
    (('-EU-Delegierte', 'N'), '-EU-Delegierter'),
    (('EU-Delegierte-', 'N'), 'EU-Delegierte-'),
    (('Xyz123', 'N'), 'Xyz123'),
    (('', 'ADV'), ''),
)


def test_find_lemma():
    for test, expected in test_table:
        assert lemmatizer.find_lemma(*test) == expected


def test_find_lemma_exceptions():
    with pytest.raises(ValueError):
        lemmatizer.find_lemma('Der', 'DET')
