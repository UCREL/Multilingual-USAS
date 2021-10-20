# Multilingual-USAS

Lexicons for the Multilingual UCREL Semantic Analysis System 

<hr/>

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Introduction

The UCREL semantic analysis system (USAS) is a framework for undertaking the automatic semantic analysis of text. The framework has been designed and used across a number of research projects since 1990.

The USAS framework initially in English is being extended to other languages. **This repository houses the lexicons and tagsets for the non-English versions of the USAS tagger.**


For more details about the USAS tagger, see our website: [http://ucrel.lancs.ac.uk/usas/](http://ucrel.lancs.ac.uk/usas/). Others collaborating on multilingual lexicon development are listed on this site.


## Lexicon File Format

All lexicon files are `tsv` formatted. There are two main type of file formats the **single word** and the **multi word expression (MWE)** lexicons. These two file formats can be easily distinguished in two ways:

1. The **MWE** files will always have the word **mwe** within the file name e.g. the Welsh MWE lexicon file name is called `mwe-welsh.tsv` and can be found at [./Welsh/mwe-welsh.tsv](./Welsh/mwe-welsh.tsv). Where as the **single word** lexicon files will never have the word **mwe** within it's file name.
2. The **MWE** files compared to the **single** word would typically only contain 2 headers:
    * `mwe_template`
    * `semantic_tags`

### Single word lexicon file format

These lexicons on each line will contain at minimum a lemma and a list of semantic tags associated to that lemma in rank order, whereby the most likely semantic tag is the first tag in white space separated list, an example of a line can be seen below:

``` tsv
Austin	Z1 Z2
```

In the example above we can see that for the lemma `Austin` the most likely semantic tag is `Z1`.

A full list of valid TSV headers and their expected value:

| Header name | Required | Value | Example |
| ------------|----------|-------|---------|
| `lemma`     | :heavy_check_mark: | The base/dictionary form of the `token`. See [Manning, Raghavan, and Schütze IR book for more details on lemmatization.](https://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html) | `car` |
| `semantic_tags` | :heavy_check_mark: | A list of semantic/USAS tags separated by whitespace, whereby the most likely semantic tag is the first tag in the list.| `Z0 Z3` |
| `pos` | :x: | Part Of Speech (POS) tag associated with the `lemma` and `token`. | `Noun` |
| `token` | :x: | The full word/token form of the `lemma`. | `cars` |

Example single word lexicon file:

``` tsv
lemma	token	pos	semantic_tags
Austin	Austin	Noun	Z1 Z2
car	cars	Noun	Z0 Z3
```

### Multi Word Expression (MWE) lexicon file format

These lexicons on each line will contain only a value for the `mwe_template` and the `semantic_tags`. The `semantic_tags` will contain the same information as the `semantic_tags` header for the single word lexicon data. The `mwe_template`, which is best described in the [The UCREL Semantic Analysis System paper (see Fig 3, called multiword templates in the paper)](https://www.lancaster.ac.uk/staff/rayson/publications/usas_lrec04ws.pdf), is a simplified pattern matching code, like a regular expression, that is used to capture MWEs that have similar structure. For example, `*_* Ocean_N*1` will capture `Pacific Ocean`, `Atlantic Ocean`, etc. The templates not only match continuous MWEs, but also match discontinuous ones. MWE templates allow other words to be embedded within them. For example, the set phrase `turn on` may occur as `turn it on`, `turn the light on`, `turn the TV on` etc. Using the template ` turn*_* {N*/P*/R*} on_RP ` we can identify this set phrase in various contexts. 

You will have noticed that these `mwe_templates` have the following pattern matching structure of `{token}_{pos} {token}_{pos}`, etc. In which each token and/or POS can have a wildcard applied to it, the wildcard means zero or more additional characters.

A full list of valid TSV headers and their expected value:

| Header name | Required | Value | Example |
| ------------|----------|-------|---------|
| `mwe_template`     | :heavy_check_mark: | See the description in the paragraphs above | `*_* Ocean_N*1` |
| `semantic_tags` | :heavy_check_mark: | A list of semantic/USAS tags separated by whitespace, whereby the most likely semantic tag is the first tag in the list.| `Z2 Z0` |

Example multi word expression lexicon file:

``` tsv
mwe_template	semantic_tags
turn*_* {N*/P*/R*} on_RP	A1 A1.6 W2
*_* Ocean_N*1	Z2 Z0
```

## Test File Format

To test that a lexicon collection conforms to the file format specified in [the Lexicon File Format section above](#lexicon-file-format) you can use the [test_collection.py python script.](./test_collection.py). The script takes two arguments:

1. The path to the lexicon file you want to check.
2. Wether the lexicon file is a single word lexicon (`single`) or a Multi Word Expression lexicon (`mwe`).

Example for a single word lexicon:

``` bash
python test_collection.py Welsh/semantic_lexicon_cy.tsv single
```

Example for a Multi Word Expression lexicon:

``` bash
python test_collection.py Welsh/mwe-welsh.tsv mwe
```

The script tests the following:

1. The minimum header names exist, 
2. All lines contain the minimum information e.g. no comment lines exist in the middle of the file.

### Python Requirements

This has been tested with Python >= `3.7`, does not require any pips, just pure Python.

## Citation

In order to reference this further development of the multilingual USAS tagger, please cite our [paper at NAACL-HLT 2015](https://aclanthology.org/N15-1137/), which described our bootstrapping approach: 

``` bibtex
@inproceedings{piao-etal-2015-development,
    title = "Development of the Multilingual Semantic Annotation System",
    author = "Piao, Scott  and
      Bianchi, Francesca  and
      Dayrell, Carmen  and
      D{'}Egidio, Angela  and
      Rayson, Paul",
    booktitle = "Proceedings of the 2015 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies",
    month = may # "{--}" # jun,
    year = "2015",
    address = "Denver, Colorado",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/N15-1137",
    doi = "10.3115/v1/N15-1137",
    pages = "1268--1274",
}
```

In 2015/16, we extended this initial approach to twelve languages and evaluated the coverage of these lexicons on multilingual corpora. Please cite our [LREC-2016 paper](https://aclanthology.org/L16-1416/):

``` bibtex
@inproceedings{piao-etal-2016-lexical,
    title = "Lexical Coverage Evaluation of Large-scale Multilingual Semantic Lexicons for Twelve Languages",
    author = {Piao, Scott  and
      Rayson, Paul  and
      Archer, Dawn  and
      Bianchi, Francesca  and
      Dayrell, Carmen  and
      El-Haj, Mahmoud  and
      Jim{\'e}nez, Ricardo-Mar{\'\i}a  and
      Knight, Dawn  and
      K{\v{r}}en, Michal  and
      L{\"o}fberg, Laura  and
      Nawab, Rao Muhammad Adeel  and
      Shafi, Jawad  and
      Teh, Phoey Lee  and
      Mudraya, Olga},
    booktitle = "Proceedings of the Tenth International Conference on Language Resources and Evaluation ({LREC}'16)",
    month = may,
    year = "2016",
    address = "Portoro{\v{z}}, Slovenia",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://aclanthology.org/L16-1416",
    pages = "2614--2619",
}
```

## Contact Information

If you are interested in getting involved in creating lexicons for new languages or updating the existing ones then please get in touch with: Paul Rayson (p.rayson@lancaster.ac.uk) and Scott Piao (s.piao@lancaster.ac.uk) at Lancaster University.

## License

This work is licensed under a 
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative 
Commons Attribution-NonCommercial-ShareAlike 4.0 International 
License</a>.