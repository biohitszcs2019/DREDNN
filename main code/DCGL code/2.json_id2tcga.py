import pandas as pd
import json

pth = r'C:\Users\Administrator\Desktop\DCGL\source data\TCGA'
file_json =  pth + r'\TCGA_raw data\note\metadata.cart.2018-07-15.json'            #metadata json文件路径

#加载json文件，其中包含的文件id和TCGAid的对应信息，建立映射series
#pd.read_json(file)

#打开json文件                                                                                           ☆
file = open(file_json, encoding='utf-8')            #不设置的话遇到中文会报错
js = file.read()
js = json.loads(js)

#提取对应信息
TCGAid= []
fileid = []
for item in js:
    TCGAid.append(item['associated_entities'][0]['entity_submitter_id'])          #TCGAid
    fileid.append(item['file_name'])                                              #fileid

#保存两组对应信息结果为series
jss = pd.Series(TCGAid,index = fileid)
print(jss)

jss.to_csv(r"C:\Users\Administrator\Desktop\DCGL\source data\TCGA\result\jss.csv", index=True, sep=',')