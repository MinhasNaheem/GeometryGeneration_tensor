import tensorflow as tf
import pandas as pd
import plotly.graph_objects as go
from scipy.spatial.transform import Rotation as R
tnp = tf.experimental.numpy
from itertools import combinations
from tensorflow.python.ops.numpy_ops import np_config
np_config.enable_numpy_behavior()
import numpy as np
import time

def unit (vector):
    return vector / tf.raw_ops.EuclideanNorm(input=vector,axis=0)


def DistanceFromLine (p1,p2,p3):
    p = p2-p1
    if tf.raw_ops.EuclideanNorm(input=p,axis=0) == 0:
        return 100
    else:
        d = tf.raw_ops.EuclideanNorm(input=tnp.cross(p2-p1,p1-p3),axis=0)/tf.raw_ops.EuclideanNorm(input=p,axis=0)
        return d
    
def compute_tre(vector,target):
    centroid = tnp.mean(vector,axis = 0)
    axis =[]
    temp_vec =  unit(vector[1] -  centroid)

    temp_vec2 = tnp.cross(temp_vec,unit(vector[2]-centroid))
    temp_vec3 = tnp.cross(temp_vec,temp_vec2)
    axis.append(temp_vec)
    axis.append(temp_vec2)
    axis.append(temp_vec3)


    # fiducials to principal axis
    # target from principal axis 
    tp = []
    tp.append(DistanceFromLine(centroid,centroid + axis[0],target))
    tp.append(DistanceFromLine(centroid,centroid + axis[1],target))
    tp.append(DistanceFromLine(centroid,centroid + axis[2],target))

    fp = []
    f = np.zeros(3)
    for i in range(3):
        sum = 0
        for j in range(len(vector)):
            fp = tnp.around(DistanceFromLine(centroid,centroid+axis[i],vector[j]),3)
            # print(fp)
            sum = sum + fp**2
        if tnp.round(sum/len(vector)) == 0:
            f[i]=10000
            # print(f[i])
        else:
            f[i] = tp[i]**2/(sum/len(vector))
            
        
        

    fle = 0.3
    tre = (fle**2/len(vector))*(tnp.mean(f)+1)
    return tf.math.sqrt(tnp.around(tre,3))


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
        diff = tf.abs(dist[i[0]]-dist[i[1]])
        # print(i,dist[i[0]],dist[i[1]])
        if diff < increment:
            flag2 = False
            # print("flag2",flag2)
    return flag and flag2

def compute_intermarker(f,fiducial_count):
    comb = combinations(tnp.arange(fiducial_count),2)
    imd = []
    for indices in comb:
        # print(indices)
        dist = tf.raw_ops.EuclideanNorm(input=f[indices[0]]-f[indices[1]],axis=0)
        imd.append([indices[0],indices[1],dist])

    imd_array = tnp.array(imd)
    return imd_array
  