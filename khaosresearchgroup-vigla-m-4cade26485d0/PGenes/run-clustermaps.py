# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 12:00:42 2018

@author: Jose-Manuel
"""

import sys, ast
import genplots as gp

labelList=['t1', 't2', 't3', 't4']
idList=[1,2,3, 10114]
percentage=0.05


#idList = sys.argv[1] 
#labelList=sys.argv[2] 
#percentage=sys.argv[3]

if __name__ == '__main__':

    gp.generate_clustermap(idList, labelList, percentage)

