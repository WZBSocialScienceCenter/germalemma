"""
Evaluate results of GermaLemma using data in eval_table/eval_table_lemmata.csv.

Markus Konrad <markus.konrad@wzb.eu>, Wissenschaftszentrum Berlin für Sozialforschung
January 2019
"""

from math import sqrt

import pandas as pd
from pattern.de import singularize, conjugate, predicative

pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 140)

from germalemma import GermaLemma


def lemma_via_patternlib(token, pos):
    if pos == 'NP':  # singularize noun
        return singularize(token)
    elif pos.startswith('V'):  # get infinitive of verb
        return conjugate(token)
    elif pos.startswith('ADJ') or pos.startswith('ADV'):  # get baseform of adjective or adverb
        return predicative(token)

    return token


def get_mean_and_ci(series):
    match_mean = series.mean()
    match_sd = series.std()
    match_se = match_sd / sqrt(len(eval_df))
    ci_upper = match_mean + 1.96 * match_se
    ci_lower = match_mean - 1.96 * match_se

    return match_mean * 100, ci_lower * 100, ci_upper * 100


print("loading data...")

eval_df = pd.read_csv('eval_table/eval_table_lemmata.csv')
eval_df = eval_df.loc[~eval_df.lemma.isna(), :]

print('loaded %d rows' % len(eval_df))

lemmatizer = GermaLemma()

eval_df['germalemma'] = eval_df.apply(lambda row: lemmatizer.find_lemma(row[3], row[2]), axis=1)

eval_df['match'] = eval_df.lemma == eval_df.germalemma
eval_df.head()

print('wrong lemmata:')
print(eval_df.loc[~eval_df.match, ['token', 'pos', 'lemma', 'germalemma']])

match_mean, ci_lower, ci_upper = get_mean_and_ci(eval_df.match)

print('Success rate for germalemma: %.2f%% (95%% CI: [%.2f%%, %.2f%%])' % (match_mean, ci_lower, ci_upper))

eval_df['pattern'] = eval_df.apply(lambda row: lemma_via_patternlib(row[3], row[2]), axis=1)
eval_df['match_pattern'] = eval_df.lemma == eval_df.pattern
eval_df.head()

match_mean, ci_lower, ci_upper = get_mean_and_ci(eval_df.match_pattern)

print('Success rate for pattern only: %.2f%% (95%% CI: [%.2f%%, %.2f%%])' % (match_mean, ci_lower, ci_upper))

