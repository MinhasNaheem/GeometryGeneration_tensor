import numpy as np
from numpy.linalg import norm
from itertools import combinations


def compute_intermarker(f,fiducial_count):
    comb = combinations(np.arange(fiducial_count),2)
    imd = []
    for indices in comb:
        # print(indices)
        dist =norm(f[indices[0]]-f[indices[1]])
        imd.append([indices[0],indices[1],dist])

    imd_array = np.array(imd)
    return imd_array


arr = np.array([[-40,	-15	,0],
[-40,	30,	0],
[35	,-30,	0],
[50,	30,	0]])

imd = compute_intermarker(arr , len(arr))
print(imd)