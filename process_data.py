#!/usr/bin/env python
# encoding: utf-8
import json
import csv
import time
import term_print as console
import datetime
import sys, getopt
import pathlib
from dateutil.parser import parse

# Local modules
import directory as DIR_CONST
import phenotype_constants as PHN_CONST
import dataset_constants as DS_CONST
import germplasm_constants as GERM_CONST

# Helper imports
from data_check_helpers import data_type_check, date_pattern_match, germplasm_check, sorghum_date_process, remove_underscores, split_germplasm_sorghum_nam
from spreadsheet_helper import spreadsheet_helper
from preprocess_sorghum import preprocess_sorghum_phenotype

SOY_CONFIG_DUMP = []

MAIZE_CONFIG_DUMP = []
MAIZE_HEREDITY_CONFIG_DUMP = []
MAIZE_HEREDITY_LOC_CONF = []
LOCATION_LIST = []
EXP_LIST = []
PHENOTYPE_FIELD_LIST = {}
DIST_PHENOTYPE_FIELD_LIST = []
MAIZE_GERM_MAP = {}
GERMPLASM_DATA_LIST = []

MAIZE_DUP_PHENOTYPE = DS_CONST.MAIZE_PHENOTYPE_DUP_MAP

'''
Read file and populate records
'''
def read_file(file_name, delimiter, germplasm_cols, phenotype_cols, config, data_type = None):
    global GERMPLASM_DATA_LIST
    global MAIZE_DUP_PHENOTYPE

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
                        year = '9999'

                if data_type == 'SORGHUM' and year_col_name != 'None':
                    year = sorghum_date_process(row[year_col_name])
                    experiment_name = config['experiment_prefix']+'_'+row['author']+'_'+year
                else:
                    experiment_name = config['experiment_prefix']+'_'+year

                # Process germplasm
                if config['compound_germplasm'] == True:
                    pop_col = germplasm_cols[0]
                    entry_col = germplasm_cols[1]
                    germplasm_id = 'Z'+row[pop_col].rjust(3,'0')+'E'+row[entry_col].rjust(4,'0')
                else:
                    germplasm_col = germplasm_cols[0]
                    if data_type == 'SORGHUM_NAM':
                        germplasm_id = split_germplasm_sorghum_nam(row[germplasm_col])
                    else:
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

                        if skip_column == False and row[column] != '#VALUE!' and row[column] != '.' and row[column] != '(null)':
                            row_templ = [experiment_name, '', location_name, '', '', '', '', '', germplasm_id]
                            if config['compound_phenotype'] == True:
                                if 'maize_inflo7_rawdata.txt' in file_name or 'baptraits.csv' in file_name:
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
                                elif data_type == 'SORGHUM_NAM':
                                    family_index = row['fam']
                                    GERMPLASM_DATA_LIST.append(tuple([germplasm_id, family_index]))
                                else:
                                    GERMPLASM_DATA_LIST.append(germplasm_id)

                                if phenotype_name.lower() in MAIZE_DUP_PHENOTYPE and MAIZE_DUP_PHENOTYPE[phenotype_name.lower()] != 0:
                                    phenotype_name = phenotype_name.lower()+str(MAIZE_DUP_PHENOTYPE[phenotype_name.lower()])
                                else:
                                    phenotype_name = phenotype_name.lower()
                                row_templ.append(phenotype_name)
                                row_templ.append(phenotype_value)
                                add_to_phenotype_field_list(phenotype_name, phenotype_value)
                                add_exp_loc_list(experiment_name, year, location_name)
                                if data_type == 'SORGHUM' and phenotype_value != 'NA':
                                    file_data.append(row_templ)
                                elif data_type != 'SORGHUM':
                                    file_data.append(row_templ)
                console._print('Processed %d records' % len(file_data))
        except (UnicodeError, KeyError) as e:
            console.error('File name: '+file_name+' MISSING :>>>> '+str(e))
            pass
        for phenotype_col in phenotype_cols:
            if phenotype_col.lower() in MAIZE_DUP_PHENOTYPE:
                MAIZE_DUP_PHENOTYPE[phenotype_col.lower()] = int(MAIZE_DUP_PHENOTYPE[phenotype_col.lower()]) + 1
        return file_data

'''
Read heredity dataset
'''
def read_heredity_data(file_name, phenotype_cols):
    global GERMPLASM_DATA_LIST
    global MAIZE_DUP_PHENOTYPE

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
                                phenotype_value = float(row[column])
                            except ValueError as e:
                                phenotype_value = 'NA'

                            if phenotype_name.lower() in MAIZE_DUP_PHENOTYPE and MAIZE_DUP_PHENOTYPE[phenotype_name.lower()] != 0:
                                phenotype_name = phenotype_name.lower()+str(MAIZE_DUP_PHENOTYPE[phenotype_name.lower()])
                            else:
                                phenotype_name = phenotype_name.lower()
                            row_templ.append(phenotype_name)
                            row_templ.append(phenotype_value)
                            add_to_phenotype_field_list(phenotype_name, phenotype_value)
                            add_exp_loc_list(experiment_name, year, location_name)
                            file_data.append(row_templ)
                console._print('Processed %d records' % len(file_data))
        except(UnicodeError, KeyError) as e:
            console.error('File name: '+file_name+' MISSING :>>>> '+str(e))
            pass

    for phenotype_col in phenotype_cols:
        if phenotype_col.lower() in MAIZE_DUP_PHENOTYPE:
            MAIZE_DUP_PHENOTYPE[phenotype_col.lower()] = int(MAIZE_DUP_PHENOTYPE[phenotype_col.lower()]) + 1
    return file_data
'''
Maintain data records for phenotype measure for threshold calculation
'''
def add_to_phenotype_field_list(fieldname, value):
    global PHENOTYPE_FIELD_LIST
    global DIST_PHENOTYPE_FIELD_LIST
    if fieldname in PHENOTYPE_FIELD_LIST:
        PHENOTYPE_FIELD_LIST[fieldname].append(value)
    else:
        PHENOTYPE_FIELD_LIST[fieldname] = []
        DIST_PHENOTYPE_FIELD_LIST.append(fieldname)
        PHENOTYPE_FIELD_LIST[fieldname].append(value)

'''
Maintain data records for phenotype measure for threshold calculation
'''
def add_exp_loc_list(experiment, year, location):
    global LOCATION_LIST
    global EXP_LIST
    LOCATION_LIST.append(location)
    EXP_LIST.append(tuple([experiment, year, location]))


##############################
# Maize Data processes
##############################
'''
Read Maize config and load in memory
'''
def load_maize_config():
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
    workbook.create_germplasm_workbook(germplasm_data)

'''
Process Maize Phenotype Data
'''
def process_maize_phenotype_data():
    global PHENOTYPE_FIELD_LIST
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
    # print(PHENOTYPE_FIELD_LIST)
    workbook.create_phenotype_workbook(raw_data, DS_CONST.MAIZE_PHENOTYPE_UNIT_MAP, DIST_PHENOTYPE_FIELD_LIST, EXP_LIST, LOCATION_LIST, PHENOTYPE_FIELD_LIST)

##############################
# SOY Data processes
##############################
'''
Read Soy config and load in memory
'''
def load_soy_config():
    with open(DIR_CONST.SOY_CONFIG) as file:
        global SOY_CONFIG_DUMP
        SOY_CONFIG_DUMP = json.load(file)

'''
Process Soy Germplasm Data
'''
def process_soy_germplasm_data(speciesName, germplasm_dict):
    print('\bCreating Germplasm WorkBook')
    germplasm_data = []
    for germplasm_id in germplasm_dict:
        family_name = 'NAM '+ str(germplasm_dict[germplasm_id])
        female_parent_id = GERM_CONST.HUB_PARENT
        male_parent_id = GERM_CONST.GERMPLASM_FAMILY_MAP[family_name]
        origin = female_parent_id+'_x_'+male_parent_id
        germplasm_row = [speciesName, germplasm_id, '', 'inbred', '', '', origin, female_parent_id, '', male_parent_id, '']
        germplasm_data.append(germplasm_row)
    workbook.create_germplasm_workbook(germplasm_data)

'''
Pre-process Soy Germplasm Data
'''
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
    process_soy_germplasm_data(DS_CONST.SOY_SPECIES_NAME, germplasm_family_dict)

'''
Process Soy Phenotype Data
'''
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
    workbook.create_phenotype_workbook(raw_data, DS_CONST.SOY_PHENOTYPE_UNIT_MAP, DS_CONST.SOY_PHENOTYPE_FIELD_LIST, EXP_LIST, LOCATION_LIST, PHENOTYPE_FIELD_LIST)

##############################
# SORGHUM Data processes
##############################
'''
Read Soy config and load in memory
'''
def load_sorghum_config(sorghum_type):
    global SORGHUM_CONFIG_DUMP
    if sorghum_type == 'BAP':
        with open(DIR_CONST.SORGHUM_BAP_CONFIG) as file:
            SORGHUM_CONFIG_DUMP = json.load(file)
    elif sorghum_type == 'DIV':
        with open(DIR_CONST.SORGHUM_DIV_CONFIG) as file:
            SORGHUM_CONFIG_DUMP = json.load(file)

'''
Fetch germplasm taxa
'''
def fetch_sorghum_germplasm_taxa():
    console.info('Reading Taxa germplasm data for Sorghum BAP')
    with open(DIR_CONST.SORGHUM_GERM_TAXA) as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            germplasm_id = remove_underscores(row['Taxa'])
            GERMPLASM_DATA_LIST.append(germplasm_id)
'''
Process Sorghum Germplasm Data
'''
def process_sorghum_germplasm_data():
    print('\bCreating Germplasm WorkBook')
    sorted_germplasm_list = sorted(set(GERMPLASM_DATA_LIST))
    germplasm_data = []
    for germplasm_id in sorted_germplasm_list:
        germplasm_row = [DS_CONST.SORGHUM_SPECIES_NAME, germplasm_id, '', 'inbred', '', '', '', '', '', '', '']
        germplasm_data.append(germplasm_row)
    workbook.create_germplasm_workbook(germplasm_data)

'''
Process Sorghum Phenotype Data
'''
def process_sorghum_phenotype_data(sorghum_type):
    global PHENOTYPE_FIELD_LIST
    raw_data = []
    load_sorghum_config(sorghum_type)
    for file_config in SORGHUM_CONFIG_DUMP:
        file_name = DIR_CONST.SORGHUM_RAW_DIR + '/' + file_config['file']
        delimiter = file_config['delimiter']
        germplasm_cols = file_config['germplasm_cols']
        phenotype_cols = file_config['phenotype_cols']
        file_data = read_file(file_name, delimiter, germplasm_cols, phenotype_cols, file_config, 'SORGHUM')
        raw_data = raw_data + file_data
    workbook.create_phenotype_workbook(raw_data, DS_CONST.SORGHUM_UNIT_MAP, DIST_PHENOTYPE_FIELD_LIST, EXP_LIST, LOCATION_LIST, PHENOTYPE_FIELD_LIST)

##############################
# SORGHUM NAM Data processes
##############################
'''
Read Sorghum SAP config and load in memory
'''
def load_sorghum_sap_config():
    global SORGHUM_SAP_CONFIG_DUMP
    with open(DIR_CONST.SORGHUM_SAP_CONFIG) as file:
        SORGHUM_SAP_CONFIG_DUMP = json.load(file)

'''
Process Sorghum SAP Phenotype data
'''
def process_sorghum_sap_phenotype_data():
    global PHENOTYPE_FIELD_LIST
    raw_data = []
    load_sorghum_sap_config()
    for file_config in SORGHUM_SAP_CONFIG_DUMP:
        file_name = DIR_CONST.SORGHUM_SAP_RAW_DIR + '/' + file_config['file']
        delimiter = file_config['delimiter']
        germplasm_cols = file_config['germplasm_cols']
        phenotype_cols = file_config['phenotype_cols']
        file_data = read_file(file_name, delimiter, germplasm_cols, phenotype_cols, file_config, 'SORGHUM_SAP')
        raw_data = raw_data + file_data
    workbook.create_phenotype_workbook(raw_data, DS_CONST.SORGHUM_SAP_UNIT_MAP, DIST_PHENOTYPE_FIELD_LIST, EXP_LIST, LOCATION_LIST, PHENOTYPE_FIELD_LIST)

'''
Process Sorghum SAP Germplasm Data
'''
def process_sorghum_sap_germplasm_data():
    print('\bCreating Germplasm WorkBook')
    sorted_germplasm_list = sorted(set(GERMPLASM_DATA_LIST))
    germplasm_data = []
    for germplasm_id in sorted_germplasm_list:
        germplasm_row = [DS_CONST.SORGHUM_SAP_SPECIES_NAME, germplasm_id, '', 'inbred', '', '', '', '', '', '', '']
        germplasm_data.append(germplasm_row)
    workbook.create_germplasm_workbook(germplasm_data)

##############################
# SORGHUM NAM Data processes
##############################
'''
Read Sorghum NAM config and load in memory
'''
def load_sorghum_nam_config():
    global SORGHUM_NAM_CONFIG_DUMP
    with open(DIR_CONST.SORGHUM_NAM_CONFIG) as file:
        SORGHUM_NAM_CONFIG_DUMP = json.load(file)

'''
Process Sorghum NAM Germplasm data
'''
def process_sorgum_nam_germplasm_data(speciesName):
    print('\bCreating Germplasm WorkBook')
    germplasm_data = []
    sorted_germplasm_list = sorted(set(GERMPLASM_DATA_LIST))
    prev_family_index = 0
    for item in sorted_germplasm_list:
        family_index = item[1]
        if(family_index != ''):
            female_parent_id = GERM_CONST.SORGHUM_NAM_HUB_PARENT
            male_parent_id = GERM_CONST.SORGHUM_NAM_FAM_MAP[int(family_index)]
            germplasm_id = item[0]
            origin = female_parent_id+'_x_'+male_parent_id
            germplasm_row = [speciesName, germplasm_id, '', 'inbred', '', '', origin, female_parent_id, '', male_parent_id, '']
            germplasm_data.append(germplasm_row)
            prev_family_index = family_index
        else:
            female_parent_id = GERM_CONST.SORGHUM_NAM_HUB_PARENT
            male_parent_id = GERM_CONST.SORGHUM_NAM_FAM_MAP[int(prev_family_index)]
            germplasm_id = item[0]
            origin = female_parent_id+'_x_'+male_parent_id
            germplasm_row = [speciesName, germplasm_id, '', 'inbred', '', '', origin, female_parent_id, '', male_parent_id, '']
            germplasm_data.append(germplasm_row)
    workbook.create_germplasm_workbook(germplasm_data)

'''
Pre-process Sorghum NAM Germplasm Data
'''
def pre_preprocess_sorghum_nam_germplasm():
    global GERMPLASM_DATA_LIST
    germplasm_genotype_list = []
    germplasm_phenotype_list = []
    sorted_germplasm_list = sorted(set(GERMPLASM_DATA_LIST))

    for item in sorted_germplasm_list:
        germplasm_phenotype_list.append(item[0])

    with open(DIR_CONST.SORGHUM_NAM_RAW_DIR+'/NAM.germplasms.txt') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            germplasm_genotype_list.append(row['Taxa'])

    missing_germplasm_list = set(germplasm_phenotype_list).symmetric_difference(set(germplasm_genotype_list))
    for germplasm_id in missing_germplasm_list:
        GERMPLASM_DATA_LIST.append(tuple([germplasm_id, '']))


'''
Process Sorghum NAM Phenotype data
'''
def process_sorghum_nam_phenotype_data():
    global PHENOTYPE_FIELD_LIST
    raw_data = []
    load_sorghum_nam_config()
    for file_config in SORGHUM_NAM_CONFIG_DUMP:
        file_name = DIR_CONST.SORGHUM_NAM_RAW_DIR + '/' + file_config['file']
        delimiter = file_config['delimiter']
        germplasm_cols = file_config['germplasm_cols']
        phenotype_cols = file_config['phenotype_cols']
        file_data = read_file(file_name, delimiter, germplasm_cols, phenotype_cols, file_config, 'SORGHUM_NAM')
        raw_data = raw_data + file_data
    workbook.create_phenotype_workbook(raw_data, {}, DIST_PHENOTYPE_FIELD_LIST, EXP_LIST, LOCATION_LIST, PHENOTYPE_FIELD_LIST)

#################################################

def generate_soy_data_files():
    global workbook
    workbook = spreadsheet_helper(experimentName=DS_CONST.SOY_EXP_NAM)
    process_soy_phenotype_data()
    preprocess_soy_germplasm_data()

def generate_maize_data_files():
    global workbook
    workbook = spreadsheet_helper(experimentName=DS_CONST.MAIZE_EXP_NAM)
    process_maize_phenotype_data()
    process_maize_germplasm_data()

def generate_sorghum_DIV_data_files():
    global workbook
    workbook = spreadsheet_helper(experimentName=DS_CONST.SORGHUM_DIV_EXP_NAM)
    preprocess_sorghum_phenotype(DIR_CONST.SORGHUM_RAW_DIR+'/div.common.PT.csv', DIR_CONST.SORGHUM_RAW_DIR+'/div.common.PT_processed.csv')
    process_sorghum_phenotype_data('DIV')
    process_sorghum_germplasm_data()

def generate_sorghum_BAP_data_files():
    global workbook
    workbook = spreadsheet_helper(experimentName=DS_CONST.SORGHUM_BAP_EXP_NAM)
    process_sorghum_phenotype_data('BAP')
    fetch_sorghum_germplasm_taxa()
    process_sorghum_germplasm_data()

def generate_sorghum_sap_data_files():
    global workbook
    workbook = spreadsheet_helper(experimentName=DS_CONST.SORGHUM_SAP_EXP_NAM)
    process_sorghum_sap_phenotype_data()
    process_sorghum_sap_germplasm_data()

def generate_sorghum_nam_data_files():
    global workbook
    workbook = spreadsheet_helper(experimentName=DS_CONST.SORGHUM_NAM_EXP_NAM)
    process_sorghum_nam_phenotype_data()
    pre_preprocess_sorghum_nam_germplasm()
    process_sorgum_nam_germplasm_data(DS_CONST.SORGHUM_SPECIES_NAME)

#################################################
def process_data(arg):
    start_time = time.time()
    # Create Output directory
    pathlib.Path('processed-data').mkdir(parents=True, exist_ok=True)
    if arg == 'SOY':
        generate_soy_data_files()
    elif arg == 'MAIZE':
        generate_maize_data_files()
    elif arg == 'SORGHUM-DIV':
        generate_sorghum_DIV_data_files()
    elif arg == 'SORGHUM-BAP':
        generate_sorghum_BAP_data_files()
    elif arg == 'SORGHUM-SAP':
        generate_sorghum_sap_data_files()
    elif arg == 'SORGHUM-NAM':
        generate_sorghum_nam_data_files()
    total_execution_time = time.time() - start_time
    total_execution_time_ms = repr(total_execution_time).split('.')[1][:3]
    console.success('\bTotal execution time : '+time.strftime("%H:%M:%S.{}".format(total_execution_time_ms), time.gmtime(total_execution_time)))

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hm:d', ['help', 'dataset='])
    except getopt.GetoptError:
        print('\nUSAGE:')
        console.success('process_data.py --dataset <dataset_name>')
        print('\bAvailable datasets :')
        console.error(str(DS_CONST.AVAILABLE_DATASETS))
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('\nUSAGE:')
            console.success('process_data.py --dataset <dataset_name>')
            print('\bAvailable datasets :')
            console.error(str(DS_CONST.AVAILABLE_DATASETS))
            sys.exit()
        elif opt in ('-d', '--dataset'):
            if arg in DS_CONST.AVAILABLE_DATASETS:
                process_data(arg)
            else:
                console.error('Invalid dataset\nRun with -h to see a list of available datasets')

if __name__== "__main__":
    main(sys.argv[1:])
