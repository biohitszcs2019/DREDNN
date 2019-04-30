import pandas as pd
import numpy as np
import os
pth = r'C:\Users\Administrator\Desktop\DCGL\source data\TCGA\TCGA_raw data'       #基准路径
target_path = pth + r'\files'                                                     #实例压缩文件所在目录

#提取csv 转变为nparray二维数组（excel表格式），read_csv读入的是dataframe 无法转成series #☆
jss0 = np.array(pd.read_csv(r"C:\Users\Administrator\Desktop\DCGL\source data\TCGA\result\jss.csv",header= None))
gene_name0 = np.array(pd.read_csv(r"C:\Users\Administrator\Desktop\DCGL\source data\TCGA\result\gene_name.csv",header= None))

c=[]
r=[]
for item in jss0:                   # 每行item两个元素item[0][1]
    c.append(item[1])
    r.append(item[0])
jss = pd.Series(c,index=r)
print(jss)

c=[]
r=[]
for item in gene_name0:
    c.append(item[1])
    r.append(item[0])
gene_name = pd.Series(c,index=r)
print(gene_name)

#以上为恢复保存的csv文件保存的series
##################################################################################################################################

def file_name_td(file_dir,ftpye):                                              #提取指定文件夹下的所有类型为.txt的文件路径
    L=[]
    Q=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == ftpye:
                L.append(os.path.join(root, file))                #路径
                Q.append(os.path.basename(file))                  #无后缀文件名
    return L,Q

#创建ndarray矩阵与格式设计
rows = 58336
cols = 424
mat = np.zeros((rows,cols))

#读取目标文件中实例的路径和文件名
L,Q = file_name_td(target_path, '.txt')                           #查询.txt实例文件路径集合  L是文件夹中文件路径列表，Q是文件名列表


##################################################  索  引  ###############################################################################
#矩阵列索引：Q中的行fileid转换为对应的TCGAid  （标签映射）
col_label=[]
for item in Q:
    str = item + '.gz'
    col_label.append(jss[str])

#矩阵行索引：每个实例的行索引
ensembls = []
txt = pd.read_table(L[0], sep = '\t',engine='python',header=None)             #打开实例的txt文件table转化为数据框, 无指定行列索引
for i in range(rows):
    t = txt[0][i]                                                              #提取第一列为行索引☆
    tt = [s.strip() for s in t.split('.')]                                     #去掉ensemble·后面的位
    ensembls.append(tt[0])
print(ensembls)

row_label = []                                                                 #行索引由ensenbls的id转化为gene名
for item in ensembls:
    if item in gene_name.index:
       row_label.append(gene_name[item])
    else:
        row_label.append(item)
#################################################### 矩  阵 ##############################################################################


#数组赋值
for i in range(cols):
    txt = pd.read_table(L[i], sep='\t', engine='python', header=None)            #读出来的txt是一个数据框
    for j in range(rows):
        mat[j][i] = txt[1][j]                                                    #数据框的行列与矩阵行列选择顺序相反

#创建数据框
DF = pd.DataFrame(mat, index=row_label, columns = col_label)

#保存数据为csv表格
DF.to_csv(r"C:\Users\Administrator\Desktop\DCGL\source data\TCGA\result\matrix.csv",index=True,sep=',')









