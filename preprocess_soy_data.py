#!/usr/bin/env python
# encoding: utf-8
'''
Converts the Raw data to a CSV format and a
corresponding config json with column to index mapping
'''
import json
import os
import time
import term_print as console

from generate_phenotype_data import generate_phenotype_measures_data
# Constants Import
import directory as DIR_CONST
import phenotype_constants as PHN_CONST
import dataset_constants as DS_CONST

'''
Write to file
usage write_file(<file_name>, <mode: 'w', 'r', 'rt'>, <file_data>)
'''
def write_file(filename, mode, data):
    with open(filename, mode) as file:
        file.write(data)
        file.close()
'''
Generates the column key value pairs as json config file
to enable querying data based on column name
Example: Column_name : index
'''
def generate_column_config_file(filename, column_headers):
    filename = filename.split('.')
    config_filename = filename[0]+'.config.json'
    reverse_map_filename = filename[0]+'_reverse.config.json'
    headers = column_headers.split(',')
    header_dict = dict(enumerate(headers))
    config_json = {v: k for k, v in header_dict.items()}
    write_file(PHN_CONST.FILE_COLUMN_CONFIG_REV, 'w', json.dumps(header_dict, indent=4, sort_keys=False))
    write_file(PHN_CONST.FILE_COLUMN_CONFIG, 'w', json.dumps(config_json, indent=4, sort_keys=False))

'''
Converts the raw data to a CSV format for easy reading
'''
def convert_to_csv(filename):
    existing_data = []
    try:
        with open(DIR_CONST.SOY_RAW_DIR+'/'+filename, 'rt+') as file:
            for line in file:
                # Removes leading and trailing whitespaces
                line = line.strip()
                # Substitute whitespaces with comma
                line = ','.join(line.split('\t'))
                existing_data.append(line)
            file.close()
    except IOError as e:
        console.error('I/O error', str(e))
        quit()
    except:
        console.error('An error has occured')
        quit()

    column_headers = existing_data[0]
    generate_column_config_file(filename, column_headers)
    existing_data.pop(0)
    write_file(PHN_CONST.FILE_DATA_CSV, 'w', '\n'.join(existing_data))

'''
Process raw data - Traverse raw data directory and process files
'''
def process_raw_data():
    for root, dirs, files in os.walk(DIR_CONST.SOY_RAW_DIR):
        for filename in files:
            if not filename.startswith('.'):
                convert_to_csv(filename)
                return 0
    return 1

def clean_up_files():
    for root, dirs, files in os.walk(DIR_CONST.CSV_DIR):
        for f in files:
            os.unlink(os.path.join(root, f))

def main():
    start_time = time.time()
    process_status = process_raw_data()
    if process_status == 0:
        # For Soy family only
        # Add logic to toggle between multiple datasets
        generate_phenotype_measures_data(DS_CONST.SOY_EXP_NAM, DS_CONST.SOY_SPECIES_NAME, DS_CONST.SOY_PHENOTYPE_FIELD_LIST, DS_CONST.SOY_PHENOTYPE_UNIT_MAP)
        clean_up_files()
    else:
        console.error('Error reading raw data. Is the file present?')
        quit()
    total_execution_time = time.time() - start_time
    total_execution_time_ms = repr(total_execution_time).split('.')[1][:3]
    console.success('\bTotal execution time : '+time.strftime("%H:%M:%S.{}".format(total_execution_time_ms), time.gmtime(total_execution_time)))

if __name__== "__main__":
    main()
