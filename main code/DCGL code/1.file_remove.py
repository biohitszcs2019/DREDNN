import os
import shutil

pth = r'C:\Users\Administrator\Desktop\DCGL\source data\TCGA\TCGA_raw data'       #基准路径

source_path = pth + r'\gdc_download_20180715_120104'                              #数据下载目录
target_path = pth + r'\files'                                                     #实例压缩文件所在目录

file_json = pth + r'\note\metadata.cart.2018-07-15.json'                           #jsong文件路径
ensembl = pth + r'\Homo_sapiens.GRCh38.92.chr.gtf\Homo_sapiens.GRCh38.92.chr.gtf'

def file_name(file_dir):                                                           #查看指定文件夹下的文件信息
    for root, dirs, files in os.walk(file_dir):
        print(root)                 #当前目录路径
        print(dirs)                 #当前路径下所有子目录
        print(files)                #当前路径下所有非目录子文件


def file_name_td(file_dir,file_type):                                            #提取指定文件夹下的所有类型为.gz的文件路径 保存在列表L中
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == file_type:
                L.append(os.path.join(root, file))
    return L


L = file_name_td(source_path,'.gz')

for item in L:                                                                     #文件移动至新文件夹下
    print(item)
    shutil.move(item,target_path)

























