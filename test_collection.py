import argparse
from os import error
from pathlib import Path
import csv
from typing import Set, List, Union
import typing
import traceback
import sys


def check_file(file_type: str, lexicon_collection_file: Path) -> None:
    '''
    Will raise a `ValueError` if the `lexicon_collection_file` is not formatted 
    correctly. 

    # Parameters

    file_type : `str`
        Type of the file can be one of the following values:
        1. `single` -- single lexicon files.
        2. `mwe` -- multi word expresion lexicon files.

    lexicon_collection_file : `Path`
        File path to the lexicon file.

    # Raises

    ValueError
        If the `lexicon_collection_file` is not formatted correctly. The three main
        sources of this error: 1. When the TSV field does not contain a header with
        the minimum field names for the type of file, 2. When a row does not contain
        enough tab seperated values, 3. When the field values in the row does
        not contain a string value when it should.
    '''

    minimum_field_names = {'lemma', 'semantic_tags'}
    if file_type == 'mwe':
        minimum_field_names = {'mwe_template', 'semantic_tags'}
    extra_field_names = ['pos', 'token']
    if file_type == 'mwe':
        extra_field_names = []
    field_names_to_extract = []

    with lexicon_collection_file.open('r', newline='') as lexicon_data:
        csv_reader = csv.DictReader(lexicon_data, delimiter='\t')
        file_field_names: Set[str] = set()
        if csv_reader.fieldnames is not None:
            file_field_names = set(csv_reader.fieldnames)
        if minimum_field_names.issubset(file_field_names):
            field_names_to_extract.extend(list(minimum_field_names))
        else:
            header_error_message = (f"The TSV file {str(lexicon_collection_file)} should "
                                    "contain a header that has as minimum the following fields "
                                    f"{minimum_field_names}. The field names found "
                                    f"were {file_field_names}")
            raise ValueError(header_error_message)
        
        for extra_field_name in extra_field_names:
            if extra_field_name in file_field_names:
                field_names_to_extract.append(extra_field_name)

        for row_index, row in enumerate(csv_reader):
            general_error_message = '\n' + ('-' * 50) + '\n\n'
            general_error_message += (f'The Error occurred on row {row_index} '
                                      f'within the lexicon File: {str(lexicon_collection_file)}\n '
                                      f'Line contains: \n{row}\n\n')
            try:
                if None in row.keys():
                    row_header_error_message = ('This row contains an extra field that does'
                                                ' not have a header name associated to it.'
                                                ' This is represented by the `None` key in '
                                                'the row data.\n\n')
                    raise ValueError(general_error_message + row_header_error_message + '-' * 50)
                row_data: typing.MutableMapping[str, Union[str, List[str]]] = {}
                for field_name in field_names_to_extract:
                    if not isinstance(row[field_name], str):
                        field_value_error = (f'The value within the header {field_name}'
                                             f' should be of type `str` and not {type(row[field_name])}'
                                             f', the value is: {row[field_name]}.\n\n')
                        raise ValueError(general_error_message + field_value_error + '-' * 50)
                    if field_name == 'semantic_tags':
                        row_data[field_name] = row[field_name].split()
                    else:
                        row_data[field_name] = row[field_name]
            except ValueError as value_error:
                raise value_error
            except:
                raise Exception(general_error_message + '-' * 50)
                

if __name__ == '__main__':
    description = '''
    A file checker for single word and multi word expression lexicon files. 
    This file checker checks the following; 
    
    1. The minimum header names exist, 
    2. All fields/columns have a header name,
    3. All lines contain the minimum information e.g. no comment lines exist 
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

    check_file(args.file_type, args.lexicon_file_path)
