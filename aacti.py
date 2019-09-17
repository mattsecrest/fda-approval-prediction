# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 14:00:18 2019

@author: matth
"""

"Import modules"
import psycopg2
import pandas as pd
pd.set_option('display.max_columns', 500)

"Connect to AACT"
con = psycopg2.connect(database="aact", user="mattsecrest", password="Furniture3#", host="aact-db.ctti-clinicaltrials.org", port="5432")

"Import interventions that are drugs are biologics"
call = con.cursor()
drugbio = ('Drug','Biological')
qry = "SELECT * FROM INTERVENTIONS WHERE intervention_type IN {0}".format(drugbio)
call.execute(qry)
interventions_temp = pd.DataFrame(call.fetchall())
interventions_temp.columns = [desc[0] for desc in call.description]
interventions_temp = interventions_temp.set_index('nct_id')

"Create index of interventions that are drugs or biologics"
nct_int = tuple(interventions_temp.index)

"Create study database of interventional trials from 2000 onwards"
call = con.cursor()
qry = "SELECT * FROM STUDIES WHERE NCT_ID IN {0}".format(nct_int)
call.execute(qry)
studies_temp = pd.DataFrame(call.fetchall())
studies_temp.columns = [desc[0] for desc in call.description]
studies_temp = studies_temp.set_index('nct_id')
studies_temp.start_date = pd.to_datetime(studies_temp.start_date,format="%Y-%m-%d")
studies_temp = studies_temp[(studies_temp.start_date > "1999-12-31" )&( studies_temp.study_type == "Interventional")]

"Create index of interventions that started after 2000, were drugs/biologics, and were interventional"
nct_int = tuple(studies_temp.index)

"Create dict of dataframes from AACT"                 
dfs = ['STUDIES','ANALYZED_STUDIES','BASELINE_COUNTS','BASELINE_MEASUREMENTS',
       'COUNTRIES','DETAILED_DESCRIPTIONS','INTERVENTIONS','INTERVENTION_OTHER_NAMES',
       'KEYWORDS','BRIEF_SUMMARIES','STUDY_REFERENCES','CALCULATED_VALUES',
       'REPORTED_EVENTS','OUTCOMES','OUTCOME_MEASUREMENTS','DOCUMENTS','IPD_INFORMATION_TYPES',
       'ELIGIBILITIES','DESIGNS','DESIGN_GROUPS','DESIGN_GROUP_INTERVENTIONS',
       'DESIGN_OUTCOMES','BROWSE_INTERVENTIONS','BROWSE_CONDITIONS',
       'CONDITIONS','RESULTS_GROUPS','PROVIDED_DOCUMENTS','ID_INFORMATION',
       'LINKS','OVERALL_OFFICIALS','RESULT_AGREEMENTS','RESULT_GROUPS',
       'PENDING_RESULTS']
res = {}
for db in dfs:
    call = con.cursor()
    call.execute("SELECT * FROM %s WHERE NCT_ID IN %s" % (db,nct_int))
    temp = pd.DataFrame(call.fetchall())
    temp.columns = [desc[0] for desc in call.description]
    temp = temp.set_index('nct_id')
    res[db] = temp

