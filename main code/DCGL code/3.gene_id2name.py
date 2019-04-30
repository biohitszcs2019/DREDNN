import pandas as pd

pth = r'C:\Users\Administrator\Desktop\DCGL\source data\TCGA'
ensembl =  pth + r'\TCGA_raw data\Homo_sapiens.GRCh38.92.chr.gtf\Homo_sapiens.GRCh38.92.chr.gtf'            #metadata json文件路径


#打开未知文本文件                                                                                                  ☆
with open(ensembl) as  file_object:             #逐行读取保存为2维列表line[行号][行内字符号]
   lines = file_object.readlines()

for i in range(0,20):                            #测试观察前20行
    print(lines[i])
result = lines[5:len(lines)]                     #去掉前5行非数据行


#拆分每行字符串，分析：只挑选gene样例t[2]=='gene'，且只提取最后一个字段t[-1] 中的tt[0],tt[2]两项对应提取 id 和 name字段 ☆
id = []
name = []
for item in result:
   t  = [s.strip() for s in item.split('\t')]
   if t[2]=='gene':
        tt = [s.strip() for s in t[-1].split(';')]
        ttt1 = [s.strip() for s in tt[0].split('"')]
        ttt2 = [s.strip() for s in tt[2].split('"')]
        id.append(ttt1[1])
        name.append(ttt2[1])


#保存两组对应信息结果为series
gene_name = pd.Series(name,index=id)
print(gene_name)

gene_name.to_csv(r"C:\Users\Administrator\Desktop\DCGL\source data\TCGA\result\gene_name.csv",index=True,sep=',')












