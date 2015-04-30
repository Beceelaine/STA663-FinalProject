
from __future__ import division
import numpy as np
import math
import time as time
import pandas as pd
from sampler_old import sampler_old
from sampler import sampler
from sampler_cy import sampler_cy
import os

np.random.seed(1)

X=np.genfromtxt("data_files/X_orig.csv", delimiter=",")

E=1000 #change to 1000
BURN_IN=0
SAMPLE_SIZE=E-BURN_IN
object_dim=X.shape[1]
num_objects=X.shape[0]

sigma_A=1.
sigma_X=1.
alpha=1.

t0 = time.time()
chain_Z, chain_K, chain_sigma_A, chain_sigma_X, chain_alpha, Z=sampler_old(X, E, BURN_IN, SAMPLE_SIZE, sigma_A, sigma_X, alpha, object_dim, num_objects)
t1 = time.time()
total_old=t1-t0

np.random.seed(1)

t0 = time.time()
chain_Z, chain_K, chain_sigma_A, chain_sigma_X, chain_alpha, Z=sampler(X, E, BURN_IN, SAMPLE_SIZE, sigma_A, sigma_X, alpha, object_dim, num_objects)
t1 = time.time()
total_new=t1-t0

np.random.seed(1)

t0 = time.time()
chain_Z, chain_K, chain_sigma_A, chain_sigma_X, chain_alpha, Z=sampler_cy(X, E, BURN_IN, SAMPLE_SIZE, sigma_A, sigma_X, alpha, object_dim, num_objects)
t1 = time.time()
total_cy=t1-t0

time=np.array((total_old,total_new,total_cy))
print time

index=['Naive','Optimized','Cythonized']
columns=['Time (in secs)']

if not os.path.exists('data_files'):
    os.makedirs('data_files')
    
df = pd.DataFrame(np.hstack((total_old,total_new,total_cy)),index=index,columns=columns)
tab = df.to_latex()
text_file = open("data_files/times.tex", "w")
text_file.write(tab)
text_file.close()