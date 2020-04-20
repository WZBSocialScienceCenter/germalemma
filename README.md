# GermaLemma

December 2019, Markus Konrad <markus.konrad@wzb.eu> / [Berlin Social Science Center](https://www.wzb.eu/en)

## A lemmatizer for German language text

Germalemma lemmatizes Part-of-Speech-tagged German language words. To do so, it combines a large lemma dictionary (an excerpt of the [TIGER corpus from the University of Stuttgart](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger.html)), functions from the CLiPS "Pattern" package, and an algorithm to split composita.

## Installation

### Easy option: Installing from PyPI via `pip`

You can install the package from [PyPI](https://pypi.org/project/germalemma/) via `pip`:

```
pip install -U germalemma
```

### Downloading and installing from source

In order to use GermaLemma, you will need to install some additional packages (see *Requirements* section below) and then download the [TIGER corpus from the University of Stuttgart](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger.html). You will need to use the CONLL09 format, *not* the XML format.
The corpus is free to use for non-commercial purposes (see [License Agreement](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/TIGERCorpus/license/htmlicense.html)).

Then, you should convert the corpus into pickle format for faster loading by executing *germalemma/__init__.py* and passing the path to the corpus file in CONLL09 format:

```
python germalemma/__init__.py tiger_release_[...].conll09
```

This will place a `lemmata.pickle` file in the `data` directory which is then automatically loaded.

## Part-of-Speech (POS) Tagging

You will need to apply [Part-of-Speech (POS) tagging](https://en.wikipedia.org/wiki/Part-of-speech_tagging) to your text before you can lemmatize its words. See [this blog post](https://datascience.blog.wzb.eu/2016/07/13/accurate-part-of-speech-tagging-of-german-texts-with-nltk/) on how to do that.

## Usage

You have set up GermaLemma to use the TIGER corpus (as explained above). You have tokenized your text (e.g. with NLTK). You have POS-tagged your tokens. Now you can use GermaLemma:

```python
from germalemma import GermaLemma

lemmatizer = GermaLemma()

# passing the word and the POS tag ("N" for noun)
lemma = lemmatizer.find_lemma('Feinstaubbelastungen', 'N')
print(lemma)
# -> lemma is "Feinstaubbelastung"
```

## Valid POS tags

You can pass POS tags from the [STTS tagset](http://www.ims.uni-stuttgart.de/forschung/ressourcen/lexika/TagSets/stts-table.html), however, only four POS tags can be processed:

* 'N...' (nouns)
* 'V...' (verbs)
* 'ADJ...' (adjectives)
* 'ADV...' (adverbs)

**All other POS tags will result in a `ValueError` so you should wrap the call to `find_lemma` in a *try-except block*.**

## Accuracy

GermaLemma's accuracy was evaluated using a sample of 696 POS tagged and manually lemmatized words from a sample of paragraphs from proceedings of the European Parliament, Goethe's "Werther", Kafka's "Verwandlung" and a news article from the website of the WZB (see samples in folder "eval_texts").

**Under the assumption that the POS tag is correct** (only those words were selected), GermaLemma finds the correct lemma in 99.43% of the cases. For comparison, *Pattern* achieved 95.11% for the same sample.

## Requirements

* Python 3.6 or newer
* required package [*Pyphen*](http://pyphen.org/)
* optional package [*PatternLite*](https://github.com/WZBSocialScienceCenter/patternlite) (This package is optional but highly recommended as it boosts the lemmatizer's accuracy.)

## License

Apache License 2.0. See *LICENSE* file.

The TIGER corpus is **not** part of this repository and has to be downloaded separately under separate license conditions.
