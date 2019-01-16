#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 10:05:57 2018

@author: khaosdev
"""

############ GENE REGULATORY NETWORKS ##############################
import os #, sys, ast
#os.path.abspath(os.path.dirname(sys.argv[0]))
path='/home/khaosdev/AnacondaProjects/scripts (2)'
os.chdir(path) #Para cambiar al directorio actual
import time
from datetime import datetime
#import parse2 as pr
import numpy as np
#import read2 as rd
#import normalize2 as nor
from scipy import stats as sst
import pandas as pd
import seaborn as sns
import findStable as fs
import prelimAnalisis as pa
from arboretum.algo import grnboost2, genie3
import matplotlib.pyplot as plt
import json




import networkx as nx

import plotly.plotly as py
import plotly.graph_objs as go
import plotly
plotly.tools.set_credentials_file(username='sandrohr', api_key='F8o5VvB8jDUIMKBRvWoC')

from plotly.graph_objs import Figure,Data,Layout,Marker,Scatter,Line,XAxis,YAxis


labelList=['t1', 't2', 't3', 't4']
type(labelList)
#idList=[1, 2, 3, 20, 21, 22, 25, 31, 32]
idList=[1,2,3, 10114]
percentage=0.05
netthreshold=0.3
data=pd.read_csv("network.csv")

def load_gexpressions(idList, labelList, percentage):
    os.getcwd()  #Para conocer el directorio actual
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
    
    return dfz



dfz = load_gexpressions(idList, labelList, percentage)
    
dfinvert=dfz.transpose()
     
#Netdata=pd.read_csv("network.csv")
 #   Netdata.head()
    
labels=list(dfinvert)
    
 #   limit=Netdata.index.size*netthreshold
    
    #G=nx.from_pandas_edgelist(Netdata.head(int(limit)), 'TF', 'target',['importance'], create_using=nx.Graph() )
    #print(nx.info(G))
    
 


def Adjacency_Graph(data,threshold):
    edge=[]
    for i in range(len(data)):
        if data['importance'][i]>=threshold:
            edge.append((data['TF'][i],data['target'][i]))      
   

#Get number of edges
    n=len(data)
    num_of_adjacencies=[]
    for i in range(n):
        num_of_adjacencies.append(0)
    for d in edge:
        num_of_adjacencies[d[0]-1]+=1
        num_of_adjacencies[d[1]-1]+=1

#prepare de graph

    edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')
    
    for i in range(len(edge)):
        e1=edge[i][0]-1
        e2=edge[i][1]-1
        x0, y0 = data['TF'][e1],data['target'][e1]
        x1, y1 = data['TF'][e2],data['target'][e2]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=Marker(
            showscale=True,
            colorscale='YIGnBu',
            reversescale=True,
            color=[],
            size=10,
             colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))
    
    for i in range(len(data)):
        x, y = data['TF'][i],data['target'][i]
        node_trace['x'].append(x)
        node_trace['y'].append(y)

    for i in range(len(data)):
        node_info = labels[i]
        node_trace['text'].append(node_info)
        node_trace['marker']['color'].append(num_of_adjacencies[i])

        
    fig = Figure(data=Data([edge_trace, node_trace]),
                 layout=Layout(
                    title='<br>NYC texi trip neighborhood interactions',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))
    
    return fig

Adjacency_Graph(data,500)




