import json
import csv
from pathlib import Path
import argparse


def string_to_path(string_argument: str) -> Path:
    return Path(string_argument).resolve()


if __name__ == '__main__':
    description = '''
    Converts a TSV file into a JSON file.
    
    The TSV file is expected to have only two fields/columns whereby the first
    and second fields represent the keys and values that will be added to the
    dictionary object that will be saved to the given JSON file. 
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('tsv_file', type=string_to_path)
    parser.add_argument('output_json_file', type=string_to_path)
    args = parser.parse_args()

    tsv_file = args.tsv_file
    output_json_file = args.output_json_file

    with tsv_file.open('r', encoding='utf-8', newline='') as tsv_fp:
        tsv_reader = csv.reader(tsv_fp, delimiter='\t')
        with output_json_file.open('w', encoding='utf-8') as output_json_fp:
            pos_mapping = {}
            for line_index, value in enumerate(tsv_reader):
                if line_index == 0:
                    continue
                if len(value) != 2:
                    raise ValueError('Line should only contain two fields and '
                                     f'not {len(value)}. Line index {line_index}'
                                     f', line contains: {value}')
                if value[0] in pos_mapping:
                    raise KeyError(f'This POS tag already has a mapping: {value[0]}')
                pos_mapping[value[0]] = value[1]
            json.dump(pos_mapping, output_json_fp)