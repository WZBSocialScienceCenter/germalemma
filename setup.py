"""
geovoronoi setuptools based setup module
"""

from setuptools import setup

import germalemma

GITHUB_URL = 'https://github.com/WZBSocialScienceCenter/germalemma'

setup(
    name=germalemma.__title__,
    version=germalemma.__version__,
    description='A lemmatizer for German language text.',
    long_description="""Germalemma lemmatizes Part-of-Speech-tagged German language words. To do so, it combines a large lemma dictionary (an excerpt of the TIGER corpus from the University of Stuttgart), functions from the CLiPS "Pattern" package, and an algorithm to split composita.""",
    url=GITHUB_URL,
    project_urls={
        'Source': GITHUB_URL,
        'Tracker': GITHUB_URL + '/issues',
    },
    author='Markus Konrad',
    author_email='markus.konrad@wzb.eu',

    license='Apache 2.0',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',

        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],

    keywords='text lemmatization normalization textmining textanalysis mining preprocessing',

    py_modules=['germalemma'],
    data_files=[('data', ['data/lemmata.pickle'])],
    python_requires='>=3.4',
    install_requires=['Pattern>=3.6', 'Pyphen>=0.9.5']
)
