# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 14:54:02 2018

@author: Jose-Manuel
"""
import plotly
plotly.tools.set_credentials_file(username='sandrohr', api_key='••••••••••')
import os
path='/home/khaosdev/Documentos/Sandro/Investigación/scripts (2)'
os.chdir(path)
import time
from datetime import datetime
import parse2 as pr
import numpy as np
import read2 as rd
import normalize2 as nor
from scipy import stats as sst
import pandas as pd
import seaborn as sns
import findStable as fs
import prelimAnalisis as pa

#idList=sys.argv[2:]
#runNorm(idList, sys.argv[1])

################################### PREPROCESS DATA ########################################################
#idList, labelList, percentage

#labelList=['l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7','l8', 'l9']

labelList=['t1', 't2', 't3', 't4']
#idList=[1, 2, 3, 20, 21, 22, 25, 31, 32]
idList=[1, 2, 3, 10114]
percentage=0.05
#
#iris = sns.load_dataset("iris")
#species = iris.pop("species")
#lut = dict(zip(species.unique(), "rbg"))

def generate_heatmap(idList, labelList, percentage):
    
    path = os.getcwd()
    # Connect to database to obtain data according to idList ids
    res=pa.runNorm(idList, 'webapp/khaosmelanomaweb@192.168.43.84:1521')
    
    # convert data to proper dataframe
    cont=0
    df=pd.DataFrame(index=res[cont].tolist())
    for i in labelList:
        cont += 1
        df[i]=res[cont].tolist()        
        
    ## obtain unstable genes 
    ngenes=int(df.index.size*percentage)
    unstable_genes=fs.findUnstable(df.values,ngenes)
    
    ## select unstable genes from dataframe to plot
    M=pd.DataFrame()
    for g in unstable_genes:
        M=pd.concat([M,df.iloc[[g]]])
    
    # transform to zscope in axis 1 (rows)
    dfzs1=sst.zscore(M.values, axis=1, ddof=1)
    dfz=pd.DataFrame(index=M.index,data=dfzs1,columns=labelList)
    
    # generate hetmap plot
    # add colored label
    #sns_plot = sns.clustermap(dfz, figsize=(len(labelList)/2, ngenes/2), cmap='viridis', metric="correlation", row_colors=row_colors)
    sns_plot = sns.clustermap(dfz, figsize=(ngenes/3, ngenes/2), cmap='viridis')
    
    #obtain time stamp
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')
    
    #save figure with hetmap
    figpath =  path + "\\output_" + st + ".png"
    sns_plot.savefig(figpath)
    
    return figpath


p = generate_heatmap(idList, labelList, 0.05)


# hacer función para correlation plot 

###################################### ANALYSIS AND VISUALIZATION #############################################
#idList=[1, 2, 3, 20, 21, 22, 25, 31, 32]

#res=loadData(idList, 'webapp/khaosmelanomaweb@192.168.43.84:1521')

df=pd.DataFrame(index=res[0].tolist(),data=res.values,columns=labelList)


df=pd.DataFrame(index=res[0].tolist(),data=res[1].tolist(),columns=['E1'])  # 1st row as the column names
df['E2']=res[2].tolist()
df['E3']=res[3].tolist()
df['E20']=res[4].tolist()
df['E21']=res[5].tolist()
df['E22']=res[6].tolist()
df['E25']=res[7].tolist()
df['E31']=res[8].tolist()
df['E32']=res[9].tolist()

sns.clustermap(df, figsize=(5, 100), cmap='viridis')

df.describe()

df.to_csv('dataset.csv');



unstable_genes=fs.findUnstable(df.values,100)




M=pd.DataFrame()
for g in unstable_genes:
    M=pd.concat([M,df.iloc[[g]]])
    
sns.clustermap(M, figsize=(5, 50), cmap='viridis')

# =============================================================================
# df=pd.DataFrame(index=res[0].tolist(),data=sst.zscore(res[1],axis=0, ddof=1).tolist(),columns=['E1'])  # 1st row as the column names
# df['E2']=sst.zscore(res[2],axis=1, ddof=10).tolist()
# df['E3']=sst.zscore(res[3],axis=1, ddof=10).tolist()
# df['E20']=sst.zscore(res[4],axis=1, ddof=10).tolist()
# df['E21']=sst.zscore(res[5],axis=1, ddof=10).tolist()
# df['E22']=sst.zscore(res[6],axis=1, ddof=10).tolist()
# df['E25']=sst.zscore(res[7],axis=1, ddof=10).tolist()
# df['E31']=sst.zscore(res[8],axis=1, ddof=10).tolist()
# df['E32']=sst.zscore(res[9],axis=1, ddof=10).tolist()
# =============================================================================

dfzs1=sst.zscore(M.values, axis=1, ddof=1)
dfz=pd.DataFrame(index=M.index,data=dfzs1,columns=['E1', 'E2','E3','E20','E21','E22','E25','E31','E32',])


sns.clustermap(dfz, figsize=(5, 50), cmap='viridis')

#sns.clustermap(df,z_score=0, figsize=(5, 40), cmap='viridis') # z_score 0 (rows) 1 (columns)

#sns.clustermap(df,standard_scale=0, figsize=(5, 40), cmap='viridis')



import cufflinks as cf
import plotly as py


#import plotly.figure_factory as ff
# Correct datatypes cufflinks does not support CategoryType so we make them strings and rebuild the dataframe. 
#df_flights = pd.DataFrame(data=flight_matrix.as_matrix(), index=flight_matrix.index.astype('str'), columns=flight_matrix.columns)

#fig = ff.create_annotated_heatmap(z=dfz.values, colorscale='Viridis')


fig=dfz.iplot(kind='heatmap', colorscale='spectral',  asFigure=True )
py.offline.plot(fig,filename="example.html")

########################### GENE REGULATION NETWORKS ###################################

#from pypanda import Panda
#from pypanda import AnalyzePanda
#from pypanda import Lioness
#import pandas as pd
#
#p = Panda('ToyExpressionData.txt', 'ToyMotifData.txt', 'ToyPPIData.txt', remove_missing=True)
#p.save_panda_results(file = 'Toy_Panda.pairs')
#plot = AnalyzePanda(p)
#plot.top_network_plot(top=100, file='top_100_genes.png')

from arboretum.algo import grnboost2, genie3
from arboretum.utils import load_tf_names

netdata=dfz.T # rotate matrix
network = grnboost2(expression_data=netdata, tf_names=list(netdata)) # generate network

############################ PLOT 3D NETWORK ############################################

import networkx as nx
import matplotlib.pyplot as plt
 
# Build a dataframe with your connections
df = pd.DataFrame({ 'from':['A', 'B', 'C','A'], 'to':['D', 'A', 'E','C'], 'value':[1, 10, 5, 5]})
df.rename(columns={'importance': 'value'}, inplace=True)
df

network.rename(columns={'importance': 'value'}, inplace=True)
 
# Build your graph
#G=nx.from_pandas_dataframe(network.head(100), 'TF', 'target', create_using=nx.Graph() )
G=nx.from_pandas_dataframe(df.head(100), 'from', 'to', create_using=nx.Graph() )
 
# Custom the nodes:
#nx.draw(G, with_labels=True, node_color='blue', node_size=150, edge_color=network['value'].head(100), width=100.0, edge_cmap=plt.cm.Blues)
nx.draw(G, with_labels=True, node_color='blue', node_size=1500, edge_color=df['value'], width=10.0, edge_cmap=plt.cm.Blues)
 

