import argparse
from pathlib import Path
import json
import csv
import copy


def string_to_path(string_argument: str) -> Path:
    return Path(string_argument).resolve()


if __name__ == '__main__':
    description = '''
    Given a column/header name, mapping file, and a lexicon file path it will
    map the values within the column name in the lexicon file using the mapping
    file. The resulting lexicon file will then be saved to the given output file
    path. 
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('lexicon_file_path', type=string_to_path,
                        help='File path to a lexicon file whose column values will be mapped.')
    parser.add_argument('column_name', type=str,
                        help='Column to be mapped.')
    parser.add_argument('mapping_file_path', type=string_to_path,
                        help='JSON file that contains a mapping in the form of a dictionary.')
    parser.add_argument('output_file_path', type=string_to_path,
                        help='File path to save the lexicon too with the column values mapped')
    args = parser.parse_args()

    lexicon_file = args.lexicon_file_path
    output_lexicon_file = args.output_file_path
    column_name = args.column_name
    mapper = {}
    with args.mapping_file_path.open('r', encoding='utf-8') as mapping_data:
        mapper = json.load(mapping_data)
    
    with output_lexicon_file.open('w', encoding='utf-8', newline='') as write_lexicon_data:
        with lexicon_file.open('r', encoding='utf-8', newline='') as lexicon_data:
            csv_reader = csv.DictReader(lexicon_data, delimiter='\t')
            
            writer_field_names = copy.deepcopy(csv_reader.fieldnames)
            csv_writer = csv.DictWriter(write_lexicon_data, 
                                        fieldnames=writer_field_names, 
                                        delimiter='\t')
            csv_writer.writeheader()
            
            for row in csv_reader:
                row[column_name] = mapper[row[column_name]]
                csv_writer.writerow(row)
