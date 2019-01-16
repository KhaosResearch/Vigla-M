#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 09:01:35 2018

@author: khaosdev
"""
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
import igraph as ig




import networkx as nx

import plotly.plotly as py
import plotly.graph_objs as go
import plotly
plotly.tools.set_credentials_file(username='sandrohr', api_key='F8o5VvB8jDUIMKBRvWoC')

from plotly.graph_objs import Figure,Data,Layout,Marker,Scatter,Scatter3d,Line,XAxis,YAxis,ZAxis,Scene,Margin,Annotations,Font,Annotation

edges=np.array([(2,3), (3, 1), (1, 0)], dtype=np.uint8)
nodes_loc=np.array([[0.3, 0.7], [1.2, 2.6], [2, 3.5], [0.85, 0.5]])
colors=['red', 'green', 'magenta']
nodes=dict(type='scatter',
           x=nodes_loc[:,0],
           y=nodes_loc[:,1],
           mode='markers',
           marker=dict(size=8, color='blue'))

edges_list=[ dict(type='scatter',
             x=[nodes_loc[e[0]][0], nodes_loc[e[1]][0]],
             y=[nodes_loc[e[0]][1], nodes_loc[e[1]][1]],
              mode='lines',
              line=dict(width=2, color=colors[k]))  for k, e in enumerate(edges)]
data=edges_list+[nodes]
fig=dict(data=data, layout=Layout)

py.iplot(fig, filename='Interacciones')