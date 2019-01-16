#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 09:02:14 2018

@author: khaosdev
"""
import genplots as gp
import sys
labelList=['t1', 't2', 't3', 't4']
idList=[1,2,3, 10114]
percentage=0.05
netthreshold=0.05

#idList = sys.argv[1] 
#labelList=sys.argv[2] 
#percentage=sys.argv[3]




if __name__ == '__main__':
    
    gp.generate_clustermap(idList, labelList, percentage)
    gp.generate_correlation(idList,labelList,percentage)
    gp.Generate_3DModel()

    
    