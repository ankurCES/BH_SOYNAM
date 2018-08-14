#!/usr/bin/env python
# encoding: utf-8
import re
from dateutil.parser import parse

def data_type_check(data_type, year, phenotype_value):
    if(data_type == 'SOY' and year != '' and year != 'NA' and phenotype_value != 'NA'):
        return True
    elif (data_type == None):
        return True
    elif (data_type == 'SORGHUM'):
        return True
    else:
        return False

def date_pattern_match(value):
    date_pattern = re.compile(r"^(1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])/(?:[0-9]{2})?[0-9]{2}$")
    return date_pattern.match(value)

def germplasm_check(value, data_type = None):
    if data_type == None:
        germplasm_pattern = re.compile(r"^[Z]{1}0[0-2][1-6]")
        return germplasm_pattern.match(value)
    else:
        return True

def sorghum_date_process(value):
    dateString = value.split()
    return parse(dateString[0]).strftime("%Y")

def remove_underscores(value):
    return value.replace('_', '')
