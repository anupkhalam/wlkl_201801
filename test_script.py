#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 13:31:17 2017

@author: anup
"""

import time
start_time = time.time()
from html.parser import HTMLParser
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
    

import pandas as pd
dataset = pd.read_csv('kbarticles_20180116.csv')
dataset = dataset.iloc[:, [17,21,22,29]]

import numpy as np
import re
import nltk
from nltk.corpus import stopwords
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


#html processing starts here
#dataset['parsed_html'] = dataset.details__c.apply(html_to_text)
#dataset['parsed_html'].fillna('', inplace=True)
#dataset['parsed_html'] = dataset['parsed_html'].str.replace('\n', ' ')
#dataset['parsed_html'] = dataset['parsed_html'].str.replace('\t', ' ')
#dataset['parsed_html'] = dataset['parsed_html'].str.replace('-', '')
#dataset['parsed_html'] = dataset['parsed_html'].map(lambda x: re.sub('[^A-Za-z0-9]+', ' ', x))
#dataset['parsed_html'] = dataset['parsed_html'].map(lambda x: re.sub(r'Resolution.+', '', x))
#dataset['parsed_html'] = dataset.parsed_html.apply(lambda x: x.lower())
#html processing ends here


#input_method__c processing starts here
dataset['input_method__c'].fillna('xxxnovaluesxxx', inplace=True)
dataset['input_method__c'] = dataset['input_method__c'].str.replace('\n', ' ')
dataset['input_method__c'] = dataset['input_method__c'].str.replace('\t', ' ')
dataset['input_method__c'] = dataset['input_method__c'].str.replace('-', '')
dataset['input_method__c'] = dataset['input_method__c'].map(lambda x: re.sub('[^A-Za-z0-9]+', ' ', x))
dataset['input_method__c'] = dataset.input_method__c.apply(lambda x: x.lower())
#input_method__c processing ends here


#summary processing starts here
dataset['summary'].fillna('', inplace=True)
dataset['summary'] = dataset['summary'].str.replace('\n', ' ')
dataset['summary'] = dataset['summary'].str.replace('\t', ' ')
dataset['summary'] = dataset['summary'].str.replace('-', '')
dataset['summary'] = dataset['summary'].map(lambda x: re.sub('[^A-Za-z0-9]+', ' ', x))
dataset['summary'] = dataset.summary.apply(lambda x: x.lower())
#summary processing ends here


#title processing starts here
dataset['title'].fillna('', inplace=True)
dataset['title'] = dataset['title'].str.replace('\n', ' ')
dataset['title'] = dataset['title'].str.replace('\t', ' ')
dataset['title'] = dataset['title'].str.replace('-', '')
dataset['title'] = dataset['title'].map(lambda x: re.sub('[^A-Za-z0-9]+', ' ', x))
dataset['title'] = dataset.title.apply(lambda x: x.lower())
#title processing ends here


#string concatenation starts here
# title + summary + input
dataset['tokenized_entry'] = dataset['title'].map(str) + ' ' + dataset['summary'].map(str) + ' ' + dataset['input_method__c'].map(str)

# title + summary + html + input
#dataset['tokenized_entry'] = dataset['title'].map(str) + ' ' + dataset['summary'].map(str) + ' ' + dataset['parsed_html'].map(str) + ' ' + dataset['input_method__c'].map(str)

# title + input
#dataset['tokenized_entry'] = dataset['title'].map(str) + ' ' + dataset['input_method__c'].map(str)

#string concatenation ends here


#concatenated string processing starts here
dataset['tokenized_entry'] = dataset['tokenized_entry'].str.replace('xxxnovaluesxxx', '')
dataset['tokenized_entry'] = dataset.tokenized_entry.apply(lambda x: x.split())
dataset['tokenized_entry'] = dataset['tokenized_entry'].apply(lambda x: [item for item in x if item not in stop_words])
dataset['tokenized_entry'] = dataset['tokenized_entry'].apply(lambda x: list(set(x)))
#concatenated string processing ends here


# processing prep & init starts here
dataset['word_count'] = 0
dataset['article_num_sel'] = 0
dataset['tokenized_entry_string'] = ''
dataset['token_length'] = ''
dataset['diagnostic_number'] = 0
dataset['temp'] = 0
counter_1 = 0
counter_2 = 0
# processing prep & init ends here


# logic for iteration starts here
dataset['token_length'] = dataset['tokenized_entry'].apply(len)
for index, row in dataset.iterrows():
    print ("counter_1: ",counter_1)
    word_list = row['tokenized_title']
    word_list = list(set(word_list))
    tokenized_entry_list = row['tokenized_entry']
    tokenized_entry_str = ' '.join(tokenized_entry_list)
    dataset.loc[counter_1,'tokenized_entry_string'] = tokenized_entry_str
    for word in word_list:
        dataset['temp'] = dataset.tokenized_entry.apply(lambda x: x.count(str(word)))
        dataset['word_count'] = dataset['word_count'].add(dataset['temp'])
    highest_value_row = np.asscalar(np.int16(dataset['word_count'].idxmax()))
    
    
    # logic to forcefully match the row for multiple article number starts here
#    if dataset.loc[counter_1,'word_count'] == dataset['word_count'].max():
#        dataset.loc[counter_1,'article_num_sel'] = int(dataset.loc[counter_1,'articlenumber'])
#        counter_2 += 1
#    else:
#        dataset.loc[counter_1,'article_num_sel'] = int(dataset.loc[highest_value_row,'articlenumber'])
    dataset.loc[counter_1,'article_num_sel'] = int(dataset.loc[highest_value_row,'articlenumber'])
    # logic to forcefully match the row for multiple article number starts here
    
    
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
    
    
    # post processing memoery cleaning starts here
    del word_list, word, highest_value_row, tokenized_entry_list, tokenized_entry_str
    dataset['word_count'] = 0
    dataset['temp'] = 0
    counter_1 +=1
    # post processing memoery cleaning ends here
    
    
dataset = dataset.drop('word_count', 1)
dataset = dataset.drop('temp', 1)
print("--- %s seconds ---" % (time.time() - start_time))
# logic for iteration ends here


# perofrmance check starts here
dataset['check'] = np.where(dataset['articlenumber'] == dataset['article_num_sel'], 'yes', 'no')
dataset['check'].value_counts()
# perofrmance check ends here


# writing to csv file starts here
dataset = dataset.drop_duplicates(subset=['articlenumber'], keep='first')
dataset1 = dataset.iloc[:, [0,1,2,4,7,9,10,11]]
dataset1.to_csv('kb_repo_tit_sum_input_many.csv', index=False)
#dataset1.to_csv('kb_repo_tit_sum_input_stem.csv', index=False)
#dataset1.to_csv('kb_repo_tit_sum_html_input.csv', index=False)
#dataset1.to_csv('kb_repo_tit_sum_html_input_stem.csv', index=False)
#dataset1.to_csv('kb_repo_tit_input.csv', index=False)
#dataset1.to_csv('kb_repo_html_input.csv', index=False)
# writing to csv file ends here


# outlier identification starts here
dataset['article_num_sel'].value_counts()
# outlier identification ends here
