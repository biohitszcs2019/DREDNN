import pandas as pd

matrix_T = pd.read_csv(r"C:\Users\Administrator\Desktop\DCGL\source data\TCGA\result\matrix_T.csv",index_col=None,header=None)
matrix_N = pd.read_csv(r"C:\Users\Administrator\Desktop\DCGL\source data\TCGA\result\matrix_N.csv",index_col=None,header=None)

id =[]
t = []
i=-1                                     #取第一列去冗余
for item in matrix_N[0]:                 #dataframe 每一列 每一行是一个 series ， series的 item 是一个值
    i=i+1
    if item not in t:
        id.append(i)
        t.append(item)
print(id)

TCGA_N = matrix_N.reindex(index = id)
TCGA_T = matrix_T.reindex(index = id)
TCGA_N.to_csv(r"C:\Users\Administrator\Desktop\DCGL\source data\TCGA\result\TCGA_N.csv",index=False,header = False,sep=',')
TCGA_T.to_csv(r"C:\Users\Administrator\Desktop\DCGL\source data\TCGA\result\TCGA_T.csv",index=False,header = False,sep=',')






