#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 23:00:05 2017

@author: anup
"""

import pandas as pd
df01 = pd.read_csv('kb_q.csv')
counter_3 = 0
df02 = pd.DataFrame()
df02['articlenumber'] = ''
df02['user_question'] = ''
for index, row1 in df01.iterrows():
    df02.loc[counter_3,'articlenumber'] = row1['articlenumber']
    counter_3 += 1
    df02.loc[counter_3,'articlenumber'] = row1['articlenumber']
    df02.loc[counter_3,'user_question'] = row1['q1']
    counter_3 += 1
    df02.loc[counter_3,'articlenumber'] = row1['articlenumber']
    df02.loc[counter_3,'user_question'] = row1['q2']
    counter_3 += 1
    df02.loc[counter_3,'articlenumber'] = row1['articlenumber']
    df02.loc[counter_3,'user_question'] = row1['q3']
    counter_3 += 1
    df02.loc[counter_3,'articlenumber'] = row1['articlenumber']
    df02.loc[counter_3,'user_question'] = row1['q4']
    counter_3 += 1




df02 = df02.dropna()

df02.to_csv('kb_testing_v1.csv', index=False)
del df01, df02, counter_3, row1


#####################################################
import time
start_time = time.time()
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))

#dataset = pd.read_csv('kb_repo.csv')
#dataset = pd.read_csv('kb_repo_tit_sum_html_input.csv')
dataset = pd.read_csv('kb_repo_tit_sum_input.csv')
#dataset = pd.read_csv('kb_repo_tit_sum_input.csv')
#dataset = pd.read_csv('kb_repo_tit_input.csv')
#dataset = pd.read_csv('kb_repo_html_input.csv')
#dataset = pd.read_csv('kb_repo_tit_sum_input_stem.csv')
#dataset = pd.read_csv('kb_repo_tit_sum_html_input_stem.csv')



df03 = pd.read_csv('kb_testing_v3.csv')


df03['tokenized_title'] = df03['user_question'].str.replace('\n', ' ')
df03['tokenized_title'] = df03['tokenized_title'].str.replace('\t', ' ')
df03['tokenized_title'] = df03['tokenized_title'].str.replace('-', '')
#df03['tokenized_title'] = df03['tokenized_title'].map(lambda x: re.sub(r'^https?:\/\/.*[\r\n]*', '', x))
df03['tokenized_title'] = df03['tokenized_title'].map(lambda x: re.sub('[^A-Za-z0-9]+', ' ', x))
df03['tokenized_title'] = df03.tokenized_title.apply(lambda x: x.lower())
df03['tokenized_title'] = df03.tokenized_title.apply(lambda x: x.split())
df03['tokenized_title'] = df03['tokenized_title'].apply(lambda x: [item for item in x if item not in stop_words])
#df03['tokenized_title'] = df03['tokenized_title'].apply(lambda x: [ps.stem(word) for word in x if word not in stop_words])
df03['tokenized_title'] = df03['tokenized_title'].apply(lambda x: list(set(x)))



dataset['word_count'] = 0
df03['article_num_sel'] = ''
df03['article_num_list'] = ''
df03['best_six_article_num'] = ''
df03['check_in_list'] = ''
df03['score'] = ''
df03['match_ratio'] = ''
df03['total_words'] = ''
dataset['temp1'] = 0
counter_1 = 0
for index, row in df03.iterrows():
    print ("counter_1: ",counter_1)
    word_list = row['tokenized_title']
    word_list = list(set(word_list))
    for word in word_list:
        dataset['temp1'] = dataset.tokenized_entry_string.apply(lambda x: len(re.findall(r'(?<!\S)'+ word + r'(?!\S)',x, re.IGNORECASE)))
        dataset['word_count'] = dataset['word_count'].add(dataset['temp1'])
    highest_value_row = np.asscalar(np.int16(dataset['word_count'].idxmax()))
    
    # logic for new list starts here
    if dataset['word_count'].max() == 0:
        highest_value_article =[]
    else:
        highest_value_article = dataset.loc[dataset['word_count'] == dataset['word_count'].max(), 'articlenumber'].values.tolist()
    df03.at[counter_1,'article_num_list'] = highest_value_article
    # logic for new list ends here
    
    # logic to get the best five article number starts here
    if len(highest_value_article) > 6:
        df03.at[counter_1,'best_six_article_num'] = highest_value_article[0:6]
    else:
        df03.at[counter_1,'best_six_article_num'] = dataset.nlargest(6, 'word_count', keep='first')['articlenumber'].tolist()
    # logic to get the best five article number ends here
    


    df03.loc[counter_1,'article_num_sel'] = int(dataset.loc[highest_value_row,'articlenumber'])
    df03.loc[counter_1,'score'] = int(dataset.loc[highest_value_row,'word_count'])
    df03.loc[counter_1,'total_words'] = len(word_list)
    df03.loc[counter_1,'match_ratio'] = (int(dataset.loc[highest_value_row,'word_count']))/(len(word_list))
    df03.loc[counter_1,'token_length'] = dataset.loc[highest_value_row,'token_length']
    
    # diagonostic number check
    if 'diagnostic' in word_list:
        diagnostic_title = row['user_question']
        diagnostic_num = re.findall(r"\D(\d{5})\D", diagnostic_title)
        if not diagnostic_num:
            pass
        else:
            df01 = dataset
            if 'worksheet' in word_list:
                del df01
                df01 = pd.DataFrame()
                df01 = dataset[dataset['input_method__c']=='worksheet']
            
            if 'interview' in word_list:
                del df01
                df01 = pd.DataFrame()
                df01 = dataset[dataset['input_method__c']=='interview']
            
            if 'worksheet' in word_list and 'interview' in word_list:
                del df01
                df01 = pd.DataFrame()
                df01 = dataset[dataset['input_method__c']=='interview worksheet']
            
            diagnostic_article = df01.loc[df01['diagnostic_number']==int(diagnostic_num[0]), 'articlenumber'].tolist()
            if type(diagnostic_article) is list:
                diagnostic_article_number = int(diagnostic_article[0])
            else:
                diagnostic_article_number = int(diagnostic_article)

            df03.loc[counter_1,'article_num_sel'] = int(diagnostic_article_number)
            df03.at[counter_1,'article_num_list'] = diagnostic_article
            del diagnostic_article_number, df01, diagnostic_article
        del diagnostic_title, diagnostic_num
        
    # logic to check the article number list starts
    temp_articlenumber = row['articlenumber']
    temp_articlenumber_list = df03.loc[counter_1,'best_six_article_num']
    if temp_articlenumber in temp_articlenumber_list:
        df03.loc[counter_1,'check_in_list'] = 'yes'
    else:
        df03.loc[counter_1,'check_in_list'] = 'no'
    # logic to check the article number list ends
    
    
    del word_list, word, highest_value_row, highest_value_article
    del temp_articlenumber, temp_articlenumber_list
    dataset['word_count'] = 0
    dataset['temp1'] = 0
    counter_1 +=1
dataset = dataset.drop('word_count', 1)
dataset = dataset.drop('temp1', 1)
print("--- %s seconds ---" % (time.time() - start_time))
del row, index, counter_1, start_time


df03['check'] = np.where(df03['articlenumber'] == df03['article_num_sel'], 'yes', 'no')
df03['check'].value_counts()

df03['check_in_list'].value_counts()

df03['article_num_sel'].value_counts()


df03['five_element_check'] = df03['article_num_list'].apply(lambda x: len(x)<6)

#k=len(df05.loc[df05['five_element_check'] == True])

df05 = df03.loc[df03['check_in_list']=='yes']
df05['five_element_check'] = df05['article_num_list'].apply(lambda x: len(x)<6)
df05 = df05.loc[df05['five_element_check'] == True]

len(df05)
df06['article_num_list'].value_counts()

cols = ['tokenized_title',
 'user_question',
 'articlenumber',
 'article_num_sel',
 'article_num_list',
 'best_six_article_num',
 'check_in_list',
 'check',
 'five_element_check',
 'match_ratio',
 'score',
 'total_words',
 'token_length']

df03 = df03[cols]

#########################################
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))

#dataset = pd.read_csv('kb_repo.csv')
dataset = pd.read_csv('kb_repo_tit_input.csv')
df03 = pd.read_csv('kb_testing_v1.csv')

df03['tokenized_title'] = df03.user_question.apply(lambda x: x.lower())
df03['tokenized_title'] = df03['tokenized_title'].str.replace('\n', ' ')
df03['tokenized_title'] = df03['tokenized_title'].str.replace('\t', ' ')
df03['tokenized_title'] = df03['tokenized_title'].str.replace('-', '')
df03['tokenized_title'] = df03['tokenized_title'].map(lambda x: re.sub('[^A-Za-z0-9]+', ' ', x))
df03['tokenized_title'] = df03.tokenized_title.apply(lambda x: x.split())
df03['tokenized_title'] = df03['tokenized_title'].apply(lambda x: [item for item in x if item not in stop_words])
df03['tokenized_title'] = df03['tokenized_title'].apply(lambda x: list(set(x)))

dataset['word_count'] = 0
df03['article_num_sel'] = ''
dataset['temp'] = 0
counter_1 = 0
for index, row in df03.iterrows():
    print ("counter_1: ",counter_1)
    word_list = row['tokenized_title']
    word_list = list(set(word_list))
    for word in word_list:
        dataset['temp'] = dataset.tokenized_entry_string.apply(lambda x: len(re.findall(r'(?<!\S)'+ word + r'(?!\S)',x, re.IGNORECASE)))
        dataset['word_count'] = dataset['word_count'].add(dataset['temp'])
    if dataset['word_count'].max() == 0:
        highest_value_article =[]
    else:
        highest_value_article = dataset.loc[dataset['word_count'] == dataset['word_count'].max(), 'articlenumber'].values.tolist()
    highest_value_article = tuple(highest_value_article)
    df03.at[counter_1,'article_num_sel'] = highest_value_article
#    del word_list, word, highest_value_row
    del word_list, word, highest_value_article
    dataset['word_count'] = 0
    dataset['temp'] = 0
    counter_1 +=1
dataset = dataset.drop('word_count', 1)
dataset = dataset.drop('temp', 1)
#del row, index, counter_1

df03['articlenumber'] = df03['articlenumber'].apply(lambda x: [x])
df03['articlenumber'] = df03['articlenumber'].apply(lambda x: tuple(x))
df03['check'] = np.where(df03.articlenumber.isin(df03.article_num_sel), 'yes', 'no')
df03['check'].value_counts()

df03['article_num_sel'].value_counts()


#plotting graph for finding best match_ratio
import matplotlib.pyplot as plt

ax1 = plt.figure(figsize=(28,16))
x_values = df03['match_ratio'].tolist()
y_values = []
for i in x_values:
    x1 = len(df03[(df03['match_ratio'] >= i) & (df03['check'] == 'yes')])
    x2 = len(df03[(df03['match_ratio'] >= i) & (df03['check'] == 'no')])
    x3 = x1/(x1+x2)
    y_values.append(x3)
plt.bar(x_values,y_values)
plt.show()

#########################################

cols2 = ['user_question',
         'tokenized_title',
         'articlenumber']

df04 = df03[cols2]
counter_2 = 0
dataset['word_count'] = 0
dataset['temp'] = 0
dataset['match_ratio'] = 0
dataset['rank'] = 0
df04['match_rank'] = 0
df04['art_above_correct_art'] = 0
for index, row in df04.iterrows():
    print ("counter_2: ",counter_2)
    word_list = row['tokenized_title']
    word_list = list(set(word_list))
    dataset['word_count'] = 0
    dataset['temp'] = 0
    dataset['rank'] = 0
    dataset['match_ratio'] = 0
    for word in word_list:
        dataset['temp'] = dataset.tokenized_entry_string.apply(lambda x: len(re.findall(r'(?<!\S)'+ word + r'(?!\S)',x, re.IGNORECASE)))
        dataset['word_count'] = dataset['word_count'].add(dataset['temp'])
    dataset['match_ratio'] = dataset['word_count']/len(word_list)
    dataset['rank'] = dataset['word_count'].rank(method='dense',ascending=False,pct=False)
    matched_rank=0
    matched_rank = dataset.loc[dataset['articlenumber'] == row['articlenumber'], 'rank']
    matched_rank = int(matched_rank)
    df04.at[counter_2,'art_above_correct_art'] = len((dataset[dataset['rank'] <= matched_rank]).index)
    df04.at[counter_2,'match_rank'] = matched_rank
    counter_2 += 1

del cols2, counter_2, index, word, word_list, row, matched_rank
dataset = dataset.drop('word_count', 1)
dataset = dataset.drop('temp', 1)
dataset = dataset.drop('rank', 1)
dataset = dataset.drop('match_ratio', 1)
del df04