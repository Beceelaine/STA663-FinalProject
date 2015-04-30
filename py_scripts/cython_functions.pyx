
from __future__ import division
import numpy as np
import math

np.random.seed(1)
#cythonizing

def likelihood(X, Z, sigma_A, sigma_X, K_plus, num_objects, object_dim):
    """cythonized likelihood"""
    M1 = (np.dot(Z.T,Z) + np.dot((sigma_X**2/sigma_A**2),np.eye(K_plus)))
    log_ll=(-1)*num_objects*object_dim*0.5*np.log(2*np.pi)-1*(num_objects-K_plus)*object_dim*np.log(sigma_X)-K_plus*object_dim*np.log(sigma_A)-object_dim*(0.5)*np.log(np.linalg.det(M1))+(-1/(2*sigma_X**2))*np.trace(np.dot(np.dot(X.T,(np.eye(num_objects)-np.dot(np.dot(Z,np.linalg.inv(M1)),Z.T))),X))
    return log_ll

def sampleIBP(alpha, num_objects):
    """cythonized IBP"""
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