import numpy as np
from scipy.optimize import minimize
from functions import distanceFromLine,unit
from numpy.linalg import norm
from scipy import optimize





def compute_tre(vec):
    vector = vec.reshape(4,3)
    target=np.array([0,0,500])

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
    # if np.sum(norm(vector,axis=1)>threshold):
    #     return 100
    # else:
    return np.sqrt(np.around(tre,3))






bnd = 10

bounds = [(-bnd, bnd), (-bnd, bnd),(-bnd, bnd),(-bnd, bnd),(-bnd, bnd),(-bnd, bnd),(-bnd, bnd),(-bnd, bnd),(-bnd, bnd),(-bnd, bnd),(-bnd, bnd),(-bnd, bnd)]
results = dict()
results['shgo'] = optimize.shgo(compute_tre, bounds)
print(results['shgo'])



 
