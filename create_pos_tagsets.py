from pathlib import Path
import json
from typing import List, Dict, Iterable
import csv
from collections import Counter
import re

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

def single_lexicon_pos_count(file_path: str) -> Counter:
    pos_counter = Counter()
    for row in read_tsv_file(file_path):
        pos_counter.update([row['pos'].lower()])
    return pos_counter

def mwe_lexicon_pos_count(file_path: str) -> Counter:
    pos_counter = Counter()
    pos_matcher = re.compile(r'([^_\s]*)_([^_\s]*)')
    for row in read_tsv_file(file_path):
        mwe_template = row['mwe_template']
        pos_matches = pos_matcher.findall(mwe_template)
        for _, pos_value in pos_matches:
            pos_value = pos_value.lower()
            #if pos_value == '*':
            #    continue
            pos_counter.update([pos_value])
    return pos_counter

if __name__ == '__main__':
    json_data = Path(__file__, '..', 'language_resources.json').resolve()

    with json_data.open('r') as json_fp:
        data = json.load(json_fp)
        for language_code, meta_data in data.items():
            language_code: str
            language_description: str = meta_data['language data']['description']
            language_and_code: str = f'{language_description} ({language_code})'
            
            resources: List[Dict[str, str]] = meta_data['resources']
            pos_label_counts = Counter()
            resource_file_path = ''
            for resource in resources:
                resource_type = resource['data type']
                if resource_type == 'pos':
                    continue
                resource_file_path = resource['file path']

                
                if resource_type == 'single':
                    if not contains_pos_information(resource_file_path):
                        continue
                    pos_label_counts += single_lexicon_pos_count(resource_file_path)
                if resource_type == 'mwe':
                    pos_label_counts += mwe_lexicon_pos_count(resource_file_path)
            if resource_file_path and pos_label_counts:
                with Path(Path(resource_file_path).parent, 'generated_pos_tagset.tsv').open('w', newline='') as pos_tagset_fp:
                    csv_writer = csv.DictWriter(pos_tagset_fp, fieldnames=['POS', 'Count'], delimiter='\t')
                    csv_writer.writeheader()
                    for label, count in pos_label_counts.items():
                        csv_writer.writerow({'POS': label, 'Count': count})
    
                    