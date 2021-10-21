import argparse
from pathlib import Path
import csv
import copy

if __name__ == '__main__':
    description = '''
    Given a header name and a lexicon file path, it will remove the column 
    from the lexicon file with the given header name and then write the rest of 
    the data to the given `lexicon_file_to_write_too` (2nd argument).
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('lexicon_file_path', type=Path, 
                        help='File path to the lexicon')
    parser.add_argument('lexicon_file_to_write_too', type=Path, 
                        help='File path to write the rest of the lexicon data too')
    parser.add_argument('header_name', type=str, 
                        help='The header name')                        
    args = parser.parse_args()

    lexicon_collection_file = args.lexicon_file_path
    lexicon_file_to_write_too = args.lexicon_file_to_write_too
    header_name = args.header_name
    with lexicon_file_to_write_too.open('w', newline='') as write_lexicon_data:
        with lexicon_collection_file.open('r', newline='') as lexicon_data:
            csv_reader = csv.DictReader(lexicon_data, delimiter='\t')
            
            writer_field_names = copy.deepcopy(csv_reader.fieldnames)
            if writer_field_names is not None:
                del writer_field_names[writer_field_names.index(header_name)]

            csv_writer = csv.DictWriter(write_lexicon_data, 
                                        fieldnames=writer_field_names, 
                                        delimiter='\t')
            csv_writer.writeheader()
            
            for row in csv_reader:
                del row[header_name]
                csv_writer.writerow(row)
            