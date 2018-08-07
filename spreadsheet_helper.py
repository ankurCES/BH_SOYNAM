#!/usr/bin/env python
# encoding: utf-8
import xlsxwriter
import time
import term_print as console
import numpy as np

# Constant imports
import germplasm_constants as GERM_CONST
import directory as DIR_CONST
import phenotype_constants as PHN_CONST
import dataset_constants as DS_CONST


class spreadsheet_helper:

    def __init__(self, experimentName):
        self.__experimentName = experimentName

    def create_phenotype_workbook(self, data, phenotypeUnitMap, phenotypeFieldList, experiment_list, location_list, phenotypeFieldMap):
        '''
        Creates the xlsx phenotype workbook
        '''
        phenotype_measure_file = DIR_CONST.OUTPUT_DIR+'/'+self.__experimentName+'_phenotype_measures.xlsx'
        workbook = xlsxwriter.Workbook(phenotype_measure_file)
        # Create Data Sheets
        experiment_worksheet = workbook.add_worksheet(PHN_CONST.EXPERIMENTS_SHEET)
        location_worksheet = workbook.add_worksheet(PHN_CONST.LOCATIONS_SHEET)
        phenotype_worksheet = workbook.add_worksheet(PHN_CONST.PHENOTYPES_SHEET)
        phenotype_measures_worksheet = workbook.add_worksheet(PHN_CONST.PHENOTYPE_MEASURES_SHEET)

        print('\nCreating Phenotype Measures WorkBook')
        self.__create_experiment_worksheet(experiment_worksheet, 1, 0, experiment_list)
        self.__create_location_worksheet(location_worksheet, 1, 0, location_list)
        self.__create_phenotype_worksheet(phenotype_worksheet, 1, 0, phenotypeUnitMap, phenotypeFieldList, phenotypeFieldMap)
        self.__create_phenotype_measure_worksheet(phenotype_measures_worksheet, 1, 0, data)
        # Finalize writing to workbook
        workbook.close()


    '''
    Creates the xlsx germplasm workbook
    '''
    def create_germplasm_workbook(self, germplasm_data):
        start_time = time.time()
        row_num = 1
        col_num = 0
        germplasm_file = DIR_CONST.OUTPUT_DIR+'/'+self.__experimentName+'_germplasm.xlsx'
        workbook = xlsxwriter.Workbook(germplasm_file)
        # Create Data Sheets
        germplasm_worksheet = workbook.add_worksheet(GERM_CONST.GERMPLASM_SHEET)
        germplasm_worksheet.write_row(0, 0, tuple(GERM_CONST.GERMPLASM_HEADERS))
        for germ_row in germplasm_data:
            germplasm_worksheet.write_row(row_num, col_num, tuple(germ_row))
            row_num += 1
        console.info('* Added germplasm data')
        elapsed_time = time.time() - start_time
        mlsec = repr(elapsed_time).split('.')[1][:3]
        print('\bGermplasm Data written to file in : '+time.strftime("%H:%M:%S.{}".format(mlsec), time.gmtime(elapsed_time)))


    # Internal functions

    def __levenshtein(self, seq1, seq2):
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros ((size_x, size_y))
        for x in range(size_x):
            matrix [x, 0] = x
        for y in range(size_y):
            matrix [0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x-1] == seq2[y-1]:
                    matrix [x,y] = min(
                        matrix[x-1, y] + 1,
                        matrix[x-1, y-1],
                        matrix[x, y-1] + 1
                    )
                else:
                    matrix [x,y] = min(
                        matrix[x-1,y] + 1,
                        matrix[x-1,y-1] + 1,
                        matrix[x,y-1] + 1
                    )
        return int(matrix[size_x - 1, size_y - 1])

    def __create_experiment_worksheet(self, experiment_worksheet, row_num, col_num, experiment_list):
        sorted_experiment_list = sorted(set(experiment_list))
        experiment_worksheet.write_row(0, 0, tuple(PHN_CONST.EXPERIMENT_HEADERS))
        for experiment in sorted_experiment_list:
            experiment_name = experiment[0]
            year = experiment[1]
            location = experiment[2]
            experiment_row = [experiment_name, location, '', '', '', '', '', year]
            experiment_worksheet.write_row(row_num, col_num, tuple(experiment_row))
            row_num += 1
        console.info('* Added experiments data')

    def __create_location_worksheet(self, location_worksheet, row_num, col_num, location_list):
        sorted_location_list = sorted(set(location_list))
        location_worksheet.write_row(0, 0, tuple(PHN_CONST.LOCATION_HEADERS))
        for location in sorted_location_list:
            if location == 'NA':
                location_row = ['NA', 'NA', 'NA', '', '', '', '', '', '']
            else:
                location_row = [1, 'USA', location, '', '', '', '', '', '']
            location_worksheet.write_row(row_num, col_num, tuple(location_row))
            row_num += 1
        console.info('* Added locations data')

    def __create_phenotype_worksheet(self, phenotype_worksheet, row_num, col_num, phenotypeUnitMap, phenotypeFieldList, phenotypeFieldMap):
        phenotype_worksheet.write_row(0, 0, tuple(PHN_CONST.PHENOTYPE_HEADERS))
        local_field_map = {}
        for field in phenotypeFieldList:
            for key in phenotypeUnitMap:
                distance = self.__levenshtein(field.lower(), key.lower())
                if distance < 1:
                    local_field_map[field] = key

        for field in phenotypeFieldList:
            try:
                list = phenotypeFieldMap[field.lower()]
                if field in phenotypeUnitMap:
                    unit_of_measure = phenotypeUnitMap[field]
                elif field in local_field_map:
                    key = local_field_map[field]
                    unit_of_measure = phenotypeUnitMap[key]
                seq_list = [x for x in list if x != 'NA']
                phenotype_row_data = [field.lower(), unit_of_measure, '', min(seq_list), max(seq_list)]
                phenotype_worksheet.write_row(row_num, col_num, tuple(phenotype_row_data))
                row_num += 1
            except ValueError as e:
                pass
        console.info('* Added phenotype data')

    def __create_phenotype_measure_worksheet(self, phenotype_measures_worksheet, row_num, col_num, data):
        phenotype_measures_worksheet.write_row(0, 0, tuple(PHN_CONST.PHENOTYPE_MEASURES_HEADERS))
        for row in data:
            phenotype_measures_worksheet.write_row(row_num, col_num, tuple(row))
            row_num += 1
        console.info('* Added phenotype measures data')
