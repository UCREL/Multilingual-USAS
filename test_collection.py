import argparse
from pathlib import Path
import csv
from typing import Set, List, Union
import typing
import traceback
import sys

if __name__ == '__main__':
    description = '''
    A file checker for single word and multi word expression lexicon files. 
    This file checker checks the following; 1. The minimum header names exist, 
    2. All lines contain the minimum information e.g. no comment lines exist 
    in the middle of the file.
    '''
    file_type_help = ('single for single word lexicon file format or '
                      'mwe for multi word expression file format')
    parser = argparse.ArgumentParser()
    parser.add_argument('lexicon_file_path', type=Path, 
                        help='File path to the lexicon file to check')
    parser.add_argument('file_type', type=str, choices=['single', 'mwe'], 
                        help=file_type_help)
    args = parser.parse_args()

    file_type = args.file_type
    minimum_field_names = {'lemma', 'semantic_tags'}
    if file_type == 'mwe':
        minimum_field_names = {'mwe_template', 'semantic_tags'}
    extra_field_names = ['pos', 'token']
    if file_type == 'mwe':
        extra_field_names = []
    field_names_to_extract = []

    lexicon_collection_file = args.lexicon_file_path
    with lexicon_collection_file.open('r', newline='') as lexicon_data:
        csv_reader = csv.DictReader(lexicon_data, delimiter='\t')
        file_field_names: Set[str] = set()
        if csv_reader.fieldnames is not None:
            file_field_names = set(csv_reader.fieldnames)
        if minimum_field_names.issubset(file_field_names):
            field_names_to_extract.extend(list(minimum_field_names))
        else:
            error_msg = ("The TSV file given should contain a header that"
                         " has at minimum the following fields "
                         f"{minimum_field_names}. The field names found "
                         f"were {file_field_names}")
            raise ValueError(error_msg)
        
        for extra_field_name in extra_field_names:
            if extra_field_name in file_field_names:
                field_names_to_extract.append(extra_field_name)

        for row_index, row in enumerate(csv_reader):
            try:
                row_data: typing.MutableMapping[str, Union[str, List[str]]] = {}
                for field_name in field_names_to_extract:
                    if field_name == 'semantic_tags':
                        row_data[field_name] = row[field_name].split()
                    else:
                        row_data[field_name] = row[field_name]
            except:
                print(f'Error on row {row_index} within the lexicon File:\n'
                      f'{str(lexicon_collection_file)}\n\n'
                      f'Line contains: \n{row}\n\n')
                traceback.print_exc(file=sys.stdout)
