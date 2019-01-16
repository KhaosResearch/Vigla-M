# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 18:00:55 2018

@author: Jose-Manuel
"""

import os #, sys, ast
#os.path.abspath(os.path.dirname(sys.argv[0]))
path='/home/khaosdev/Documentos/Sandro/Investigación/scripts (2)/genplots (copia)'
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


def generate_clustermap(idList, labelList, percentage):
    path = os.getcwd()
    
    dfz = load_gexpressions(idList, labelList, percentage)
    
    dfz.index.name='Genes'
    dfz.columns.name = 'Muestras'
   
    dfej = pd.DataFrame(dfz.stack(), columns=['percentage']).reset_index()
    
    genes = list(dfz.index)
    muestras = list(dfz.columns)
   
    colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    mapper = LinearColorMapper(palette=colors, low=dfej.percentage.min(), high=dfej.percentage.max())

    source = ColumnDataSource(dfej)  #Contiene los datos que le hemos pasado en forma de columnas

    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

    p = figure(title="HEATMAPMelanoma",
             x_range=genes, y_range=muestras,
             x_axis_location="above", plot_width=900, plot_height=400,
             tools=TOOLS, toolbar_location='below')
   
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "5pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = pi / 3
        
   # m1=list(dfz['t1'])
   # m2=list(dfz['t2'])
   # m3=list(dfz['t3'])
   # m4=list(dfz['t4'])
   # genes=dfz.index
    
    #dfz = dfz.set_index('Muestras')
    #dfz.columns.name='Genes'

    
   # for m in [m1,m2,m3,m4]:
    #    for g in genes:
     #       contm=0
      #      contg=0
       #     s2= genes[contg],m[contm]
        #    contg=contg+1
         #   print (s2)
       # contm=contm+1

    #for g in genes:    
     #   gen=0
      #  for m in [m1, m2, m3, m4]:
      #      cont=0
       #     s1=genes[gen],m[cont]
        #    cont=cont+1 
         #   gen=gen+1
         #   print (s1)
        
  #  M=m1+m2

   # Genes=genes+genes
    
   # dfnew=pd.DataFrame(M,Genes)
   
    #Formamos un rectangulo

    p.rect(x='Genes', y='Muestras', width=1, height=1,
        source=source,
        fill_color={'field':'percentage', 'transform': mapper},
        line_color=None)
    
    
   
    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                     ticker=BasicTicker(desired_num_ticks=len(colors)),
                     formatter=PrintfTickFormatter(format="%d%%"),
                     label_standoff=6, border_line_color=None, location=(0, 0))
    p.add_layout(color_bar, 'right')

    #rate: porcentaje
    p.select_one(HoverTool).tooltips = [
     ('percentage', '@percentage%')  
     ]   

    show(p)      # show the plot
    
    #obtain time stamp
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')
    
    #save figure with hetmap
    figpath =  path + "\\figures\\clustermap_" + st + ".png"    
    #fig=plt.figure(p)
    #fig.savefig(figpath)
    #export_png(p, filename="\\figures\\clustermap_" + st + ".png" )

    return figpath



#############################################################  test 
    
#p = generate_clustermap(idList, labelList, percentage)

################################### DIAGONAL CORRELATION MATRIX #####################################################
def generate_correlation(idList,labelList,percentage):
    
    path = os.getcwd()
    
    dfz = load_gexpressions(idList, labelList, percentage)
    dfinvert=dfz.transpose()

    
    sns.set(style="white")

    # Generate a large random dataset
    #rs = np.random.RandomState(100)
    #df1 = pd.DataFrame(dfz,
     #            columns=(dfz.index))
    
    # Compute the correlation matrix
    corr = dfinvert.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns_plot=sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')
    
    #save figure with hetmap
    figpath =  path + "\\figures\\DiagonalCorrelationMatrix_" + st + ".png"
    sns_plot.savefig(figpath)
    
    return figpath

#generate_correlation(idList, labelList, percentage)



################################### GENE REGULATORY NETWORKS ########################################################
    
def generate_grnets(idList, labelList, percentage,netthreshold):
    path = os.getcwd()
    dfz = load_gexpressions(idList, labelList, percentage)   
    
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

############################################################  test
    
generate_grnets(idList, labelList, percentage,0.3)

#%> python -c "import genplots as gp; p=gp.generate_grnets([1, 2, 3, 10114], ['t1', 't2', 't3', 't4'], 0.05)"

#%> python -c "import genplots as gp; p=gp.generate_clustermap([1, 2, 3, 10114], ['t1', 't2', 't3', 't4'], 0.05)"
"""
if __name__== "__main__":
    
    p = generate_clustermap(idList, labelList, percentage)
    network=generate_grnets(idList, labelList, percentage,0.5)


    path = os.getcwd()
    
    dfz = load_gexpressions(idList, labelList, percentage)
    
    dfz.index.name='Genes'
    dfz.columns.name = 'Muestras'

    genes = list(dfz.index)
    muestras = list(dfz.columns)
    dfej = pd.DataFrame(dfz.stack(), columns=['rate']).reset_index()
"""