#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 11:00:22 2017

@author: anup
"""
def article_check(string):
    # check for title match with repo starts here
    title_match_string = string
    title_match_string = title_match_string.replace('\n', ' ')
    title_match_string = title_match_string.replace('\t', ' ')
    title_match_string = title_match_string.replace('-', '')
    title_match_string = title_match_string.replace('many', '')
    title_match_string = re.sub('[^A-Za-z0-9]+', ' ', title_match_string)
    title_match_string = title_match_string.lower()
    article_num_selected = list(dataset.loc[dataset['title'] == title_match_string, 'articlenumber'])
    if article_num_selected:
        match_report = {}
        match_report['status_code'] = 1
        match_report['articlenumber'] = article_num_selected[0]
        match_report['matching_article_numbers'] = 'not_applicable'
        match_report['match_ratio'] = 1
        return match_report
    # check for title match with repo ends here
    
    
    # user_input preprocessing starts here
    captured_string = title_match_string
    captured_string = captured_string.split()
    captured_string = [word for word in captured_string if word not in stop_words]
    captured_string = list(set(captured_string))
    # user_input preprocessing ends here
        
        
    # matchng logic starts here
    dataset['word_count'] = 0
    dataset['temp_count'] = 0
    for word in captured_string:
        dataset['temp_count'] = dataset.tokenized_entry_string.apply(lambda x: len(re.findall(r'(?<!\S)'+ word + r'(?!\S)',x, re.IGNORECASE)))
        dataset['word_count'] = dataset['word_count'].add(dataset['temp_count'])
    highest_value_row = np.asscalar(np.int16(dataset['word_count'].idxmax()))
    highest_value_article_list = dataset.loc[dataset['word_count'] == dataset['word_count'].max(), 'articlenumber'].values.tolist()
    # matchng logic ends here
    
    # logic to get best six for all cases starts here
    if len(highest_value_article_list) > 6:
        best_six_article_numbers =  highest_value_article_list[1:6]
    else:
        best_six_article_numbers = dataset.nlargest(6, 'word_count', keep='first')['articlenumber'].tolist()
    # logic to get best six for all cases ends here
    
    
    # logic for checking worksheet or interview starts here
    if 'interview' not in captured_string and 'worksheet' not in captured_string:
        df04 = dataset[dataset['articlenumber'].isin(highest_value_article_list)]
        highest_value_article_input_list = df04['input_method__c'].tolist()
        while 'xxxnovaluesxxx' in highest_value_article_input_list: highest_value_article_input_list.remove('xxxnovaluesxxx')
        highest_value_article_input_list = list(set(highest_value_article_input_list))
        if len(highest_value_article_input_list) > 1:
            status_code = 2
        else:
            status_code = 1
    else:
        status_code = 1
    # logic for checking worksheet or interview ends here
    
    
    # match_ratio calculations starts here
    article_num_selected = int(dataset.loc[highest_value_row,'articlenumber'])
    match_score = int(dataset.loc[highest_value_row,'word_count'])
    captured_string_count = len(captured_string)
    if captured_string_count > 0:
        match_ratio = round(match_score/(len(captured_string)),2)
    else:
        match_ratio = 0
    if match_ratio == 0:
        highest_value_article_list = []
    # match_ratio calculations ends here
    
    
    # setting cutoff for match_ratio starts here
    match_ratio_cutoff = 0.2
    # setting cutoff for match_ratio ends here


    # match_report prep and sending starts here
    match_report = {}
    if match_ratio > match_ratio_cutoff:
        match_report['status_code'] = status_code
        match_report['articlenumber'] = article_num_selected
        match_report['matching_article_numbers'] = highest_value_article_list
        match_report['match_ratio'] = match_ratio
        match_report['best_six_article_numbers'] = best_six_article_numbers
        return match_report
    else:
        match_report['status_code'] = 0
        match_report['articlenumber'] = 'not_found'
        match_report['matching_article_numbers'] = highest_value_article_list
        match_report['match_ratio'] = match_ratio
        match_report['best_six_article_numbers'] = best_six_article_numbers
        return match_report
    # match_report prep and sending ends here

k = 'resubmit a rejected return?'
article_check(k)
k='How do I split a joint return?'
article_check(k)
k='Where do I input Foreign Earned Income?'
article_check(k)
k='How do I input Foreign Earned Income?'
article_check(k)
k='How do I attach a PDF document?'
article_check(k)
k='Can I stop a return once I have e-filed it?'
article_check(k)
k='How do I stop a return after it\'s been e-filed?'
article_check(k)
k='Where do I input income for the 1116?'
article_check(k)
k='Where do I enter the 1116 income?'
article_check(k)
k='Where do I enter Foreign income?'
article_check(k)
k='How many days do I have to resubmit a rejected return?'
article_check(k)
k='How do I create a footnote?'
article_check(k)
k='Where do I enter the Non-employee compensation?'
article_check(k)

	
b = article_check(k)
b['articlenumber']
b['match_ratio']


import IPython
app = IPython.Application.instance()
app.kernel.do_shutdown(True)


#%reset

