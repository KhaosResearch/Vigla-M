#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 13:12:06 2018

@author: khaosdev
"""

import os #, sys, ast
#os.path.abspath(os.path.dirname(sys.argv[0]))
path='/home/khaosdev/AnacondaProjects/PGenes'
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
import igraph as ig




import networkx as nx

import plotly.plotly as py
import plotly.graph_objs as go
import plotly
plotly.tools.set_credentials_file(username='sandrohr', api_key='F8o5VvB8jDUIMKBRvWoC')

from plotly.graph_objs import Figure,Data,Layout,Marker,Scatter,Scatter3d,Line,XAxis,YAxis,ZAxis,Scene,Margin,Annotations,Font,Annotation


labelList=['t1', 't2', 't3', 't4']
type(labelList)
#idList=[1, 2, 3, 20, 21, 22, 25, 31, 32]
idList=[1,2,3, 10114]
percentage=0.05
netthreshold=0.01

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



def Create_Graph(idList, labelList, percentage,netthreshold):
    dfz = load_gexpressions(idList, labelList, percentage)
    dfinvert=dfz.transpose()
    
    #network = grnboost2(expression_data=dfinvert, tf_names=list(dfinvert)) # generate network
    #networkG = genie3(expression_data=dfinvert, tf_names=list(dfinvert)) # generate network
    #network.to_csv(path + "\\figures\\network_" + st + ".csv")
    
     
    network=pd.read_csv("network.csv")
    
    labels=list(dfinvert)
    
    limit=network.index.size*netthreshold
    
    G=nx.from_pandas_edgelist(network.head(int(limit)), 'TF', 'target',['importance'], create_using=nx.Graph(directed=False) )
    print(nx.info(G))
    
    return G;

def Generate_3DModel(idList, labelList, percentage):
   
    network=pd.read_csv("network.csv")
    L=len(network['TF'])
    
    
    #Values=[network['importance'][k] for k in range(L)]
    
    #G=ig.Graph(Edges, directed=False)
    #layt=G.layout('kk', dim=3)
    
        
    G=Create_Graph(idList, labelList, percentage,netthreshold)
    N=len(list(G.node())) #--> Numero de nodos
    V=list(G.node())    # lista con todos los nodos
    
    #Edges=[(network['TF'][k], network['target'][k]) for k in range(L)] 
    Edges= list(G.edges())

  
    #layt=nx.spectral_layout(G,dim=3)
   
    #layt=nx.spring_layout(G, dim=3)
    #layt=nx.fruchterman_reingold_layout(G,dim=3) 
    #layt=laytdict.values()
    
    #g=nx.Graph()
    #g.add_nodes_from(V)
    #g.add_edges_from(Edges)
    
    layt=nx.fruchterman_reingold_layout(G,dim=3) 
    #layt = nx.circular_layout(G,scale=10,dim=3)
    #layt=nx.spring_layout(G,dim=3) 
    laytN=list(layt.values())
    

    Xn=[laytN[k][0] for k in range(N)]# x-coordinates of nodes
    Yn=[laytN[k][1] for k in range(N)]# y-coordinates
    Zn=[laytN[k][2] for k in range(N)]# z-coordinates
    Xe=[]
    Ye=[]
    Ze=[]
    for e in Edges:
        Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
        Ye+=[layt[e[0]][1],layt[e[1]][1], None]
        Ze+=[layt[e[0]][2],layt[e[1]][2], None]


        
    trace1=Scatter3d(x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=Line(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )
    trace2=Scatter3d(x=Xn,
                   y=Yn,
                   z=Zn,
                   mode='markers+text',
                   textposition='top',
                   name='genes',
                   marker=Marker(symbol='dot',
                                 size=6,
                                 color='#6959CD',
                                 colorscale='Viridis',
                                 line=Line(color='rgb(50,50,50)', width=1)
                                 ),
                   text=V,
                   hoverinfo='text'
                   )
                   
   
    #for node, adjacencies in enumerate(G.adjacency()):
      #trace2['marker']['color'].append(len(adjacencies))
      #node_info = 'Number of connections: '+str(len(adjacencies))
      #trace2['text'].append(node_info)
                   
    axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )
    
    fig=Figure(data=Data([trace1, trace2]),
        layout = Layout(
             title="Network (3D visualization)",
             width=1000,
             height=1000,
             showlegend=False,
             scene=Scene(
             xaxis=XAxis(axis),
             yaxis=YAxis(axis),
             zaxis=ZAxis(axis),
            ),
         margin=Margin(
            t=100
        ),
        hovermode='closest',
        annotations=Annotations([
               Annotation(
               showarrow=False,
                text="",
                xref='paper',
                yref='paper',
                x=0,
                y=0.1,
                xanchor='left',
                yanchor='bottom',
                font=Font(
                size=14
                )
                )
            ]),    ))

    py.iplot(fig, filename='networkx3D')

    
    
Generate_3DModel(idList, labelList, percentage)



    


    
    





