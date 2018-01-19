#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 09:30:05 2018

@author: anup
"""

dataset['summary_count'] = 0
dataset['summary_count'] = dataset.summary.apply(lambda x: len(x.split()))
dataset['summary_count'].mean()
dataset['summary_count'].max()

import pandas as pd
df_test = pd.read_csv('kb_repo/loc_kb_tit_sum_inp_v_2.csv')

df04 = df01.iloc[0:9003,:]
df04['check'] = np.where(df04['articlenumber'] == df04['article_num_sel'], 'yes', 'no')
df04.to_csv('report3.csv', index=False)
df04['check'].value_counts()

matched_question = process.extractOne('la it565 it565b k1s printed',
                                      choices=df01.loc[:, 'repo_check'],
                                      scorer=fuzz.ratio,
                                      score_cutoff=50)

fuzz.ratio("la it565 it565b k1s printed", "la it565 it565b k1s printed print client's louisiana form it565 return schedules k1 printed")
fuzz.partial_ratio("la it565 it565b k1s printed", "la it565 it565b k1s printed print client's louisiana form it565 return schedules k1 printed")

fuzz.ratio("la it565 it565b k1s printed", "report 10610 reprinted  ")
fuzz.partial_ratio("la it565 it565b k1s printed", "report 10610 reprinted  ")

fuzz.ratio("change direct deposit checks", "change direct deposit checks article explains change direct deposit information live payroll")
fuzz.ratio("change direct deposit checks", "direct deposit report cas")

dataset['title'].value_counts()

import pandas as pd
import random

n = 47000 #number of records in file
s = 46000 #desired sample size
filename = "data.txt"
skip = sorted(random.sample(range(n),n-s))
skip
len(skip)
df = pd.read_csv('reports/fuzzy_report_no_1.csv')

import shutil
shutil.rmtree('sampling/*')
import glob
import os
files = glob.glob('sampling/*')
for f in files:
    os.remove(f)

#writing random samples for sampling starts here
files_to_delete = glob.glob('sampling/*')
for file_to_delete in files_to_delete:
    os.remove(file_to_delete)

total_records = len(dataset_required_loc)

for sampling_epoch in range(1,11,1):
    sample_file_name = 'sampling/' + 'sample_' + str(sampling_epoch) + '.csv'
    skip_rows = sorted(random.sample(range(total_records),1000))
    dataset_required_loc.to_csv(out_file_name_loc, index=False, skiprows=skip_rows)
#writing random samples for sampling ends here


#sampling logic starts here
dataset = pd.read_csv(in_file_name)
total_records = len(dataset)
skip_reords = total_records - 1000
del dataset
skip_rows = sorted(random.sample(range(total_records),skip_reords))
#sampling logic ends here


import re

k= """You may want taxability rules applied to Stocking Units (SKUs) that are not in your SKU / Product Mapping table. If so, there is a way to set up a default map-to that will treat these unknown SKUs as if they were of a particular Transaction Type Code (PGPI).
To set up a default map-to, please do the following:
Go to Configuration > SKU / Product Mappings. The SKU / Product Mapping tab opens.
Click Add Mapping. The Add SKU / Product Mapping dialog displays.
Enter information in the minimal required fields:
SKU /        Product Value. '-1' (negative one)
Transaction Type Code. The mapping that should be applied to all unknown SKUs
Example: 
    The Transaction Type Code for General Merchandise (taxable everywhere) is 990101 - General Sales.
Reason. 'Default Map-to' plus any other pertinent information, such as who is creating the default map-to 
Start Effective Date and End Effective Date
Click Save.
You will then see the SKU / Product Value of -1 appearing in the SKU table, and any unknown SKUs that are passed to CCH SureTax will be treated as if they were the default CCH SureTax Transaction Type Code listed
"""


j = re.sub(r"^\s+", "", k, flags = re.MULTILINE)

j2 = re.sub(r"[\\n\\t\s+]*", "", k)




