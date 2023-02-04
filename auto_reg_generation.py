import tensorflow as tf
from functions import *
import pandas as pd
import numpy as np
from tensorflow.python.ops.numpy_ops import np_config
np_config.enable_numpy_behavior()
# tf.debugging.set_log_device_placement(True)
gpus = tf.config.list_physical_devices('GPU')
tf.config.set_soft_device_placement(True)
with tf.device('/device:GPU:0'):


    class generate_fiducial:
        def __init__(self,xlim,ylim,zlim):
            self.xlim = xlim
            self.ylim = ylim
            self.zlim = zlim
            
        def compute_cube(self):
            x_axis = np.array([1,0,0])
            y_axis = np.array([0,1,0])
            z_axis = np.array([0,0,1])

            xlim_half = int(self.xlim/2)
            ylim_half = int(self.ylim/2)
            zlim_half = int(self.zlim/2)
            vec_list = []
            a=20
            for i in range(-xlim_half,xlim_half+a,a):
                for j in range(-ylim_half,ylim_half+a,a):
                    for k in range(-zlim_half,zlim_half+a,a):

                        if tf.abs(k) == zlim_half:
                            vec_list.append(x_axis*i+y_axis*j+k*z_axis)
                        if tf.abs(i) == xlim_half or tf.abs(j) == ylim_half:
                            vec_list.append(x_axis*i+y_axis*j+k*z_axis)
            meshes = np.array(vec_list)    
            return meshes

    xlim = 100
    ylim = 80
    zlim = 40
    gen_cube = generate_fiducial(xlim,ylim,zlim)
    fid = gen_cube.compute_cube()

    c = 6
    from itertools import combinations
    combin = combinations(np.arange(len(fid)),c)


    target = np.array([0, 0, 50])
    name = "auto_reg"
    csv_file = name+'_'+str(xlim)+'_'+str(ylim)+'_'+str(target)+'.csv'
    fids_list = []
    tre_list = []
    ndi_con_list = []
    minimum = 50
    increment = 5
    counter = 0

    for i in combin:
        # print(i)
        fiducials = []
        for j in range(c):
            fiducials.append(fid[i[j]])

        tre = compute_tre(fiducials,target)
        tre_list.append(tre)
        fids_list.append(fiducials)
        imd = compute_intermarker (fiducials,len(fiducials))
        geo_pass = min_dist_and_incr(imd,minimum,increment)
        counter = counter + 1
        ndi_con_list.append(int(geo_pass))
        # print(len(tre_list))
        if geo_pass == True:
            print(i)

            # print(i)
            ff = np.array(fids_list)
            tt = np.array([tre_list]).transpose()
            ndi = np.array([ndi_con_list]).transpose()
            fids_reshaped = ff.reshape(ff.shape[0], -1)
            data = np.hstack((fids_reshaped,tt,ndi))
            df = pd.DataFrame(data, columns = ['fid1x','fid1y','fid1z','fid2x','fid2y','fid2z','fid3x','fid3y','fid3z','fid4x','fid4y','fid4z','fid5x','fid5y','fid5z','fid6x','fid6y','fid6z','tre','geopass'])

            with open(csv_file, 'a') as f:
                df.to_csv(f, header=False)
            fids_list = []
            tre_list = []
            ndi_con_list = []
            # plt.scatter(np.linspace(0,len(tt),len(tt)),tt)
        
        

    print("Done")