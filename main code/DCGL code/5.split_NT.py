import pandas as pd
import numpy as np

matrix = pd.read_csv(r"C:\Users\Administrator\Desktop\DCGL\source data\TCGA\result\matrix.csv",index_col=0)               #read_csv读入的是dataframe
print(matrix.index)                                                                                                       #index类型的特殊列表
print(matrix.columns)

matrix_colT = []
matrix_colN = []
matrix_ind = []

#分别提取正负列标签保存为列表
for item in matrix.columns[1:len(matrix.columns)+1]:
    t = [s.strip() for s in item.split('-')]
    if t[3][0] == '0':
        matrix_colT.append(item)
    else:
        matrix_colN.append(item)

#提取行标签保存为列表
for item in matrix.index:
    matrix_ind.append(item)

#分开NT样本集
matrix_T = matrix.reindex(columns = matrix_colT)
matrix_N = matrix.reindex(columns = matrix_colN)

matrix_T.to_csv(r"C:\Users\Administrator\Desktop\DCGL\source data\TCGA\result\matrix_T.csv",index=True,sep=',')
matrix_N.to_csv(r"C:\Users\Administrator\Desktop\DCGL\source data\TCGA\result\matrix_N.csv",index=True,sep=',')


