import tensorflow as tf
import pandas as pd
from itertools import combinations,combinations_with_replacement
from tensor_flow import *
from functions import plot_fids
from math import factorial
import time
tnp = tf.experimental.numpy


gpus = tf.config.list_physical_devices('GPU')
with tf.device('/job:localhost/replica:0/task:0/device:GPU:0'):


    class GenerateFiducials:
        def __init__(self,xlim,ylim,zlim,target):
            self.xlim = xlim
            self.ylim = ylim
            self.zlim = zlim
            self.target = target
        def compute_bounce(self):
            x_axis = tf.constant([1,0,0],dtype='float16')
            y_axis = tf.constant([0,1,0],dtype='float16')
            z_axis = tf.constant([0,0,1],dtype='float16')
            
            xlim_half = int(self.xlim/2)
            ylim_half = int(self.ylim/2)
            zlim_half = int(self.zlim/2)
            vec = []
            global sampling
            a = sampling 
           
            #Defining bounds for the generation
            for i in range(-xlim_half,xlim_half+a,a):
                for j in range(0,ylim+a,a):
                    # for k in range(-zlim_half,zlim_half+a,a):
                    vec.append(x_axis*i+y_axis*j)

            fids = tnp.array(vec,dtype='float16')
            # for i in range(-xlim_half,xlim_half+a,a):
            #     for j in range(-ylim_half,ylim_half+a,a):
            #         # for k in range(-zlim_half,zlim_half+a,a):
            #          vec.append(x_axis*i+y_axis*j)
            #             # vec.append(x_axis*i+y_axis*j+zlim_half*k)
            # fids = tnp.array(vec,dtype='float16')
            return fids

        def tre_mesh(self,fid,combin):
            start = time.time()
            global pass_tre
            global number_of_fiducials
            global number2generate

            name = 'TAP_new'
            csv_file = name+'_'+str(xlim)+','+str(ylim)+','+str(zlim)+'.csv'
            fids_list = []
            tre_list = []
            ndi_con_list = []
            minimum = 45
            increment = 5
            fid = fid.numpy()

            for i in combin:
                
               
                fiducials = []
                # fiducials.append(tnp.array([0,-50,0]))
                # fiducials.append(tnp.array([0,110,0]))
                # fiducials.append(tnp.array([0,0,0]))
                

                for j in range(number2generate):
                    fiducials.append(fid[i[j]])
                
                target1 = self.target
                target2 = self.target  + np.array([0,40,0])
                tre1 = compute_tre(fiducials,target1)
                tre2 = compute_tre(fiducials,target2)
                tre = (tre1+tre2)/2

                imd = compute_intermarker(fiducials,len(fiducials))
                geo_pass = min_dist_and_incr(imd,minimum,increment)
                
                if tre < pass_tre and geo_pass:
                    
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
                    
                    
                    for col in range(number_of_fiducials):
                        col=col+1
                        ax = ['x','y','z']
                        for axis in ax:
                            fids_col_index.append('fid'+str(col)+axis)
                    fids_col_index.append('tre')
                    fids_col_index.append('geopass')

                    df = pd.DataFrame(data.numpy(), columns = fids_col_index)

                    with open(csv_file, 'a') as f:
                        df.to_csv(f, header=False)
                    fids_list = []
                    tre_list = []
                    ndi_con_list = []
                    # plt.scatter(np.linspace(0,len(tt),len(tt)),tt)
                # print((time.time()-start)/60)
            return 1

if __name__ == '__main__':
    xlim = 85
    ylim= 155
    zlim = 0
    global number2generate, pass_tre, number_of_fiducials, sampling
    number2generate = 4
    pass_tre = 0.5
    number_of_fiducials = 4
    sampling = 25

    target = tnp.array([0,-150,65])
    gen = GenerateFiducials(xlim,ylim,zlim,target)
    fids = gen.compute_bounce()
    n = len(fids)
    k = number2generate
    iterations = C = factorial(n) / (factorial(k) * factorial(n - k))
    time_taken = iterations*0.12/60**2
    print(f'time taken {time_taken} hrs')
    fig = plot_fids(fids)
    fig.show()
    combin = combinations(tnp.arange(len(fids)),number2generate)
    gen.tre_mesh(fids,combin)
    print('Done')

            
        