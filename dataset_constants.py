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

# Maize Data Constants
MAIZE_EXP_NAM = 'maizeNAM'
MAIZE_SPECIES_NAME = 'Zea mays'

MAIZE_PHENOTYPE_FIELD_LIST = [
    "TasselingDate", "SilkingDate",
    "DaysToTassel", "DaysToSilk",
    "leaf_length",	"leaf_width",
    "upper_leaf_angle",	"leaf_angle_boxcox_transformed",
    "dla1", "dla2",
    "dla3", "dta",
    "db", "dc", "dg", "dr",
    "si", "sf", "so",
    "dta", "dts", "asi", "gdd_dta", "gdd_dts", "gdd_asi",
    "DTA", "slb1",	"slb2",
    "cob_diameter", "cob_length", "cob_mass", "ear_mass", "ear_row_num",
    "Days_To_Silk",	"Days_To_Anthesis", "ASI", "ph", "kernel_number", "kernels_per_row",
    "tassel_length", "tassel_primary_branch_num", "total_kernel_weight", "twenty_kernel_weight"
]

MAIZE_PHENOTYPE_UNIT_MAP = {
    "TasselingDate": "date",
    "SilkingDate": "date",
    "DaysToTassel": "days",
    "DaysToSilk": "days",
    "leaf_angle_boxcox_transformed": "NA",
    "dla1": "NA",
    "dla2": "NA",
    "dla3": "NA",
    "db": "NA",
    "dc": "NA",
    "dg": "NA",
    "dr": "NA",
    "si": "NA",
    "sf": "NA",
    "so": "NA",
    "dta": "days",
    "dts": "days",
    "asi": "days",
    "gdd_dta": "NA",
    "gdd_dts": "NA",
    "gdd_asi": "NA",
    "DTA": "days",
    "slb1": "NA",
    "slb2": "NA",
    "cob_diameter": "NA",
    "cob_length": "NA",
    "cob_mass": "NA",
    "ear_mass": "NA",
    "ear_row_num": "NA",
    "Days_To_Silk": "days",
    "Days_To_Anthesis": "days",
    "ASI": "days",
    "ph": "NA",
    "kernel_number": "NA",
    "kernels_per_row": "NA",
    "leaf_length": "NA",
    "leaf_width": "NA",
    "tassel_length": "NA",
    "tassel_primary_branch_num": "NA",
    "total_kernel_weight": "NA",
    "upper_leaf_angle": "degrees",
    "twenty_kernel_weight": "NA"
}
