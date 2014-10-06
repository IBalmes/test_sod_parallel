#############################################################################
#reading the halos mass and position
#from simu boxlen648_n256_rpcdmw5
#in order to compare the results from SOD and pSOD
#############################################################################
import matplotlib.pyplot as plt
import numpy as np 
import re
from mpl_toolkits.mplot3d import Axes3D
#############################################################################

#############################################################################
#A few remarks
#
#The halos found in the buffer zone by pSOD should have the same center as 
#those found in the buffer zone by SOD (since the center is just the densest
#particle). However, they will not contain the same particles, at least for
#those who are close to the border: they will contain more particles, because
#all the missing particles lower the estimated overdensity.
#
#It seems really weird that some halos don't have the same center then...
#Since it is just a problem of densest part, this should not change between
#SOD and pSOD.
#############################################################################

#############################################################################
#Some remarks on halo sizes
#############################################################################
#one sub-cube is, in this simulation, 237 Mpc/h wide, or 64 coarse cells.
#So far, I have studied buffer zones of 64, 32 or 16 coarse cells,
#or 237, 118.5, 59.25 Mpc/h.
#However, the radius of a halo is typically between 1 and 3 Mpc/h!
#(in this simu).
#Therefore, maybe a _way_ smaller buffer zone would create better results?
#Trying with a buffer zone of 4 coarse cells (around 4 times the radius of
# a halo)
#with a buffer of 4 coarse cells, around 25% more halos are found in the 
#parallel version.
#############################################################################

#############################################################################
#Number of halos in each case
#############################################################################
#serial: 1512
#buff4: 2101
#buff8: 2101
#buff16: 1507
#buff32: 1523
#buff64: 2101
#############################################################################
#Seems clear that buff16 and buff32 perform better than the others...
#############################################################################


#############################################################################
#reading serial data
#############################################################################
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
#############################################################################

#############################################################################
#reading parallel data
#############################################################################
mp=[]
xp=[]
yp=[]
zp=[]
rp=[]
cubep=[]
from os import listdir
from os.path import isfile, join
#path='/home/irene/Desktop/test SOD parallel/parallel/'
#alternate lines to read archived data
path='/home/irene/Desktop/test SOD parallel/parallel/buff32/'
files = [join(path,f) for f in listdir(path) if isfile(join(path,f))]
for name in files:
    f=open(name)
    lines=f.readlines()
    temp=re.findall(r"[\w']+",name)
#    tmp=temp[7]
    tmp=temp[8]
    temp=tmp.split('_')
    cubeid=temp[2]
    for line in lines:
        p=line.split()
        mp.append(float(p[1]))
        xp.append(float(p[3]))
        yp.append(float(p[4]))
        zp.append(float(p[5]))
        rp.append(float(p[6]))
        cubep.append(int(cubeid))

#############################################################################

#############################################################################
#defining stuff to study differences between the two detections
#############################################################################
mall=ms+mp
xall=xs+xp
yall=ys+yp
zall=zs+zp

sets=set(zip(ms,xs,ys,zs))
setp=set(zip(mp,xp,yp,zp))
setall=set(zip(mall,xall,yall,zall))

#halo in both catalogs
halo_both=sets&setp
mboth,xboth,yboth,zboth=zip(*halo_both)

#halos detected only in serie
halo_sonly=sets-halo_both
msonly,xsonly,ysonly,zsonly=zip(*halo_sonly)

#halos detected only in parallel
halo_ponly=setp-halo_both
mponly,xponly,yponly,zponly=zip(*halo_ponly)

#all halos different
halo_different=halo_sonly|halo_ponly
mdiff,xdiff,ydiff,zdiff=zip(*halo_different)
#############################################################################

#############################################################################
#Are there differences between the number of identical halos with and without
#mass taken into account?
#############################################################################
#The real question here is: do all found halos have _exactly_ the same center
#because they should!
#############################################################################
setposs=set(zip(xs,ys,zs))
setposp=set(zip(xp,yp,zp))
center_both=setposs&setposp
len(center_both)
len(halo_both)
#############################################################################
#and the answer is: they don't!
#only three halos have the same center and different masses
#############################################################################

#############################################################################
#number of identical and different halos, for different cases
#############################################################################
len(halo_both)
len(halo_sonly)
len(halo_ponly)
#32 cell buffer:
#1087 halos are _exactly_ the same 
#64 cell buffer:
#1114
#32 cell buffer, don't take into account halos with center closer than 16 cells
#1105
#8 cell buffer:
#1124

#BUT
#the number of halos found _only_ by pSOD increases with the buffer size (??)
#no, not monotonic.
#############################################################################

#############################################################################
#converting everything to numpy arrays
#############################################################################
ms=np.array(ms)
xs=np.array(xs)
ys=np.array(ys)
zs=np.array(zs)
rs=np.array(rs)

mp=np.array(mp)
xp=np.array(xp)
yp=np.array(yp)
zp=np.array(zp)
rp=np.array(rp)
cubep=np.array(cubep)

mboth=np.array(mboth)
xboth=np.array(xboth)
yboth=np.array(yboth)
zboth=np.array(zboth)

msonly=np.array(msonly)
xsonly=np.array(xsonly)
ysonly=np.array(ysonly)
zsonly=np.array(zsonly)

mponly=np.array(mponly)
xponly=np.array(xponly)
yponly=np.array(yponly)
zponly=np.array(zponly)

mdiff=np.array(mdiff)
xdiff=np.array(xdiff)
ydiff=np.array(ydiff)
zdiff=np.array(zdiff)
#############################################################################

#############################################################################
#vertices of the cubes
#############################################################################
xgrid=[0,0.25,0.5,0.75,1]
ygrid=xgrid
zgrid=xgrid
#############################################################################

#############################################################################
#Plotting in 3D -- this is unreadable
#############################################################################
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xs,ys,zs,c='g')
ax.scatter(xp,yp,zp,c='r')
ax.set_xlim([0,0.3])
ax.set_ylim([0,0.3])
ax.set_zlim([0,0.3])
plt.show()
#############################################################################

#############################################################################
#checking if the largest halos are similar
#############################################################################
ms.max()
mp.max()
indmaxs,=np.where(ms==ms.max())
indmaxp,=np.where(mp==mp.max())
xs[indmaxs],xp[indmaxp]
ys[indmaxs],yp[indmaxp]
zs[indmaxs],zp[indmaxp]
rs[indmaxs],rp[indmaxp]
#ok, the larger halo is similar.
#############################################################################

#############################################################################
#checking the mass function
#############################################################################
a,b = np.histogram(np.log10(ms*1e12),bins=60)#,color='blue',label='SOD')
ap,bp = np.histogram(np.log10(mp*1e12),bins=60)#,color='red',label='pSOD')
plt.plot(b[:-1],a,color='blue',label='SOD')
plt.plot(bp[:-1],ap,color='red',label='pSOD')
plt.xlabel('$\log(M/M_\odot)$')
plt.title('halo number counts')
plt.legend()
plt.show()
#mostly similar, but there seems to be marginal differences in the masses of halos.
#############################################################################

#############################################################################
#testing the positions in slices of z
#############################################################################
for i in np.arange(0,1,0.05):
    inds,=np.where((zs > i) & (zs < i+0.05))
    indp,=np.where((zp > i) & (zp < i+0.05))
    fig,ax=plt.subplots()
    ax.scatter(xs[inds],ys[inds],c='r',marker='o',s=ms[inds]/10)
    ax.scatter(xp[indp],yp[indp],c='b',marker='+',s=mp[indp]/10)
    plt.show()
#############################################################################
#mostly ok, only small size halos appear to be different.
#differences due to the stopping criterion?
#############################################################################

#############################################################################
#plotting the halos that are different together on a grid,
#slice by slice in z
#############################################################################
for i in np.arange(0,1,0.05):
    inds,=np.where((zsonly > i) & (zsonly < i+0.05))
    indp,=np.where((zponly > i) & (zponly < i+0.05))
    fig,ax=plt.subplots()
    ax.scatter(xsonly[inds],ysonly[inds],c='r',marker='o',s=msonly[inds]/10)
    ax.scatter(xponly[indp],yponly[indp],c='b',marker='+',s=mponly[indp]/10)
    plt.show()
#most of the halos detected in serie are also detected in parallel
#however _a lot_ more halos are detected in parallel, including at very high mass!!!
#############################################################################

#############################################################################
#for the halos that are different, measure the mean distance to the border of a cube
#compare this with the mean distance obtained from a random distribution
#############################################################################
#parallel only
distponly=xponly*0+1
for xl in xgrid:
    tmp=np.abs(xponly-xl)
    distponly=np.minimum(distponly,tmp)

for yl in ygrid:
    tmp=np.abs(yponly-yl)
    distponly=np.minimum(distponly,tmp)

for zl in zgrid:
    tmp=np.abs(zponly-zl)
    distponly=np.minimum(distponly,tmp)

distponly.mean()
#0.0285 for a buffer of 32 cells, not taking into account halos whose center
#is closer than 16 cells from the border.

#random points
xr=np.random.uniform(size=len(xponly))
yr=np.random.uniform(size=len(xponly))
zr=np.random.uniform(size=len(xponly))

distr=xr*0+1
for xl in xgrid:
    tmp=np.abs(xr-xl)
    distr=np.minimum(distr,tmp)

for yl in ygrid:
    tmp=np.abs(yr-yl)
    distr=np.minimum(distr,tmp)

for zl in zgrid:
    tmp=np.abs(zr-zl)
    distr=np.minimum(distr,tmp)

distr.mean()
#0.03
#the distribution is not significantly different for random points or for 
#the halos found only by the parallel algorithm.
#############################################################################

#############################################################################
#Checking if the differences arise from fragmentation of larger halos
#if so, additional smaller halos should be contained in larger ones.
#############################################################################
set_parallel=set(zip(mp,xp,yp,zp,rp))

#sorting the parallel catalog by mass
allp=sorted(set_parallel,reverse=True)
mp,xp,yp,zp,rp=zip(*allp)
nhalo=len(mp)
mp=np.array(mp)
xp=np.array(xp)
yp=np.array(yp)
zp=np.array(zp)
rp=np.array(rp)

#variable containing the id of inner halos
inp=[]
#variable containing the id of main halos
outp=[]
for i in range(nhalo):
    for j in range(i+1,nhalo):
        d=np.sqrt((xp[i]-xp[j])**2+(yp[i]-yp[j])**2+(zp[i]-zp[j])**2)
        if (d<rp[i]):
            inp.append(j)
            outp.append(i)

#No, fragmenting halos is not the problem there (not with buffer=32)
#SO WHAT IS?????
#ACTUALLY, when the buffer is large and half of it is not taken into account,
#there is substantial fragmenting (around 200 halos found twice!)
#Happens also if the buffer zone is 64, without buffer zone splitting.

#it's actually not so much fragmenting as finding the same halo twice in
#two different cubes: the masses are usually very close.

#There must be a sweet spot for the buffer zone: need to minimize splitting
#and avoid missing halos.
#Though I don't really understand why it should go down with buffer size?
#############################################################################

#############################################################################
#Looking halo by halo at the differences
#############################################################################

#############################################################################

#############################################################################
#below this point, things are more or less obsolete
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#list of ids of the different halos
#in the parallel cat, but not in the serial
idp=[888,1097,41,1401,78,1287,1063,1040,231,953,947,758,1379,1510,21,1522,1117,1520,457,723,899,925,922,911,588,469,784,926,1080,1308,565,1253,519,691,689,196]
#in the serial cat, but not in the parallel
ids=[1497,591,1152,937,1420,1381,1280,771,958,1219,1371,1087,1103,1263,569,1207,611,261,826,1401,1279,819]
idp=np.array(idp)
ids=np.array(ids)
#############################################################################

#############################################################################
#computing the distances between the diff halos and the vertices of the cubes
#for a line of equation (xl=cst,yl=cst), the shortest dist. between this line and a point (x,y,z) is given by sqrt((x-xl)**2+(y-yl)**2).
#this computation must be done for _every_ pair (xl,yl), (xl,zl), (yl,zl).
#for each point, I keep the lowest value for the distance
distp=idp*0+1
dists=ids*0+1
#x,y pairs
for xl in xgrid:
    for yl in ygrid:
        tmp=np.sqrt((xp[idp]-xl)**2+(yp[idp]-yl)**2)
        distp=np.minimum(distp,tmp)
        tmp=np.sqrt((xs[ids]-xl)**2+(ys[ids]-yl)**2)
        dists=np.minimum(dists,tmp)

#x,z pairs
for xl in xgrid:
    for zl in zgrid:
        tmp=np.sqrt((xp[idp]-xl)**2+(zp[idp]-zl)**2)
        distp=np.minimum(distp,tmp)
        tmp=np.sqrt((xs[ids]-xl)**2+(zs[ids]-zl)**2)
        dists=np.minimum(dists,tmp)

#y,z pairs
for yl in ygrid:
    for zl in zgrid:
        tmp=np.sqrt((yp[idp]-yl)**2+(zp[idp]-zl)**2)
        distp=np.minimum(distp,tmp)
        tmp=np.sqrt((ys[ids]-yl)**2+(zs[ids]-zl)**2)
        dists=np.minimum(dists,tmp)

distp.mean()
#0.065590382802119318
dists.mean()
#0.074845048520059312

#what would be the value for a random dist?
#throwing len(idp) random points and doing the same computation:
#random points
xr=np.random.uniform(size=len(distdiff))
yr=np.random.uniform(size=len(distdiff))
zr=np.random.uniform(size=len(distdiff))

distr=xr*0+1
for xl in xgrid:
    tmp=np.abs(xr-xl)
    distr=np.minimum(distr,tmp)

for yl in ygrid:
    tmp=np.abs(yr-yl)
    distr=np.minimum(distr,tmp)

for zl in zgrid:
    tmp=np.abs(zr-zl)
    distr=np.minimum(distr,tmp)

distr.mean()
#0.075477631614532109
#so the halos that pose a problem are not closer to the vertices than random points...

#checking the mass function of the different halos
plt.hist(ms[ids],bins=120,color='blue')
plt.hist(mp[idp],bins=120,color='red')
plt.show()
#almost all have a mass lower than 200 particles.

#testing if the different parallel halos are detected by the right cube
#value of the detecting cube based on the position of the halo
xtmp=xp/0.25
xtmp=xtmp.astype(int)
ytmp=yp/0.25
ytmp=ytmp.astype(int)
ztmp=zp/0.25
ztmp=ztmp.astype(int)
cubeth=(xtmp*4+ytmp)*4+ztmp

plt.scatter(cubep,cubeth)
plt.show()

#2 halos seem wrong!!!!
np.where((cubep == 40) & (cubeth == 44))
#732 
np.where((cubep == 59) & (cubeth == 60))
#1244
#red herring. both are exactly on a vertice.
#by the way, at least some halos on vertices are correctly detected by both algo, even at small mass.


plt.hist(mdiff,bins=120,color='blue')
plt.show()
#differences mostly present at small masses, but are present up to m=700!

#3D plot of where the different halos are located
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xdiff,ydiff,zdiff,c='r')
plt.show()

#mean distance of these halos to a vertice
xgrid=[0,0.25,0.5,0.75,1]
ygrid=xgrid
zgrid=xgrid

distdiff=xdiff*0+1
for xl in xgrid:
    tmp=np.abs(xdiff-xl)
    distdiff=np.minimum(distdiff,tmp)

for yl in xgrid:
    tmp=np.abs(ydiff-yl)
    distdiff=np.minimum(distdiff,tmp)

for zl in zgrid:
    tmp=np.abs(zdiff-zl)
    distdiff=np.minimum(distdiff,tmp)

#mean of distr: 0.069
plt.hist(distdiff,bins=30,color='blue')
plt.show()

#largest different halo
idmax,=np.where(mdiff== mdiff.max())
idmax2,=np.where(mdiff== mdiff.max()-1)
xdiff[idmax],ydiff[idmax],zdiff[idmax]
xdiff[idmax2],ydiff[idmax2],zdiff[idmax2]
#0.6623,0.2849,0.531 vs 0.6622,0.2848,0.5311 !!! -> it must be the 'same' halo
#This is a difference of 64.8kpc in the center position, way above even the _max_ radius of halos....????


