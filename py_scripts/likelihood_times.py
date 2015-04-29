
from __future__ import division
import numpy as np
import math
import time as time
import pandas as pd
import timeit
from likelihood_old import likelihood_old
from likelihood import likelihood
from functions import sampleIBP
import os

X=np.genfromtxt("data_files/X_orig.csv", delimiter=",")
E=1000 #change to 1000
BURN_IN=0
SAMPLE_SIZE=E-BURN_IN
object_dim=X.shape[1]
num_objects=X.shape[0]

sigma_A=1.
sigma_X=1.
alpha=1.

sam=sampleIBP(alpha,num_objects)
Z=sam[0]
K_plus=sam[1]

M1=np.linalg.inv((np.dot(Z[:,0:K_plus].T,Z[:,0:K_plus]) + np.dot(((sigma_X)**2/(sigma_A)**2),np.eye(K_plus))))
M2=np.linalg.inv((np.dot(Z[:,0:K_plus].T,Z[:,0:K_plus]) + np.dot(((sigma_X)**2/(sigma_A)**2),np.eye(K_plus))))
M=np.linalg.inv((np.dot(Z[:,0:K_plus].T,Z[:,0:K_plus]) + np.dot(((sigma_X)**2/(sigma_A)**2),np.eye(K_plus))))

start = timeit.default_timer()
for i in range(1000):
    likelihood(X, Z[:,0:K_plus], sigma_A, sigma_X, K_plus, num_objects, object_dim)
elapsed1 = timeit.default_timer() - start

start = timeit.default_timer()
for i in range(1000):
    M1=np.linalg.inv((np.dot(Z[:,0:K_plus].T,Z[:,0:K_plus]) + np.dot(((sigma_X)**2/(sigma_A)**2),np.eye(K_plus))))
    likelihood_old(X, Z[:,0:K_plus], M1, sigma_A, sigma_X, K_plus, num_objects, object_dim)
elapsed2 = timeit.default_timer() - start

elap=np.array((elapsed1,elapsed2))
print elap

index=['Old Likelihood','New Likelihood']
columns=['Time (in secs)']

if not os.path.exists('data_files'):
    os.makedirs('data_files')
    
df = pd.DataFrame(np.hstack((elapsed2,elapsed1)),index=index,columns=columns)
tab = df.to_latex()
text_file = open("data_files/times_like.tex", "w")
text_file.write(tab)
text_file.close()