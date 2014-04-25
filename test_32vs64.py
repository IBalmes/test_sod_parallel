#reading the halos mass and position
import matplotlib.pyplot as plt
import numpy as np 
from mpl_toolkits.mplot3d import Axes3D

#parallel data with a buffer of 32
mp=[]
xp=[]
yp=[]
zp=[]
rp=[]
from os import listdir
from os.path import isfile, join
path='/home/irene/Desktop/test SOD parallel/parallel/'
files = [ join(path,f) for f in listdir(path) if isfile(join(path,f))]
for name in files:
    f=open(name)
    lines=f.readlines()
    for line in lines:
        p=line.split()
        mp.append(float(p[1]))
        xp.append(float(p[3]))
        yp.append(float(p[4]))
        zp.append(float(p[5]))
        rp.append(float(p[6]))

mp=np.array(mp)
xp=np.array(xp)
yp=np.array(yp)
zp=np.array(zp)
rp=np.array(rp)

#parallel data with a buffer of 16
mp16=[]
xp16=[]
yp16=[]
zp16=[]
rp16=[]
from os import listdir
from os.path import isfile, join
path='/home/irene/Desktop/test SOD parallel/parallel/buff16/'
files = [ join(path,f) for f in listdir(path) if isfile(join(path,f))]
for name in files:
    f=open(name)
    lines=f.readlines()
    for line in lines:
        p=line.split()
        mp16.append(float(p[1]))
        xp16.append(float(p[3]))
        yp16.append(float(p[4]))
        zp16.append(float(p[5]))
        rp16.append(float(p[6]))

mp16=np.array(mp16)
xp16=np.array(xp16)
yp16=np.array(yp16)
zp16=np.array(zp16)
rp16=np.array(rp16)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xp16,yp16,zp16,c='g')
ax.scatter(xp,yp,zp,c='r')
ax.set_xlim([0,0.3])
ax.set_ylim([0,0.3])
ax.set_zlim([0,0.3])
plt.show()

#checking the mass function
plt.hist(mp16,bins=120,color='blue')
plt.hist(mp,bins=120,color='red')
plt.show()
#mostly similar, but there seems to be marginal differences in the masses of halos.

#testing the positions in slices of z
for i in np.arange(0,1,0.05):
    indp16,=np.where((zp16 >= i) & (zp16 < i+0.05))
    indp,=np.where((zp >= i) & (zp < i+0.05))
    fig,ax=plt.subplots()
    ax.scatter(xp16[indp16],yp16[indp16],c='r',marker='o',s=mp16[indp16]/10)
    ax.scatter(xp[indp],yp[indp],c='b',marker='+',s=mp[indp]/10)
    plt.show()
#mostly ok, only small size halos appear to be different.
#differences due to the stopping criterion?
