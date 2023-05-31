import numpy as np
import tensorflow as tf
from tensor_flow import *
np.set_printoptions(suppress=True) 
# from functions import *
from functions import plot_fids
import plotly.offline as py
import random
from scipy.spatial.transform import Rotation as R
from numpy.linalg import norm
from plotly.offline import init_notebook_mode, iplot
import pandas as pd

gpus = tf.config.list_physical_devices('GPU')
with tf.device('/job:localhost/replica:0/task:0/device:GPU:0'):
    radii = 180
    height = 65
    ang = 100
    counth = 10
    countang = 30
    mid_ang = int(ang/2)
    target = np.array([0, 280, 0])
    name = "double_deck"
    csv_file = name+'_'+str(counth)+'_'+str(countang)+'_'+str(target)+'.csv'



    vec = np.array([0,0,radii])
    vec_list = []
    for i in range(-mid_ang,mid_ang,int(ang/countang)):
        print(i)
        r = R.from_rotvec(np.deg2rad(i) * np.array([0, 1, 0]))
        rot_vec = r.apply(vec)
        vec_list.append(rot_vec)
    vec_arc = np.array(vec_list)

    fig = plot_fids(vec_arc)
    fig.show()
    mesh = []
    for j in range(0,height,int(height/counth)):
        arr = vec_arc + np.array([0,j,0])
        mesh.append(arr.tolist())

    mesh = np.array(mesh)


    fid = mesh.reshape(mesh.shape[0]*mesh.shape[1],3)
    fig = plot_fids(fid)
    fig.show()

    from itertools import combinations
    combin = combinations(np.arange(len(fid)),4)


    fids_list = []
    tre_list = []
    ndi_con_list = []
    minimum = 50
    increment = 5
    counter = 0

    for i in combin:
        fiducials = []
        fiducials.append(fid[i[0]])
        fiducials.append(fid[i[1]])
        fiducials.append(fid[i[2]])
        fiducials.append(fid[i[3]])
        tre = compute_tre(fiducials,target)
        tre_list.append(tre)
        fids_list.append(fiducials)
        imd = compute_intermarker (fiducials,len(fiducials))
        geo_pass = min_dist_and_incr(imd,minimum,increment)
        counter = counter + 1
        ndi_con_list.append(int(geo_pass))
        if len(tre_list) == 100000:


            ff = np.array(fids_list)
            tt = np.array([tre_list]).transpose()
            ndi = np.array([ndi_con_list]).transpose()
            fids_reshaped = ff.reshape(ff.shape[0], -1)
            data = np.hstack((fids_reshaped,tt,ndi))
            df = pd.DataFrame(data, columns = ['fid1x','fid1y','fid1z','fid2x','fid2y','fid2z','fid3x','fid3y','fid3z','fid4x','fid4y','fid4z','tre','geopass'])

            with open(csv_file, 'a') as f:
                df.to_csv(f, header=False)
            fids_list = []
            tre_list = []
            ndi_con_list = []
            # plt.scatter(np.linspace(0,len(tt),len(tt)),tt)
        
        

    print("Done")