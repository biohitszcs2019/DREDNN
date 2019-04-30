import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import json

file_met = r'C:\Users\Administrator\Desktop\DCGL\source data\TCGA\TCGA_raw data\note\metadata.cart.2018-07-15.json'            #metadata json文件路径
file_cli = r'C:\Users\Administrator\Desktop\DCGL\source data\TCGA\TCGA_raw data\note\clinical.cart.2018-07-15.json'            #metadata json文件路径

file = open(file_cli, encoding='utf-8')            #不设置的话遇到中文会报错
cli = json.loads(file.read())
#print((json_normalize(cli,'diagnoses')))

case_id = []
status = []
time = []

for item in cli:
    case_id.append(item['case_id'])
    status.append(item['diagnoses'][0]['vital_status'])

    if item['diagnoses'][0]['vital_status'] == "dead":
           time.append(item['diagnoses'][0]['days_to_death'])
    else:
           time.append(item['diagnoses'][0]['days_to_last_follow_up'])


sur = pd.DataFrame(  np.array([status,time]).T   ,  index = case_id  )
print(sur)


############################################################################################################################
file = open(file_met, encoding='utf-8')            #不设置的话遇到中文会报错
met = json.loads(file.read())

#提取信息
TCGAid= []
caseid = []
for item in met:
    TCGAid.append(item['associated_entities'][0]['entity_submitter_id'])          #TCGAid
    caseid.append(item['associated_entities'][0]['case_id'])                      #fileid

id = { }
for  i  in range(0,len(TCGAid)):
    id[TCGAid[i]] = caseid[i]
'''
id = pd.Series(caseid,index = TCGAid )
'''

d=[]
for item in id:
    d.append( list( sur.ix[id[item]] ) )

sur2 = pd.DataFrame( d ,index = id.keys(),columns=['status','surtime'] )
print(sur2)


sur2.to_csv(r"C:\Users\Administrator\Desktop\DCGL\source data\TCGA\result\tcgasur.csv",index=True, sep=',')



