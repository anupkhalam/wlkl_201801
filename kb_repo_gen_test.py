#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:35:30 2018

@author: anup
"""

import time
import pandas as pd
from nltk.corpus import stopwords
import numpy as np
import re
import os.path
start_time = time.time()


#get the latest repo starts here
in_file_name_part_1 = 'kb_tit_sum_inp_v_'
#in_file_name_part_1 = 'kb_tit_sum_htm_inp_v_'
#in_file_name_part_1 = 'kb_tit_inp_v_'

i = 0
while True:
    in_file_name = str('kb_repo/' + in_file_name_part_1 + str(i) + '.csv')
    if os.path.exists(in_file_name):
        i+=1
    else:
        i-=1
        in_file_name = str('kb_repo/' + in_file_name_part_1 + str(i) + '.csv')
        break

del i,in_file_name,in_file_name_part_1
#get the latest repo ends here


dataset = pd.read_csv(in_file_name)
stop_words = set(stopwords.words("english"))

#user_input processing starts here
dataset['tokenized_title'] = dataset['title'].str.replace('\n', ' ')
dataset['tokenized_title'] = dataset['tokenized_title'].str.replace('\t', ' ')
dataset['tokenized_title'] = dataset['tokenized_title'].str.replace('-', '')
dataset['tokenized_title'] = dataset['tokenized_title'].map(lambda x: re.sub('[^A-Za-z0-9]+', ' ', x))
dataset['tokenized_title'] = dataset.tokenized_title.apply(lambda x: x.lower())
dataset['tokenized_title'] = dataset.tokenized_title.apply(lambda x: x.split())
dataset['tokenized_title'] = dataset['tokenized_title'].apply(lambda x: [item for item in x if item not in stop_words])
dataset['tokenized_title'] = dataset['tokenized_title'].apply(lambda x: list(set(x)))
#user_input processing ends here


# processing prep & init starts here
dataset['word_count'] = 0
dataset['article_num_sel'] = 0
dataset['temp'] = 0
counter_1 = 0
counter_2 = 0
# processing prep & init ends here


# logic for iteration starts here
for index, row in dataset.iterrows():
    print ("counter_1: ",counter_1)
    word_list = row['tokenized_title']
    word_list = list(set(word_list))
    for word in word_list:
#        dataset['temp'] = dataset.tokenized_entry.apply(lambda x: x.count(str(word)))
        dataset['temp'] = dataset.tokenized_entry_string.apply(lambda x: len(re.findall(r'(?<!\S)'+ word + r'(?!\S)',x, re.IGNORECASE)))
        dataset['word_count'] = dataset['word_count'].add(dataset['temp'])
    highest_value_row = abs(np.asscalar(np.int16(dataset['word_count'].idxmax())))
    
    
    # logic to forcefully match the row for multiple article number starts here
#    if dataset.loc[counter_1,'word_count'] == dataset['word_count'].max():
#        dataset.loc[counter_1,'article_num_sel'] = int(dataset.loc[counter_1,'articlenumber'])
#        counter_2 += 1
#    else:
#        dataset.loc[counter_1,'article_num_sel'] = int(dataset.loc[highest_value_row,'articlenumber'])
    dataset.loc[counter_1,'article_num_sel'] = int(dataset.loc[highest_value_row,'articlenumber'])
    # logic to forcefully match the row for multiple article number starts here
    
    
    # post processing memoery cleaning starts here
    del word_list, word, highest_value_row
    dataset['word_count'] = 0
    dataset['temp'] = 0
    counter_1 +=1
    # post processing memoery cleaning ends here
    

#cleaning the dataset for better view starts here
dataset = dataset.drop('word_count', 1)
dataset = dataset.drop('temp', 1)
print("--- %s seconds ---" % (time.time() - start_time))
#cleaning the dataset for better view ends here
# logic for iteration ends here


# perofrmance check starts here
dataset['check'] = np.where(dataset['articlenumber'] == dataset['article_num_sel'], 'yes', 'no')
dataset['check'].value_counts()
# perofrmance check ends here


# outlier identification starts here
dataset['article_num_sel'].value_counts()
# outlier identification ends here


