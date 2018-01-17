#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 09:40:50 2018

@author: anup
"""

import os
print (os.getcwd())
wdr = '/home/anup/03_test_scripts/04_wolters_kluwer/kb_complete'
os.chdir(wdr)
del wdr
print (os.getcwd())