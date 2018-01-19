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
import os.path
from fuzzywuzzy import process, fuzz
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
df01 = dataset[['articlenumber','repo_check','title_string']]
df_dict = df01.set_index('repo_check')['articlenumber'].to_dict()
uq_list = dataset['title_string'].tolist()
del i,in_file_name,in_file_name_part_1


# processing prep & init starts here
df01['article_num_sel'] = 0
df01['uq_tested'] = ''
# processing prep & init ends here


pre_processing_time = time.time() - start_time_pre_processing
    
    
# logic for iteration starts here
execution_time_start = time.time()
df01['articlenumber'] = df01['articlenumber'].astype(int)
for i in range(len(uq_list)):
    print ("counter_1: ",i)
    matched_question = process.extractOne(uq_list[i],
                                          choices=df01.loc[:, 'repo_check'],
                                          scorer=fuzz.partial_ratio,
                                          score_cutoff=20)[0]
    df01.loc[i,'article_num_sel'] = int(df_dict[matched_question])
    df01.loc[i,'uq_tested'] = uq_list[i]
    matched_question = ''

    # post processing memoery cleaning ends here

    
execution_time = time.time() - execution_time_start
# logic for iteration ends here


# perofrmance check starts here
df01['check'] = np.where(df01['articlenumber'] == df01['article_num_sel'], 'yes', 'no')
# perofrmance check ends here


#finalizing the file name & path starts here
i = 0
while True:
    out_file_report = str('reports/'  + 'fuzzy_report_no_' + str(i) + '.csv')
    out_file_performance = str('performance/'  + 'fuzzy_perf_no_' + str(i) + '.txt')
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
df01.to_csv(out_file_report, index=False)
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
