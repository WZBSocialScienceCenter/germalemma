"""
geovoronoi setuptools based setup module
"""

import os

from setuptools import setup

import germalemma

GITHUB_URL = 'https://github.com/WZBSocialScienceCenter/germalemma'

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=germalemma.__title__,
    version=germalemma.__version__,
    description='A lemmatizer for German language text.',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],

    keywords='text lemmatization normalization textmining textanalysis mining preprocessing',

    py_modules=['germalemma'],
    data_files=[('data', ['data/lemmata.pickle'])],
    python_requires='>=3.6',
    install_requires=['PatternLite>=3.6', 'Pyphen>=0.9.5']
)
