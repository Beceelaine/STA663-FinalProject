
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
plt.style.use('ggplot')
import os

if not os.path.exists('data_files'):
    os.makedirs('data_files')
    
chain_Z=np.load('data_files/chain_Z.npy')
chain_K=np.load('data_files/chain_K.npy')
chain_sigma_X=np.load('data_files/chain_sigma_X.npy')
chain_sigma_A=np.load('data_files/chain_sigma_A.npy')
chain_alpha=np.load('data_files/chain_alpha.npy')
Z=np.load('data_files/Z.npy')

plt.figure(num=None, figsize=(12,3), dpi=80, facecolor='w', edgecolor='k')
plt.subplot(121)
plt.hist(chain_K[200:],bins=range(12),normed=True)
m=np.mean(chain_Z, axis=0)
plt.subplot(122)
plt.hist(np.ceil(np.sum(m,axis=1)),bins=range(10),normed=True)
plt.savefig('data_files/figures.png')

A=np.genfromtxt("data_files/A_orig.csv", delimiter=",")

plt.figure(num=None, figsize=(12,3), dpi=80, facecolor='w', edgecolor='k')
plt.subplot(141)
plt.pcolormesh(A[0,:].reshape(6,6),cmap=plt.cm.gray)     
plt.subplot(142)
plt.pcolormesh(A[1,:].reshape(6,6),cmap=plt.cm.gray)  
plt.subplot(143)
plt.pcolormesh(A[2,:].reshape(6,6),cmap=plt.cm.gray)  
plt.subplot(144)
plt.pcolormesh(A[3,:].reshape(6,6),cmap=plt.cm.gray) 
plt.savefig('data_files/features.png')

Z=Z[:,0:4]
X=np.genfromtxt("data_files/X_orig.csv", delimiter=",")

plt.figure(num=None, figsize=(12,3), dpi=80, facecolor='w', edgecolor='k')
plt.subplot(141)
plt.pcolormesh(X[0,:].reshape(6,6),cmap=plt.cm.gray)     
plt.subplot(142)
plt.pcolormesh(X[1,:].reshape(6,6),cmap=plt.cm.gray)  
plt.subplot(143)
plt.pcolormesh(X[2,:].reshape(6,6),cmap=plt.cm.gray)  
plt.subplot(144)
plt.pcolormesh(X[3,:].reshape(6,6),cmap=plt.cm.gray) 
plt.savefig('data_files/data.png')

A_inf=np.dot(np.dot(np.linalg.inv((np.dot(Z.T,Z)+(chain_sigma_X[999]**2/chain_sigma_A[999]**2)*np.eye(4))),Z.T),X)

plt.figure(num=None, figsize=(12,3), dpi=80, facecolor='w', edgecolor='k')
plt.subplot(141)
plt.pcolormesh(A_inf[0,:].reshape(6,6),cmap=plt.cm.gray)     
plt.subplot(142)
plt.pcolormesh(A_inf[1,:].reshape(6,6),cmap=plt.cm.gray)  
plt.subplot(143)
plt.pcolormesh(A_inf[2,:].reshape(6,6),cmap=plt.cm.gray)  
plt.subplot(144)
plt.pcolormesh(A_inf[3,:].reshape(6,6),cmap=plt.cm.gray)
plt.savefig('data_files/detected_features.png')

np.random.seed(1)

num_objects=100
object_dim=36
 
sigma_x_orig=0.5

I=sigma_x_orig*np.eye(object_dim)

Z_final=Z
X=np.zeros((num_objects,object_dim))

for i in range(num_objects):
    X[i,:]=np.dot(Z_final[i,:],A_inf[0:4,])
    
plt.figure(num=None, figsize=(12,3), dpi=80, facecolor='w', edgecolor='k')
plt.subplot(141)
plt.pcolormesh(X[0,:].reshape(6,6),cmap=plt.cm.gray)
plt.subplot(142)
plt.pcolormesh(X[1,:].reshape(6,6),cmap=plt.cm.gray)
plt.subplot(143)
plt.pcolormesh(X[2,:].reshape(6,6),cmap=plt.cm.gray)
plt.subplot(144)
plt.pcolormesh(X[3,:].reshape(6,6),cmap=plt.cm.gray)
plt.savefig('data_files/detected_total_features.png')

index=['1st image','2nd image','3rd image','4th image']
columns=['F1','F2','F3','F4']

Z_orig=np.genfromtxt("data_files/Z_orig.csv", delimiter=",")
print Z_orig[0,:]
print Z_orig[1,:]
print Z_orig[2,:]
print Z_orig[3,:]

df = pd.DataFrame(np.hstack((np.vstack([Z_orig[0,0],Z_orig[1,0],Z_orig[2,0],Z_orig[3,0]]),np.vstack([Z_orig[0,1],Z_orig[1,1],Z_orig[2,1],Z_orig[3,1]]),np.vstack([Z_orig[0,2],Z_orig[1,2],Z_orig[2,2],Z_orig[3,2]]),np.vstack([Z_orig[0,3],Z_orig[1,3],Z_orig[2,3],Z_orig[3,3]]))),index=index,columns=columns)
tab = df.to_latex()
text_file = open("data_files/table_features.tex", "w")
text_file.write(tab)
text_file.close()

plt.figure(num=None, figsize=(12,3), dpi=80, facecolor='w', edgecolor='k')
plt.subplot(131)
plt.plot(chain_alpha)
plt.subplot(132)
plt.plot(chain_sigma_X)
plt.subplot(133)
plt.plot(chain_sigma_X)
plt.savefig('data_files/trace_plots.png')