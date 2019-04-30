#设置工作目录
setwd("C:/Users/Administrator/Desktop/DCGL/DCGL_network")
getwd()

#加载数据与库
library(DCGL)
data("tf2target")

#分析初始数据格式
ls()                                  #查看列表名
dim(data_symbol_cli_N)
names(data_symbol_cli_N)
class(data_symbol_cli_N)
mode(data_symbol_cli_N)


#重新读三套python处理后的数据
dmat_cli_N = read.csv("data/cli_Nd.csv",header = TRUE,row.names = 1)
dmat_cli_T = read.csv("data/cli_Td.csv",header = TRUE,row.names = 1)

dmat_N_cli = read.csv("data/N_clid.csv",header = TRUE,row.names = 1)
dmat_T_cli = read.csv("data/T_clid.csv",header = TRUE,row.names = 1)

dmat_N = read.csv("data/TCGA_Nd.csv",header = TRUE,row.names = 1)
dmat_T = read.csv("data/TCGA_Td.csv",header = TRUE,row.names = 1)


#执行
exprs.1 = as.matrix(dmat_cli_N)
exprs.2 = as.matrix(dmat_cli_T)

#exprs.1 = as.matrix(dmat_N_cli)
#exprs.2 = as.matrix(dmat_T_cli)

#exprs.1 = as.matrix(dmat_N)
#exprs.2 = as.matrix(dmat_T)



#DCGL
expressionBasedfilter(exprs.1)
expressionBasedfilter(exprs.2)
expGenes<-rownames(exprs.1)

rLinkfilter(exprs.1, exprs.2, cutoff = 0.8,r.method = c("pearson", "spearman")[1])
#基因筛选和链接删选

DCp.res<-DCp(exprs.1,exprs.2,link.method='qth',cutoff=0.25,N=0)
DCe.res<-DCe(exprs.1,exprs.2,link.method='qth',cutoff=0.25,nbins=10,p=0.1) 
DCsum.res<-DCsum(DCp.res,DCe.res,DCpcutoff=0.25,DCecutoff=0.4)
#最终DCsum.res包含DCGs和DCLs（差异共表达基因和链接）

DRsort.res<-DRsort(DCsum.res$DCGs,DCsum.res$DCLs,tf2target,expGenes)
#对DCsum输出的DCG和DCL进行排序筛选出可能的DRGs和DRLs(差异调控基因和链接)

DRplot.res<-DRplot(DCsum.res$DCGs,DCsum.res$DCLs,tf2target,expGenes,type='TF_bridged_DCL',vsize=5,asize=0.25,lcex=0.3,ewidth=1,figname=c('TF2target_DCL.pdf','TF_bridged_DCL.pdf'))
#可视化DRL和DCL交缠的网络

DRrank.res<-DRrank(DCsum.res$DCGs,DCsum.res$DCLs,tf2target,expGenes,rank.method=c('TED','TDD')[1],Nperm=0)
#使用三种可选择的测度指标优先处理候选因果调控基因。


#保存所有结果
DCE=DCe.res
DCP=DCp.res
DCSUM=DCsum.res
DCRPLOT=DRplot.res
DRSORT=DRsort.res
DRRANK=DRrank.res

save(DCE,DCP,DCSUM,DCRPLOT,DRSORT,DRRANK,file="result/result_GEO1.Rdata")
#save(DCE,DCP,DCSUM,DCRPLOT,DRSORT,DRRANK,file="result/result_GEO2.Rdata")
#save(DCE,DCP,DCSUM,DCRPLOT,DRSORT,DRRANK,file="result/result_TCGA.Rdata")





