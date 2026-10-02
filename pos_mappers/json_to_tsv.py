import json
import csv
from pathlib import Path
import argparse


def string_to_path(string_argument: str) -> Path:
    return Path(string_argument).resolve()


if __name__ == '__main__':
    description = '''
    Converts a JSON file into a TSV file.
    
    The JSON file is expected to be a simple dictionary object of key and value
    pairs whereby this will be converted into TSV format such that keys and values
    are in separated fields/columns.
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('json_file', type=string_to_path)
    parser.add_argument('output_tsv_file', type=string_to_path)
    args = parser.parse_args()

    json_file = args.json_file
    output_tsv_file = args.output_tsv_file

    with json_file.open('r', encoding='utf-8') as json_fp:
        json_data = json.load(json_fp)
        with output_tsv_file.open('w', encoding='utf-8', newline='') as output_tsv_fp:
            tsv_writer = csv.writer(output_tsv_fp, delimiter='\t')
            for key, value in json_data.items():
                tsv_writer.writerow([key, value])