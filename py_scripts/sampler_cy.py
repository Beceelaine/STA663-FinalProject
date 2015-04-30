
from __future__ import division
import numpy as np
import math
from cython_functions import sampleIBP, likelihood

def sampler_cy(X, E, BURN_IN, SAMPLE_SIZE, sigma_A, sigma_X, alpha, object_dim, num_objects):
    """cythonized sampler"""
    HN=0.0
    for i in range(1,num_objects+1): 
        HN=HN+1.0/i

    K_inf=20

    sam=sampleIBP(alpha,num_objects)

    Z=sam[0]
    K_plus=sam[1]

    chain_Z=np.zeros((SAMPLE_SIZE,num_objects,K_inf))
    chain_K=np.zeros((SAMPLE_SIZE,1))
    chain_sigma_X=np.zeros((SAMPLE_SIZE,1))
    chain_sigma_A=np.zeros((SAMPLE_SIZE,1))
    chain_alpha=np.zeros((SAMPLE_SIZE,1))
    
    P=np.array([0,0])
    #gibbs
    s_counter=0
    for e in range(E):
        print e, K_plus, alpha
        if((e+1)>BURN_IN):
            chain_Z[s_counter,:,0:K_plus]=Z[:,0:K_plus]
            chain_K[s_counter]=K_plus
            chain_sigma_X[s_counter]=sigma_X
            chain_sigma_A[s_counter]=sigma_A
            chain_alpha[s_counter]=alpha
            s_counter=s_counter+1

        for i in range(num_objects):
            for k in range(K_plus):
                if (k+1)>K_plus:
                    break
                if Z[i,k]>0:
                    if (sum(Z[:,k]) - Z[i,k])<=0:
                        Z[i,k]=0
                        Z[:,k:(K_plus-1)] = Z[:,(k+1):K_plus]
                        K_plus = K_plus-1
                        continue

                Z[i,k]=1
                P[0]=likelihood(X, Z[:,0:K_plus], sigma_A, sigma_X, K_plus, num_objects, object_dim) + np.log(sum(Z[:,k])- Z[i,k]) -np.log(num_objects)

                Z[i,k]=0
                P[1]=likelihood(X, Z[:,0:K_plus], sigma_A, sigma_X, K_plus, num_objects, object_dim) + np.log(num_objects - sum(Z[:,k])) -np.log(num_objects)

                P=np.exp(P - max(P))

                if np.random.uniform(0,1,1)<(P[0]/(P[0]+P[1])):
                    Z[i,k] = 1
                else:
                    Z[i,k] = 0

            trun=np.zeros(5) 
            alpha_N = alpha/num_objects

            for k_i in range(5):
                if Z.shape[1]>(K_plus+k_i):
                    Z[i,K_plus:(K_plus+k_i)]=1       
                else:
                    Ztemp=np.zeros((Z.shape[0],K_plus+k_i))
                    Ztemp[0:Z.shape[0],0:Z.shape[1]]=Z
                    Ztemp[i,K_plus:(K_plus+k_i)] = 1
                    Z=Ztemp

                trun[k_i] = k_i*np.log(alpha_N) - alpha_N - np.log(math.factorial(k_i)) + likelihood(X, Z[:,0:(K_plus+k_i)], sigma_A, sigma_X, K_plus+k_i, num_objects, object_dim)

            Z[i,K_plus:K_plus+4] = 0
            trun = np.exp(trun - max(trun))
            trun = trun/sum(trun)
            p = np.random.uniform(0,1,1)
            t = 0
            
            #new dishes
            for k_i in range(5):
                t = t+trun[k_i]
                if p<t:
                    new_dishes = k_i
                    break
            if Z.shape[1]>(K_plus+new_dishes):
                Ztemp=Z
                Ztemp[i,K_plus:(K_plus+new_dishes)]=1       
            else:
                Ztemp=np.zeros((Z.shape[0],K_plus+new_dishes))
                Ztemp[0:Z.shape[0],0:Z.shape[1]]=Z
                Ztemp[i,K_plus:(K_plus+new_dishes)] = 1

            Z=Ztemp
            K_plus = K_plus + new_dishes
        #metropolis 
        l_curr=likelihood(X, Z[:,0:(K_plus+new_dishes)], sigma_A, sigma_X, K_plus+new_dishes, num_objects, object_dim)
        if np.random.uniform(0,1,1)<.5:
            pr_sigma_X=sigma_X-np.random.uniform(0,1,1)/20
        else:
            pr_sigma_X=sigma_X+np.random.uniform(0,1,1)/20

        l_new_X=likelihood(X, Z[:,0:(K_plus+new_dishes)], sigma_A, pr_sigma_X[0], K_plus+new_dishes, num_objects, object_dim)
        acc_X=np.exp(min(0,l_new_X-l_curr))

        if np.random.uniform(0,1,1)<.5:
            pr_sigma_A=sigma_A-np.random.uniform(0,1,1)/20
        else:
            pr_sigma_A=sigma_A+np.random.uniform(0,1,1)/20

        l_new_A=likelihood(X, Z[:,0:(K_plus+new_dishes)], pr_sigma_A[0], sigma_X, K_plus+new_dishes, num_objects, object_dim)
        acc_A=np.exp(min(0,l_new_A-l_curr))

        if np.random.uniform(0,1,1)<acc_X:
            sigma_X=pr_sigma_X[0]

        if np.random.uniform(0,1,1)<acc_A:
            sigma_A=pr_sigma_A[0]

        alpha = np.random.gamma(1+K_plus, 1/(1+HN))
    
    return(chain_Z, chain_K, chain_sigma_A, chain_sigma_X, chain_alpha, Z)