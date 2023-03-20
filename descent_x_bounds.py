import numpy as np
import random as ran
import plotly.graph_objects as go

#Generate
height = 345
width = 325
samples = 1000
x = width/2
y = height/2
z = 0 
q1_1  = np.array([0,x,z])
q1_2  = np.array([x,y,z])
q1_3  = np.array([x,0,z])

q2_1  = np.array([0,-x,z])
q2_2  = np.array([x,-y,z])
q2_3  = np.array([x,0,z])

q3_1  = np.array([0,-x,z])
q3_2  = np.array([-x,-y,z])
q3_3  = np.array([-x,0,z])

q4_1  = np.array([0,y,z])
q4_2  = np.array([-x,y,z])
q4_3  = np.array([-x,0,z])

B1=np.array([q1_1,q1_2,q1_3])
B2=np.array([q2_1,q2_2,q2_3])
B3=np.array([q3_1,q3_2,q3_3])
B4=np.array([q4_1,q4_2,q4_3])
hulls = [B1,B2,B3,B4]

def generate_B(B):
    df = []
    vdata = []
    for i in range(int(samples/4)):
        l = []
        r = [ran.random() for i in range(len(B))]
        r = np.array([r])
        r = r/r.sum()
        x_ = B.transpose()@r.transpose()
        vdata.append(x_.transpose()[0])
    return np.array(vdata)

def get_mesh(hulls):
    
    data = []
    for i in hulls:
        vdata = generate_B(i)
        if len(data)==0:
            data = vdata
        else:
            data = np.vstack((data,vdata))
    return data


data = get_mesh(hulls)
def plot_fids(fids,target=np.array([[0,0,0]])):
    target = np.around(target,2)
    fids=np.vstack((fids,[0, 0, 0]))
    fiducials = go.Scatter3d(
        x=fids[:,0], y=fids[:,1], z=fids[:,2],
        marker=dict(size=4,colorscale='Viridis',),line=dict(color='darkblue',width=2))
    target_int = go.Scatter3d(x=target[:,0], y=target[:,1], z=target[:,2],
        marker=dict(size=4,colorscale='Viridis',),line=dict(color='coral',width=2))

    axes = go.Scatter3d(x = [0,0,0,100,0,0],y = [0, 100,0,0,0,0 ],z=[0,0,0,0,0,100],marker = dict( size = 1,color = "rgb(84,48,5)"),line=dict(color="rgb(84,48,5)",width=6))
    axx = go.Cone(x=[10], y=[10], z=[10], u=[5], v=[5], w=[5])
    data = [fiducials,axes,target_int,axx]
    name = 'default'
# Default parameters which are used when `layout.scene.camera` is not provided
    camera = dict(up=dict(x=-1, y=0, z=0),center=dict(x=0, y=0, z=0),eye=dict(x=0, y=0, z=1.25))

    fig = go.Figure(data=data)
    fig.update_layout(scene_camera=camera, title=name)
    fig.update_layout(scene = dict(xaxis = dict(nticks=4, range=[-300+np.min(fids[:,0]),np.max(fids[:,0])+100],),yaxis = dict(nticks=4, range=[-300,300],),zaxis = dict(nticks=4, range=[-300,100],),),
    width=700,
    margin=dict(r=20, l=10, b=10, t=10))
    return fig




fig = plot_fids(data)
fig.show()
    