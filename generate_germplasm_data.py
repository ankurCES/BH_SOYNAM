#!/usr/bin/env python
# encoding: utf-8
'''
Generates The germplasm XLSX file in the required template
from the CSV converted data
'''
import xlsxwriter
import time
import term_print as console

# Constant imports
import germplasm_constants as GERM_CONST
import directory as DIR_CONST

'''
Write generated data to an excel file
'''
def create_germplasm_workbook(experimentName, germplasm_data):
    start_time = time.time()
    row_num = 1
    col_num = 0
    germplasm_file = DIR_CONST.OUTPUT_DIR+'/'+experimentName+'_germplasm.xlsx'
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

'''
Pre-process germplasm list
Gets the highest value for family for a given germplasm id
and creates a dictionary
'''
# Remove this if falling back to v1
def preprocess_germplasm_data(experimentName, speciesName, germplasm_list):
    sorted_germplasm_list = sorted(set(germplasm_list))
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
    generate_germplasm_data_v2(experimentName, speciesName, germplasm_family_dict)


'''
Generate the germplasm data from the list of tuples (GermplasmId, Family)
'''
def generate_germplasm_data_v2(experimentName, speciesName, germplasm_dict):
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
