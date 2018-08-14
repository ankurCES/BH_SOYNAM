#!/usr/bin/env python
# encoding: utf-8
'''
Constants for Different Datasets
'''
# AVAILABLE DATASETS
AVAILABLE_DATASETS = ['SOY', 'MAIZE', 'SORGHUM-BAP', 'SORGHUM-DIV']

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

MAIZE_PHENOTYPE_DUP_MAP = {
	'dta': 0,
	'slb1': 0,
	'slb2': 0,
	'dts': 0,
	'asi': 0,
	'leaf_length': 0,
	'leaf_width': 0,
	'upper_leaf_angle': 0,
	'leaf_angle_boxcox_transformed': 0
}

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

# SORGHUM Constants

SORGHUM_BAP_EXP_NAM = 'sorghumBAP'
SORGHUM_DIV_EXP_NAM = 'sorghumDiversity'
SORGHUM_SPECIES_NAME = 'Sorghum bicolor'

SORGHUM_PHENOTYPE_FIELD_LIST = [
    "canopy_height",
    "seedling_vigor",
    "leaf_angle",
    "leaf_width",
    "emergence_score",
    "leaf_length",
    "stem_width",
    "lodging_percent",
    "Sugar_content",
    "crude_protein",
    "adf",
    "ndf",
    "aboveground_biomass_moisture",
    "coleoptile_color",
    "flowering_time",
    "aboveground_fresh_biomass_per_plot",
    "plant_basal_tiller_number",
    "stem_elongated_internodes_number",
    "canopy_cover",
    "stalk_diameter_major_axis",
    "stalk_diameter_minor_axis",
    "stalk_diameter_fixed_height",
    "leaf_desiccation_present",
    "lodging_present",
    "panicle_height",
    "planter_seed_drop",
    "stand_count",
    "emergence_count",
    "seedling_emergence_rate",
    "aboveground_dry_biomass",
    "dry_matter_fraction",
    "harvest_lodging_rating",
    "aboveground_fresh_biomass",
    "flag_leaf_emergence_time",
    "grain_stage_time",
    "surface_temperature_leaf",
    "leaf_stomatal_conductance",
    "chlorophyll_index",
    "flavonol_index",
    "anthocyanin_index",
    "NBI_nitrogen_balance_index",
    "absorbance_850",
    "roll",
    "PhiNO",
    "PhiNPQ",
    "absorbance_530",
    "absorbance_605",
    "absorbance_730",
    "absorbance_880",
    "absorbance_940",
    "Fs",
    "NPQt",
    "qL",
    "qP",
    "RFd",
    "SPAD_530",
    "SPAD_605",
    "SPAD_730",
    "leaf_thickness",
    "ambient_humidity",
    "leaf_angle_clamp_position",
    "pitch",
    "proximal_air_temperature",
    "FvP/FmP",
    "gH+",
    "ECSt",
    "leaf_temperature_differential",
    "Phi2",
    "relative_chlorophyll",
    "FmPrime",
    "FoPrime",
    "LEF",
    "SPAD_420",
    "SPAD_650",
    "SPAD_850",
    "SPAD_880",
    "light_intensity_PAR",
    "vH+",
    "absorbance_650",
    "absorbance_420",
    "surface_temperature"
]

SORGHUM_DIV_PHENOTYPE_FIELD_LIST = [
    "SEED WEIGHT", "Brix", "Plant Height", "Anthracnose", "Basil Tiller", "Desirability Rating",
    "Height Uniformity", "Inflorescence Exsertion", "Panicle Length", "Rust", "Short Day Anthesis", "Vigor",
    "Yield Potential", "Acid Detergent Fiber", "Crude Protein", "Dry Matter Digestibility", "Fat", "Metabolizable Energy",
    "Net Energy for Gain", "Net Energy for Lactation", "Net Energy for Maintenance", "Phosphorous", "Starch",
    "Total Digestible Nutrients", "Greenbug Biotype-E", "ALUMINUM TOXICITY", "Manganese Toxicity", "Fall Army Worm", "Long Day Anthesis", "Ladder Spot", "Zonate Leaf Spot"
]

SORGHUM_UNIT_MAP = {
    "canopy_height": "cm",
    "seedling_vigor": "score",
    "leaf_angle": "NA",
    "leaf_width": "mm",
    "emergence_score": "scale",
    "leaf_length": "mm",
    "stem_width": "mm",
    "lodging_percent": "%",
    "Sugar_content": "%",
    "crude_protein": "%",
    "adf": "%",
    "ndf": "%",
    "aboveground_biomass_moisture": "%",
    "coleoptile_color": "NA",
    "flowering_time": "days",
    "aboveground_fresh_biomass_per_plot": "kg/plot",
    "plant_basal_tiller_number": "NA",
    "stem_elongated_internodes_number": "NA",
    "canopy_cover": "%",
    "stalk_diameter_major_axis": "mm",
    "stalk_diameter_minor_axis": "mm",
    "stalk_diameter_fixed_height": "mm",
    "leaf_desiccation_present": "NA",
    "lodging_present": "NA",
    "panicle_height": "cm",
    "planter_seed_drop": "count",
    "stand_count": "count",
    "emergence_count": "NA",
    "seedling_emergence_rate": "ratio",
    "aboveground_dry_biomass": "kg / ha",
    "dry_matter_fraction": "ratio",
    "harvest_lodging_rating": "NA",
    "aboveground_fresh_biomass": "kg / ha",
    "flag_leaf_emergence_time": "days",
    "grain_stage_time": "days",
    "surface_temperature_leaf": "K",
    "leaf_stomatal_conductance": "mmol/(m¬≤ s)",
    "chlorophyll_index": "ratio",
    "flavonol_index": "ratio",
    "anthocyanin_index": "ratio",
    "NBI_nitrogen_balance_index": "ratio",
    "absorbance_850": "arbitrary absorbance units",
    "roll": "NA",
    "PhiNO": "NA",
    "PhiNPQ": "NA",
    "absorbance_530": "arbitrary absorbance units",
    "absorbance_605": "arbitrary absorbance units",
    "absorbance_730": "arbitrary absorbance units",
    "absorbance_880": "arbitrary absorbance units",
    "absorbance_940": "arbitrary absorbance units",
    "Fs": "NA",
    "NPQt": "NA",
    "qL": "NA",
    "qP": "NA",
    "RFd": "NA",
    "SPAD_530": "NA",
    "SPAD_605": "NA",
    "SPAD_730": "NA",
    "leaf_thickness": "mm",
    "ambient_humidity": "%",
    "leaf_angle_clamp_position": "NA",
    "pitch": "NA",
    "proximal_air_temperature": "C",
    "FvP/FmP": "NA",
    "gH+": "NA",
    "ECSt": "NA",
    "leaf_temperature_differential": "C",
    "Phi2": "NA",
    "relative_chlorophyll": "NA",
    "FmPrime": "NA",
    "FoPrime": "NA",
    "LEF": "¬µmol electrons m-1¬†s-1",
    "SPAD_420": "NA",
    "SPAD_650": "NA",
    "SPAD_850": "NA",
    "SPAD_880": "NA",
    "light_intensity_PAR": "NA",
    "vH+": "NA",
    "absorbance_650": "arbitrary absorbance units",
    "absorbance_420": "arbitrary absorbance units",
    "surface_temperature": "C",
    "SEED WEIGHT": "NA",
    "Brix": "NA",
    "Plant Height": "NA",
    "Anthracnose": "NA",
    "Basil Tiller": "NA",
    "Desirability Rating": "NA",
    "Height Uniformity": "NA",
    "Inflorescence Exsertion": "NA",
    "Panicle Length": "NA",
    "Rust": "NA",
    "Short Day Anthesis": "NA",
    "Vigor": "NA",
    "Yield Potential": "NA",
    "Acid Detergent Fiber": "NA",
    "Crude Protein": "NA",
    "Dry Matter Digestibility": "NA",
    "Fat": "NA",
    "Metabolizable Energy": "NA",
    "Net Energy for Gain": "NA",
    "Net Energy for Lactation": "NA",
    "Net Energy for Maintenance": "NA",
    "Phosphorous": "NA",
    "Starch": "NA",
    "Total Digestible Nutrients": "NA",
    "Greenbug Biotype-E": "NA",
    "ALUMINUM TOXICITY": "NA",
    "Manganese Toxicity": "NA",
    "Fall Army Worm": "NA",
    "Long Day Anthesis": "NA",
    "Ladder Spot": "NA",
    "Zonate Leaf Spot": "NA"
}
