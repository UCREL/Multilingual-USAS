import argparse
from pathlib import Path
import csv
from typing import Set
import collections

if __name__ == '__main__':
    description = '''
    Given a header name and a lexicon file path, it will print all of the 
    unique values and how often they occur from that header's column from 
    the given lexicon file.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('lexicon_file_path', type=Path, 
                        help='File path to the lexicon')
    parser.add_argument('header_name', type=str, 
                        help='The header name')                        
    args = parser.parse_args()

    lexicon_collection_file = args.lexicon_file_path
    header_name = args.header_name
    with lexicon_collection_file.open('r', newline='') as lexicon_data:
        csv_reader = csv.DictReader(lexicon_data, delimiter='\t')
        header_values_and_count = collections.Counter()
        for row in csv_reader:
            header_values_and_count.update([row[header_name]])
        
        print(f'Unique values for the header {header_name}')
        for value, count in header_values_and_count.items():
            print(f"Value: {value} Count: {count}")
            