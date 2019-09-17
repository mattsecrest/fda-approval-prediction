# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:02:59 2019

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
appr['SUBSTATUSDATETIME'] = pd.to_datetime(appr.SubmissionStatusDate) # Convert submission status to date
appr = appr.set_index("ApplNo") # Set the index to the application number

"Import products document"
produ = pd.read_csv(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\fda-drugs\Products.txt',
                   sep="\t",encoding='latin1',error_bad_lines=False) #Import raw data
produ = produ.set_index('ApplNo') # Set the index to the application number
dn = produ.loc[:,['DrugName','ActiveIngredient']] # Subset to just include ApplNo as index and drug name

"Merge products and submission documents"
appr_dn = pd.merge(appr,dn,'left','ApplNo',left_index=True) # Add names to the approval database
appr_dn = appr_dn[(appr_dn.SubmissionType=='ORIG') & 
                (pd.notna(appr_dn.SubmissionStatusDate))&
                (appr_dn.SUBSTATUSDATETIME>pd.to_datetime('1989-12-31',format="%Y-%m-%d"))] # Remove non-approval applications and filings before 1990

"Drop duplicates and keep just the first approval"
appr_dn_dedupe = appr_dn.sort_values('SUBSTATUSDATETIME').drop_duplicates(subset='ActiveIngredient').sort_values('ActiveIngredient')

"Write file to disk"
appr_dn_dedupe.to_csv(r"C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\fda-drugs\appr_dn_dedupe_20190916.csv")

"Evaluate approvals by month and year"
subm_dn_cntmonth = appr_dn_dedupe.set_index('SUBSTATUSDATETIME').groupby(by=pd.Grouper(freq='Y')).count().loc[:,'ActiveIngredient'] # Aggregate by year and keep only unique drug names
subplot = subm_dn_cntmonth.plot(title="Approvals by year")
subplot.set(xlabel="Year",ylabel="Count of unique drug name approvals")
subplot.show()
