import pandas as pd
import pyxlsb
import numpy as np
import csv
from thefuzz import fuzz, process
from os import path


def data_read(data_path):
    data_loc = data_path
    all_data = pd.read_excel(data_loc, header=0)
    all_data = all_data.sort_values("DESC ITEM")
    all_data = all_data.reset_index(drop=True)
    all_data['COD ITEM'] = all_data['COD ITEM'].astype(np.int64)

    all_data['ORG MOA'] = all_data['ORG. EM QUE O ITEM ESTÁ ATRIBUIDO'].str.contains('312')
    return all_data



'''
def score_range(data, percent):
  min_score = int(data['SCORE'].max() * percent)
  top_score = data[data['SCORE'] > min_score].nlargest(number_max, 'SCORE')
  return top_score[['DESC ITEM', 'COD ITEM', 'ORG MOA', 'SCORE']]
'''


def extract_number(item):
    number_string = ''
    x = 1
    for character in item:
        if character.isnumeric() or character == ' ' or character == 'X':
            number_string += character
        x += 1
    return (number_string)


def score_creator(data, item):
    scores = []
    for single_word in item.split(' '):
        for item_desc in data['DESC ITEM']:
            if not item_desc.find(single_word) == -1:
                # scores.append(fuzz.ratio(item_desc, item))
                # scores.append(fuzz.partial_ratio(item_desc, item))
                letter_score = fuzz.token_sort_ratio(item_desc, item)
                number_in_item = extract_number(item)
                number_in_item_desc = extract_number(item_desc)
                number_score = fuzz.ratio(number_in_item, number_in_item_desc)
                scores.append(int(letter_score * 0.8 + number_score * 0.2))
            else:
                scores.append(0)
        if max(scores) > 55:
            return scores
        else:
            scores = []


def search_item_data(data, item):
    list_of_scores = score_creator(data, item)

    data['SCORE'] = list_of_scores
    data_312 = data[data['ORG MOA'] == True]

    result_312 = data_312.nlargest(5, 'SCORE')
    result_all = data.nlargest(5, 'SCORE')

    result = pd.concat([result_312, result_all], keys=['GMA - 312', 'MDB'])
    result = result.reset_index(drop=True, level=1)
    result = result.reset_index()
    result.index.name = 'NUMERO'
    result = result[['index', 'DESC ITEM', 'COD ITEM']]
    return result

