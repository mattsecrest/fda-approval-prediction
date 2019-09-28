# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 12:25:32 2019

@author: matth

This file is to create the analytic dataset for the abstract 
FDA prediction model
"""
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import datetime
import gzip

"Import study files"
appr_dn = pickle.load(open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\appr_dn.p','rb'))
res = pickle.load(open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\aacti_crude.p','rb'))
pmabdf = pickle.load(open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\pmabdf.p','rb'))

"""
CLEAN THE FDA DRUGS DATABASE
"""
"1) Remove duplicate approvals for the same active ingredient, keep the first"
appr_dn = appr_dn[appr_dn.SubmissionClassCodeID==7]

"2) Drop unnecessary columns"
appr_dn = appr_dn.drop(['SubmissionStatus','SubmissionType'],axis=1)

"3) Drop values with no drug or molecule name"
appr_dn = appr_dn[(pd.notna(appr_dn['DrugName'])) & (pd.notna(appr_dn['ActiveIngredient']))]

"4) Change strings to lower"
appr_dn.ActiveIngredient = [i.lower() for i in appr_dn.ActiveIngredient]
appr_dn.DrugName = [i.lower() for i in appr_dn.DrugName]

"5) Clean 'other' intervention names"
appr_dn['ActiveIngredientClean'] = appr_dn.ActiveIngredient #Copy column first
for substring in ['-.*','\(.*']:
    appr_dn.ActiveIngredientClean = appr_dn.ActiveIngredientClean.apply(lambda x:re.sub(substring,'',x))
    
"6) Remove approvals prior to 2000 and sort by approval date"
appr_dn = appr_dn[appr_dn.SubStatusDateTime > pd.to_datetime('1999-12-31',format='%Y-%m-%d')]
appr_dn = appr_dn.sort_values(by='SubStatusDateTime')

"7) Make a subset of the data just for the unique approval dates per application per drug name"
fda = appr_dn[['SubStatusDateTime','DrugName','ActiveIngredient','ActiveIngredientClean']].drop_duplicates()
   
"""
CLEAN THE ABSTRACT DATABASE
"""

"1) Fix observed string errors"
pmabdf['cleanabs']=pmabdf.crudeabs # Create clean abstract database
pmabdf['cleanabs'] = [re.sub('Copyright.*','',i) for i in pmabdf.crudeabs] # Remove copyright

"Randomized"
rand = ['randomized','randomised','random','Randomized','Randomized','random']
pmabdf['randomized'] = [any(word in i for word in rand) for i in pmabdf.cleanabs]

"Systematic review"
review = ['literature review','Literature review','systematic review',
          'Systematic review','systematic literature review','Systematic literature review']
pmabdf['review'] = [any(word in i for word in rand) for i in pmabdf.cleanabs]

"3) Remove trials meeting certain criteria"
pmabdf = pmabdf[pmabdf.cleanabs!=''] # Remove missing abs

"""
CLEAN THE AACT CLINICAL TRIAL DATA
"""
"0) Studies"
res['STUDIES'].start_date = pd.to_datetime(res['STUDIES'].start_date,format='%Y-%m-%d')
res['STUDIES'].completion_date = pd.to_datetime(res['STUDIES'].completion_date,format='%Y-%m-%d')

"1) Study references"
res['STUDY_REFERENCES'] = res['STUDY_REFERENCES'][(res['STUDY_REFERENCES'].reference_type=='results_reference') & (pd.notnull(res['STUDY_REFERENCES'].pmid))] # Remove the references that are not results and where there's no abstract
res['STUDY_REFERENCES'] = res['STUDY_REFERENCES'].drop(['id','reference_type'],axis=1) # Drop some unnecessary columns in the study references file

# Create a function to extract dates from citations
def dateExtract(citation):
    months = ['[0-9]{4}\s+Jan','[0-9]{4}\s+Feb',
              '[0-9]{4}\s+Mar','[0-9]{4}\s+Apr','[0-9]{4}\s+May',
              '[0-9]{4}\s+Jun','[0-9]{4}\s+Jul','[0-9]{4}\s+Aug',
              '[0-9]{4}\s+Sep','[0-9]{4}\s+Oct',
              '[0-9]{4}\s+Nov','[0-9]{4}\s+Dec']
    found = False
    for month in months:
        if re.findall(month,citation):
            datestr = re.findall(month,citation)
            date = pd.to_datetime(datestr[0],format="%Y %b")
            found = True
            return date
    if not found:
        return None

res['STUDY_REFERENCES']['pubdate'] = [dateExtract(i) for i in res['STUDY_REFERENCES'].citation]
    
"2) Designs"
res['DESIGNS'] = res['DESIGNS'][res['DESIGNS'].allocation=='Randomized'] # Limit to randomized studies
res['DESIGNS'].index

"3) Interventions"
res['INTERVENTIONS'] = res['INTERVENTIONS'].drop(['id'],axis=1) # Drop the ID field
res['INTERVENTIONS'] = res['INTERVENTIONS'][(res['INTERVENTIONS'].intervention_type=="Drug") | (res['INTERVENTIONS'].intervention_type=="Biological")] #Drop everything but drugs/biologics
res['INTERVENTIONS'] = res['INTERVENTIONS'].loc[res['DESIGNS'].index,:]
res['INTERVENTIONS'].name = [name.lower() for name in res['INTERVENTIONS'].name]
for exc in ['placebo','placebo oral tablet']:
    res['INTERVENTIONS'] = res['INTERVENTIONS'][res['INTERVENTIONS'].name!=exc] # Exclude placebo and placebo oral tablet terms
res['INTERVENTIONS'] = res['INTERVENTIONS'].join(res['STUDIES'].start_date,on='nct_id') # Get intervention start date
res['INTERVENTIONS'] = res['INTERVENTIONS'].join(res['STUDIES'].completion_date,on='nct_id')

res['INTERVENTIONS']=res['INTERVENTIONS'].join(res['STUDIES'].phase)
res['INTERVENTIONS'] = res['INTERVENTIONS'][
        (res['INTERVENTIONS'].phase =='Phase 2') |
        (res['INTERVENTIONS'].phase =='Phase 3') |
        (res['INTERVENTIONS'].phase =='Phase 1/Phase 2') |
        (res['INTERVENTIONS'].phase =='Phase 2/Phase 3')] # Drop all but phase 2-3
res['INTERVENTIONS'] = res['INTERVENTIONS'].sort_values(by='start_date')


"5) Other interventions"
res['INTERVENTION_OTHER_NAMES'].name = [name.lower() for name in res['INTERVENTION_OTHER_NAMES'].name] # Make everything lower case

"""
START MERGING TO CREATE ITERABLE FOR ANALYTIC DATABASE
"""
"1) Merge the abstract database to the PMID database to get NCT number"
mRA = res['STUDY_REFERENCES'].join(pmabdf,on='pmid',how='inner')
intunique = res['INTERVENTIONS'][res['INTERVENTIONS'].index.isin(list(res['INTERVENTIONS'].index.unique()))].completion_date
studesc = res['STUDIES'][res['STUDIES'].index.isin(list(res['INTERVENTIONS'].index.unique()))].brief_title
studfulldesc = res['STUDIES'][res['STUDIES'].index.isin(list(res['INTERVENTIONS'].index.unique()))].official_title

mRA = mRA.join(intunique,how='right')
mRA = mRA.join(studesc,how='right')
mRA = mRA.join(studfulldesc,how='right')

mRA = mRA[mRA.pmid.notnull()] # Drop missing pmids

mRA = mRA.sort_values(by='completion_date')

" Save files to pass them to Jupyter"
resint = res['INTERVENTIONS'] # Save to make it easier for Jupyter
mRA.to_csv(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\mRA.csv')
fda.to_csv(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\fda.csv')
resint.to_csv(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\resint.csv')

#fda_dict = {theappl:[] for theappl in fda.index} # list of FDA approvals
#nct_list =list(mRA.index.unique()) # List of unique NCTs
#counter=0
## Loop over FDA drug names and application numbers
#for fdadrug,fdadate,appl,active in zip(fda.DrugName,fda.SubStatusDateTime,fda.index,fda.ActiveIngredientClean):
#    stop = False
#    ncti = 0 # NCT iterable
#    counter = counter + 1
#    print('starting fda drug',counter,'out of ',len(fda))
#    #Start with looking for names and ingredients
#    while ncti < len(nct_list) and not stop:
#        nct_intervention = resint[resint.index==nct_list[ncti]]     
#        if nct_intervention.start_date.iloc[0] > fdadate:
#            stop = True
#            print("stopping because of date")
#        else:
#            if ncti!=0 and ncti %100==0:
#                print("the ncti is",ncti, "out of",str(len(nct_list)))
#            highest = False
#            if any(fdadrug in nctdrug for nctdrug in nct_intervention.name):
#                toappend = [nct_list[ncti],nct_intervention.phase.iloc[0],
#                            nct_intervention.start_date.iloc[0],nct_intervention.completion_date.iloc[0]]
#                for nctdrug in nct_intervention.name:
#                    toappend.append(nctdrug)                    
#                fda_dict[appl].append(toappend)
#                print("FOUND A MATCH")
#                highest = True
#            if not highest:
#                nexthighest = False
#                if any(active in nctdrug for nctdrug in nct_intervention.name):
#                    toappend = [nct_list[ncti],nct_intervention.phase.iloc[0],
#                                nct_intervention.start_date.iloc[0],nct_intervention.completion_date.iloc[0]]
#                    for nctdrug in nct_intervention.name:
#                        toappend.append(nctdrug)
#                        fda_dict[appl].append(toappend)
#                    print('FOUND A MATCH')
#                    nexthighest = True
#                if not nexthighest:
#                    abstracts = mRA.loc[nct_list[ncti]].cleanabs
#                    if type(abstracts) is str:
#                        abstracts = [abstracts]
#                    if any(fdadrug in abstract for abstract in abstracts):
#                        toappend = [nct_list[ncti],nct_intervention.phase.iloc[0],
#                                    nct_intervention.start_date.iloc[0],nct_intervention.completion_date.iloc[0]]
#                        for nctdrug in nct_intervention.name:
#                            toappend.append(nctdrug)
#                            fda_dict[appl].append(toappend)
#            ncti = ncti+1

"Load the dict of FDA and NCT trials that we calculated in Jupyter"
fda_dict = pickle.load(open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\fda_dict.p','rb'))
fda_dict_drop = {key:val for key,val in fda_dict.items()if val !=[]} # Drop FDA without matches

"Create a function to count unique trials per FDA submission"
def countNCT(val):
    if len(val)==0:
        return 0
    if len(val)==1:
        return 1
    out = True
    if len(val)>1:
        for n in range(len(val)-1):
            if val[n]!=val[n+1]:
                out = False
    if out == True:
        return 1
    elif out==False:
        return len(val)
    
"Explore features of FDA dicts"
fda_counter = {key:countNCT(val) for key,val in fda_dict_drop.items()}
known = {key:val[0][0] for key,val in fda_dict_drop.items() if countNCT(val)==1} # Create a dict of 
known = pd.DataFrame.from_dict(known,orient='index')
known.columns=['nct_id']
known_fda = fda.join(known,how='inner')
#known_fda['ApplNo'] = known_fda.index
known_fda=known_fda.set_index('nct_id')

"Shorten resint database to drop drug names"
resintshort = resint.drop(['name','intervention_type','description'],axis=1).drop_duplicates()

"Create analytic database"
df_np = mRA.join(known_fda,how='left').drop(['completion_date'],axis=1) # Unique NCT and PMID
df_np = df_np.join(resintshort,how='left') # Add Intervention data
df_np = df_np.drop_duplicates()
df_np['approved'] = [1 if pd.notna(datetime) else 0 for datetime in df_np.SubStatusDateTime]
df_np = df_np[df_np.pubdate>pd.to_datetime('1990-01-01')]

pickle.dump(df_np,open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\df_np.p','wb'))
df_np.to_csv(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\df_np.csv')
