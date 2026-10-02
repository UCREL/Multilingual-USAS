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
    This script finds all of the unique POS values within a MWE lexicon file,
    including POS values that are part of a curly brace discontinues MWE
    expression. By default the unique POS values are output to stdout.

    If the optional `output-file` argument is passed the unique POS values are
    also saved to the `output-file` in TSV format.

    If another optional argument, `pos-mapper-file`, is given it will try to map
    the unique POS values given the JSON POS mapper file, any values it cannot
    map it will leave blank, and add a new column called `mapped` with all the
    POS values it could map.
    '''

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input_file', type=string_to_path)
    parser.add_argument('--output-file', type=string_to_path)
    parser.add_argument('--pos-mapper-file', type=string_to_path)
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
        csv_reader = csv.DictReader(lexicon_data, delimiter='\t')
        
        for row in csv_reader:
            mwe_template = row['mwe_template']
            matches = re.finditer(r'([^_\s]+)_([^_\s}]+)', mwe_template)
            for match in matches:
                pos_tags.add(match.groups()[1])
            
            matches = re.finditer(r'\s\{([a-zA-Z*]+)(/[a-zA-Z*]+)*\}\s', mwe_template)
            for match in matches:
                curly_brace_start, curly_brace_end = match.span()
                for pos_tag in mwe_template[curly_brace_start: curly_brace_end].strip().strip('{}').strip().split('/'):
                    pos_tags.add(pos_tag.strip())

    print('Unique POS Values:')
    if output_file:
        with output_file.open('w', encoding='utf-8', newline='') as write_lexicon_data:
            fieldnames = ['Unique POS Values']
            if pos_mapping:
                fieldnames.append('mapped')
            csv_writer = csv.DictWriter(write_lexicon_data, 
                                        fieldnames=fieldnames, 
                                        delimiter='\t')
            csv_writer.writeheader()
            for pos_tag in pos_tags:
                mapped_pos_tag = pos_mapping.get(pos_tag, '')
                print(f'{pos_tag}\t{mapped_pos_tag}')
                if pos_mapping:
                    csv_writer.writerow({'Unique POS Values': pos_tag,
                                         'mapped': mapped_pos_tag})
                else:
                    csv_writer.writerow({'Unique POS Values': pos_tag})
    else:
        for pos_tag in pos_tags:
            mapped_pos_tag = pos_mapping.get(pos_tag, '')
            print(f'{pos_tag}\t{mapped_pos_tag}')
            