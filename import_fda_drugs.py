# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:02:59 2019

This file creates a crude FDA drug approval database

@author: matth
"""
"Import Modules"
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import zipfile
import wget
import os
import pickle

"Remove previous files"
direct = r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\fda-drugs'
if os.path.exists(direct+'\\'+'fda_drugs.zip'):
        os.remove(direct+'\\'+'fda_drugs.zip')

zipout = ['ActionTypes_Lookup.txt','ApplicationDocs.txt','Applications.txt',
         'ApplicationsDocsType_Lookup.txt','MarketingStatus.txt',
         'MarketingStatus_Lookup.txt','Products.txt','SubmissionClass_Lookup.txt',
         'SubmissionPropertyType.txt','Submissions.txt','TE.txt']

for file in zipout:
    if os.path.exists(direct+'\\'+file):
        os.remove(direct+'\\'+file)

"Import most recent FDA drug approvals"
fdaurl = "https://www.fda.gov/media/89850/download"
wget.download(fdaurl,r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\fda-drugs\fda_drugs.zip')

"Unzip the fda_drugs zip file"
with zipfile.ZipFile(direct+'\\'+'fda_drugs.zip','r') as zip_ref:
    zip_ref.extractall(direct)

"Import submissions document"
appr = pd.read_csv(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\fda-drugs\Submissions.txt',
                  sep="\t",encoding='latin1') #Import raw data
appr['SubStatusDateTime'] = pd.to_datetime(appr.SubmissionStatusDate) # Convert submission status to date
appr = appr.set_index("ApplNo") # Set the index to the application number

"Import products document"
produ = pd.read_csv(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\fda-drugs\Products.txt',
                   sep="\t",encoding='latin1',error_bad_lines=False) #Import raw data
produ = produ.set_index('ApplNo') # Set the index to the application number
dn = produ.loc[:,['DrugName','ActiveIngredient']] # Subset to just include ApplNo as index and drug name

"Merge products and submission documents"
appr_dn = pd.merge(appr,dn,'left','ApplNo',left_index=True) # Add names to the approval database
appr_dn = appr_dn[(appr_dn.SubmissionType=='ORIG') & 
                (pd.notna(appr_dn.SubmissionStatusDate))]

pickle.dump(appr_dn,open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\appr_dn.p','wb'))
appr_dn.to_csv(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\appr_dn.csv')
appr_dn = pickle.load(open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\appr_dn.p','rb'))