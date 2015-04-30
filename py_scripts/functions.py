
from __future__ import division
import numpy as np
import math

np.random.seed(1)

#IBP function
def sampleIBP(alpha, num_objects):
    """generates the IBP prior"""
    result=np.zeros((num_objects, 1000))
    t=np.random.poisson(alpha)
    result[0,0:t]=np.ones(t)
    K_plus=t
    p=np.array((0,0))
    for i in range(2, num_objects+1):
        for j in range(K_plus):
            p[0]=np.log(sum(result[0:i,j]))-np.log(i) 
            p[1]=np.log(i - sum(result[0:i,j])) - np.log(i)
            p = np.exp(p-max(p))
            if np.random.uniform(0,1,1)<(p[0]/sum(p)):
                result[i-1,j]=1
            else:
                result[i-1,j]=0
        t=np.random.poisson(alpha/i)
        result[i-1,K_plus:K_plus+t]=np.ones(t)
        K_plus=K_plus+t
    
    result=result[:,0:K_plus]
    return(result,K_plus)     

#calcinverse proposed by Griffiths
def calcInverse(Zn,M,i,k,val):
    """calculates inverse based on Griffiths and Ghahramani approximation"""
    M_i = M-np.dot(np.dot(np.dot(M,Zn[i,:].T),Zn[i,:]),M)/(np.dot(np.dot(Zn[i,:],M),Zn[i,:].T)-1)
    Zn[i,k] = val
    M = M_i-np.dot(np.dot(np.dot(M_i,Zn[i,:].T),Zn[i,:]),M_i)/(np.dot(np.dot(Zn[i,:],M_i),Zn[i,:].T)+1)
    Inv = M
    return Inv