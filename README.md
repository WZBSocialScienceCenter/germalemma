# GermaLemma

April/Mai 2017, Markus Konrad <markus.konrad@wzb.eu> / [Berlin Social Science Center](https://www.wzb.eu/en)

## A Lemmatizer for German language text

In order to use GermaLemma, you will need to install some additional packages (see *Requirements* section below) and then download the [TIGER corpus from the University of Stuttgart](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger.html). You will need to use the CONLL09 format, *not* the XML format.
The corpus is free to use for non-commercial purposes (see [License Agreement](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/TIGERCorpus/license/htmlicense.html)).

Then, you should convert the corpus into pickle format for faster loading by executing *germalemma.py* and passing the path to the corpus file in CONLL09 format:

```
python germalemma.py tiger_release_[...].conll09
```

This will place a lemmata.pickle file in the "data" directory which is then automatically loaded.

## Part-of-Speech (POS) Tagging

You will need to apply [Part-of-Speech (POS) tagging](https://en.wikipedia.org/wiki/Part-of-speech_tagging) to your text before you can lemmatize its words. See [this blog post](https://datascience.blog.wzb.eu/2016/07/13/accurate-part-of-speech-tagging-of-german-texts-with-nltk/) on how to do that.

## Usage

You have set up GermaLemma to use the TIGER corpus (as explained above). You have tokenized your text (e.g. with NLTK). You have POS-tagged your tokens. Now you can use GermaLemma:

```python
from germalemma import GermaLemma

lemmatizer = GermaLemma()

# passing the word and the POS tag ("N" for noun)
lemma = lemmatizer.find_lemma(u'Feinstaubbelastungen', u'N')
print(lemma)
# -> lemma is "Feinstaubbelastung"
```

## Valid POS tags

You can pass POS tags from the [STTS tagset](http://www.ims.uni-stuttgart.de/forschung/ressourcen/lexika/TagSets/stts-table.html), however, only four POS tags can be processed:

* 'N...' (nouns)
* 'V...' (verbs)
* 'ADJ...' (adjectives)
* 'ADV...' (adverbs)

All other POS tags will result in a `ValueError` so you should wrap the call to `find_lemma` in a *try-except block*.

## Accuracy

Using 90% of the TIGER corpus as lemmata dictionary and the remaining 10% as test data, GermaLemma finds out the correct lemma for about **~84%** of all nouns, verbs, adjectives and adverbs, **when the [*Pattern*](http://www.clips.ua.ac.be/pattern) package is installed**. Without *Pattern*, about **71%** accuracy can be achieved. Run `evaluate_germalemma.py` to see the exact results and see [this blog post](https://datascience.blog.wzb.eu/2017/05/19/lemmatization-of-german-language-text/) for more information.

## Requirements

* Python 2.7 or Python 3.x
* required package [*Pyphen*](http://pyphen.org/)
* optional package [*Pattern*](http://www.clips.ua.ac.be/pattern) (This package is only available for Python 2.x but improves the accuracy from ~71% to ~84%)

## License

Apache License 2.0. See *LICENSE* file.

The TIGER corpus is **not** part of this repository and has to be downloaded separately under separate license conditions.
