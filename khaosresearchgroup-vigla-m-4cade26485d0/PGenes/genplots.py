# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 18:00:55 2018

@author: Jose-Manuel
"""

import os #, sys, ast
#os.path.abspath(os.path.dirname(sys.argv[0]))
path='/home/khaosdev/AnacondaProjects/PGenes'
os.chdir(path) #Para cambiar al directorio actual
import time
from datetime import datetime
#import parse2 as pr
#import read2 as rd
#import normalize2 as nor
from scipy import stats as sst
import pandas as pd
import seaborn as sns
import findStable as fs
import prelimAnalisis as pa
from dask.distributed import Client, LocalCluster 

from arboretum.algo import grnboost2 , genie3
#from arboretum.utils import load_tf_names
import networkx as nx
import matplotlib.pyplot as plt

from math import pi
from bokeh.io import show
from bokeh.io import export_png, output
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    BasicTicker,
    PrintfTickFormatter,
    ColorBar,
)
from bokeh.plotting import figure,output_file, save




import plotly.plotly as py
import plotly
plotly.tools.set_credentials_file(username='sandrohr', api_key='F8o5VvB8jDUIMKBRvWoC')
from plotly.graph_objs import Figure,Data,Layout,Marker,Scatter3d,Line,XAxis,YAxis,ZAxis,Scene,Margin,Annotations,Font,Annotation



#from bokeh.sampledata.unemployment1948 import data

#####################################   TEST    ################################################

#labelList=['l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7','l8', 'l9']
labelList=['t1', 't2', 't3', 't4']
type(labelList)
#idList=[1, 2, 3, 20, 21, 22, 25, 31, 32]
idList=[1,2,3, 10114]
percentage=0.05
netthreshold=0.05

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

    #show(p)      # show the plot
    filename = save(p,filename="bokeh.html",title="Gene_Heatmap")
    #output_file("clustermap.html",title="Gene_Heatmap" )
    
    #obtain time stamp
    #ts = time.time()
    #st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')
    
    #save figure with hetmap
    #figpath =  path + "\\fig\\clustermap_" + st + ".png"    
    
    #filepath="clustermap.png"
    #p.savefig(figpath)
    #save(p)
    #export_png(p, filename=filepath)
    
    #fig=p.get_figure()
    #Figure=fig.savefig("clustermap.png")
    


    return filename



#############################################################  test 
#p = generate_clustermap(idList, labelList, percentage)


################################### DIAGONAL CORRELATION MATRIX #####################################################
def generate_correlation(idList,labelList,percentage):
    
    path = os.getcwd()
    
    dfz = load_gexpressions(idList, labelList, percentage)
    #Transpongo el dataframe para obetener el formato que necesito
    dfinvert=dfz.transpose()

    
    sns.set(style="white")
    
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
    #figpath =  path + "\\figures\\DiagonalCorrelationMatrix_" + st + ".png"
    
    fig=sns_plot.get_figure()
    
    Figure=fig.savefig(path+"DiagonalCorrelationMatrix_" + st + ".png")
    
    return Figure

#correlacion=generate_correlation(idList,labelList,percentage)

################################ REDES NEURONALES GÉNICAS #################################################

def Create_Graph(idList, labelList, percentage,netthreshold): #CREACIÓN DEL GRAFO
    dfz = load_gexpressions(idList, labelList, percentage)
    
    #Preparo Dataframe de forma que contenga todos los genes en las columnas
    dfinvert=dfz.transpose()
    #Obtengo la lista de genes
    TF_names=list(dfinvert)
    
    client = Client(processes=False)

    
    network = grnboost2(expression_data=dfinvert, tf_names=TF_names, client_or_address=client) # generate network
    #networkG = genie3(expression_data=dfinvert, tf_names=TF_names) # generate network
    #ts = time.time()
    #st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')
    #network.to_csv(path + "\\figures\\network_" + st + ".csv")
    
     
    #network=pd.read_csv("network.csv")
    
    #labels=list(dfinvert)
    
    limit=network.index.size*netthreshold
    
    G=nx.from_pandas_edgelist(network.head(int(limit)), 'TF', 'target',['importance'], create_using=nx.Graph(directed=False) )
    print(nx.info(G))
    
    return G;

def Generate_3DModel(): #REPRESENTACIÓN DEL MODELO 3D
   
    #network=pd.read_csv("network.csv")
    #L=len(network['TF'])
    
    
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

    
    #for  e in enumerate(Edges):
    
     #   text=V[e[0]]['label']+' to '+V[e[1]]['label']
        
   # edge_info=[]
   # edge_info.append(Scatter3d( 
    #                         mode='markers', 
     #                        marker=Marker( size=0.5,  color='#6959CD'),
      #                       text=text, 
       #                      hoverinfo='text'
        #                     ))
        
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
                text="Redes Neuronales Génicas",
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
    
    fig=plotly.offline.plot(fig, filename='3DNetworkx.html',auto_open=False)
    
    return fig

    
    
Generate_3DModel()


################################### GENE REGULATORY NETWORKS ########################################################
    
def generate_grnets(idList, labelList, percentage,netthreshold):
    path = os.getcwd()
    dfz = load_gexpressions(idList, labelList, percentage)   
    
    ## generate network 
    netdata=dfz.T # rotate matrix
    network = grnboost2(expression_data=netdata, tf_names=list(netdata)) # generate network
    networkG = genie3(expression_data=netdata, tf_names=list(netdata)) # generate network

    network.rename(columns={'importance': 'value'}, inplace=True)
    # Build your graph
    limit=network.index.size*netthreshold
    G=nx.from_numpy_matrix(data.head(int(limit)), 'TF', 'target', create_using=nx.Graph() )
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
    plt.show()
    
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')
    
    #save figure with hetmap
    figpath =  path + "\\figures\\network_" + st + ".png"
    #network.to_csv(path + "\\figures\\network_" + st + ".csv")
    plt.savefig(figpath)
    
    return figpath

############################################################  test
    
#generate_grnets(idList, labelList, percentage,0.03)

#%> python -c "import genplots as gp; p=gp.generate_grnets([1, 2, 3, 10114], ['t1', 't2', 't3', 't4'], 0.05)"

#%> python -c "import genplots as gp; p=gp.generate_clustermap([1, 2, 3, 10114], ['t1', 't2', 't3', 't4'], 0.05)"

#int __name__=="__main__"
    
    
    


    
    
    
