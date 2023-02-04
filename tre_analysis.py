import pandas as pd
import numpy as np
np.set_printoptions(suppress=True) 
from functions import *
import time

filename = 'PAKWithoutInline_set2_70,90,01.csv'

# filename = "tre_phantom90_50_[   0 -190    0].csv"
df = pd.read_csv(filename)
# condition to check if the geometry constraints are passed
df = df[df.iloc[:,-1]==1]
tre_col = df.columns[-2]
df = df.sort_values(by=[df.columns[-2]])

fid1 = df.iloc[:,1:4].to_numpy()
fid2 = df.iloc[:,4:7].to_numpy()
fid3 = df.iloc[:,7:10].to_numpy()
fid4 = df.iloc[:,10:13].to_numpy()
# fid5 = df.iloc[:,13:16].to_numpy()
# fid6 = df.iloc[:,16:19].to_numpy()
# fid7 = df.iloc[:,19:22].to_numpy()
# fid8 = df.iloc[:,22:25].to_numpy()

tre = df.iloc[:,-2].to_numpy()

# np.amin(tre)
k = 4
result = np.where(tre == np.amin(tre))
# result = np.where(np.round(tre,2)==0.31)
minimum = 40
increment = 4
marker0 = np.vstack((fid1[0],fid2[0],fid3[0],fid4[0]))
imd0 = compute_intermarker (marker0,k)[:,2]
# index = result[0][0] 
# for index in result[0]:
intermarker_var = []
count = 0
for index in range(len(tre)):
    fids = np.vstack((fid1[index],fid2[index],fid3[index],fid4[index]))

    imd = compute_intermarker (fids,len(fids))
    inter_x = imd0-imd[:,2]
    inter_dev = np.sqrt(np.mean(inter_x**2))
    intermarker_var.append(inter_dev)
    # print(inter_dev)
    # print("index",index)

    # print(imd)
    # print(fids)
    # print (tre[index])
    dist = 0
    if min_dist_and_incr(imd,minimum,increment) and inter_dev >= dist :
    #if True :

        if count ==50:
            break
        count = count + 1
        print("geometry pass",min_dist_and_incr(imd,minimum,increment))
        print("intermarker")
        print(imd)
        print("fiducials")
        print(fids)
        print("tre")
        print(tre[index])
        
        print("index",index)
        fig = plot_fids(fids)
        fig.update_layout(
            height=1000,
            title_text=str(tre[index])
            )
        fig.write_html(str(filename)+str(index)+str(tre[index])+".html")
        fig.show()
        time.sleep(5)
        dist = 4

        

ind = []