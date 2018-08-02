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
    "leaf_length", "leaf_width", "tassel_length", "tassel_primary_branch_num", "total_kernel_weight",
    "upper_leaf_angle", "twenty_kernel_weight"
]

MAIZE_PHENOTYPE_UNIT_MAP = {
    'DTA': 'days to anthesis',
    'slb1': 'resistance to southern left blight score1',
    'slb2': 'resistance to southern leave blight score2',
    'dta': 'days to anthesis',
    'dts' :'days to silking',
    'asi': 'anthesis-silking interval',
    'gdd_dta': 'growing degree days of dta',
    'gdd_dts': 'gdd of dts',
    'gdd_asi': 'gdd of asi',
    'db': 'tassel length',
    'dc': 'spike length',
    'dg': 'branch zone',
    'dr': 'branch number',
    'si': 'cob length',
    'sf': 'cob diameter',
    'so': 'ear row number',
    'dla1': 'diseased leaf area measurement1',
    'dla2': 'diseased leaf area measurment2',
    'dla3': 'diseased leaf area measurement3'
}
