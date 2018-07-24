#!/usr/bin/env python
# encoding: utf-8
'''
Generates The phenotype XLSX file in the required template
from the CSV converted data
'''
import xlsxwriter
import json
import csv
import time
import term_print as console

from generate_germplasm_data import preprocess_germplasm_data
# Constants Imports
import directory as DIR_CONST
import phenotype_constants as PHN_CONST

PHENOTYPE_FIELD_LIST = {}
PHENOTYPE_FIELD_MAP = {}
PHENOTYPE_FIELD_MAP_REV = {}

LOCATION_LIST = []
EXP_LIST = []
GERMPLASM_DATA_LIST = []

'''
Creates the xlsx phenotype datasheet
'''
def create_phenotype_datasheet(experimentName, data, phenotypeFieldList, phenotypeUnitMap):

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
    create_phenotype_worksheet(phenotype_worksheet, 1, 0, phenotypeFieldList, phenotypeUnitMap)
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
        experiment_row = [experiment_name, location, '', '', '', '', '', int(year)]
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

def create_phenotype_worksheet(phenotype_worksheet, row_num, col_num, phenotypeFieldList, phenotypeUnitMap):
    global PHENOTYPE_FIELD_LIST
    phenotype_worksheet.write_row(0, 0, tuple(PHN_CONST.PHENOTYPE_HEADERS))
    for field in phenotypeFieldList:
        list = PHENOTYPE_FIELD_LIST[field]
        unit_of_measure = phenotypeUnitMap[field]
        phenotype_row_data = [field, unit_of_measure, '', min(list), max(list)]
        phenotype_worksheet.write_row(row_num, col_num, tuple(phenotype_row_data))
        row_num += 1
    console.info('* Added phenotype data')

def create_phenotype_measure_worksheet(phenotype_measures_worksheet, row_num, col_num, data):
    phenotype_measures_worksheet.write_row(0, 0, tuple(PHN_CONST.PHENOTYPE_MEASURES_HEADERS))
    for row in data:
        phenotype_measures_worksheet.write_row(row_num, col_num, tuple(row))
        row_num += 1
    console.info('* Added phenotype measures data')

'''
Read the CSV pre-processed data by the list of indices
'''
def read_delimited_data(experimentName, filename, indices):
    global GERMPLASM_DATA_LIST
    read_data = []
    with open(filename, 'rt') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            year = row[get_column_index_by_name(PHN_CONST.FILE_COLUMN_CONFIG, PHN_CONST.YEAR)]
            experiment_name = experimentName + '_' + year
            germplasm_id = row[get_column_index_by_name(PHN_CONST.FILE_COLUMN_CONFIG, PHN_CONST.GERM_ID)];
            location = row[get_column_index_by_name(PHN_CONST.FILE_COLUMN_CONFIG, PHN_CONST.LOCATION)];
            family_name = row[get_column_index_by_name(PHN_CONST.FILE_COLUMN_CONFIG, PHN_CONST.FAMILY)];
            family_num = row[get_column_index_by_name(PHN_CONST.FILE_COLUMN_CONFIG, PHN_CONST.FAM_NO)]
            GERMPLASM_DATA_LIST.append(tuple([germplasm_id, family_name, family_num]))
            for index in indices:
                try:
                    if row[index] != '.' and row[index] != '#VALUE!':
                        row_templ = [experiment_name, '', location, '', '', '', '', '', germplasm_id]
                        fieldname = get_column_index_by_name(PHN_CONST.FILE_COLUMN_CONFIG_REV, str(index))
                        value = float(row[index])
                        row_templ.append(fieldname)
                        row_templ.append(value)
                        add_to_phenotype_field_list(fieldname, value)
                        add_exp_loc_list(experiment_name, year, location)
                        read_data.append(row_templ)
                except (IndexError, ValueError) as e:
                    pass
                continue
            console._print('Processed %d records' % len(read_data))
    file.close()
    return read_data

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
Returns the index of the field by name from the generated config json file
'''
def get_column_index_by_name(filename, fieldname):
    if(filename == PHN_CONST.FILE_COLUMN_CONFIG):
        return PHENOTYPE_FIELD_MAP[fieldname]
    elif(filename == PHN_CONST.FILE_COLUMN_CONFIG_REV):
        return PHENOTYPE_FIELD_MAP_REV[fieldname]
    else:
        return None

'''
Returns the indices of the fields needed from the generated column config json file
'''
def get_column_indices_by_name(filename, phenotypeFieldList):
    field_indices = []
    for fieldname in phenotypeFieldList:
        index = get_column_index_by_name(filename, fieldname)
        field_indices.append(index)
    return field_indices

'''
Load the Column mappings in memory
'''
def load_column_mappings(phenotypeFieldList):
    global PHENOTYPE_FIELD_LIST
    for field in phenotypeFieldList:#PHN_CONST.PHENOTYPE_FIELD_LIST:
        PHENOTYPE_FIELD_LIST[field] = []

    try:
        with open(PHN_CONST.FILE_COLUMN_CONFIG) as file:
            global PHENOTYPE_FIELD_MAP
            PHENOTYPE_FIELD_MAP = json.load(file)
        file.close()

        with open(PHN_CONST.FILE_COLUMN_CONFIG_REV) as file:
            global PHENOTYPE_FIELD_MAP_REV
            PHENOTYPE_FIELD_MAP_REV = json.load(file)
        file.close()
    except IOError as e:
        console.error('I/O error', str(e))
        quit()
    except:
        console.error('An error has occured')
        quit()

def generate_phenotype_measures_data(experimentName, speciesName, phenotypeFieldList, phenotypeUnitMap):
    start_time = time.time()
    load_column_mappings(phenotypeFieldList)
    indices = get_column_indices_by_name(PHN_CONST.FILE_COLUMN_CONFIG, phenotypeFieldList)
    data = read_delimited_data(experimentName, PHN_CONST.FILE_DATA_CSV, indices)
    create_phenotype_datasheet(experimentName, data, phenotypeFieldList, phenotypeUnitMap)
    elapsed_time = time.time() - start_time
    mlsec = repr(elapsed_time).split('.')[1][:3]
    print('\bPhenoType Measures data file generated in : '+time.strftime("%H:%M:%S.{}".format(mlsec), time.gmtime(elapsed_time)))
    preprocess_germplasm_data(experimentName, speciesName, GERMPLASM_DATA_LIST)
