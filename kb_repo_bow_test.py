#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:35:30 2018

@author: anup
"""

import time
import random
import sys
import pandas as pd
import numpy as np
import re
import os.path
from nltk.corpus import stopwords
start_time_pre_processing = time.time()


#get the latest repo starts here
in_file_name_part_1 = 'kb_tit_sum_inp_v_'
#in_file_name_part_1 = 'kb_tit_sum_htm_inp_v_'
#in_file_name_part_1 = 'kb_tit_inp_v_'

i = 1
while True:
    in_file_name = str('kb_repo/' + 'loc_' + in_file_name_part_1 + str(i) + '.csv')
    if os.path.exists(in_file_name):
        i+=1
    else:
        i-=1
        in_file_name = str('kb_repo/' +  'loc_' + in_file_name_part_1 + str(i) + '.csv')
        break
#get the latest repo ends here


#sampling logic starts here
dataset = pd.read_csv(in_file_name)
total_records = len(dataset)
skip_reords = total_records - 1000
del dataset
skip_rows = sorted(random.sample(range(1,total_records),skip_reords))
#sampling logic ends here


dataset = pd.read_csv(in_file_name, skiprows=skip_rows)
dataset = dataset[['title','articlenumber','repo_check','title_string']]
del i,in_file_name,in_file_name_part_1
uq_list = dataset['title_string'].tolist()


# processing prep & init starts here
dataset['word_count'] = 0
dataset['article_num_sel'] = 0
# processing prep & init ends here


pre_processing_time = time.time() - start_time_pre_processing
    

# logic for iteration starts here
execution_time_start = time.time()
for i in range(len(uq_list)):
    print ("counter_1: ",i)
    word_list = uq_list[i].split()
    for word in word_list:
#        dataset['word_count'] = dataset['word_count'].add(dataset.repo_check.apply(lambda x: x.count(str(word))))
        dataset['word_count'] = dataset['word_count'].add(dataset.repo_check.apply(lambda x: len(re.findall(r'(?<!\S)'+ word + r'(?!\S)',x, re.IGNORECASE))))
    highest_value_row = abs(np.asscalar(np.int16(dataset['word_count'].idxmax())))
    dataset.loc[i,'article_num_sel'] = int(dataset.loc[highest_value_row,'articlenumber'])
    # logic to forcefully match the row for multiple article number starts here

    dataset.loc[i,'score'] = int(dataset.loc[highest_value_row,'word_count'])
    dataset.loc[i,'total_words'] = len(word_list)
    dataset.loc[i,'match_ratio'] = (int(dataset.loc[highest_value_row,'word_count']))/(len(word_list))
    del word_list, highest_value_row
    dataset['word_count'] = 0

    
execution_time = time.time() - execution_time_start
dataset = dataset.drop('word_count', 1)
# logic for iteration ends here


# perofrmance check starts here
dataset['check'] = np.where(dataset['articlenumber'] == dataset['article_num_sel'], 'yes', 'no')
# perofrmance check ends here


#finalizing the file name & path starts here
i = 0
while True:
    out_file_report = str('reports/'  + 'bow_report_no_' + str(i) + '.csv')
    out_file_performance = str('performance/'  + 'bow_perf_no_' + str(i) + '.txt')
    if os.path.exists(out_file_report):
        i+=1
    else:
        with open(out_file_report, "w") as empty_csv_report:
            pass
        with open(out_file_performance, "w") as empty_txt_performance:
            pass
        break
#finalizing the file name & path ends here
        

#writing outputs starts here
dataset.to_csv(out_file_report, index=False)
filename  = open(out_file_performance,'w')
sys.stdout = filename

# outlier identification starts here
print (dataset['check'].value_counts())
print (dataset['article_num_sel'].value_counts().nlargest(5))
print ("Pre-processing time: ",round(pre_processing_time,3)," seconds")
print ("Execution time: ",round(execution_time,3)," seconds")
print ("Time required for one respose: ",round(execution_time/47307,3)," seconds")
# outlier identification ends here
#writing outputs ends here
