#!/usr/bin/env python
# encoding: utf-8
import xlsxwriter
import json
import csv
import time
import term_print as console
import datetime
import re
from dateutil.parser import parse

# Local modules
import directory as DIR_CONST
import phenotype_constants as PHN_CONST
import dataset_constants as DS_CONST

from generate_germplasm_data import create_germplasm_workbook

MAIZE_CONFIG_DUMP = []
MAIZE_HEREDITY_CONFIG_DUMP = []
MAIZE_HEREDITY_LOC_CONF = []
LOCATION_LIST = []
EXP_LIST = []
PHENOTYPE_FIELD_LIST = {}
MAIZE_GERM_MAP = {}
GERMPLASM_DATA_LIST = []

'''
Creates the xlsx phenotype datasheet
'''
def create_phenotype_datasheet(experimentName, data, phenotypeUnitMap):

    phenotype_measure_file = DIR_CONST.OUTPUT_DIR+'/'+experimentName+'_phenotype_measures.xlsx'
    workbook = xlsxwriter.Workbook(phenotype_measure_file)
    # Create Data Sheets
    experiment_worksheet = workbook.add_worksheet(PHN_CONST.EXPERIMENTS_SHEET)
    location_worksheet = workbook.add_worksheet(PHN_CONST.LOCATIONS_SHEET)
    phenotype_worksheet = workbook.add_worksheet(PHN_CONST.PHENOTYPES_SHEET)
    phenotype_measures_worksheet = workbook.add_worksheet(PHN_CONST.PHENOTYPE_MEASURES_SHEET)

    print('\nCreating Phenotype Measures WorkBook')
    create_experiment_worksheet(experiment_worksheet, 1, 0)
    create_location_worksheet(location_worksheet, 1, 0)
    create_phenotype_worksheet(phenotype_worksheet, 1, 0, phenotypeUnitMap)
    create_phenotype_measure_worksheet(phenotype_measures_worksheet, 1, 0, data)
    # Finalize writing to workbook
    workbook.close()

def create_experiment_worksheet(experiment_worksheet, row_num, col_num):
    experiment_list = sorted(set(EXP_LIST))
    experiment_worksheet.write_row(0, 0, tuple(PHN_CONST.EXPERIMENT_HEADERS))
    for experiment in experiment_list:
        experiment_name = experiment[0]
        year = experiment[1]
        location = experiment[2]
        experiment_row = [experiment_name, location, '', '', '', '', '', year]
        experiment_worksheet.write_row(row_num, col_num, tuple(experiment_row))
        row_num += 1
    console.info('* Added experiments data')

def create_location_worksheet(location_worksheet, row_num, col_num):
    location_list = sorted(set(LOCATION_LIST))
    location_worksheet.write_row(0, 0, tuple(PHN_CONST.LOCATION_HEADERS))
    for location in location_list:
        location_row = [1, 'USA', location, '', '', '', '', '', '']
        location_worksheet.write_row(row_num, col_num, tuple(location_row))
        row_num += 1
    console.info('* Added locations data')

def create_phenotype_worksheet(phenotype_worksheet, row_num, col_num, phenotypeUnitMap):
    global PHENOTYPE_FIELD_LIST
    phenotype_worksheet.write_row(0, 0, tuple(PHN_CONST.PHENOTYPE_HEADERS))
    for field in DS_CONST.MAIZE_PHENOTYPE_FIELD_LIST:
        try:
            list = PHENOTYPE_FIELD_LIST[field]
            # unit_of_measure = phenotypeUnitMap[field]
            unit_of_measure = ''
            seq_list = [x for x in list if x != 'NA']
            phenotype_row_data = [field, unit_of_measure, '', min(seq_list), max(seq_list)]
            phenotype_worksheet.write_row(row_num, col_num, tuple(phenotype_row_data))
            row_num += 1
        except ValueError as e:
            pass
    console.info('* Added phenotype data')

def create_phenotype_measure_worksheet(phenotype_measures_worksheet, row_num, col_num, data):
    phenotype_measures_worksheet.write_row(0, 0, tuple(PHN_CONST.PHENOTYPE_MEASURES_HEADERS))
    for row in data:
        phenotype_measures_worksheet.write_row(row_num, col_num, tuple(row))
        row_num += 1
    console.info('* Added phenotype measures data')

'''
Read file and populate records
'''
def read_file(file_name, delimiter, germplasm_cols, phenotype_cols, config):
    global GERMPLASM_DATA_LIST
    with open(file_name, encoding="latin-1") as file:
        try:
            file_data = []
            reader = csv.DictReader(file, delimiter=delimiter)
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
                        year = ''

                # Experiment Names
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
                if( germplasm_check(germplasm_id) ):
                    GERMPLASM_DATA_LIST.append(germplasm_id)
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

                        if skip_column == False:
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

                            row_templ.append(phenotype_name)
                            row_templ.append(phenotype_value)
                            add_to_phenotype_field_list(phenotype_name, phenotype_value)
                            add_exp_loc_list(experiment_name, year, location_name)
                            file_data.append(row_templ)
        except (UnicodeError, KeyError) as e:
            print(e)
            pass
        return file_data

def date_pattern_match(value):
    date_pattern = re.compile(r"^(1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])/(?:[0-9]{2})?[0-9]{2}$")
    return date_pattern.match(value)

def germplasm_check(value):
    germplasm_pattern = re.compile(r"^[Z]{1}0[0-2][1-6]")
    return germplasm_pattern.match(value)
'''
Read heredity dataset
'''
def read_heredity_data(file_name, phenotype_cols):
    global GERMPLASM_DATA_LIST
    with open(file_name, encoding="latin-1") as file:
        try:
            file_data = []
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                location_col_name = 'env'
                compound_location = row[location_col_name]
                location_name = MAIZE_HEREDITY_LOC_CONF[compound_location]['name']
                year = MAIZE_HEREDITY_LOC_CONF[compound_location]['year']

                germplasm_id = 'Z'+row['pop'].rjust(3,'0')+'E'+row['entry_num'].rjust(4,'0')

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
        except(UnicodeError, KeyError) as e:
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
Read config and load in memory
'''
def load_config():
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
Process Germplasm Data
'''
def process_germplasm_data():
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
Read config file and process the raw data files
'''
def process_maize_data():
    raw_data = []
    load_config()
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
    create_phenotype_datasheet(DS_CONST.MAIZE_EXP_NAM, raw_data, '')


def main():
    process_maize_data()
    process_germplasm_data()

if __name__== "__main__":
    main()
