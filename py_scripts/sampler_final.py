
from __future__ import division
import numpy as np
import math
import time as time
from sampler import sampler
import os

X=np.genfromtxt("data_files/X_orig.csv", delimiter=",")

E=1000
BURN_IN=0
SAMPLE_SIZE=E-BURN_IN
object_dim=X.shape[1]
num_objects=X.shape[0]

sigma_A=1.
sigma_X=1.
alpha=1.

np.random.seed(1)
chain_Z, chain_K, chain_sigma_A, chain_sigma_X, chain_alpha, Z=sampler(X, E, BURN_IN, SAMPLE_SIZE, sigma_A, sigma_X, alpha, object_dim, num_objects)

if not os.path.exists('data_files'):
    os.makedirs('data_files')
    
np.save('data_files/chain_Z', chain_Z)
np.save('data_files/chain_K', chain_K)
np.save('data_files/chain_sigma_A', chain_sigma_A)
np.save('data_files/chain_sigma_X', chain_sigma_X)
np.save('data_files/chain_alpha', chain_alpha)
np.save('data_files/Z', Z)