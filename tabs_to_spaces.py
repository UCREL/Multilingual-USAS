import argparse
from pathlib import Path
import csv


def string_to_path(string_argument: str) -> Path:
    return Path(string_argument).resolve()


if __name__ == '__main__':

    description = '''
    This script assumes that the semantic tags in the input_file have been
    separated by tabs rather than spaces, this script will reverse this process
    and output the spaced version into a new output_file. Both files are expected
    to be in TSV format.
    '''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input_file', type=string_to_path)
    parser.add_argument('output_file', type=string_to_path)
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    with output_file.open('w', encoding='utf-8', newline='') as write_lexicon_data:
        with input_file.open('r', encoding='utf-8', newline='') as lexicon_data:
            csv_reader = csv.DictReader(lexicon_data, delimiter='\t')
            
            writer_field_names = csv_reader.fieldnames
            csv_writer = csv.DictWriter(write_lexicon_data, 
                                        fieldnames=writer_field_names, 
                                        delimiter='\t')
            csv_writer.writeheader()
            
            for row in csv_reader:
                row['semantic_tags'] = ' '.join(row['semantic_tags'].split() + \
                                                row[None]
                                                ).strip()
                del row[None]
                row_header = list(row.keys())
                if len(row_header) > len(writer_field_names):
                    raise ValueError('This row contains an extra column header '
                                     f'{row_header}')
                csv_writer.writerow(row)
