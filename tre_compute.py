from functions import compute_tre


import numpy as np


fid = np.array([[-47 ,  0,   0],
[-47,  75,   0],
[ 58,   0,   0],
[ 58, 120,   0]])

tre = compute_tre(fid,np.array([0,-180,55]))
print(tre)