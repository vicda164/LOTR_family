# LOTR_family
Using NLP to extract family trees from J.R.R.Tolkien's univers.

## Install

requirements:
python 3.6
plac
numpy
spacy
networkx
matplotlib

Run: 'python -m spacy download en'
To get language model.

## Usage

usage: main.py [-h] [-r] [-v] [-d] [-f] name

positional arguments:
  name                 Character name

optional arguments:
  -h, --help           show this help message and exit
  -r, --disbale-cache  Delete family tree from root name Name
  -v, --validate       Validate
  -d, --draw           Draw graph
  -f, --fetchall       Fetch all character desciptions of names in
                       kaggle_data/Characters

