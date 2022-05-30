import argparse
from pathlib import Path
import csv
from collections import Counter
from typing import Dict

def string_to_path(string_argument: str) -> Path:
    return Path(string_argument).resolve()


if __name__ == '__main__':

    description = '''
    This script finds duplicate entries within either a single word and MWE 
    lexicon file and displays how many duplicates there are.
    '''

    file_type_help = ('single for single word lexicon file format or '
                      'mwe for multi word expression file format')

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input_file', type=string_to_path)
    parser.add_argument('--output-file', type=string_to_path)
    parser.add_argument('file_type', type=str, choices=['single', 'mwe'], 
                        help=file_type_help)
    args = parser.parse_args()

    input_file = args.input_file
    file_type = args.file_type
    output_file = args.output_file

    with input_file.open('r', encoding='utf-8', newline='') as lexicon_data:
        csv_reader = csv.DictReader(lexicon_data, 
                                    delimiter='\t')
        fieldnames = csv_reader.fieldnames
        duplicate_counter = Counter()
        
        duplicate_entries: Dict[str, int] = {}
        output_file_field_names = []
        if file_type == 'single':
            for values in csv_reader:
                lemma = values.get('lemma')
                pos_tag = values.get('pos', '')
                duplicate_counter.update([lemma+ ' ' + pos_tag])
            print(f'Lemma (POS Tag): Count')
            total_number_duplicates = 0
            for lemma_pos_tag, count in duplicate_counter.items():
                if count > 1:
                    print(f'{lemma_pos_tag}: {count}')
                    total_number_duplicates += 1
                    duplicate_entries[lemma_pos_tag] = count
            print(f'Total number of duplicate entires: {total_number_duplicates}')
            output_file_field_names = ['Lemma (POS Tag)', 'Count']
        else:
            for values in csv_reader:
                mwe_template = values.get('mwe_template')
                duplicate_counter.update([mwe_template])
            print(f'MWE Template: Count')
            total_number_duplicates = 0
            for mwe_template, count in duplicate_counter.items():
                if count > 1:
                    print(f'{mwe_template}: {count}')
                    total_number_duplicates += 1
                    duplicate_entries[mwe_template] = count
            print(f'Total number of duplicate entires: {total_number_duplicates}')
            output_file_field_names = ['MWE Template', 'Count']
        if output_file:
            with output_file.open('w', encoding='utf-8', newline='') as output_fp:
                tsv_writer = csv.DictWriter(output_fp,
                                            output_file_field_names,
                                            delimiter='\t')
                tsv_writer.writeheader()
                for key, count in duplicate_entries.items():
                    tsv_writer.writerow({output_file_field_names[0]: key,
                                         output_file_field_names[1]: count})
        