import parse as pr
import numpy as np
import read as rd
import normalize as nor
from scipy import stats as sst

fileList=['20170901_CART04_37_01.RCC', '20170901_CART04_39_03.RCC']

datalist=[]

for f in fileList:
    print(f) 
    t=rd.read(f)
    t2=pr.parse(t)
    datalist.append(t2)

results = nor.normalize(datalist)

print (results)
