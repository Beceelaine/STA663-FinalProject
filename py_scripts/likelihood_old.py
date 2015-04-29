
from __future__ import division
import numpy as np
import math

np.random.seed(1)

def likelihood_old(X, Z, M, sigma_A, sigma_X, K_plus, num_objects, object_dim):
    log_ll=(-1)*num_objects*object_dim*0.5*np.log(2*np.pi)-1*(num_objects-K_plus)*object_dim*np.log(sigma_X)-K_plus*object_dim*np.log(sigma_A)-object_dim*(0.5)*np.log(np.linalg.det((np.dot(Z.T,Z) + np.dot((sigma_X**2/sigma_A**2),np.eye(K_plus)))))+(-1/(2*sigma_X**2))*np.trace(np.dot(np.dot(X.T,(np.eye(num_objects)-np.dot(np.dot(Z,M),Z.T))),X))
    return log_ll