#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:35:30 2018

@author: anup
"""

import time
import random
import re
import sys
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import os.path
from fuzzywuzzy import process, fuzz
from collections import OrderedDict
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


dataset = pd.read_csv(in_file_name)
df01 = dataset[['articlenumber','repo_check','title_string']]
df_dict = df01.set_index('repo_check')['articlenumber'].to_dict()
df02 = pd.read_csv('kb_var_0001.csv')
stop_words = set(stopwords.words("english"))
del i,in_file_name,in_file_name_part_1


#processing user question starts here
df02['uq_processed'] = df02['user_question'].str.replace('\n', ' ')
df02['uq_processed'] = df02['uq_processed'].str.replace('\t', ' ')
df02['uq_processed'] = df02['uq_processed'].str.replace('-', '')
df02['uq_processed'] = df02['uq_processed'].str.replace("n't", ' not')
df02['uq_processed'] = df02['uq_processed'].map(lambda x: re.sub('[^A-Za-z0-9\"\']+', ' ', x))
df02['uq_processed'] = df02.uq_processed.apply(lambda x: x.lower())
df02['uq_processed'] = df02.uq_processed.apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
df02['uq_processed'] = df02.uq_processed.apply(lambda x: ' '.join(OrderedDict((w,w) for w in x.split()).keys()))
df02['uq_processed'] = df02['uq_processed'].str.replace('  ', '')
#processing user question ends here


# processing prep & init starts here
df02['article_num_sel'] = 0
# processing prep & init ends here


pre_processing_time = time.time() - start_time_pre_processing
    
    
# logic for iteration starts here
execution_time_start = time.time()
df01['articlenumber'] = df01['articlenumber'].astype(int)
for index, row in df02.iterrows():
    print ("counter_1: ",index)
    uq_processed = row['uq_processed']
    matched_question = process.extractOne(uq_processed,
                                          choices=df01.loc[:, 'repo_check'],
                                          scorer=fuzz.partial_ratio,
                                          score_cutoff=20)[0]
    df02.loc[index,'article_num_sel'] = int(df_dict[matched_question])
    matched_question = ''

execution_time = time.time() - execution_time_start
# logic for iteration ends here


# perofrmance check starts here
df02['check'] = np.where(df02['articlenumber'] == df02['article_num_sel'], 'yes', 'no')
# perofrmance check ends here


#finalizing the file name & path starts here
i = 0
while True:
    out_file_report = str('variation/'  + 'fuzzy_batch_001_no_' + str(i) + '.csv')
    out_file_performance = str('performance/'  + 'fuzzy_var_batch_001_no_' + str(i) + '.txt')
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
df02.to_csv(out_file_report, index=False)
filename  = open(out_file_performance,'w')
sys.stdout = filename

# outlier identification starts here
print (df01['check'].value_counts())
print (df01['article_num_sel'].value_counts().nlargest(5))
print ("Pre-processing time: ",round(pre_processing_time,3)," seconds")
print ("Execution time: ",round(execution_time,3)," seconds")
print ("Time required for one respose: ",round(execution_time/47307,3)," seconds")
# outlier identification ends here
#writing outputs ends here
