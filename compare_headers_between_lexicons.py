import argparse
from pathlib import Path
import csv
from typing import TextIO, Set

def get_header_values(header_name: str, lexicon_fp: TextIO) -> Set[str]:
    csv_reader = csv.DictReader(lexicon_fp, delimiter='\t')
    header_values = set()
    for row in csv_reader:
        header_values.add(row[header_name])
    return header_values

if __name__ == '__main__':
    description = '''
    Write to stdout the following:
    
    1. Number of unique values in the column with `header_name_1` from `lexicon_file_path_1`
    2. Number of unique values in the column with `header_name_1` from `lexicon_file_path_1`
    3. Number of unique values in common between the two files.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('lexicon_file_path_1', type=Path, 
                        help='File path to a lexicon file')
    parser.add_argument('lexicon_file_path_2', type=Path, 
                        help='File path to a lexicon file')
    parser.add_argument('header_name_1', type=str, 
                        help='Header name for values to be compared from lexicon file path 1')
    parser.add_argument('header_name_2', type=str, 
                        help='Header name for values to be compared from lexicon file path 2')
    args = parser.parse_args()

    lexicon_file_path_1 = args.lexicon_file_path_1
    lexicon_file_path_2 = args.lexicon_file_path_2

    header_name_1 = args.header_name_1
    header_name_2 = args.header_name_2
    with lexicon_file_path_1.open('r', newline='') as lexicon_data_1:
        with lexicon_file_path_2.open('r', newline='') as lexicon_data_2:
            lexicon_values_1 = get_header_values(header_name_1, lexicon_data_1)
            lexicon_values_2 = get_header_values(header_name_2, lexicon_data_2)
            lexicon_value_intersection = lexicon_values_1.intersection(lexicon_values_2)

            print(f'Number of unique values in lexicon file 1 {len(lexicon_values_1)}')
            print(f'Number of unique values in lexicon file 2 {len(lexicon_values_2)}')
            print('Number of unique values in common between the two files:'
                  f'{len(lexicon_value_intersection)}')

            