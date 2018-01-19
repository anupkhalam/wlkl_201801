#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 13:31:17 2017

@author: anup
"""

import time
import random
import os
import glob
from html.parser import HTMLParser
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
import os.path
from collections import OrderedDict
start_time = time.time()


#html parsing function starts here
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def handle_entityref(self, name):
        self.fed.append('&%s;' % name)
    def convert_charrefs(self, name):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def html_to_text(html):
    s = MLStripper()
    try:
        s.feed(html)
        return s.get_data()
    except Exception as e:
        return html
#html parsing function ends here


dataset = pd.read_csv('kbarticles_20180116.csv')
#dataset = pd.read_csv('kb.csv')
dataset = dataset.iloc[:, [17,21,22,28,29]]
stop_words = set(stopwords.words("english"))

#removing duplicates starts here
dataset = dataset.drop_duplicates(subset=['articlenumber'], keep='first')
dataset = dataset.drop_duplicates(subset=['title'], keep='first')

#removing duplicates ends here


#user_input processing starts here
dataset['title_string'] = dataset['title'].str.replace('\n', ' ')
dataset['title_string'] = dataset['title_string'].str.replace('\t', ' ')
dataset['title_string'] = dataset['title_string'].str.replace('-', '')
dataset['title_string'] = dataset['title_string'].str.replace("n't", "not")
dataset['title_string'] = dataset['title_string'].map(lambda x: re.sub('[^A-Za-z0-9\"\']+', ' ', x))
dataset['title_string'] = dataset.title_string.apply(lambda x: x.lower())
dataset['title_string'] = dataset.title_string.apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
dataset['title_string'] = dataset.title_string.apply(lambda x: ' '.join(OrderedDict((w,w) for w in x.split()).keys()))
#user_input processing ends here


dataset['diagnostic_number'] = dataset['title_string'].apply(lambda x: (re.findall(r"\D(\d{5})\D", x)) if 'diagnostic' in x else 0)


#html processing starts here
dataset['parsed_html'] = dataset.details__c.apply(html_to_text)
dataset['parsed_html'].fillna('', inplace=True)
dataset['parsed_html'] = dataset['parsed_html'].str.replace('\n', ' ')
dataset['parsed_html'] = dataset['parsed_html'].str.replace('\t', ' ')
dataset['parsed_html'] = dataset['parsed_html'].str.replace('-', '')
dataset['parsed_html'] = dataset['parsed_html'].str.replace("n't", "not")
dataset['parsed_html'] = dataset['parsed_html'].map(lambda x: re.sub('[^A-Za-z0-9\"\']+', ' ', x))
dataset['parsed_html'] = dataset['parsed_html'].map(lambda x: re.sub(r'Resolution.+', '', x))
dataset['parsed_html'] = dataset.parsed_html.apply(lambda x: x.lower())
dataset['parsed_html'] = dataset.parsed_html.apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
dataset['parsed_html'] = dataset.parsed_html.apply(lambda x: ' '.join(OrderedDict((w,w) for w in x.split()).keys()))
#html processing ends here


#input_method__c processing starts here
dataset['input_method__c'].fillna('xxxnovaluesxxx', inplace=True)
dataset['input_method__c'] = dataset['input_method__c'].str.replace('\n', ' ')
dataset['input_method__c'] = dataset['input_method__c'].str.replace('\t', ' ')
dataset['input_method__c'] = dataset['input_method__c'].str.replace('-', '')
dataset['input_method__c'] = dataset['input_method__c'].map(lambda x: re.sub('[^A-Za-z0-9\"\']+', ' ', x))
dataset['input_method__c'] = dataset.input_method__c.apply(lambda x: x.lower())
#input_method__c processing ends here


#summary processing starts here
dataset['summary'].fillna('', inplace=True)
dataset['summary_string'] = dataset['summary'].str.replace('\n', ' ')
dataset['summary_string'] = dataset['summary_string'].str.replace('\t', ' ')
dataset['summary_string'] = dataset['summary_string'].str.replace('-', '')
dataset['summary_string'] = dataset['summary_string'].str.replace("n't", "not")
dataset['summary_string'] = dataset['summary_string'].map(lambda x: re.sub('[^A-Za-z0-9\"\']+', ' ', x))
dataset['summary_string'] = dataset.summary_string.apply(lambda x: x.lower())
dataset['summary_string'] = dataset.summary_string.apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
dataset['summary_string'] = dataset.summary_string.apply(lambda x: ' '.join(OrderedDict((w,w) for w in x.split()).keys()))
dataset['summary_string'] = dataset.summary_string.apply(lambda x: ' '.join(x.split()[0:25]))
#summary processing ends here


#string concatenation starts here
# title + summary + input
dataset['repo_check'] = dataset['title_string'].map(str) + ' ' + dataset['summary_string'].map(str) + ' ' + dataset['input_method__c'].map(str)
out_file_name_part_1 = 'kb_tit_sum_inp_v_'

# title + summary + html + input
#dataset['tokenized_entry'] = dataset['title'].map(str) + ' ' + dataset['summary'].map(str) + ' ' + dataset['parsed_html'].map(str) + ' ' + dataset['input_method__c'].map(str)
#out_file_name_part_1 = 'kb_tit_sum_htm_inp_v_'

# title + input
#dataset['tokenized_entry'] = dataset['title'].map(str) + ' ' + dataset['input_method__c'].map(str)
#out_file_name_part_1 = 'kb_tit_inp_v_'

#string concatenation ends here


#concatenated string processing starts here
dataset['repo_check'] = dataset['repo_check'].str.replace('xxxnovaluesxxx', '')
dataset = dataset.drop_duplicates(subset=['repo_check'], keep='first')
dataset['tokenized_repo_check'] = dataset.repo_check.apply(lambda x: x.split())
dataset['token_length'] = dataset['tokenized_repo_check'].apply(len)
#concatenated string processing ends here


#selecting columns to write to csv file starts here
dataset_dup_remd = dataset.drop_duplicates(subset=['articlenumber'], keep='first')
column_list_loc =['title','summary','articlenumber','parsed_html','input_method__c','token_length','diagnostic_number','title_string','repo_check','tokenized_repo_check',]
column_list_ser = ['title','articlenumber','repo_check','input_method__c','diagnostic_number','tokenized_repo_check']
dataset_required_loc = dataset_dup_remd[column_list_loc]
dataset_required_ser = dataset_dup_remd[column_list_ser]
#selecting columns to write to csv file ends here


#finalizing the file name & path starts here
i = 0
while True:
    out_file_name_loc = str('kb_repo/' + 'loc_' + out_file_name_part_1 + str(i) + '.csv')
    out_file_name_ser = str('kb_repo/' + 'ser_' + out_file_name_part_1 + str(i) + '.csv')
    if os.path.exists(out_file_name_loc):
        i+=1
    else:
        with open(out_file_name_loc, "w") as empty_csv_loc:
            pass
        with open(out_file_name_ser, "w") as empty_csv_ser:
            pass
        break
#finalizing the file name & path ends here


# writing to csv file starts here
dataset_required_loc.to_csv(out_file_name_loc, index=False)
dataset_required_ser.to_csv(out_file_name_ser, index=False)
# writing to csv file ends here


print ("Execution time: ", round(time.time()-start_time,3), " seconds")



