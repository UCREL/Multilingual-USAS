import argparse
from pathlib import Path
import csv
import json
from typing import List, Dict, Iterable
import re

from test_collection import check_file


def read_comment_txt_file(txt_file_path: str) -> Iterable[str]:
    '''
    Given a text file path it will return all lines in the text file that are 
    not comment lines.

    A comment is any line that starts with a `#` and contains no tab (`\t`) 
    characters within the comment line.

    # Parameters

    txt_file_path : `str`
        File path to the text file

    # Returns

    `Iterable[str]`

    # Raises

    ValueError
        If a comment line contains a tab (`\t`)
    '''
    comment_pattern = re.compile(r'#.*')
    tab_pattern = re.compile(r'\t')
    with Path(txt_file_path).open('r', newline='', encoding='utf-8-sig') as text_file:
        for line_number, line in enumerate(text_file):
            # All comment lines are those with a # and contain no tab.
            if (comment_pattern.match(line) and
                tab_pattern.search(line) is None):
                continue

            comment_error = ('\n\nA comment line cannot contain a tab.\n\n'
                             f'This occurred on line number: {line_number}\n\n'
                             f'In the following file: {txt_file_path}\n\n'
                             f'The line contains the following: {line}\n\n')
            comment_error = '\n' + ('-' * 50) + comment_error + ('-' * 50)
            if (comment_pattern.match(line) and 
                tab_pattern.search(line) is not None):
                raise ValueError(comment_error)
            line = line.replace('\ufeff', '')
            if line.strip():
                yield line

def txt_to_tsv(txt_file_path: str, tsv_file_path: str) -> None:
    '''
    Converts the text file into a TSV file. This conversion will remove all 
    comments.

    A comment is any line that starts with a `#` and contains no tab (`\t`) 
    characters within the comment line.

    # Parameters

    txt_file_path : `str`
        File path to the text file
    
    tsv_file_path : `str`
        File path to the TSV file
    ''' 
    txt_tsv_reader = csv.DictReader(read_comment_txt_file(txt_file_path), 
                                    delimiter='\t')
    with Path(tsv_file_path).open('w', newline='', encoding='utf-8') as tsv_file:
        tsv_writer = csv.DictWriter(tsv_file, 
                                    fieldnames=txt_tsv_reader.fieldnames,
                                    delimiter='\t')
        tsv_writer.writeheader()
        for row in txt_tsv_reader:
            tsv_writer.writerow(row)

if __name__ == '__main__':

    description = """
    This script does the following:

    1. Converts all lexicon files (single and MWE) from text file format to TSV. The 
       lexicon files are found through the meta data file (language_resources.json).
    2. Checks that the TSV files are formatted correctly:
        1. The minimum header names exist, 
        2. All fields/columns have a header name,
        3. All lines contain the minimum information e.g. no comment lines exist 
           in the middle of the file.
    """

    arguments = argparse.ArgumentParser(description=description, 
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    arguments.parse_args()

    json_data = Path(__file__, '..', 'language_resources.json').resolve()
    valid_resource_types = set(['single', 'mwe'])
    
    with json_data.open('r') as json_fp:
        data = json.load(json_fp)
        for language_code, meta_data in data.items():
            resources: List[Dict[str, str]] = meta_data['resources']
            for resource in resources:
                resource_type = resource['data type']
                if resource_type not in valid_resource_types:
                    continue
                tsv_resource_file_path = Path(resource['file path']).resolve()
                txt_resource_file_path = tsv_resource_file_path.with_suffix('.txt')
                txt_to_tsv(txt_resource_file_path, tsv_resource_file_path)
                check_file(resource_type, tsv_resource_file_path)

                

