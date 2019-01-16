import parse2 as pr
import numpy as np
import read2 as rd
import normalize2 as nor
import cx_Oracle
from scipy import stats as sst

#fileList=['/home/khaosdev7/Downloads/20170901_CART04_RCC/20170901_CART04_56_12.RCC', '/home/khaosdev7/Downloads/20170901_CART04_RCC/20170901_CART04_54_10.RCC', '/home/khaosdev7/Downloads/20170901_CART04_RCC/20170901_CART04_42_11.RCC']

idList=[1,2]

con = cx_Oracle.connect('webapp/khaosmelanomaweb@192.168.43.84:1521')

datalist=[]
flags=[]

for f in idList:
    print(f) 
    dt=rd.read(f, con)
    dt=pr.parse(dt)
    datalist.append(dt[2])
    flags.append(dt[3])

con.close()    

nor.process(dt[0], dt[1], idList, datalist, flags)
#print (results)
