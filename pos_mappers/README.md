# POS tagset mappers

This folder contains POS tagset mappers, whereby it maps a POS tag from one tagset to another tagset. All pos tagset mappers are either a one to one mapping, or many to one mapping. All files will be in JSON format and the mapping will be a dictionary like object. Below is a list of the POS tagset mappers in this folder and a brief description of what tagset they map from and to and what type of mapping it is:

* [Finnish_pos_mapper.json](./Finnish_pos_mapper.json) - Maps from an unknown tagset to the USAS core POS tagset. It is a many to one mapping. The unknown tagset is used within the non-mapped Finnish semantic lexicon files; [semantic_lexicon_fin.tsv](../Finnish/semantic_lexicon_fin.tsv) and [semantic_lexicon_fin.txt](../Finnish/semantic_lexicon_fin.txt).
* [c7_to_c5.json](./c7_to_c5.json) - Maps from the [CLAWS C7 tagset](https://ucrel.lancs.ac.uk/claws7tags.html) to the [CLAWS C5 tagset](https://ucrel.lancs.ac.uk/claws5tags.html). It is a many to one mapping. The tagset was generated using the [c7_to_c5_txt_to_json.py script.](./c7_to_c5_txt_to_json.py)
* [c5_to_upos.json](./c5_to_upos.json) - Maps from the [CLAWS C5 tagset](https://ucrel.lancs.ac.uk/claws5tags.html) to the [Universal Part Of Speech (UPOS) tagset](https://universaldependencies.org/u/pos/). It is a many to one mapping. The tagset was generated using the [c5_to_upos.py script.](./c5_to_upos.py).
* [c7_to_upos.json](./c7_to_upos.json) - Maps from the [CLAWS C7 tagset](https://ucrel.lancs.ac.uk/claws7tags.html) to the [UPOS tagset](https://universaldependencies.org/u/pos/). It is a many to one mapping. The tagset was generated using the [c7_to_upos.py script.](./c7_to_upos.py).
* [mwe_c7_to_upos.json](./mwe_c7_to_upos.json) - Maps from the [CLAWS C7 tagset](https://ucrel.lancs.ac.uk/claws7tags.html) to the [UPOS tagset](https://universaldependencies.org/u/pos/). **Compared too** [c7_to_upos.json](./c7_to_upos.json) this tagset contains a lot special syntax on the C7 tags that maps to the UPOS, e.g. `NP*`: `PROPN` and can be used to map all of the CLAWS C7 tags in the MWE file to UPOS.


**Note** these mappings are very similar to the POS mappers within the [PyMUSAS repository](https://github.com/UCREL/pymusas/blob/main/pymusas/pos_mapper.py), the main difference is that in this repository we do not allow one to many mappings.


## Python Scripts

### c7_to_c5_txt_to_json

Converts the `mapC7toC5.txt` file, which can be found [here](https://ucrel.lancs.ac.uk/claws/mapC7toC5.txt), from a tab separated list of C7 to C5 CLAWS tags to a dictionary object that is saved in JSON format to the specified output file, in this example case the JSON file is called `c7_to_c5.json`.

Example:

``` bash
python c7_to_c5_txt_to_json.py mapC7toC5.txt c7_to_c5.json
```

### c5_to_upos.py

Creates a JSON formatted C5 to UPOS mapping. Whereby the mapping has come from the following [Python script](https://github.com/COST-ELTeC/Scripts/blob/fa8083e4ea47280e7c18e41536d3fbb4014a6e6d/posPipe/udpMap.py#L45), except for the tags "UNC" and "NULL". The example below creates the JSON formatted C5 to UPOS mapping to the file called `c5_to_upos.json`.

Example:

``` bash
python c5_to_upos.py c5_to_upos.json
```

### c7_to_upos.py

**Note** a C7 tag that is not in the [C7 tagset](https://ucrel.lancs.ac.uk/claws7tags.html), but is in the English single word lexicon is the tag `PUNC`, this is manually added to the C7 to UPOS JSON mapping with the mapping of `PUNC` to the UPOS tag `PUNCT`.

Based on the two pervious scripts listed, [c7_to_c5_txt_to_json](./c7_to_c5_txt_to_json.py) and [c5_to_upos.py](./c5_to_upos.py), this script creates a C7 to UPOS JSON formatted mapping. In the example below the script uses the two existing mappings, [c7_to_c5.json](./c7_to_c5.json) and [c5_to_upos.json](./c5_to_upos.json), to create the C7 to UPOS JSON formatted mapping file called `c7_to_upos.json`.

Example:

``` bash
python c7_to_upos.py c7_to_c5.json c5_to_upos.json c7_to_upos.json
```

### JSON to TSV

Converts a JSON file into a TSV file. The JSON file is expected to be a simple dictionary object of key and value pairs whereby this will be converted into TSV format such that keys and values are in separated fields/columns.

``` bash
python json_to_tsv.py c7_to_upos.json c7_to_upos.tsv
```

The `c7_to_upos.tsv` file will look like the following:

``` tsv
!	PUNCT
""""	PUNCT
(	PUNCT
)	PUNCT
,	PUNCT
-	PUNCT
...
```


### TSV to JSON

Converts a TSV file into a JSON file. The TSV file is expected to have only two fields/columns whereby the first and second fields represent the keys and values that will be added to the dictionary object that will be saved to the given JSON file. 

``` bash
python tsv_to_json.py c7_to_upos.tsv c7_to_upos.json
```

The `c7_to_upos.json` file will look like the following:

``` json
{
    "!": "PUNCT",
    "\"": "PUNCT",
    "(": "PUNCT",
    ")": "PUNCT",
    ",": "PUNCT",
    "-": "PUNCT",
    ...
}
```

