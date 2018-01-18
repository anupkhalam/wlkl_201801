#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 13:31:17 2017

@author: anup
"""

import time
from html.parser import HTMLParser
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
import os.path
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


#user_input processing starts here
dataset['tokenized_title'] = dataset['title'].str.replace('\n', ' ')
dataset['tokenized_title'] = dataset['tokenized_title'].str.replace('\t', ' ')
dataset['tokenized_title'] = dataset['tokenized_title'].str.replace('-', '')
dataset['tokenized_title'] = dataset['tokenized_title'].str.replace("'s", "subs1")
dataset['tokenized_title'] = dataset['tokenized_title'].str.replace("n't", " not")
dataset['tokenized_title'] = dataset['tokenized_title'].map(lambda x: re.sub('[^A-Za-z0-9\"\']+', ' ', x))
dataset['tokenized_title'] = dataset.tokenized_title.apply(lambda x: x.lower())
dataset['tokenized_title'] = dataset.tokenized_title.apply(lambda x: x.split())
dataset['tokenized_title'] = dataset['tokenized_title'].apply(lambda x: [item for item in x if item not in stop_words])
dataset['tokenized_title'] = dataset['tokenized_title'].apply(lambda x: list(set(x)))
#user_input processing ends here


#html processing starts here
dataset['parsed_html'] = dataset.details__c.apply(html_to_text)
dataset['parsed_html'].fillna('', inplace=True)
dataset['parsed_html'] = dataset['parsed_html'].str.replace('\n', ' ')
dataset['parsed_html'] = dataset['parsed_html'].str.replace('\t', ' ')
dataset['parsed_html'] = dataset['parsed_html'].str.replace('-', '')
dataset['parsed_html'] = dataset['parsed_html'].str.replace("'s", "subs1")
dataset['parsed_html'] = dataset['parsed_html'].str.replace("n't", " not")
dataset['parsed_html'] = dataset['parsed_html'].map(lambda x: re.sub('[^A-Za-z0-9\"\']+', ' ', x))
dataset['parsed_html'] = dataset['parsed_html'].map(lambda x: re.sub(r'Resolution.+', '', x))
dataset['parsed_html'] = dataset.parsed_html.apply(lambda x: x.lower())
#html processing ends here


#input_method__c processing starts here
dataset['input_method__c'].fillna('xxxnovaluesxxx', inplace=True)
dataset['input_method__c'] = dataset['input_method__c'].str.replace('\n', ' ')
dataset['input_method__c'] = dataset['input_method__c'].str.replace('\t', ' ')
dataset['input_method__c'] = dataset['input_method__c'].str.replace('-', '')
dataset['input_method__c'] = dataset['input_method__c'].str.replace("'s", "subs1")
dataset['input_method__c'] = dataset['input_method__c'].str.replace("n't", " not")
dataset['input_method__c'] = dataset['input_method__c'].map(lambda x: re.sub('[^A-Za-z0-9\"\']+', ' ', x))
dataset['input_method__c'] = dataset.input_method__c.apply(lambda x: x.lower())
#input_method__c processing ends here


#summary processing starts here
dataset['summary'].fillna('', inplace=True)
dataset['summary'] = dataset['summary'].str.replace('\n', ' ')
dataset['summary'] = dataset['summary'].str.replace('\t', ' ')
dataset['summary'] = dataset['summary'].str.replace('-', '')
dataset['summary'] = dataset['summary'].str.replace("'s", "subs1")
dataset['summary'] = dataset['summary'].str.replace("n't", " not")
dataset['summary'] = dataset['summary'].map(lambda x: re.sub('[^A-Za-z0-9\"\']+', ' ', x))
dataset['summary'] = dataset.summary.apply(lambda x: x.lower())
dataset['summary'] = dataset.summary.apply(lambda x: ' '.join(x.split()[0:25]))
#summary processing ends here


#title processing starts here
dataset['title'].fillna('', inplace=True)
dataset['title'] = dataset['title'].str.replace('\n', ' ')
dataset['title'] = dataset['title'].str.replace('\t', ' ')
dataset['title'] = dataset['title'].str.replace('-', '')
dataset['title'] = dataset['title'].str.replace("'s", "subs1")
dataset['title'] = dataset['title'].str.replace("n't", " not")
dataset['title'] = dataset['title'].map(lambda x: re.sub('[^A-Za-z0-9\"\']+', ' ', x))
dataset['title'] = dataset.title.apply(lambda x: x.lower())
#title processing ends here


#string concatenation starts here
# title + summary + input
dataset['tokenized_entry'] = dataset['title'].map(str) + ' ' + dataset['summary'].map(str) + ' ' + dataset['input_method__c'].map(str)
out_file_name_part_1 = 'kb_tit_sum_inp_v_'

# title + summary + html + input
#dataset['tokenized_entry'] = dataset['title'].map(str) + ' ' + dataset['summary'].map(str) + ' ' + dataset['parsed_html'].map(str) + ' ' + dataset['input_method__c'].map(str)
#out_file_name_part_1 = 'kb_tit_sum_htm_inp_v_'

# title + input
#dataset['tokenized_entry'] = dataset['title'].map(str) + ' ' + dataset['input_method__c'].map(str)
#out_file_name_part_1 = 'kb_tit_inp_v_'

#string concatenation ends here


#concatenated string processing starts here
dataset['tokenized_entry'] = dataset['tokenized_entry'].str.replace('xxxnovaluesxxx', '')
dataset['tokenized_entry'] = dataset.tokenized_entry.apply(lambda x: x.split())
dataset['tokenized_entry'] = dataset['tokenized_entry'].apply(lambda x: [item for item in x if item not in stop_words])
dataset['tokenized_entry'] = dataset['tokenized_entry'].apply(lambda x: list(set(x)))
#concatenated string processing ends here


# processing prep & init starts here
dataset['tokenized_entry_string'] = ''
dataset['tokenized_title_str'] = ''
dataset['token_length'] = ''
dataset['diagnostic_number'] = 0
counter_1 = 0
# processing prep & init ends here


# logic for iteration starts here
dataset['token_length'] = dataset['tokenized_entry'].apply(len)
for index, row in dataset.iterrows():
    print ("counter_1: ",counter_1)
    word_list = row['tokenized_title']
    word_list = list(set(word_list))
    tokenized_entry_list = row['tokenized_entry']
    tokenized_entry_str = ' '.join(tokenized_entry_list)
    tokenized_title_list = row['tokenized_title']
    tokenized_title_str = ' '.join(tokenized_title_list)
    
    dataset.loc[counter_1,'tokenized_entry_string'] = tokenized_entry_str
    dataset.loc[counter_1,'tokenized_title_str'] = tokenized_title_str
    
    
    #adding column for diagonostic message starts here
    if 'diagnostic' in word_list:
        diagnostic_title = row['title']
        diagnostic_num = re.findall(r"\D(\d{5})\D", diagnostic_title)
        if not diagnostic_num:
            pass
        else:
            dataset.loc[counter_1,'diagnostic_number'] = int(diagnostic_num[0])
        del diagnostic_title, diagnostic_num
    #adding column for diagonostic message ends here
    
    
    # post processing memory cleaning starts here
    del word_list, tokenized_entry_list, tokenized_entry_str, tokenized_title_list, tokenized_title_str
    counter_1 +=1
    # post processing memoery cleaning ends here
    

#cleaning the dataset for better view starts here
print("--- %s seconds ---" % (time.time() - start_time))
#cleaning the dataset for better view ends here
# logic for iteration ends here


#selecting columns to write to csv file starts here
dataset_dup_remd = dataset.drop_duplicates(subset=['articlenumber'], keep='first')
column_list_loc = ['title','summary','articlenumber','parsed_html','tokenized_entry','tokenized_entry_string','input_method__c','token_length','diagnostic_number','tokenized_title_str']
column_list_ser = ['title','articlenumber','tokenized_entry_string','input_method__c','diagnostic_number']
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





