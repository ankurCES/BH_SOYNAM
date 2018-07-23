#!/usr/bin/env python
# encoding: utf-8
'''
Constants for Phenotype measures
'''

# Config File Path
FILE_COLUMN_CONFIG = 'csv-data/column_map.config.json'
FILE_COLUMN_CONFIG_REV = 'csv-data/column_reverse_map.config.json'
FILE_DATA_CSV = 'csv-data/raw_data_csv.txt'

# Worksheet Names
EXPERIMENTS_SHEET = 'Experiments'
LOCATIONS_SHEET = 'Locations'
PHENOTYPES_SHEET = 'Phenotypes'
PHENOTYPE_MEASURES_SHEET = 'Phenotype Measures'

# Worksheet headers
EXPERIMENT_HEADERS = [ 'ExperimentName', 'Location', 'Field', 'PlantingDate', 'HarvestDate', 'Stage', 'Season', 'Year' ]
LOCATION_HEADERS = [ 'Region', 'Country', 'Location', 'Field', 'LowerLeftCoordinate', 'UpperLeftCoordinate', 'LowerRightCoordinate', 'UpperRightCoordinate', 'CoordinateType' ]
PHENOTYPE_HEADERS = [ 'PhenotypeCode', 'UnitOfMeasure', 'Description', 'MinThreshold', 'MaxThreshold' ]
PHENOTYPE_MEASURES_HEADERS = [ 'Experiment', 'Entry', 'Location', 'Field', 'Rep', 'Plot', 'Range', 'Row', 'GermplasmId', 'Phenotype', 'Value' ]

# Experiment Name DataSets
GERM_ID = 'Original Strain'
YEAR = 'Year'
LOCATION = 'Loc'
FAMILY = 'Family'
FAM_NO = 'FamNo'

# Phenotype Measures Field Names
PHENOTYPE_FIELD_LIST = [ 'Ht (in)', 'Ht (cm)', 'Days to Mat', 'Lod', 'Yld (bu/a)', 'Yld (kg/ha)', 'Moisture', 'Protein', 'Oil', 'Fiber', '100 sdwt (g)']

# Unit of Measure Mapping
PHENOTYPE_UNIT_MAP = {
    'Ht (in)':'inches',
    'Ht (cm)':'cm',
    'Days to Mat':'days',
    'Lod':'NA',
    'Yld (bu/a)':'bushels/acre',
    'Yld (kg/ha)':'kilograms/hectare',
    'Moisture':'percent',
    'Protein':'percent',
    'Oil':'percent',
    'Fiber':'percent',
    '100 sdwt (g)':'grams'
}

# Phenotype Measures Column List
PHENOTYPE_COLUMN_LIST = ['Experiment', 'Entry', 'Location', 'Field', 'Rep', 'Plot', 'Range', 'Row', 'GermplasmId', 'Phenotype', 'Value']
