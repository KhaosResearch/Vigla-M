import os
path='/home/khaosdev/AnacondaProjects/PGenes'
os.chdir(path)
import parse2 as pr
import numpy as np
import read2 as rd
import normalize2 as nor
import cx_Oracle
#import sys
#from scipy import stats as sst
#import pandas as pd
#import seaborn as sns
#import findStable as fs

######################################################################################################
def loadData(idList, conString):
    con = cx_Oracle.connect(conString)
    datalist=[]
    flags=[]  
    genes=[]

    for f in idList:
    #print(f) 
        dt=rd.read(int(f), con)
        dt=pr.parse(dt)
        if (len(genes)>0):
            if not np.all(np.array(dt[0])==np.array(genes)):
                print('Gene lists do not match')        
                exit()
        genes=dt[0]
        datalist.append(dt[2])
        flags.append(dt[3])
        
    con.close()    
    
    results = []
    results.append(genes)
    results.append(flags)
    results.append(datalist)
    
    return results



def runNorm(idList, conString):
    con = cx_Oracle.connect(conString)
    datalist=[]
    flags=[]  
    genes=[]

    for f in idList:
    #print(f) 
        dt=rd.read(int(f), con)
        dt=pr.parse(dt)
        if (len(genes)>0):
            if (np.all(np.array(dt[0])==np.array(genes))!=True):
                print('Gene lists do not match')        
                exit()
        genes=dt[0]
        datalist.append(dt[2])
        flags.append(dt[3])
        
    con.close()    

    return nor.process(genes, dt[1], idList, datalist, flags)






