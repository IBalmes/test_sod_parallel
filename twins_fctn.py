def twins(sets,setp):
    #reading the halos mass and position
    import matplotlib.pyplot as plt
    import numpy as np 
    from mpl_toolkits.mplot3d import Axes3D

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

    print 'number of halos with a twin: ',len(twins)
    print 'number of halos without a twin: ',len(reject)
    print 'total number of halos: ',len(set_sonly),len(twins)+len(reject)

    print 'largest difference in mass: ', max(Mscore)
    print 'largest difference in center: ', max(Cscore)

    plt.plot(Mscore,Cscore,'bs')
    plt.xlabel('Mscore')
    plt.ylabel('Cscore')
    plt.show()

    #for the rejected halos
    msonly=np.array(msonly)
    plt.hist(msonly[reject],bins=50)
    plt.show() 
