import argparse
from pathlib import Path
import csv
from typing import Set
import json

if __name__ == '__main__':
    description = '''
    Tests for single word lexicon files if the `token` and `lemma` values per 
    row/line are equal. Will output to stdout a JSON object for each 
    line that contains a different `token` and `lemma` value. An example of the 
    JSON object is shown below:

    {"token": "A.E", "lemma": "A.E.", "row index": 0}
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('lexicon_file_path', type=Path, 
                        help='File path to the single word lexicon file to check')
    args = parser.parse_args()

    lexicon_collection_file = args.lexicon_file_path
    with lexicon_collection_file.open('r', newline='') as lexicon_data:
        csv_reader = csv.DictReader(lexicon_data, delimiter='\t')
        file_field_names: Set[str] = set()

        for row_index, row in enumerate(csv_reader):
            
            if row['token'] != row['lemma']:
                output_dict = {'token': row['token'], 'lemma': row['lemma'], 
                               'row index': row_index}
                print(json.dumps(output_dict))
            