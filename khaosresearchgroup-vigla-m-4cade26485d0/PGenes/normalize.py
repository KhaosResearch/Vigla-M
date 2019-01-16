import numpy as np
import math as mt
from scipy import stats as sst

def normalize(datalist, hkLabel='Housekeeping', endoLabel='Endogenous', valIndex=2, nameIndex=0):
    factors=[]
    endoLists=[]

    hkeepers=[]
    for dt in datalist:
        mask = np.any(dt==hkLabel, axis=1)
        hkeeping=dt[mask]
        mask = np.any(dt==endoLabel, axis=1)
        endo=dt[mask]
        endoLists.append(endo)
        hkeepers.append(hkeeping[:,valIndex].astype(np.float32))

    A=np.zeros((len(hkeepers[0]),len(hkeepers[0])))
    M=np.zeros(len(hkeepers[0]))

    # for each gene a series of pairwise ratios
    for i in range(0, len(hkeepers[0])):
        for j in range(0, len(hkeepers[0])):
            if i!=j:
                val=[]
                for hkVect in hkeepers:
                    val.append(mt.log(hkVect[i]/hkVect[j], 2))
                A[i,j]=np.std(val)
        M[i]=np.mean(A[i,:])
    
    oldFact=[]
    eps=0.15
    for n in range(3,10):
        v=100
        factors=[]
        indexes=M.argsort()[:n]    
        for hkVect in hkeepers:
            reduced=hkVect[indexes]
            gm=sst.gmean(reduced) 
            factors.append(gm)
        av=np.mean(factors)
        factors=av/factors
        if len(oldFact)>0:
            v=np.std(np.log2(oldFact/factors))
        if v<eps:
            print(n)
            print(factors)
            break
        oldFact=factors

    results = []
    results.append(endoLists[0][:,nameIndex])
    for i in range(0,len(factors)):
        f=factors[i]
        endo=endoLists[i]
        results.append(endo[:,valIndex].astype(np.float32)*f)
    return results
