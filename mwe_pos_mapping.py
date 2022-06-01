import argparse
from pathlib import Path
import csv
import re
from typing import Dict
import json

def string_to_path(string_argument: str) -> Path:
    return Path(string_argument).resolve()


if __name__ == '__main__':

    description = '''
    This maps POS values within a MWE lexicon file given a POS mapper, the
    mapped MWE lexicon file will be saved to the given output file.
    '''

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input_file', type=string_to_path)
    parser.add_argument('pos_mapper_file', type=string_to_path)
    parser.add_argument('output_file', type=string_to_path)
    args = parser.parse_args()


    input_file = args.input_file
    output_file = args.output_file
    pos_mapper_file = args.pos_mapper_file

    pos_tags = set()
    pos_mapping: Dict[str, str] = {}
    if pos_mapper_file:
        with pos_mapper_file.open('r', encoding='utf-8') as pos_mapper_fp:
            pos_mapping = json.load(pos_mapper_fp)

    with input_file.open('r', encoding='utf-8', newline='') as lexicon_data:
        with output_file.open('w', encoding='utf-8', newline='') as mapped_lexicon_data:
            csv_writer = csv.DictWriter(mapped_lexicon_data,
                                        fieldnames=['mwe_template', 'semantic_tags'],
                                        delimiter='\t')
            csv_writer.writeheader()
            csv_reader = csv.DictReader(lexicon_data, delimiter='\t')
            
            for row in csv_reader:
                mwe_template = row['mwe_template']
                matches = re.finditer(r'([^_\s]+)_([^_\s}]+)', mwe_template)
                sorted_matches = sorted(matches, key=lambda match: match.span()[0], reverse=True)
                for match in sorted_matches:
                    pos_tag = match.group(2)
                    pos_tag_start, pos_tag_end = match.span(2)
                    mapped_pos_tag = pos_mapping[pos_tag]
                    mwe_template = f'{mwe_template[:pos_tag_start]}{mapped_pos_tag}{mwe_template[pos_tag_end:]}'
                
                matches = re.finditer(r'\s\{([a-zA-Z*]+)(/[a-zA-Z*]+)*\}\s', mwe_template)
                sorted_matches = sorted(matches, key=lambda match: match.span()[0], reverse=True)
                for match in sorted_matches:
                    curly_brace_start, curly_brace_end = match.span()
                    mapped_pos_tags = set()
                    for pos_tag in mwe_template[curly_brace_start: curly_brace_end].strip().strip('{}').strip().split('/'):
                        mapped_pos_tags.add(pos_mapping[pos_tag.strip()])
                    mapped_pos_curly_braces = ' {' + '/'.join(mapped_pos_tags) + '} '
                    
                    mwe_template = f'{mwe_template[:curly_brace_start]}{mapped_pos_curly_braces}{mwe_template[curly_brace_end:]}'

                csv_writer.writerow({'mwe_template': mwe_template,
                                     'semantic_tags': row['semantic_tags']})
            