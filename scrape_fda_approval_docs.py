# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 11:14:02 2019

@author: matth
"""

import pickle
import pandas as pd
import requests
from bs4 import BeautifulSoup

"Load analytic dataset to get FDA ApplNos "
appr_dn = pickle.load(open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\appr_dn.p','rb'))

"First create a dict of URLs"
applnolong = []
appldict = {}
for appl in appr_dn.index:
    appls=str(appl)
    le = 6-len(appls)
    appls = '0'*le+appls
    applnolong.append(appls)
    appldict[appl]=appls
    
