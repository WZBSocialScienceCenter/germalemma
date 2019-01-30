"""
Script that generates "eval_table/eval_table.csv" from text samples in folder "eval_texts". This table is later
used to manually add correct lemmata.

Markus Konrad <markus.konrad@wzb.eu>, Wissenschaftszentrum Berlin für Sozialforschung
January 2019
"""

import pandas as pd
from tmtoolkit.corpus import Corpus
from tmtoolkit.preprocess import TMPreproc

corpus = Corpus.from_folder('eval_texts')

preproc = TMPreproc(corpus.docs, language='german')

postagged = preproc.tokenize().pos_tag()
postagged = postagged.filter_for_pos({'N', 'V', 'ADJ', 'ADV'})

tok_pos_df = pd.DataFrame()
for doc_id, tok_pos in postagged.tokens_with_pos_tags.items():
    tok, pos = zip(*tok_pos)
    tok_pos_df = tok_pos_df.append(pd.DataFrame({
        'doc_id': doc_id,
        'token': tok,
        'pos': pos
    }), ignore_index=True)

tok_pos_df.drop_duplicates(['token', 'pos'], inplace=True)

tok_pos_df.to_csv('eval_table/eval_table.csv')
