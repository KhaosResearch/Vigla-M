# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 13:19:06 2018

@author: Jose-Manuel
"""

import json
import pandas as pd
import igraph as ig

data = []

import urllib.request

with urllib.request.urlopen('https://raw.githubusercontent.com/plotly/datasets/master/miserables.json') as response:
   jsonfile = response.read()


data = json.loads(jsonfile)

print(data.keys())

N=len(data['nodes'])

## Define the list of edges and the Graph object from Edges:

L=len(data['links'])
Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]

G=ig.Graph(Edges, directed=False)

## Extract the node attributes, 'group', and 'name':

data['nodes'][0]

labels=[]
group=[]
for node in data['nodes']:
    labels.append(node['name'])
    group.append(node['group'])
    
# Get the node positions, set by the Kamada-Kawai layout for 3D graphs:
    
layt=G.layout('kk', dim=3)
layt[5]

# layt is a list of three elements lists (the coordinates of nodes):

# Set data for the Plotly plot of the graph:

Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
Yn=[layt[k][1] for k in range(N)]# y-coordinates
Zn=[layt[k][2] for k in range(N)]# z-coordinates
Xe=[]
Ye=[]
Ze=[]
for e in Edges:
    Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
    Ye+=[layt[e[0]][1],layt[e[1]][1], None]
    Ze+=[layt[e[0]][2],layt[e[1]][2], None]
    
import plotly.plotly as py
from plotly.graph_objs import *

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
               mode='markers',
               name='actors',
               marker=Marker(symbol='dot',
                             size=6,
                             color=group,
                             colorscale='Viridis',
                             line=Line(color='rgb(50,50,50)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
               )
               
axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

layout = Layout(
         title="Network of coappearances of characters in Victor Hugo's novel<br> Les Miserables (3D visualization)",
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
            text="Data source: <a href='http://bost.ocks.org/mike/miserables/miserables.json'>[1] miserables.json</a>",
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
        ]),    )
            
data=Data([trace1, trace2])
fig=Figure(data=data, layout=layout)

py.iplot(fig, filename='Les-Miserables')


