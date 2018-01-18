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