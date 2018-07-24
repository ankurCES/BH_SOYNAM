#!/usr/bin/env python
# encoding: utf-8
'''
Constants for Different Datasets
'''

# Soyabean Family
SOY_EXP_NAM = 'soyNAM'
SOY_SPECIES_NAME = 'Glycine Max'

# Phenotype Measures Field Names
SOY_PHENOTYPE_FIELD_LIST = [ 'Ht (in)', 'Ht (cm)', 'Days to Mat', 'Lod', 'Yld (bu/a)', 'Yld (kg/ha)', 'Moisture', 'Protein', 'Oil', 'Fiber', '100 sdwt (g)']

# Unit of Measure Mapping
SOY_PHENOTYPE_UNIT_MAP = {
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

# Further dataset family constansts go here
