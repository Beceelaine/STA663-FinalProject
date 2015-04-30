
from __future__ import division
import numpy.testing as npt
import numpy as np
import math
import scipy.stats as stats
from functions import calcInverse, sampleIBP
from likelihood import likelihood

np.random.seed(1)

sigma_A=1.
sigma_X=1.
alpha=1.
num_objects=100
K_plus=4
alpha=1
object_dim=36

X=np.genfromtxt("data_files/X_orig.csv", delimiter=",")
chain_sigma_X=np.load('data_files/chain_sigma_X.npy')
chain_alpha=np.load('data_files/chain_alpha.npy')

Z=np.zeros((num_objects,100))

dish=0
while dish<num_objects:
    t=stats.poisson.rvs(alpha)
    if t>0:
        Z[dish,0:t]=1
        dish+=1

M=np.linalg.inv(np.dot(Z[:,0:K_plus].T,Z[:,0:K_plus])+((sigma_X/sigma_A)**2)*np.identity(K_plus))

#calcInverse
def test1():
    inv=np.dot(Z[:,0:K_plus].T,Z[:,0:K_plus])+((sigma_X/sigma_A)**2)*np.identity(K_plus)
    npt.assert_almost_equal(np.dot(M,inv),np.identity(K_plus))
    
Z = Z[:,0:K_plus]
Z_final=np.load('data_files/Z.npy')

#calcInverse
def test2():
    (i,k,val) = (7,1,1)
    M1=calcInverse(Z,M,i,k,val)
    Z[i,k]=val
    M_new=np.linalg.inv(np.dot(Z[:,0:K_plus].T,Z[:,0:K_plus])+((sigma_X/sigma_A)**2)*np.identity(K_plus))
    np.allclose(M1,M_new)

#calcInverse
def test3():
    (i,k,val) = (9,3,0)
    M1=calcInverse(Z,M,i,k,val)
    Z[i,k]=val
    M_new=np.linalg.inv(np.dot(Z[:,0:K_plus].T,Z[:,0:K_plus])+((sigma_X/sigma_A)**2)*np.identity(K_plus))
    np.allclose(M1,M_new)

#convergence of sampler for sigma X
def test4():
    assert (np.abs(np.mean(chain_sigma_X[200:])-0.5))<=.05

#convergence of sampler for alpha
def test5():
    assert (np.abs(np.mean(chain_alpha[200:])-1))<=.05

#testing likelihood to be > 0
def test6():
    like=np.exp(likelihood(X, Z, sigma_A, sigma_X, K_plus, num_objects, object_dim))
    assert like>=0

#testing likelihood for -ve sigma A
def test7():
    assert(math.isnan(likelihood(X, Z, -0.5, sigma_X, K_plus, num_objects, object_dim)))

#testing likelihood for -ve sigma X
def test8():
    assert(math.isnan(likelihood(X, Z, sigma_A, -0.4, K_plus, num_objects, object_dim)))

#testing likelihood for div by 0
def test9():
    npt.assert_raises(ZeroDivisionError, likelihood, X, Z, 0, sigma_X, K_plus, num_objects, object_dim)

#testing that each object sampled atleast one feature
def test10():
    summ=np.sum(Z_final,axis=1)
    for i in range(100):
        assert summ[i] >=1
    