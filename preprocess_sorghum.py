#!/usr/bin/env python
# encoding: utf-8
'''
Pre-process Sorghum data to a common format
'''
import csv
import re

VALUE_DICT = {
    'Anthracnose': {
        'Resistant': 1.0,
        'Susceptible': 5.0
    },
    'Height Uniformity': {
        'Veryuniform': 1.0,
        'Notuniform': 5.0
    },
    'Rust': {
        'Resistant': 1.0,
        'Susceptible': 5.0
    },
    'Vigor': {
        'Poor': 1,
        'Average': 5,
        'Excellent': 9
    },
    'Ladder Spot': {
        'Resistant': 1.0,
        'Susceptible': 5.0
    },
    'Greenbug Biotype-E': {
        'Resistant': 1,
        'Intermediate': 5,
        'Susceptible': 9
    },
    'Fall Army Worm': {
        'Resistant': 1,
        'Susceptible': 9
    },
    'Zonate Leaf Spot': {
        'Resistant': 1.0,
        'Susceptible': 5.0
    }
}

def preprocess_sorghum_phenotype(file_name, out_file_name):
    with open(file_name, encoding="latin-1") as file:
        file_data = []
        reader = csv.DictReader(file, delimiter=',')
        with open(out_file_name, "w") as outfile:
            csvwriter = csv.writer(outfile)
            csvwriter.writerow(reader.fieldnames)
            for row in reader:
                dict = {}
                split_count = []
                for column in row:
                    split_num = 0
                    value = remove_dictionary_def(row[column])
                    if(';' in value):
                        split_num = value.count(';') + 1
                        dict[column] = value.split(';')
                        split_count.append(split_num)
                    else:
                        row[column] = substitute_values(column, value)

                if len(split_count) > 0:
                    row_cp = []
                    for x in range(max(split_count)):
                        row_cp.append(row)
                        for column in dict:
                            try:
                                row_cp[x][column] = substitute_values(column, dict[column][x])
                            except (IndexError) as e:
                                row_cp[x][column] = ''
                                pass
                        csvwriter.writerow(row_cp[x].values())
                else:
                    csvwriter.writerow(row.values())

def remove_dictionary_def(string):
    text = re.sub(r'\([^)]*\)', '', string)
    text = re.sub(r'\[.*?\]', '', text)
    text = text.replace(' ', '')
    return text

def substitute_values(column, value):
    text = value
    if column in VALUE_DICT:
        val_dict = VALUE_DICT[column]
        if value in val_dict:
            text = val_dict[value]
    return text
