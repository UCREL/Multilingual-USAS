import argparse
from collections import defaultdict
from pathlib import Path
import json
from typing import List, Dict, Set, Tuple, Optional
import re

from find_formatting_issues import (FIELD_NAMES_TO_CHECK, find_field_problems,
                                    mechanical_fix,
                                    read_txt_lexicon_with_line_numbers)
from test_collection import check_file
from txt_to_tsv import txt_to_tsv

# The fields that together identify a lexicon entry, used to find fixes that
# would create a duplicate entry, e.g. a `lemma` of ` جمع` becoming `جمع` when
# an entry with the `lemma` `جمع` and the same `pos` already exists.
ENTRY_KEY_FIELD_NAMES = ['lemma', 'token', 'pos', 'mwe_template']
LINE_ENDING_PATTERN = re.compile(r'(\r\n|\r|\n)$')


def get_lexicon_resources() -> List[Tuple[str, str, Path, str]]:
    '''
    Returns all of the single, autotag, and MWE lexicon resources listed in the
    meta data file (language_resources.json), each as a tuple of language
    code, language description, lexicon text file path, and data type.

    # Returns

    `List[Tuple[str, str, Path, str]]`
    '''
    json_data = Path(__file__, '..', 'language_resources.json').resolve()
    repository_folder = json_data.parent
    with json_data.open('r') as json_fp:
        data = json.load(json_fp)
    lexicon_resources: List[Tuple[str, str, Path, str]] = []
    for language_code, meta_data in data.items():
        language_description: str = meta_data['language data']['description']
        for resource in meta_data['resources']:
            resource_type = resource['data type']
            if resource_type not in ('single', 'autotag', 'mwe'):
                continue
            txt_file_path = Path(repository_folder, resource['file path']).resolve().with_suffix('.txt')
            lexicon_resources.append((language_code, language_description,
                                      txt_file_path, resource_type))
    return lexicon_resources


def get_lexicon_txt_files(language: str) -> List[Tuple[Path, Optional[str]]]:
    '''
    Returns the file paths to the single, autotag, and MWE lexicon text files
    of the given `language`, along with their data type, as listed in the meta
    data file (language_resources.json).

    # Parameters

    language : `str`
        The language code, e.g. `ur`, or the language description, e.g.
        `Urdu`, both are case insensitive.

    # Returns

    `List[Tuple[Path, Optional[str]]]`

    # Raises

    ValueError
        If the `language` is not in the meta data file.
    '''
    language_files = [(txt_file_path, resource_type)
                      for language_code, language_description, txt_file_path, resource_type
                      in get_lexicon_resources()
                      if language.lower() in (language_code.lower(), language_description.lower())]
    if not language_files:
        raise ValueError(f'The language `{language}` is not in language_resources.json, '
                         'use either the language code, e.g. `ur`, or the description, '
                         'e.g. `Urdu`.')
    return language_files


def get_data_type(txt_file_path: Path) -> Optional[str]:
    '''
    Returns the data type, e.g. `single`, of the lexicon text file as listed
    in the meta data file (language_resources.json), or `None` if the file is
    not listed.

    # Parameters

    txt_file_path : `Path`
        File path to the lexicon text file.

    # Returns

    `Optional[str]`
    '''
    for _, _, resource_txt_file_path, resource_type in get_lexicon_resources():
        if resource_txt_file_path == txt_file_path:
            return resource_type
    return None


def fix_txt_file(txt_file_path: Path, skip_lines: Set[int], dry_run: bool) -> bool:
    '''
    Applies all of the mechanical fixes, as found by `find_formatting_issues.py`,
    to the lexicon text file and prints each fix made and each fix skipped.
    Only the fixed field values are changed, everything else within the file,
    e.g. comments and line endings, stays the same.

    A fix is skipped when:
    1. The line number is in `skip_lines`.
    2. The fix is not mechanical, i.e. it `needs review`.
    3. The fixed entry would be a duplicate of another entry, e.g. the same
       `lemma` and `pos`, as the entries then need to be merged.

    # Parameters

    txt_file_path : `Path`
        File path to the lexicon text file.

    skip_lines : `Set[int]`
        Line numbers, starting at 1, that should not be fixed.

    dry_run : `bool`
        If `True` the fixes are printed but the file is not changed.

    # Returns

    `bool`
        `True` if the file was changed (or would be changed if `dry_run`).
    '''
    entries = list(read_txt_lexicon_with_line_numbers(txt_file_path))
    if not entries:
        return False
    field_names = list(entries[0][1].keys())
    key_field_names = [field_name for field_name in ENTRY_KEY_FIELD_NAMES
                       if field_name in field_names]

    # Line number -> {field name: fixed value}
    fixes: Dict[int, Dict[str, str]] = defaultdict(dict)
    for line_number, entry in entries:
        for field_name in FIELD_NAMES_TO_CHECK:
            value = entry.get(field_name)
            if value is None:
                continue
            problems = find_field_problems(field_name, value)
            if not problems:
                continue
            location = f'{txt_file_path.name}:{line_number} `{field_name}` {value!r}'
            if line_number in skip_lines:
                print(f'SKIPPED {location}: line is in --skip-line')
                continue
            fixed_value = mechanical_fix(field_name, value, problems)
            if fixed_value is None:
                print(f'SKIPPED {location}: needs review ({"; ".join(problems)})')
                continue
            fixes[line_number][field_name] = fixed_value

    # Skip fixes that would make an entry the same as another entry.
    key_to_line_numbers: Dict[Tuple[str, ...], List[int]] = defaultdict(list)
    for line_number, entry in entries:
        fixed_entry = {**entry, **fixes.get(line_number, {})}
        key = tuple(fixed_entry[field_name] for field_name in key_field_names)
        key_to_line_numbers[key].append(line_number)
    for line_numbers in key_to_line_numbers.values():
        if len(line_numbers) < 2:
            continue
        for line_number in line_numbers:
            if line_number not in fixes:
                continue
            other_line_numbers = [str(other) for other in line_numbers if other != line_number]
            print(f'SKIPPED {txt_file_path.name}:{line_number} {fixes[line_number]!r}: '
                  f'the fixed entry would be a duplicate of line(s) '
                  f'{", ".join(other_line_numbers)}, these need to be merged by hand')
            del fixes[line_number]

    if not fixes:
        return False

    with txt_file_path.open('r', newline='', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()
    line_number_to_entry = dict(entries)
    for line_number, field_fixes in sorted(fixes.items()):
        # A byte order mark within the file is removed when reading the
        # entries, as in `txt_to_tsv.py`, so it is also removed from the line.
        line = lines[line_number - 1].replace('\ufeff', '')
        line_ending_match = LINE_ENDING_PATTERN.search(line)
        line_ending = line_ending_match.group(0) if line_ending_match else ''
        values = line[:len(line) - len(line_ending)].split('\t')
        entry = line_number_to_entry[line_number]
        for field_name, fixed_value in field_fixes.items():
            field_index = field_names.index(field_name)
            if values[field_index] != entry[field_name]:
                # e.g. the field is quoted, so the raw text does not match the
                # value read by the CSV reader, safer to leave it for a person.
                print(f'SKIPPED {txt_file_path.name}:{line_number} `{field_name}` '
                      f'{entry[field_name]!r}: could not find the value in the raw line')
                continue
            print(f'FIXED   {txt_file_path.name}:{line_number} `{field_name}` '
                  f'{entry[field_name]!r} -> {fixed_value!r}')
            values[field_index] = fixed_value
        lines[line_number - 1] = '\t'.join(values) + line_ending

    if not dry_run:
        with txt_file_path.open('w', newline='', encoding='utf-8') as txt_file:
            txt_file.writelines(lines)
    return True


if __name__ == '__main__':
    description = '''
    Fixes the lexicon formatting issues found by `find_formatting_issues.py`
    that have a mechanical fix, e.g. removing whitespace from the start and
    end of a `pos` value, within the lexicon text files of the given language
    or the given lexicon file. Each fix made, and each fix skipped, is printed.

    A fix is skipped when the issue needs review by someone who knows the
    language, when the line is given with --skip-line, or when the fixed
    entry would be a duplicate of another entry (these need merging by hand).

    The TSV version of each changed text file is regenerated and then checked
    with the same check as CI (`test_collection.py`), the result of which is
    printed, a file can still fail after its fixes, e.g. when issues need
    review, which does not stop the script. Files not listed in
    language_resources.json are not checked, as their data type is unknown.
    Afterwards run `python find_formatting_issues.py` to see the remaining
    issues and `python create_pos_tagsets.py` to update the generated POS
    tagsets.
    '''
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument('--language', type=str,
                       help='Language code, e.g. `ur`, or description, e.g. `Urdu`, '
                            'whose lexicon files should be fixed.')
    scope.add_argument('--file', type=Path,
                       help='The lexicon file to fix, either the `.txt` or `.tsv` '
                            'path, the `.txt` file is the one that is changed.')
    parser.add_argument('--skip-line', type=int, action='append', default=[],
                        help='Line number within the `.txt` file that should not be '
                             'fixed, can be given more than once. Only with --file.')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print the fixes without changing any files.')
    args = parser.parse_args()

    if args.skip_line and args.file is None:
        parser.error('--skip-line can only be used with --file, as line numbers '
                     'are specific to a file.')

    if args.file is not None:
        txt_file_path = args.file.resolve().with_suffix('.txt')
        txt_files = [(txt_file_path, get_data_type(txt_file_path))]
    else:
        try:
            txt_files = get_lexicon_txt_files(args.language)
        except ValueError as language_error:
            parser.error(str(language_error))

    for txt_file_path, resource_type in txt_files:
        if not txt_file_path.exists():
            parser.error(f'The lexicon text file {txt_file_path} does not exist.')
        changed = fix_txt_file(txt_file_path, set(args.skip_line), args.dry_run)
        if not changed or args.dry_run:
            continue
        tsv_file_path = txt_file_path.with_suffix('.tsv')
        txt_to_tsv(str(txt_file_path), str(tsv_file_path))
        print(f'Regenerated {tsv_file_path.name}')
        # The same check as CI, it does not stop the script as a file can
        # still fail after its fixes, e.g. when issues need review.
        if resource_type is None:
            print(f'{tsv_file_path.name} is not in language_resources.json, so its '
                  'data type is unknown and it has not been checked')
            continue
        try:
            check_file(resource_type, tsv_file_path)
            print(f'{tsv_file_path.name} passes validation')
        except ValueError:
            print(f'{tsv_file_path.name} still fails validation, run '
                  '`python find_formatting_issues.py` to see the remaining issues')
