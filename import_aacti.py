# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 14:00:18 2019

This file creates a crude dataset of AACTI trial data and PubMed abstracts

@author: matth
"""

"Import modules"
import psycopg2
import pandas as pd
import pickle
import requests
from bs4 import BeautifulSoup
pd.set_option('display.max_columns', 500)

#"Connect to AACT"
#con = psycopg2.connect(database="aact", user="mattsecrest", password="Furniture3#", host="aact-db.ctti-clinicaltrials.org", port="5432")
#
#"Import interventions that are drugs are biologics"
#call = con.cursor()
#drugbio = ('Drug','Biological')
#qry = "SELECT * FROM INTERVENTIONS WHERE intervention_type IN {0}".format(drugbio)
#call.execute(qry)
#interventions_temp = pd.DataFrame(call.fetchall())
#interventions_temp.columns = [desc[0] for desc in call.description]
#interventions_temp = interventions_temp.set_index('nct_id')
#
#"Create index of interventions that are drugs or biologics"
#nct_int = tuple(interventions_temp.index)
#
#"Create study database of interventional trials from 2000 onwards"
#call = con.cursor()
#qry = "SELECT * FROM STUDIES WHERE NCT_ID IN {0}".format(nct_int)
#call.execute(qry)
#studies_temp = pd.DataFrame(call.fetchall())
#studies_temp.columns = [desc[0] for desc in call.description]
#studies_temp = studies_temp.set_index('nct_id')
#studies_temp.start_date = pd.to_datetime(studies_temp.start_date,format="%Y-%m-%d")
#studies_temp = studies_temp[(studies_temp.start_date > "1999-12-31" )&( studies_temp.study_type == "Interventional")]
#
#"Create index of interventions that started after 2000, were drugs/biologics, and were interventional"
#nct_int = tuple(studies_temp.index)
#
#"Create dict of dataframes from AACT"                 
#dfs = ['STUDIES','ANALYZED_STUDIES','BASELINE_COUNTS']
#dfs2 = ['BASELINE_MEASUREMENTS','COUNTRIES','DETAILED_DESCRIPTIONS','INTERVENTIONS']
#dfs3 = ['INTERVENTION_OTHER_NAMES','KEYWORDS','BRIEF_SUMMARIES','STUDY_REFERENCES']
#dfs4 = ['CALCULATED_VALUES','REPORTED_EVENTS','OUTCOMES','OUTCOME_MEASUREMENTS','DOCUMENTS','IPD_INFORMATION_TYPES']
#dfs5 = ['ELIGIBILITIES','DESIGNS','DESIGN_GROUPS','DESIGN_GROUP_INTERVENTIONS']
#dfs6 = ['DESIGN_OUTCOMES','BROWSE_INTERVENTIONS','BROWSE_CONDITIONS']
#dfs7 = ['CONDITIONS','PROVIDED_DOCUMENTS','ID_INFORMATION']
#dfs8 = ['LINKS','OVERALL_OFFICIALS','RESULT_AGREEMENTS','RESULT_GROUPS','PENDING_RESULTS']
#
##res = {}
#for df in[dfs,dfs2,dfs3,dfs4,dfs5,dfs6,dfs7,dfs8]:
#    con = psycopg2.connect(database="aact", user="mattsecrest", password="Furniture3#", host="aact-db.ctti-clinicaltrials.org", port="5432")
#    for db in df:
#        call = con.cursor()
#        call.execute("SELECT * FROM %s WHERE NCT_ID IN %s" % (db,nct_int))
#        temp = pd.DataFrame(call.fetchall())
#        temp.columns = [desc[0] for desc in call.description]
#        temp = temp.set_index('nct_id')
#        res[db] = temp
# 
#pickle.dump(res,open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\aacti_crude.p','wb'))

res = pickle.load(open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\aacti_crude.p','rb'))
#refs = res['STUDY_REFERENCES'] # Define the result dataframe
#resrefs = refs[(refs.reference_type=='results_reference') & (refs.pmid.notnull())] #Subset to just result references and non-missing PMIDs
#
#def abscrape(pmid):
#    url = 'https://www.ncbi.nlm.nih.gov/pubmed/'+pmid
#    pmreq = requests.get(url)
#    soup = BeautifulSoup(pmreq.text,"lxml")
#    try:
#        abstract = soup.find('div',attrs={'class':'abstr'}).find('div',attrs={'class':''}).text
#        return abstract
#    except:
#        return ""
#
#pmabdict = {}
#for i in resrefs.pmid:
#    pmabdict[i] = ""
#
#counter = 0
#for pid in pmabdict:
#    counter = counter+1
#    print("starting abstract "+pid+", "+str(counter)+" out of "+str(len(pmabdict))+": "+str((counter/len(pmabdict))*100)+"%")
#    if pmabdict[pid]=="":
#        pmabdict[pid] = abscrape(pid)
#
#pmabdict['9707298']

#pickle.dump(pmabdict,open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\pmabdict.p','wb'))
pmabdict = pickle.load(open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\pmabdict.p','rb'))

# Convert the dict of abstracts to a DataFrame
#pmabdf = pd.DataFrame.from_dict(pmabdict,orient='index',columns=['crudeabs'])
#pickle.dump(pmabdf,open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\pmabdf.p','wb'))
pmabdf = pickle.load(open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\pmabdf.p','rb'))
