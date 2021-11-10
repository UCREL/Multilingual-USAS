from pathlib import Path
import json
from typing import List, Dict, Iterable
import csv

from tabulate import tabulate

from test_collection import check_file


def read_tsv_file(file_path: str) -> Iterable[Dict[str, str]]:
    with Path(file_path).open('r', newline='') as lexicon_data:
        csv_reader = csv.DictReader(lexicon_data, delimiter='\t')
        for row in csv_reader:
            yield row

def contains_pos_information(file_path: str) -> bool:
    for value in read_tsv_file(file_path):
        if 'pos' in value:
            return True
        else:
            return False

def number_entries_in_lexicon_file(file_path: str) -> int:
    count = 0
    for _ in read_tsv_file(file_path):
        count += 1
    return count

def format_number_lexicon_entries(number_entries: List[int]) -> List[str]:
    formatted_number_entries: List[str] = []
    for value in number_entries:
        if value == 0:
            formatted_number_entries.append(':x:')
        else:
            formatted_number_entries.append(f'{value:,}')
    return formatted_number_entries

if __name__ == '__main__':
    json_data = Path(__file__, '..', 'language_resources.json').resolve()
    language_names: List[str] = []
    single_lexicon_include_pos: List[bool] = []
    single_lexicon_number_entries: List[int] = []
    mwe_lexicon_number_entries: List[int] = []
    resource_file_names: List[str] = []

    with json_data.open('r') as json_fp:
        data = json.load(json_fp)
        for language, resources in data.items():
            language: str
            resources: List[Dict[str, str]]

            

            for resource in resources:
                assert len(resource) == 1

                language_single_lexicon_entries = 0
                language_mwe_lexicon_entries = 0
                language_single_lexicon_include_pos = False

                for resource_type, resource_file_path in resource.items():
                    if resource_type == 'single':
                        language_single_lexicon_include_pos = contains_pos_information(resource_file_path)
                        language_single_lexicon_entries = number_entries_in_lexicon_file(resource_file_path)
                    if resource_type == 'mwe':
                        language_mwe_lexicon_entries = number_entries_in_lexicon_file(resource_file_path)
                    if resource_type != 'pos':
                        resource_path = Path(resource_file_path).resolve()
                        check_file(resource_type, resource_path)
                        resource_file_names.append(resource_path.name)
                        language_names.append(language)
                        single_lexicon_include_pos.append(language_single_lexicon_include_pos)
                        single_lexicon_number_entries.append(language_single_lexicon_entries)
                        mwe_lexicon_number_entries.append(language_mwe_lexicon_entries)
    
    
    formatted_single_lexicon_include_pos: List[str] = []
    for value in single_lexicon_include_pos:
        if value:
            formatted_single_lexicon_include_pos.append(':heavy_check_mark:')
        else:
            formatted_single_lexicon_include_pos.append(':x:')

    formatted_single_lexicon_number_entries = format_number_lexicon_entries(single_lexicon_number_entries)
    formatted_mwe_lexicon_number_entries = format_number_lexicon_entries(mwe_lexicon_number_entries)
    
    data_frame = {'Language': language_names,
                  'File Name': resource_file_names,
                  'Single Lexicon Number Entries': formatted_single_lexicon_number_entries,
                  'Single Lexicon Include POS': formatted_single_lexicon_include_pos,
                  'MWE Lexicon Number Entries': formatted_mwe_lexicon_number_entries}
    headers = ['Language', 'File Name', 'Single Lexicon Number Entries', 
               'Single Lexicon Include POS', 'MWE Lexicon Number Entries']
    print(tabulate(data_frame, headers=headers, tablefmt="github"))
    
                    