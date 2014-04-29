#reading the halos mass and position
import matplotlib.pyplot as plt
import numpy as np 
from mpl_toolkits.mplot3d import Axes3D

#serial data
f=open('sod_00024.dat')
lines=f.readlines()
ms=[]
xs=[]
ys=[]
zs=[]
rs=[]
for line in lines:
    p=line.split()
    ms.append(float(p[1]))
    xs.append(float(p[3]))
    ys.append(float(p[4]))
    zs.append(float(p[5]))
    rs.append(float(p[6]))

sets=set(zip(ms,xs,ys,zs,rs))
ms=np.array(ms)
xs=np.array(xs)
ys=np.array(ys)
zs=np.array(zs)
rs=np.array(rs)


#parallel data with a buffer of 32
mp=[]
xp=[]
yp=[]
zp=[]
rp=[]
from os import listdir
from os.path import isfile, join
path='/home/irene/Desktop/test SOD parallel/parallel/buff32/'
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

setp=set(zip(mp,xp,yp,zp,rp))
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

setp16=set(zip(mp16,xp16,yp16,zp16,rp16))
mp16=np.array(mp16)
xp16=np.array(xp16)
yp16=np.array(yp16)
zp16=np.array(zp16)
rp16=np.array(rp16)

#exact agreement between all three cases.
#halos that are detected in every case:
set_everytime=sets&setp&setp16
#906

#in only two sets
set_s32=sets&setp
#1087
set_s16=sets&setp16
#1054
set1632=setp&setp16
#1052

############################################
#Between serial and buffer=32
############################################
#finding probable twins for each halo 
#set of symmetric differences
set_sonly=sets-setp
msonly,xsonly,ysonly,zsonly,rsonly=zip(*set_sonly)
set_ponly=setp-sets
mponly,xponly,yponly,zponly,rponly=zip(*set_ponly)

twins=[]
twinp=[]
Mscore=[]
Cscore=[]
reject=[]
for i in range(len(set_sonly)):
    for j in range(len(set_ponly)):
        tmpm=np.abs(msonly[i]-mponly[j])/msonly[i]
        tmpc=np.sqrt((xsonly[i]-xponly[j])**2+(ysonly[i]-yponly[j])**2+(zsonly[i]-zponly[j])**2)/rsonly[i]
#        if j==0:
        if (tmpm <= 0.1 and tmpc <= 1):
            Mscore.append(tmpm)
            Cscore.append(tmpc)
            twinp.append(j)
            twins.append(i)
        else:
            if j==0:
                tmpr=1
            else:
                tmpr=tmpr+1
        if tmpr==len(set_ponly):
            reject.append(i)
#        else:
#            if(tmpm<Mscore[-1] and tmpc<Cscore[-1]):
#                Mscore[-1]=tmpm
#                Cscore[-1]=tmpc
#                twinp[-1]=j

#around 50 halos have no twins.
#the masses are in agreement to around 10% (good), and the center positions to 85% (!)            

#for the rejected halos
msonly=np.array(msonly)
plt.hist(msonly[reject],bins=50)
plt.show() 
#all different halos (in serial) have masses below 220part.
#most have masses around 100.

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
    inds,=np.where((zs >= i) & (zs < i+0.05))
    indp16,=np.where((zp16 >= i) & (zp16 < i+0.05))
    indp,=np.where((zp >= i) & (zp < i+0.05))
    fig,ax=plt.subplots()
    ax.scatter(xs[inds],ys[inds],c='g',marker='s',s=ms[inds]/10+.3)
    ax.scatter(xp16[indp16],yp16[indp16],c='r',marker='o',s=mp16[indp16]/12)
    ax.scatter(xp[indp],yp[indp],c='b',marker='+',s=mp[indp]/10)
    plt.show()

