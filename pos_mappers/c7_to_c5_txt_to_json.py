import argparse
import json
from pathlib import Path
from typing import Dict


def string_to_path(string_argument: str) -> Path:
    return Path(string_argument).resolve()


if __name__ == '__main__':
    description = '''
    Converts the tab separated `c7_to_c5_file_path` file to a dictionary
    object of C7 to C5 mapping and output it as a JSON object to the
    `output_file_path` file.
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('c7_to_c5_file_path', type=string_to_path)
    parser.add_argument('output_file_path', type=string_to_path)
    args = parser.parse_args()
    with args.c7_to_c5_file_path.open('r', encoding='utf-8') as input_fp:
        c7_to_c5: Dict[str, str] = {}
        for line in input_fp:
            c7_tag, c5_tag = line.strip().split('\t')
            if c7_tag in c7_to_c5:
                duplicate_error_message = (f'C7 tag {c7_tag} already exists '
                                           f'with value {c7_to_c5[c7_tag]}. '
                                           'The other c5 tag it maps to is '
                                           f'{c5_tag}')
                raise ValueError(duplicate_error_message)
            c7_to_c5[c7_tag] = c5_tag
        with args.output_file_path.open('w', encoding='utf-8') as output_fp:
            json.dump(c7_to_c5, output_fp)
