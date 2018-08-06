#!/usr/bin/env python
# encoding: utf-8
import xlsxwriter
import json
import csv
import time
import term_print as console
import datetime
import re
import sys, getopt
from dateutil.parser import parse

# Local modules
import directory as DIR_CONST
import phenotype_constants as PHN_CONST
import dataset_constants as DS_CONST
import germplasm_constants as GERM_CONST

from spreadsheet_helper import create_germplasm_workbook, create_phenotype_workbook

SOY_CONFIG_DUMP = []

MAIZE_CONFIG_DUMP = []
MAIZE_HEREDITY_CONFIG_DUMP = []
MAIZE_HEREDITY_LOC_CONF = []
LOCATION_LIST = []
EXP_LIST = []
PHENOTYPE_FIELD_LIST = {}
MAIZE_GERM_MAP = {}
GERMPLASM_DATA_LIST = []

'''
Read file and populate records
'''
def read_file(file_name, delimiter, germplasm_cols, phenotype_cols, config, data_type = None):
    global GERMPLASM_DATA_LIST
    with open(file_name, encoding="latin-1") as file:
        try:
            file_data = []
            reader = csv.DictReader(file, delimiter=delimiter)
            console.info('\nFile Name : '+ file_name)
            for row in reader:
                # Process Location
                if config['compound_location'] == True:
                    location_col_name = config['location_column']
                    location_map = config['location_map']
                    compound_location = row[location_col_name]
                    location_name = location_map[compound_location]['name']
                    year = location_map[compound_location]['year']
                else:
                    location_col_name = config['location_col']
                    year_col_name = config['year_col']
                    if location_col_name != 'None' and year_col_name != 'None':
                        location_name = row[location_col_name]
                        year = row[year_col_name]
                    else:
                        location_name = 'NA'
                        year = 'NA'

                if year == 'NA':
                    experiment_name = config['experiment_prefix']
                else:
                    experiment_name = config['experiment_prefix']+'_'+year

                # Process germplasm
                if config['compound_germplasm'] == True:
                    pop_col = germplasm_cols[0]
                    entry_col = germplasm_cols[1]
                    germplasm_id = 'Z'+row[pop_col].rjust(3,'0')+'E'+row[entry_col].rjust(4,'0')
                else:
                    germplasm_col = germplasm_cols[0]
                    germplasm_id = row[germplasm_col]

                # Filter germplasm ids between z001 and z026
                if( germplasm_check(germplasm_id, data_type) ):
                    # Process Phenotype data
                    for column in phenotype_cols:
                        if 'column_flag' in config:
                            column_check = config['column_flag']
                            if row[column_check] == 'MISSING':
                                skip_column = True
                            else:
                                skip_column = False
                        else:
                            skip_column = False

                        if skip_column == False and row[column] != '#VALUE!' and row[column] != '.':
                            row_templ = [experiment_name, '', location_name, '', '', '', '', '', germplasm_id]
                            if config['compound_phenotype'] == True:
                                if 'maize_inflo7_rawdata.txt' in file_name:
                                    phenotype_col_name = config['phenotype_field_name']
                                    phenotype_name = row[phenotype_col_name]
                                else:
                                    phenotype_name = config['phenotype_field_name']
                            else:
                                phenotype_name = column

                            try:
                                if(date_pattern_match(row[column])):
                                    phenotype_value = parse(row[column]).strftime("%Y/%m/%d")
                                else:
                                    phenotype_value = float(row[column])
                            except ValueError as e:
                                phenotype_value = 'NA'

                            if(data_type_check(data_type, year, phenotype_value)):
                                if data_type == 'SOY':
                                    family_name = row['Family'];
                                    family_num = row['FamNo']
                                    GERMPLASM_DATA_LIST.append(tuple([germplasm_id, family_name, family_num]))
                                else:
                                    GERMPLASM_DATA_LIST.append(germplasm_id)
                                row_templ.append(phenotype_name)
                                row_templ.append(phenotype_value)
                                add_to_phenotype_field_list(phenotype_name, phenotype_value)
                                add_exp_loc_list(experiment_name, year, location_name)
                                file_data.append(row_templ)
                console._print('Processed %d records' % len(file_data))
        except (UnicodeError, KeyError) as e:
            console.error('File name: '+file_name+' MISSING :>>>> '+str(e))
            pass
        return file_data

def data_type_check(data_type, year, phenotype_value):
    if(data_type == 'SOY' and year != '' and year != 'NA' and phenotype_value != 'NA'):
        return True
    elif (data_type == None):
        return True
    else:
        return False


def date_pattern_match(value):
    date_pattern = re.compile(r"^(1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])/(?:[0-9]{2})?[0-9]{2}$")
    return date_pattern.match(value)

def germplasm_check(value, data_type = None):
    if data_type == None:
        germplasm_pattern = re.compile(r"^[Z]{1}0[0-2][1-6]")
        return germplasm_pattern.match(value)
    else:
        return True
'''
Read heredity dataset
'''
def read_heredity_data(file_name, phenotype_cols):
    global GERMPLASM_DATA_LIST
    with open(file_name, encoding="latin-1") as file:
        try:
            file_data = []
            reader = csv.DictReader(file, delimiter=',')
            console.info('\nFile Name : '+ file_name)
            for row in reader:
                location_col_name = 'env'
                compound_location = row[location_col_name]
                if len(compound_location) < 6:
                    compound_location = compound_location.rjust(6,'0')
                location_name = MAIZE_HEREDITY_LOC_CONF[compound_location]['name']
                year = MAIZE_HEREDITY_LOC_CONF[compound_location]['year']

                germplasm_id = 'Z'+row['pop'].rjust(3,'0')+'E'+row['entry_num'].rjust(4,'0')

                if year == 'NA':
                    experiment_name = 'maizeNAM_Hung_2012_Heterdity'
                else:
                    experiment_name = 'maizeNAM_Hung_2012_Heterdity_'+year

                # Filter germplasm ids between z001 and z026
                if( germplasm_check(germplasm_id) ):
                    GERMPLASM_DATA_LIST.append(germplasm_id)
                    # Process Phenotype data
                    for column in phenotype_cols:
                        if row['entry_id'] == 'MISSING':
                            skip_column = True
                        else:
                            skip_column = False

                        if skip_column == False:
                            row_templ = [experiment_name, '', location_name, '', '', '', '', '', germplasm_id]
                            phenotype_name = column
                            try:
                                phenotype_value = float(row[phenotype_name])
                            except ValueError as e:
                                phenotype_value = 'NA'
                            row_templ.append(phenotype_name)
                            row_templ.append(phenotype_value)
                            add_to_phenotype_field_list(phenotype_name, phenotype_value)
                            add_exp_loc_list(experiment_name, year, location_name)
                            file_data.append(row_templ)
                console._print('Processed %d Heredity records' % len(file_data))
        except(UnicodeError, KeyError) as e:
            console.error('File name: '+file_name+' MISSING :>>>> '+str(e))
            pass
        return file_data

'''
Maintain data records for phenotype measure for threshold calculation
'''
def add_to_phenotype_field_list(fieldname, value):
    global PHENOTYPE_FIELD_LIST
    PHENOTYPE_FIELD_LIST[fieldname].append(value)

'''
Maintain data records for phenotype measure for threshold calculation
'''
def add_exp_loc_list(experiment, year, location):
    global LOCATION_LIST
    global EXP_LIST
    LOCATION_LIST.append(location)
    EXP_LIST.append(tuple([experiment, year, location]))

'''
Read Maize config and load in memory
'''
def load_maize_config():
    global PHENOTYPE_FIELD_LIST

    for field in DS_CONST.MAIZE_PHENOTYPE_FIELD_LIST:
        PHENOTYPE_FIELD_LIST[field] = []

    with open(DIR_CONST.MAIZE_CONFIG) as file:
        global MAIZE_CONFIG_DUMP
        MAIZE_CONFIG_DUMP = json.load(file)

    with open(DIR_CONST.MAIZE_HEREDITY_CONFIG) as file:
        global MAIZE_HEREDITY_CONFIG_DUMP
        MAIZE_HEREDITY_CONFIG_DUMP = json.load(file)

    with open(DIR_CONST.MAIZE_HEREDITY_LOC_CONFIG) as file:
        global MAIZE_HEREDITY_LOC_CONF
        MAIZE_HEREDITY_LOC_CONF = json.load(file)

    with open(DIR_CONST.MAIZE_GERM_MAP_CONFIG) as file:
        global MAIZE_GERM_MAP
        MAIZE_GERM_MAP = json.load(file)

'''
Read Soy config and load in memory
'''
def load_soy_config():
    global PHENOTYPE_FIELD_LIST

    for field in DS_CONST.SOY_PHENOTYPE_FIELD_LIST:
        PHENOTYPE_FIELD_LIST[field] = []

    with open(DIR_CONST.SOY_CONFIG) as file:
        global SOY_CONFIG_DUMP
        SOY_CONFIG_DUMP = json.load(file)

'''
Process Maize Germplasm Data
'''
def process_maize_germplasm_data():
    print('\bCreating Germplasm WorkBook')
    sorted_germplasm_list = sorted(set(GERMPLASM_DATA_LIST))
    germplasm_data = []
    for germplasm_id in sorted_germplasm_list:
        germ_key = germplasm_id[:4]
        origin = MAIZE_GERM_MAP[germ_key]
        parent = origin.split('_x_')
        germplasm_row = [DS_CONST.MAIZE_SPECIES_NAME, germplasm_id, '', 'inbred', '', '', origin, parent[0], '', parent[1], '']
        germplasm_data.append(germplasm_row)
    create_germplasm_workbook(DS_CONST.MAIZE_EXP_NAM, germplasm_data)

'''
Generate the germplasm data
'''
def process_soy_germplasm_data(experimentName, speciesName, germplasm_dict):
    print('\bCreating Germplasm WorkBook')
    germplasm_data = []
    for germplasm_id in germplasm_dict:
        family_name = 'NAM '+ str(germplasm_dict[germplasm_id])
        female_parent_id = GERM_CONST.HUB_PARENT
        male_parent_id = GERM_CONST.GERMPLASM_FAMILY_MAP[family_name]
        origin = female_parent_id+'_x_'+male_parent_id
        germplasm_row = [speciesName, germplasm_id, '', 'inbred', '', '', origin, female_parent_id, '', male_parent_id, '']
        germplasm_data.append(germplasm_row)
    create_germplasm_workbook(experimentName, germplasm_data)

'''
Read config file and process the raw data files
'''
def process_maize_phenotype_data():
    raw_data = []
    load_maize_config()
    for file_config in MAIZE_CONFIG_DUMP:
        file_name = DIR_CONST.MAIZE_RAW_DIR + '/' + file_config['file']
        delimiter = file_config['delimiter']
        germplasm_cols = file_config['germplasm_cols']
        phenotype_cols = file_config['phenotype_cols']
        file_data = read_file(file_name, delimiter, germplasm_cols, phenotype_cols, file_config)
        raw_data = raw_data + file_data
    # print(raw_data)
    for file_object in MAIZE_HEREDITY_CONFIG_DUMP:
        file_name = DIR_CONST.MAIZE_HEREDITY_RAW_DIR +'/' + file_object['file']
        phenotype_cols = file_object['phenotype_cols']
        file_data = read_heredity_data(file_name, phenotype_cols)
        raw_data = raw_data + file_data
    create_phenotype_workbook(DS_CONST.MAIZE_EXP_NAM, raw_data, DS_CONST.MAIZE_PHENOTYPE_UNIT_MAP, DS_CONST.MAIZE_PHENOTYPE_FIELD_LIST, EXP_LIST, LOCATION_LIST, PHENOTYPE_FIELD_LIST)

def preprocess_soy_germplasm_data():
    sorted_germplasm_list = sorted(set(GERMPLASM_DATA_LIST))
    germplasm_family_dict = {}
    for item in sorted_germplasm_list:
        germplasm_id = item[0]
        family_name = item[1]
        family_num = item[2]
        if germplasm_id in germplasm_family_dict:
            if germplasm_family_dict[germplasm_id] < int(family_num):
                germplasm_family_dict[germplasm_id] = int(family_num)
        else:
            germplasm_family_dict[germplasm_id] = int(family_num)
    process_soy_germplasm_data(DS_CONST.SOY_EXP_NAM, DS_CONST.SOY_SPECIES_NAME, germplasm_family_dict)

def process_soy_phenotype_data():
    raw_data = []
    load_soy_config()
    for file_config in SOY_CONFIG_DUMP:
        file_name = DIR_CONST.SOY_RAW_DIR + '/' + file_config['file']
        delimiter = file_config['delimiter']
        germplasm_cols = file_config['germplasm_cols']
        phenotype_cols = file_config['phenotype_cols']
        file_data = read_file(file_name, delimiter, germplasm_cols, phenotype_cols, file_config, 'SOY')
        raw_data = raw_data + file_data
    create_phenotype_workbook(DS_CONST.SOY_EXP_NAM, raw_data, DS_CONST.SOY_PHENOTYPE_UNIT_MAP, DS_CONST.SOY_PHENOTYPE_FIELD_LIST, EXP_LIST, LOCATION_LIST, PHENOTYPE_FIELD_LIST)


def generate_soy_data_files():
    process_soy_phenotype_data()
    preprocess_soy_germplasm_data()

def generate_maize_data_files():
    process_maize_phenotype_data()
    process_maize_germplasm_data()

def process_data(arg):
    start_time = time.time()
    if arg == 'SOY':
        generate_soy_data_files()
    elif arg == 'MAIZE':
        generate_maize_data_files()
    else:
        print('Inavlid dataset\nRun with -h to see a list of available datasets')
    total_execution_time = time.time() - start_time
    total_execution_time_ms = repr(total_execution_time).split('.')[1][:3]
    console.success('\bTotal execution time : '+time.strftime("%H:%M:%S.{}".format(total_execution_time_ms), time.gmtime(total_execution_time)))

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hm:d', ['help', 'dataset='])
    except getopt.GetoptError:
        print('process_data.py -dataset <dataset_name>')
        print('Available datasets = SOY, MAIZE')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('process_data.py --dataset <dataset_name>')
            print('Available datasets = SOY, MAIZE')
            sys.exit()
        elif opt in ('-d', '--dataset'):
            process_data(arg)

if __name__== "__main__":
    main(sys.argv[1:])
