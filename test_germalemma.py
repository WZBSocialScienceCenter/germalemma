from germalemma import GermaLemma

lemmatizer = GermaLemma("data/tiger_release_aug07.corrected.16012013.conll09")


def test_find_lemma_known():
    assert lemmatizer.find_lemma(u'US-Präsident', 'N') == 'US-Präsident'
    assert lemmatizer.find_lemma(u'US-Präsidenten', 'N') == 'US-Präsident'


def test_find_lemma_unknown():
    assert lemmatizer.find_lemma(u'US-Präsidentenhaus', 'N') == 'US-Präsidentenhaus'
    assert lemmatizer.find_lemma(u'US-Präsidentenhäuser', 'N') == 'US-Präsidentenhaus'


def test_find_lemma_nonsense():
    assert lemmatizer.find_lemma(u'xyz123', 'N') == 'xyz123'
