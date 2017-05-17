# -*- coding: utf-8

from germalemma import GermaLemma

lemmatizer = GermaLemma("data/tiger_release_aug07.corrected.16012013.conll09")


def test_find_lemma_known():
    assert lemmatizer.find_lemma(u'US-Präsident', 'N') == u'US-Präsident'
    assert lemmatizer.find_lemma(u'US-Präsidenten', 'N') == u'US-Präsident'


def test_find_lemma_unknown():
    assert lemmatizer.find_lemma(u'US-Präsidentenhaus', 'N') == u'US-Präsidentenhaus'
    assert lemmatizer.find_lemma(u'US-Präsidentenhäuser', 'N') == u'US-Präsidentenhaus'


def test_find_lemma_nonsense():
    assert lemmatizer.find_lemma(u'xyz123', 'N') == u'xyz123'
