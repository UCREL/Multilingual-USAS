import argparse
from pathlib import Path
import csv
import re
import json


def string_to_path(string_argument: str) -> Path:
    return Path(string_argument).resolve()


if __name__ == '__main__':

    description = '''
    This script converts a file that contains only spaces to a file that
    separates fields/columns by tabs instead of spaces. For MWE files the
    optional POS tag argument is not used.

    For single word lexicon files we expect a POS field, further if you
    provide a JSON formatted POS tagset file where the object keys are the valid
    POS tags in the tagset then the POS field values will be checked against the
    given POS tagset.
    '''

    file_type_help = ('single for single word lexicon file format or '
                      'mwe for multi word expression file format')

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input_file', type=string_to_path)
    parser.add_argument('output_file', type=string_to_path)
    parser.add_argument('file_type', type=str, choices=['single', 'mwe'], 
                        help=file_type_help)
    parser.add_argument('--pos-tagset-file', type=string_to_path)
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    file_type = args.file_type

    with output_file.open('w', encoding='utf-8', newline='') as write_lexicon_data:
        with input_file.open('r', encoding='utf-8') as lexicon_data:
            csv_writer = csv.writer(write_lexicon_data, 
                                    delimiter='\t')
            
            if file_type == 'mwe':
                for line in lexicon_data:
                    line = line.strip()
                    match = re.search(r'^(([^\s_]+_[^\s_]+\s+)|(\{[^\s_]+\}\s+))+', line)
                    match_start, match_end = match.span()
                    mwe_template = line[match_start: match_end].strip()
                    semantic_tags = line[match_end:].strip()
                    semantic_tags = ' '.join(semantic_tags.split()).strip()
                    if '_' in semantic_tags:
                        raise ValueError('The semantic tags are not in the correct'
                                        'format as they contain an `_`. We have'
                                        f' extracted {mwe_template} as the MWE '
                                        f'template and {semantic_tags} as the '
                                        'semantic tags. The lexicon line this '
                                        f'failed on is:\n{line}')
                    csv_writer.writerow([mwe_template, semantic_tags])
            else:
                pos_tagset_file = args.pos_tagset_file
                pos_tagset = set()
                if pos_tagset_file:
                    with pos_tagset_file.open('r', encoding='utf-8') as pos_tagset_fp:
                        pos_tagset = set(json.load(pos_tagset_fp).keys())
                for line in lexicon_data:
                    line = line.strip()
                    field_values = line.split()
                    lemma = field_values[0]
                    pos_tag = field_values[1]
                    if pos_tag[-1] == '@':
                        pos_tag = pos_tag[:-1]
                    if pos_tag[-1] == '%':
                        pos_tag = pos_tag[:-1]
                    if pos_tag[-1] == '*':
                        pos_tag = pos_tag[:-1]
                    if pos_tag == 'JB':
                        pos_tag = 'JJ'
                    if pos_tag == '&FO':
                        pos_tag = 'FO'
                    if pos_tag == 'CF':
                        pos_tag = 'CS'
                    if pos_tag == 'JA':
                        pos_tag = 'JJ'
                    semantic_tags = ' '.join(field_values[2:])
                    if '_' in semantic_tags:
                        raise ValueError('The semantic tags are not in the correct'
                                         'format as they contain an `_`. We have'
                                         f' extracted {lemma} as the lemma, '
                                         f'{pos_tag} as the '
                                         f'pos tag, and {semantic_tags} as the '
                                         'semantic tags. The lexicon line this '
                                         f'failed on is:\n{line}')
                    if pos_tagset:
                        pos_error_msg = ('The POS tag extracted does not '
                                         'conform to the given POS tagset '
                                         f'We have extracted {lemma} as the lemma, '
                                         f'{pos_tag} as the '
                                         f'pos tag, and {semantic_tags} as the '
                                         'semantic tags. The lexicon line this '
                                         f'failed on is:\n{line}')
                        if pos_tag not in pos_tagset:
                            raise ValueError(pos_error_msg)
                    csv_writer.writerow([lemma, pos_tag, semantic_tags])