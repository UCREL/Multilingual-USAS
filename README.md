# Multilingual-USAS

Lexicons for the Multilingual UCREL Semantic Analysis System 

<hr/>

<p align="center">
    <a href="https://github.com/UCREL/Multilingual-USAS/actions/workflows/ci.yml">
        <img alt="CI" src="https://github.com/UCREL/Multilingual-USAS/actions/workflows/ci.yml/badge.svg?branch=master&event=push"/>
    </a>
    <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
        <img alt="License" src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg" />
    </a>
</p>

## Introduction

The UCREL semantic analysis system (USAS) is a framework for undertaking the automatic semantic analysis of text. The framework has been designed and used across a number of research projects since 1990.

The USAS framework initially in English is being extended to other languages. **This repository houses the lexicons and tagsets for the non-English versions of the USAS tagger.**


For more details about the USAS tagger, see our website: [http://ucrel.lancs.ac.uk/usas/](http://ucrel.lancs.ac.uk/usas/). Others collaborating on multilingual lexicon development are listed on this site.

## USAS Lexicon Resources Overview

This section will detail the USAS lexicon resources we have in this repository per language, in addition we have a machine readable JSON file, [./language_resources.json](./language_resources.json), that contains all of the relevant meta data to allow for easier processing of these lexicon resources.

### USAS Lexicon Statistics

The table summarising the lexicon data statistics can be found in the [./lexicon_statistics.md markdown file](./lexicon_statistics.md), each row in the table reports the statistics for one lexicon file in this repository, of which each language can have multiple lexicon files. The lexicon file can either be a **single** or **Multi Word Expression (MWE)** lexicon file, the format of these lexicon files are explained in more detail in the [lexicon file format section below.](#lexicon-file-format)

The table within [./lexicon_statistics.md markdown file](./lexicon_statistics.md) was automatically generated using the following command within the [CI GitHub Action](./.github/workflows/ci.yml):

``` bash
python lexicon_statistics.py > ./lexicon_statistics.md
```

### USAS Lexicon Meta Data

The [./language_resources.json](./language_resources.json) is a JSON file that contains meta data on what each lexicon resource file contains in this repository per language. The structure of the JSON file is the following:
``` JSON
{
  "Language one BCP 47 code": {
    "resources": [
      {
        "data type": "single",
        "file path": "FILE PATH"
      },
      {
        "data type": "pos",
        "file path": "FILE PATH"
      }
    ],
    "language data": {
      "description": "LANANGUAGE NAME",
      "macrolanguage": "Macrolanguage code",
      "script": "ISO 15924 script code"
    }
  },
  "Language two BCP 47 code": : {
    "resources": [
      {
        "data type": "mwe",
        "file path": "FILE PATH"
      },
    ],
    "language data": {
      "description": "LANANGUAGE NAME",
      "macrolanguage": "Macrolanguage code",
      "script": "ISO 15924 script code"
    }
  },
  ...
}
```

* The [BCP 47 code](https://www.w3.org/International/articles/language-tags/) of the language, the [BCP47 language subtag lookup tool](https://r12a.github.io/app-subtags/) is a great tool to use to find a BCP 47 code for a language.
  * `resources` - this is a list of resource files that are associated with the given language. There is no limit on the number of resources files associated with a language.
    * `data type` value can be 1 of 3 values:
      1. `single` - The `file path` value has to be of the **single word lexicon** file format as described in the [Lexicon File Format section](#lexicon-file-format).
      2. `mwe` - The `file path` value has to be of the **Multi Word Expression lexicon** file format as described in the [Lexicon File Format section](#lexicon-file-format).
      3. `pos` - The `file path` value has to be of the **POS tagset** file format as described in the [POS Tagset File Format section].
    * `file path` - value is always relative to the root of this repository, and the file is in the format specified by the associated `data type`.
  * `language data` - this is data that is associated with the `BCP 47` language code. To some degree this is redundant as we can look this data up through the `BCP 47` code, however we thought it is better to have it in the meta data for easy lookup. All of this data can be easily found through looking up the `BCP 47` language code in the [BCP47 language subtag lookup tool](https://r12a.github.io/app-subtags/)
    * `description` - The `description` of the language code.
    * `macrolanguage` - The macrolanguage tag, **note** if this does not exist then give the [primary language tag](https://www.w3.org/International/articles/language-tags/#language), which could be the same as the whole `BCP 47` code. The `macrolanguage` tag could be useful in future for grouping languages.
    * `script` - The [ISO 15924 script code](https://www.w3.org/International/articles/language-tags/#script) of the language code. The `BCP 47` code by default does not always include the script of the language as the default script for that language is assumed, therefore this data is here to make the default more explicit.

Below is an extract of the [./language_resources.json](./language_resources.json), to give as an example of this JSON structure:

``` JSON
{
    "arb": {
        "resources": [
            {
                "data type": "single",
                "file path": "./Arabic/semantic_lexicon_arabic.tsv"
            }
        ],
        "language data": {
            "description": "Standard Arabic",
            "macrolanguage": "ar",
            "script": "Arab"
        }
    },
    "cmn": {
        "resources":[
            {
                "data type": "single", 
                "file path": "./Chinese/semantic_lexicon_chi.tsv"
            }, 
            {
                "data type": "mwe", 
                "file path": "./Chinese/mwe-chi.tsv"
            }, 
            {
                "data type": "pos", 
                "file path": "./Chinese/simplified-pos-tagset-chi.txt"
            }
        ],
        "language data": {
            "description": "Mandarin Chinese",
            "macrolanguage": "zh",
            "script": "Hani"
        }
    },
    ...
}
```

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

#### Special cases

##### Implicit POS

If you are writing a lexicon which contains POS information, but you come across a token/lemma that can be a member of any POS tagset, e.g. the POS information would not help in disambiguating it, then assign it the POS value `*` which represents the wildcard.

Example of a single word lexicon with this implicit POS information:

``` tsv
lemma	token	pos	semantic_tags
Austin	Austin	Noun	Z1 Z2
car	cars	Noun	Z0 Z3
computer	computer	*	Z1
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

## Scripts

### Text to TSV

This is used within the [CI GitHub action](./.github/workflows/ci.yml):

1. Converts all lexicon files (single and MWE) from text file format to TSV. The lexicon files are found through the meta data file (language_resources.json).
2. Checks that the TSV files are formatted correctly:
    1. The minimum header names exist, 
    2. All fields/columns have a header name,
    3. All lines contain the minimum information e.g. no comment lines exist in the middle of the file.

### Test All File Formats

The [test_all_collections.py script](test_all_collections.py) uses the [test_collection.py script](./test_collection.py) that was explained in the [test file format section](#test-file-format) to test all of the single and multi word expression lexicon files within this repository to ensure that they conform to the file format specified in [the Lexicon File Format section](#lexicon-file-format). The script takes no arguments as it uses the [./language_resources.json](./language_resources.json), which is explained in [USAS Lexicon Meta Data section](#usas-lexicon-meta-data).

``` bash
python test_all_collections.py
```

### Test file format

To test that a lexicon collection conforms to the file format specified in [the Lexicon File Format section](#lexicon-file-format) you can use the [test_collection.py python script.](./test_collection.py). The script takes two arguments:

1. The path to the lexicon file you want to check.
2. Whether the lexicon file is a single word lexicon (`single`) or a Multi Word Expression lexicon (`mwe`).

Example for a single word lexicon:

``` bash
python test_collection.py Welsh/semantic_lexicon_cy.tsv single
```

Example for a Multi Word Expression lexicon:

``` bash
python test_collection.py Welsh/mwe-welsh.tsv mwe
```

The script tests the following:

1. The minimum header names exist.
2. All fields/columns have a header name.
3. All lines contain the minimum information e.g. no comment lines exist in the middle of the file.

### Lexicon Statistics

This generates the lexicon statistics table, as show in [USAS Lexicon Statistics section](#usas-lexicon-statistics), it does not take an arguments, but uses the [./language_resources.json](./language_resources.json) file, of which this meta data file is best explained in [USAS Lexicon Meta Data section](#usas-lexicon-meta-data).

Example:

``` bash
python lexicon_statistics.py
```

### Remove column

Given a Lexicon file path will remove the column with the given header name, and save the rest of the data from the Lexicon to the new lexicon file path. The script takes three arguments:

1. The path to the existing lexicon file.
2. The path to save the new lexicon file too, this lexicon will be the same as argument 1, but with the removal of the column with the given header name.
3. The header name for the column that will be removed.

Example:

``` bash
python remove_column.py Malay/semantic_lexicon_ms.tsv Malay/new.tsv pos
```

### Test token is equal to lemma

Tests for single word lexicon files if the `token` and `lemma` values per row/line are equal. Will output to stdout a JSON object for each line that contains a different `token` and `lemma` value. An example of the JSON object is shown below:

``` json
{"token": "A.E", "lemma": "A.E.", "row index": 0}
```

Example:

``` bash
python test_token_is_equal_to_lemma.py SINGLE_WORD_LEXICON_FILE_PATH
```

### Unique column values

Given a header name and a lexicon file path, it will output to stdout all of the unique values and how often they occur from that header's column from the given lexicon file.

Examples:

``` bash
python column_unique_values.py French/semantic_lexicon_fr.tsv pos
# Output:
Unique values for the header pos
Value: prep Count: 60
Value: noun Count: 1633
Value: adv Count: 147
Value: verb Count: 448
Value: adj Count: 264
Value: det Count: 86
Value: pron Count: 56
Value: conj Count: 20
Value: null Count: 2
Value: intj Count: 8
```

``` bash
python column_unique_values.py Welsh/mwe-welsh.tsv semantic_tags
# Output:
Unique values for the header semantic_tags
Value: G1.1 Count: 1
Value: Z1 Count: 1
Value: M3/Q1.2 Count: 3
Value: Q2.1 Count: 1
Value: I2.1/T2+ Count: 1
Value: P1/G1.1 G1.2 Count: 2
Value: A9- Count: 2
Value: Z2 Count: 1
Value: Y2 Count: 1
Value: X5.1+ Count: 1
```

### Compare header values between two files

Write to stdout the following:
    
1. Number of unique values in the column with `header_name_1` from `lexicon_file_path_1`
2. Number of unique values in the column with `header_name_1` from `lexicon_file_path_1`
3. Number of unique values in common between the two files.

Example:

``` bash
python compare_headers_between_lexicons.py Russian/semantic_lexicon_rus.tsv Russian/semantic_lexicon_rus_names.tsv lemma lemma
# Output
Number of unique values in lexicon file 1 17396
Number of unique values in lexicon file 2 7637
Number of unique values in common between the two files:3169
```

### Create Pos Tagsets

The script creates a POS tagset per language stated within the [./language_resources.json](./language_resources.json) meta data file, which is explained in the [USAS Lexicon Meta Data section](#usas-lexicon-meta-data), and creates a POS tagset based on the POS tags used within the language's single and MWE semantic lexicon files. The POS tagset generated is then saved within each language's folder under the file name `generated_pos_tagset.tsv`. Each generated tagset has two fields `POS`, and `Count`, the `POS` field represents the POS tags, and the `Count` represents the number of times the associated tag has been used within the language's lexicon file(s). An example of this generated POS tagset is shown below, taken from the Welsh language folder:

``` tsv
POS	Count
verb	130197
adv	123
art	7
conj	87
pron	67
prep	293
noun	4358
pnoun	6572
adj	1542
fw	40
num	36
intj	6
*	2
```

To run this script:

``` bash
python create_pos_tagsets.py
```

### Python Requirements

This has been tested with Python >= `3.7`, to install the relevant python requirements:

``` bash
pip install -r requirements.txt
```

## Citation

In order to reference this further development of the multilingual USAS tagger, please cite our [paper at NAACL-HLT 2015](https://aclanthology.org/N15-1137/), which described our bootstrapping approach: 

APA Format:
```
Piao, S. S., Bianchi, F., Dayrell, C., D’egidio, A., & Rayson, P. (2015). Development of the multilingual semantic annotation system. In Proceedings of the 2015 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (pp. 1268-1274).
```

BibTeX Format:
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

APA Format:
```
Piao, S. S., Rayson, P., Archer, D., Bianchi, F., Dayrell, C., El-Haj, M., Jiménez, R-M., Knight, D., Křen, M., Lofberg, L., Nawab, R. M. A., Shafi, J., Teh, P. L., & Mudraya, O. (2016). Lexical coverage evaluation of large-scale multilingual semantic lexicons for twelve languages. In Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC'16) (pp. 2614-2619).
```

BibTeX Format:
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

If you are interested in getting involved in creating lexicons for new languages or updating the existing ones then please get in touch with: Paul Rayson (p.rayson@lancaster.ac.uk) and/or the UCREL Research Centre (ucrel@lancaster.ac.uk) at Lancaster University.

## License

This work is licensed under a 
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative 
Commons Attribution-NonCommercial-ShareAlike 4.0 International 
License</a>.
