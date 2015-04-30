import time
import numpy as np
import pandas as pd
from functions import calcInverse, sampleIBP
import os
np.random.seed(1)

#load data
X=np.genfromtxt("data_files/X_orig.csv", delimiter=",")

object_dim=X.shape[1]
num_objects=X.shape[0]

sigma_A=1.
sigma_X=1.
alpha=1.

i=12
k=3

#IBP prior
sam=sampleIBP(alpha,num_objects)
Z=sam[0]
K_plus=sam[1]
 
M = np.linalg.inv(Z.T.dot(Z)+(sigma_X**2/sigma_A**2)*np.identity(K_plus))
Z[i,k] = 1
val = 0

#timing matrix inversion
t0=time.time()
for l in range(1000):
    calcInverse(Z,M,i,k,val)
t1=time.time()
tcalc=t1-t0

t0=time.time()
for l in range(1000):
    np.linalg.inv(Z.T.dot(Z)+(sigma_X**2/sigma_A**2)*np.identity(K_plus))
t1=time.time()
tlinalg=t1-t0

print (tlinalg,tcalc)
columns = ['Time']
index = ['linalg.inv','calcInverse']
 
if not os.path.exists('data_files'):
    os.makedirs('data_files')
    
df = pd.DataFrame(np.hstack((tlinalg,tcalc)),columns=columns,index=index)
tab = df.to_latex()
text_file = open("data_files/inversetimes.tex", "w")
text_file.write(tab)
text_file.close()