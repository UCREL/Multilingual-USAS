# POS tagset mappers

This folder contains POS tagset mappers, whereby it maps a POS tag from one tagset to another tagset. All pos tagset mappers are either a one to one mapping, or many to one mapping. All files will be in JSON format and the mapping will be a dictionary like object. Below is a list of the POS tagset mappers in this folder and a brief description of what tagset they map from and to and what type of mapping it is:

* [Finnish_pos_mapper.json](./Finnish_pos_mapper.json) - Maps from an unknown tagset to the USAS core POS tagset. It is a many to one mapping. The unknown tagset is used within the non-mapped Finnish semantic lexicon files; [semantic_lexicon_fin.tsv](../Finnish/semantic_lexicon_fin.tsv) and [semantic_lexicon_fin.txt](../Finnish/semantic_lexicon_fin.txt).


**Note** these mappings are very similar to the POS mappers within the [PyMUSAS repository](https://github.com/UCREL/pymusas/blob/main/pymusas/pos_mapper.py), the main difference is that in this repository we do not allow one to many mappings.