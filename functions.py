import plotly.graph_objects as go
from numpy.linalg import norm
from itertools import combinations
from scipy.spatial.transform import Rotation as R
from scipy.spatial.distance import cdist, euclidean
import numpy as np

import time
def compute_tre(vector,target):
    

    

    # add noise to system
    # vector = vector + noise

    
    centroid = np.mean(vector,axis=0)
    

    axis =[]
    temp_vec =  unit(vector[1] -  centroid)

    temp_vec2 = np.cross(temp_vec,unit(vector[2]-centroid))
    temp_vec3 = np.cross(temp_vec,temp_vec2)
    axis.append(temp_vec)
    axis.append(temp_vec2)
    axis.append(temp_vec3)


    # fiducials to principal axis
    # target from principal axis 
    tp = []
    tp.append(distanceFromLine(centroid,centroid + axis[0],target))
    tp.append(distanceFromLine(centroid,centroid + axis[1],target))
    tp.append(distanceFromLine(centroid,centroid + axis[2],target))

    fp = []
    f = np.zeros(3)
    for i in range(3):
        sum = 0
        for j in range(len(vector)):
            fp = np.around(distanceFromLine(centroid,centroid+axis[i],vector[j]),3)
            # print(fp)
            sum = sum + fp**2
        if np.round(sum/len(vector)) == 0:
            f[i]=10000
            # print(f[i])
        else:
            f[i] = tp[i]**2/(sum/len(vector))
            
        
        

    fle = 0.3
    tre = (fle**2/len(vector))*(np.mean(f)+1)
    return np.sqrt(np.around(tre,3))

def geometric_median(X, eps=1e-5):
    y = np.mean(X, 0)

    while True:
        D = cdist(X, [y])
        nonzeros = (D != 0)[:, 0]

        Dinv = 1 / D[nonzeros]
        Dinvs = np.sum(Dinv)
        W = Dinv / Dinvs
        T = np.sum(W * X[nonzeros], 0)

        num_zeros = len(X) - np.sum(nonzeros)
        if num_zeros == 0:
            y1 = T
        elif num_zeros == len(X):
            return y
        else:
            R = (T - y) * Dinvs
            r = np.linalg.norm(R)
            rinv = 0 if r == 0 else num_zeros/r
            y1 = max(0, 1-rinv)*T + min(1, rinv)*y

        if euclidean(y, y1) < eps:
            return y1

        y = y1
        
def plot_fids(fids):
    fids=np.vstack((fids,[0, 0, 0]))
    fiducials = go.Scatter3d(
        x=fids[:,0], y=fids[:,1], z=fids[:,2],
        marker=dict(
            size=4,
            colorscale='Viridis',
        ),
        text = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13'],
        line=dict(
            color='darkblue',
            width=2
        )
    )
    axes   = go.Scatter3d( x = [0, 0,   0  , 100, 0, 0  ],
                           y = [0, 100, 0  , 0,   0, 0  ],
                           z = [0, 0,   0  , 0,   0, 100],
                           marker = dict( size = 1,
                                          color = "rgb(84,48,5)"),
                           line = dict( color = "rgb(84,48,5)",
                                        width = 6)
                         )
    # data = [fiducials,axes]
    data = [fiducials,axes]
    name = 'default'
# Default parameters which are used when `layout.scene.camera` is not provided
    camera = dict(
        up=dict(x=-1, y=0, z=0),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=0, y=0, z=1.25)
        )

    fig = go.Figure(data=data)



    fig.update_layout(scene_camera=camera, title=name)

    fig.update_layout(
        scene = dict(
            xaxis = dict(nticks=4, range=[-800,800],),
            yaxis = dict(nticks=4, range=[-800,800],),
            zaxis = dict(nticks=4, range=[-800,800],),
            ),
            width=2000,
            margin=dict(r=20, l=10, b=10, t=10))
    return fig


def unit(vector):
    """ Returns the unit vector of the vector.  """
    if np.linalg.norm(vector)== 0:
        return np.array([0,0,0])
    else:
        return vector / np.linalg.norm(vector)

def distanceFromLine(p1,p2,p3):
    # distance of a point p3 from the line formed using points p1 and p2
    if norm(p2-p1) == 0:
        return 100
    else:
        d = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)
        return d


def min_dist_and_incr(imd,minimum,increment):
    dist = imd[:,2]
    combin = combinations(np.arange(len(dist)),2)
    diff_dist = []
    # print(dist)
    flag = True
    min_dist = tuple(dist>minimum)
    for i in range(len(dist)):
        if min_dist[i] == False:
            flag = False 
            # print("flag",min_dist[i])
    flag2 = True
    for i in combin:
        diff = np.abs(dist[i[0]]-dist[i[1]])
        # print(i,dist[i[0]],dist[i[1]])
        if diff < increment:
            flag2 = False
            # print("flag2",flag2)
    return flag and flag2


def compute_intermarker(f,fiducial_count):
    comb = combinations(np.arange(fiducial_count),2)
    imd = []
    for indices in comb:
        # print(indices)
        dist =norm(f[indices[0]]-f[indices[1]])
        imd.append([indices[0],indices[1],dist])

    imd_array = np.array(imd)
    return imd_array

def rotate_vec(r,p_vec):
    rotated_vec = []
    for i in range (len(p_vec)):
        rot_vec =r[i].apply(p_vec[i])
        rotated_vec.append(rot_vec)  
    return np.array(rotated_vec)
