
from __future__ import division
import numpy as np
import math
import time as time
import os

np.random.seed(1)

A=np.array([[0,1,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,1,1,1,0,0,0,1,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,1,1,1,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,1,0]])

num_objects=100
object_dim=36
 
sigma_x_orig=0.5

I=sigma_x_orig*np.eye(object_dim)
Z_orig=np.zeros((num_objects,4))

X=np.zeros((num_objects,object_dim))

for i in range(num_objects):
    Z_orig[i,:]=(np.random.uniform(0,1,4)>0.5)
    while sum(Z_orig[i,:])==0:
        Z_orig[i,:]=(np.random.uniform(0,1,4)>0.5)
    X[i,:]=np.dot(np.random.normal(0,1,object_dim),I)+np.dot(Z_orig[i,:],A)

if not os.path.exists('data_files'):
    os.makedirs('data_files')
    
np.savetxt('data_files/Z_orig.csv', Z_orig, delimiter=',')
np.savetxt('data_files/X_orig.csv', X, delimiter=',')
np.savetxt('data_files/A_orig.csv', A, delimiter=',')