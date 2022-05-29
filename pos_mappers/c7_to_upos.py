import argparse
import json
from pathlib import Path
from typing import Dict


def string_to_path(string_argument: str) -> Path:
    return Path(string_argument).resolve()


if __name__ == '__main__':
    description = '''
    Creates a JSON formatted C7 to UPOS mapping, given the C7 to C5 JSON
    formatted mapping and the C5 to UPOS JSON formatted mapping.
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('c7_to_c5_file_path', type=string_to_path)
    parser.add_argument('c5_to_upos_file_path', type=string_to_path)
    parser.add_argument('output_file_path', type=string_to_path)
    args = parser.parse_args()

    c7_to_c5: Dict[str, str] = {}
    with args.c7_to_c5_file_path.open('r', encoding='utf-8') as c7_to_c5_fp:
        c7_to_c5 = json.load(c7_to_c5_fp)
    assert c7_to_c5

    c5_to_upos: Dict[str, str] = {}
    with args.c5_to_upos_file_path.open('r', encoding='utf-8') as c5_to_upos_fp:
        c5_to_upos = json.load(c5_to_upos_fp)
    assert c5_to_upos

    c7_to_upos: Dict[str, str] = {}
    for c7_tag, c5_tag in c7_to_c5.items():
        c7_to_upos[c7_tag] = c5_to_upos[c5_tag]
    assert c7_to_upos

    with args.output_file_path.open('w', encoding='utf-8') as output_fp:
        json.dump(c7_to_upos, output_fp)
