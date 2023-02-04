import tensorflow as tf
import pandas as pd
from itertools import combinations
from tensor_flow import *
from functions import plot_fids
tnp = tf.experimental.numpy


gpus = tf.config.list_physical_devices('GPU')
with tf.device('/job:localhost/replica:0/task:0/device:GPU:0'):


    class GenerateFiducials:
        def __init__(self,xlim,ylim,zlim):
            self.xlim = xlim
            self.ylim = ylim
            self.zlim = zlim
        def compute_bounce(self):
            x_axis = tf.constant([1,0,0],dtype='float16')
            y_axis = tf.constant([0,1,0],dtype='float16')
            z_axis = tf.constant([0,0,1],dtype='float16')
            
            xlim_half = int(self.xlim/2)
            ylim_half = int(self.ylim/2)
            zlim_half = int(self.zlim/2)
            vec = []
            a =15
            
            for i in range(-xlim_half,xlim_half+a,a):
                for j in range(-ylim_half,ylim_half+a,a):
                    for k in range(zlim_half,zlim_half+a,a):
                        
                        vec.append(x_axis*i+y_axis*j+zlim_half*k)
            fids = tnp.array(vec,dtype='float16')
            return fids

    def tre_mesh(fid,combin):
        target1 = tnp.array([0,145,50])
        target2 = tnp.array([0,125,50])
        name = 'PAKWithoutInline_set2'
        csv_file = name+'_'+str(xlim)+','+str(ylim)+','+str(zlim)+'1.csv'
        fids_list = []
        tre_list = []
        ndi_con_list = []
        minimum = 40
        increment = 4
        fid = fid.numpy()
        for i in combin:
            # print(i)
            fiducials = []
            
            


            for j in range(4):
                
                
                fiducials.append(fid[i[j]])
            

            tre1 = compute_tre(fiducials,target1)
            # print(tre)
            tre2 = compute_tre(fiducials,target2)
            tre = (tre1+tre2)/2
            print(tre)
            imd = compute_intermarker(fiducials,len(fiducials))
            geo_pass = min_dist_and_incr(imd,minimum,increment)
            print(geo_pass)
            
            if tre < 1 and geo_pass:
                
                print(tre)
                tre_list.append(tre)
                fids_list.append(fiducials)
                ndi_con_list.append(int(geo_pass))
                print(imd)
                # print(len(tre_list))
            if len(tre_list) == 2:

                print(tre)
                ff = tnp.array(fids_list)
                tt = tnp.array([tre_list]).transpose()
                ndi = tnp.array([ndi_con_list]).transpose()
                fids_reshaped = ff.reshape(ff.shape[0], -1)
                data = tnp.hstack((fids_reshaped,tt,ndi))
                fids_col_index = []
                number_of_fiducials = 4
                for col in range(number_of_fiducials):
                    col=col+1
                    ax = ['x','y','z']
                    for axis in ax:
                        fids_col_index.append('fid'+str(col)+axis)
                fids_col_index.append('tre')
                fids_col_index.append('geopass')

                df = pd.DataFrame(data, columns = fids_col_index)

                with open(csv_file, 'a') as f:
                    df.to_csv(f, header=False)
                fids_list = []
                tre_list = []
                ndi_con_list = []
                # plt.scatter(np.linspace(0,len(tt),len(tt)),tt)
        return 1


    xlim = 70
    ylim= 90
    zlim = 0
    gen = GenerateFiducials(xlim,ylim,zlim)

    fids = gen.compute_bounce()

    fig = plot_fids(fids)
    fig.show()
    combin = combinations(tnp.arange(len(fids)),4)
    n = len(fids)
    k = 2

    tre_mesh(fids,combin)
    print('Done')
    
        
    