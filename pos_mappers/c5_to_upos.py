import argparse
import json
from pathlib import Path


def string_to_path(string_argument: str) -> Path:
    return Path(string_argument).resolve()


C5_TO_UPOS = {
   "AJ0": "ADJ",
   "AJC": "ADJ",
   "AJS": "ADJ",
   "AT0": "DET",
   "AV0": "ADV",
   "AVP": "ADV",
   "AVQ": "ADV",
   "CJC": "CCONJ",
   "CJS": "SCONJ",
   "CJT": "SCONJ",
   "CRD": "NUM",
   "DPS": "DET",
   "DT0": "DET",
   "DTQ": "DET",
   "EX0": "PRON",
   "ITJ": "INTJ",
   "NN0": "NOUN",
   "NN1": "NOUN",
   "NN2": "NOUN",
   "NP0": "PROPN",
   "ORD": "ADJ",
   "PNI": "PRON",
   "PNP": "PRON",
   "PNQ": "PRON",
   "PNX": "PRON",
   "POS": "PART",
   "PRF": "ADP",
   "PRP": "ADP",
   "PUL": "PUNCT",
   "PUN": "PUNCT",
   "PUQ": "PUNCT",
   "PUR": "PUNCT",
   "SENT": "PUNCT",
   "TO0": "PART",
   "VBB": "VERB",
   "VBD": "VERB",
   "VBG": "VERB",
   "VBI": "VERB",
   "VBN": "VERB",
   "VBZ": "VERB",
   "VDB": "VERB",
   "VDD": "VERB",
   "VDG": "VERB",
   "VDI": "VERB",
   "VDN": "VERB",
   "VDZ": "VERB",
   "VHB": "VERB",
   "VHD": "VERB",
   "VHG": "VERB",
   "VHI": "VERB",
   "VHN": "VERB",
   "VHZ": "VERB",
   "VM0": "AUX",
   "VVB": "VERB",
   "VVD": "VERB",
   "VVG": "VERB",
   "VVI": "VERB",
   "VVN": "VERB",
   "VVZ": "VERB",
   "XX0": "PART",
   "ZZ0": "SYM",
   "UNC": "X",
   "NULL": "X"
   }


if __name__ == '__main__':
    description = '''
    Creates a JSON formatted C5 to UPOS mapping. Whereby the mapping has come
    from the following Python script, except for the tags "UNC" and "NULL":
    https://github.com/COST-ELTeC/Scripts/blob/fa8083e4ea47280e7c18e41536d3fbb4014a6e6d/posPipe/udpMap.py#L45
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('output_file_path', type=string_to_path)
    args = parser.parse_args()
    with args.output_file_path.open('w', encoding='utf-8') as output_fp:
        json.dump(C5_TO_UPOS, output_fp)
