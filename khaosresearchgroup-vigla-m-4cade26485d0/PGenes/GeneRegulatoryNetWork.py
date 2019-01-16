#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 10:05:57 2018

@author: khaosdev
"""

############ GENE REGULATORY NETWORKS ##############################
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
netthreshold=0.03

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


def generate_clustermap(idList, labelList, percentage):
   
    
    path = os.getcwd()
    dfz = load_gexpressions(idList, labelList, percentage)
    
    data = [go.Heatmap( z=dfz.values.tolist(), colorscale='Viridis')]
    
    py.iplot(data, filename='pandas-heatmap')


def Create_Graph(idList, labelList, percentage,netthreshold):
    dfz = load_gexpressions(idList, labelList, percentage)
    
    dfinvert=dfz.transpose()
     
    Netdata=pd.read_csv("network.csv")
    
    labels=list(dfinvert)
    
    limit=Netdata.index.size*netthreshold
    
    G=nx.from_pandas_edgelist(Netdata.head(int(limit)), 'TF', 'target',['importance'], create_using=nx.Graph() )
    print(nx.info(G))
    
    return G;








def generate_grnets(idList, labelList, percentage,netthreshold):
    
    #path = os.getcwd()
    dfz = load_gexpressions(idList, labelList, percentage)
    ########################
    
    dfinvert=dfz.transpose()
    # Compute the correlation matrix
    #corr = dfinvert.corr()
    
    #Netdata=pd.read_csv("network.csv")
    
    labels=list(dfinvert)
    #D=nx.to_networkx_graph(data,'TF','target')
    
    #limit=Netdata.index.size*netthreshold

    
    #Creamos nuestro grafo y almacenamos la posicion
    #G=nx.from_pandas_edgelist(Netdata.head(int(limit)), 'TF', 'target',['importance'], create_using=nx.Graph() )
    #print(nx.info(G))
    #G=nx.from_numpy_matrix(data,'TF', 'target' )
    #pos=nx.get_node_attributes(Grafo,'pos')
    
    ##################################################
    
    G=Create_Graph(idList, labelList, percentage,netthreshold)
    print(G.neighbors('HLA-DRB4'))

    #pos = nx.spectral_layout(G)
    
    pos = nx.spring_layout(G)
    #pos = nx.kamada_kawai_layout(G)
    #nx.draw_networkx_nodes(G,pos)
    
    #dmin=1
    #ncenter='HLA-DRB4'
    #for n in pos:
    #    x,y=pos[n]
    #    d=(x-0.5)**2+(y-0.5)**2
    #    if d<dmin:
    #        ncenter=n
    #        dmin=d
    
   # p=nx.single_source_shortest_path_length(G,ncenter)
            
    #Creamos las aristas de union entre nodos
    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=1,color='#888'),
        hoverinfo='text',
        mode='lines')
        
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]
    
    node_trace = Scatter(
        x=[],
        y=[],
        text=labels, # text=labels Le proporciono los nombres de genes a los nodos
        mode='markers+text',
        textposition='top',
        hoverinfo=[],
        marker=Marker(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='YIOrRd',
            reversescale=True,
            color=[],
            size=20,
            colorbar=dict(
                thickness=20,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=4)))
    
    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        
    #proporcionamos el color a nuestro grafo
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color'].append(len(adjacencies))
        node_info = 'Number of connections: '+str(len(adjacencies))
        node_trace['text'].append(node_info)
        
    #for edge, adyacencias in enumerate(G.adjacency()):
     #   edge_info= 'Number of connections: '+str(len(adjacencies))
      #  edge_trace['hoverinfo'].append(edge_info)
        
        
    fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
                title='<br>Network graph made with Python',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Gene Regulatory Network",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

    py.iplot(fig, filename='networkx')


#generate_grnets(idList, labelList, percentage,0.3)


def generate_grnetsGenes(idList, labelList, percentage,netthreshold):
    path = os.getcwd().split('arboreum')[0]
    dfz = load_gexpressions(idList, labelList, percentage)
    
    #transpongo la matrix para obtener los genes en forma de columnas
    networkdata=dfz.transpose()
    #print (networkdata.keys())
    #print (list(networkdata))
    
    #aplicando GRNBOOST2 obtengo un dataframe con el siguiente formato: ['TF', 'target', 'importance'], para así
    #poder utilizarlo en nuestra red de inferencias genicas
    #network = grnboost2(expression_data=networkdata, tf_names=list(networkdata))
    
    
    # Vamos a leer un dataframe con el formato  ['TF', 'target', 'importance'], que seria el resultado de aplicar el algoritmo de gnrboost2
    
    data=pd.read_csv("network.csv")
    data.head() 
    netdata=pd.read_csv("network_2.csv")
    netdata.head()
    
    labels=list(networkdata)
    
    limit=data.index.size*netthreshold

    
    #Creamos nuestro grafo y almacenamos la posicion
    G=nx.from_pandas_edgelist(data.head(int(limit)), 'TF', 'target',['importance'], create_using=nx.Graph() )
    print(nx.info(G))
    
    sorted(nx.connected_components(G), key = len, reverse=True)
    
    pos = nx.spring_layout(G)
    #pos = nx.circular_layout(G)
    #pos = nx.shell_layout(G)
    #pos = nx.nx_pydot.pydot_layout(G)
    
    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')
    
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]] 
        x1, y1 = pos[edge[1]] 
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]
    
    node_trace = Scatter(x=[], y=[], mode='markers+text',
                         text=labels,
                         textposition='top',
                         marker=Marker(size=10))
    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)
       
    fig = Figure(data=Data([edge_trace, node_trace]),
                 layout=Layout(title='Gene Regulatory Network',
                               showlegend=False, xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                               yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))
    
    py.iplot(fig, filename='RedGenica')
    
    #ts = time.time()
    #st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')
    
    #figpath =  path + "/home/khaosdev/AnacondaProjects/scripts (2) " + st + ".png"
    #network.to_csv(path + "\\figures\\network_" + st + ".csv")
    #plt.savefig(figpath)

#generate_grnetsGenes(idList, labelList, percentage,0.3) 
    
    
    #plt.axis('off')
    #plt.show()
    
   
def generate_arrowheadGraph():
    
    G=Create_Graph(idList, labelList, percentage,netthreshold)
    
    node_positions = nx.spring_layout(G,scale=10, dim=2)
    
 #   E=G.edges()
    
#    text=V[e[0]]['label']+' to '+V[e[1]]['label']
    
    node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers+text',
    textposition='top center',
    textfont=dict(
        family='arial',
        size=18,
        color='rgb(0,0,0)'
    ),
    hoverinfo=[],
    marker=go.Marker(
            showscale=False,
            color='rgb(200,0,0)',
            size=25,
            line=go.Line(width=1, color='rgb(0,0,0)')))

    for node in node_positions:
        x, y = node_positions[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        node_trace['text'].append(node)
        
        
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        node_info = 'Number of connections: '+str(len(adjacencies))
        node_trace['hoverinfo'].append(node_info)
    
    # The edges will be drawn as lines:
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=go.Line(width=1, color='rgb(150,150,150)'),
        hoverinfo='none',
        mode='lines')
    
    for edge in G.edges:
        x0, y0 = node_positions[edge[0]]
        x1, y1 = node_positions[edge[1]]
        edge_trace['x'].extend([x0, x1, None])
        edge_trace['y'].extend([y0, y1, None])
    
    # Create figure:
    fig = go.Figure(data = go.Data([edge_trace, node_trace]),
                 layout = go.Layout(
                    title = 'Gene Regulatory Netowork',
                    titlefont = dict(size=16),
                    showlegend = False,
                    hovermode = 'closest',
                    margin = dict(b=20,l=5,r=5,t=40),
                    xaxis = go.XAxis(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis = go.YAxis(showgrid=False, zeroline=False, showticklabels=False)))
    
    plotly.offline.plot(fig)
    
generate_arrowheadGraph()
    

    


    

    

    
