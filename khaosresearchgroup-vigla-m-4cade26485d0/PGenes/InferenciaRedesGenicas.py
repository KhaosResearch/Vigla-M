# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 18:00:55 2018

@author: Jose-Manuel
"""

import os #, sys, ast
#os.path.abspath(os.path.dirname(sys.argv[0]))
path='/home/khaosdev/Documentos/Sandro/Investigación/scripts (2)'
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
from arboretum.algo import grnboost2 , genie3
#from arboretum.utils import load_tf_names
import networkx as nx
import matplotlib.pyplot as plt

import plotly
plotly.tools.set_credentials_file(username='sandrohr', api_key='F8o5VvB8jDUIMKBRvWoC')
import plotly.plotly as py
from plotly.graph_objs import Figure,Data,Layout,Marker,Scatter,Line,XAxis,YAxis

from math import pi
from bokeh.io import show
from bokeh.io import export_png
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    BasicTicker,
    PrintfTickFormatter,
    ColorBar,
)
from bokeh.plotting import figure
#from bokeh.sampledata.unemployment1948 import data

#####################################   TEST    ################################################

#labelList=['l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7','l8', 'l9']
labelList=['t1', 't2', 't3', 't4']
type(labelList)
#idList=[1, 2, 3, 20, 21, 22, 25, 31, 32]
idList=[1,2,3, 10114]
percentage=0.05

#res=pd.read_csv('C:\\Users\\Jose-Manuel\\Documents\\PUBLICACIONES\\REVISTAS\\BMCBioinformatics\\scripts\\dataset.csv')


################################### PREPROCESS DATA & CLUSTER MAP ########################################################
#idList, labelList, percentage

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



################################### GENE REGULATORY NETWORKS ########################################################
    
def generate_grnets(idList, labelList, percentage,netthreshold):
    path = os.getcwd()
    dfz = load_gexpressions(idList, labelList, percentage)  
    netdata=dfz.T
    #corr: nos devuelve una matriz cuadrada donde cada fila y columna representará
    #cada uno de los nodos del grafo. Los nodos serán los genes.
    corr = netdata.corr()
   # df = corr.drop('index', 1)
    G = nx.relabel_nodes(G, dict(enumerate(corr.columns)))
    #G = nx.from_numpy_matrix(corr.values)
    #G=nx.Graph(corr)
    G.name = 'Graph from pandas adjacency matrix'
    print(nx.info(G))
    
    #posición se almacena como datos de atributo de nodo para G
    #devulve un diccionario de atributos codificados por nodos
    pos=nx.get_node_attributes(G,'pos')
    #¿Porque no me almacena los valores?


    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d

    p=nx.single_source_shortest_path_length(G,ncenter)
    #ncenter no se encuentra en los valores de G
    
    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')
        
    #para añadir las aristas entre nodos
    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
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
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
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

    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'].append(x)
        node_trace['y'].append(y)
    
    for node, adjacencies in enumerate(G.adjacency_list()):
        node_trace['marker']['color'].append(len(adjacencies))
        node_info = '# of connections: '+str(len(adjacencies))
        node_trace['text'].append(node_info)


    
    
    fig = Figure(data=Data([edge_trace, node_trace]),
                 layout=Layout(
                    title='<br>Network graph made with Python',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))
    
    py.iplot(fig, filename='networkx')
    
    #nx.draw(G)
    #plt.savefig("path.png")

    
    """
    ## generate network 
    netdata=dfz.T # rotate matrix
    network = grnboost2(expression_data=netdata, tf_names=list(netdata)) # generate network
    #network = genie3(expression_data=netdata, tf_names=list(netdata)) # generate network

    network.rename(columns={'importance': 'value'}, inplace=True)
    
    # Build your graph
    limit=network.index.size*netthreshold
    G=nx.from_pandas_dataframe(network.head(int(limit)), 'TF', 'target', create_using=nx.Graph() )
    #G=nx.from_pandas_dataframe(network, 'TF', 'target', create_using=nx.Graph() )


    pos = nx.spring_layout(G, scale=10, dim=2)
    #pos = nx.circular_layout(G)
    #pos = nx.shell_layout(G)
    #pos = nx.spectral_layout(G)
    # Custom the nodes:
    #nx.draw(G, with_labels=True, node_color='blue', node_size=1500, edge_color=network['value'].head(100), width=10.0, edge_cmap=plt.cm.Blues)
    #nx.draw(G, with_labels=False, node_color='r', alpha=0.5, node_size=500, edge_color=network['value'].head(len(G.edges(data=True))), width=10.0, edge_cmap=plt.cm.Blues)
    
    pos = nx.nx_pydot.pydot_layout(G)
    #pos = nx.nx_pydot.pydot_layout(G, prog='dot')
    #pos = nx.nx_pydot.pydot_layout(G, prog='neato')
    
    # labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=200, node_color='r', alpha=0.3)
    # edges
    nx.draw_networkx_edges(G, pos, dge_color=network['value'].head(len(G.edges(data=True))), width=3.0, edge_cmap=plt.cm.Blues, alpha=0.3)    


    plt.axis('off')
    #plt.show()
    
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')
    
    #save figure with hetmap
    figpath =  path + "\\figures\\network_" + st + ".png"
    #network.to_csv(path + "\\figures\\network_" + st + ".csv")
    plt.savefig(figpath)
    
    return figpath
    """

############################################################  test
    
generate_grnets(idList, labelList, percentage,0.3)

#%> python -c "import genplots as gp; p=gp.generate_grnets([1, 2, 3, 10114], ['t1', 't2', 't3', 't4'], 0.05)"

#%> python -c "import genplots as gp; p=gp.generate_clustermap([1, 2, 3, 10114], ['t1', 't2', 't3', 't4'], 0.05)"

#int __name__=="__main__"
    
    
    


    
    
    
