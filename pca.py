#Step1:read those files and put datas into matrix
import numpy as np
import math
from numpy.lib.function_base import average
from numpy.matrixlib.defmatrix import matrix
import pandas as pd
import glob
import os
import re
from sklearn import cluster
import matplotlib.pyplot as plt

t = 100

sizes = [10,12,14,16] 

elongation = '00' 

material = "spheroid"

geometry = "taenite0_tetrataenite100"

Home = r'c:\\Users\\josea\\Desktop\\taenite_tetrataenite-main'

for size in sizes:
    home = os.path.join(Home,
                    material,
                    geometry,
                    'E{}'.format(elongation),
                    'groundstates',
                    str(size))
    os.chdir(home)     

    files=glob.glob('*.dat')
    filestoread=[]
    for i in files:
        if "{}".format(size) in i:
            filestoread.append(i)        
    dfs=[]
    pos=[]
    for i in filestoread:
        dfs.append([])
        pos.append([])
        df=open(i,'r')
        for line in df:
            nums=line
            figures=nums.split()
            for i in figures:
                i=i.replace(' ','')
            px=float(figures[0])
            py=float(figures[1])
            pz=float(figures[2])
            Mx=float(figures[3])
            My=float(figures[4])
            Mz=float(figures[5])
            dfs[-1].append([Mx,My,Mz])   
    #Step2:compare method
    from sklearn.decomposition import PCA
    from sklearn.cluster import KMeans
    from sklearn import metrics
    pca=PCA(n_components=0.99,whiten=True)
    alldata=[]
    for i in range(len(dfs)):
        alldata.append([])
        for j in dfs[i]:
            for k in j:
                alldata[i].append(k)
    alldata=np.array(alldata)
    newall=pca.fit_transform(alldata)
    #print(pca.explained_variance_ratio_)

    PC_loadings=[]
    for i in range(len(pca.explained_variance_ratio_)):
        reduce=[]
        for j in range(len(pca.explained_variance_ratio_)):
            reduce.append(0)
        reduce[i]=1
        reduce=np.array(reduce)
        X_recovered=pca.inverse_transform(reduce)
        PC_loadings.append(X_recovered)

    from sklearn.metrics import silhouette_score

    score=[]
    for n in range(2,20):
        km=KMeans(n_clusters=n).fit(newall)
        score.append(silhouette_score(newall,km.labels_))

    n=0
    #plt.plot(range(2,20),score)
    for i in range(1,len(score)):
        if score[i]>score[i-1] and score[i]>=score[i+1]-0.01:
            n=2+i
            break

    km=KMeans(n_clusters=n).fit(newall)
    labellist=list(km.labels_)
    number=100
    #print(n)
    #print(labellist)
    #print(len(labellist))
    #import os
    for num in range(n):
        foldername = os.path.join(Home,
                    material,
                    geometry,
                    'E{}'.format(elongation),
                    'plots',
                    str(size),
                    '{}_{}_{}'.format(str(size),
                                      str(t),
                                      str(num)))        
        #if not os.path.exists(foldername):
            #os.makedirs(foldername)

    ##move picture files to folders
    #import shutil
    data_frame = [['subdir','No']]
    for i in range(number):
        No=str(i+1)
        #print(No)
        filename = os.path.join(Home,
                    material,
                    geometry,
                    'E{}'.format(elongation),
                    'plots',
                    str(size),
                    '{}'.format(str(size)) + '.png')         
        #filename = 'D:\\Taenite\\jupyter\\data_{}\\E{}\\plots\\{}\\{}'.format(geometry, elongation, str(size),No) + '.png'
        #filename='F:\\study\\Pic\\x{0:g}_y{1:g}_z{2:g}_t{3:g}_sol.'.format(x,y,z,t)+No+'.png'
        folder = os.path.join(Home,
                    material,
                    geometry,
                    'E{}'.format(elongation),
                    'plots',
                    str(size),
                    '{}_{}_{}'.format(str(size),
                                      str(t),
                                      str(num)))          
        #folder = 'D:\\Taenite\\jupyter\\data_{}\\E{}\\plots\\{}\\{}_{}_{}'.format(geometry,elongation,str(size),str(size),str(t),labellist[i])
        #folder='F:\\study\\Pic\\x{0:g}_y{1:g}_z{2:g}_t{3:g}_sol{4:g}'.format(x,y,z,t,labellist[i])
        #if os.path.exists(filename) and os.path.exists(folder):
            #shutil.copyfile(filename,folder+'\\{}_sol{}'.format(str(size),No)+'.png')
        data_frame.append(['{}'.format(labellist[i]),'{}'.format(No)])
        df = pd.DataFrame(data_frame)
        df.columns = df.iloc[0]
        df = df[1:]
        df = df.sort_values('subdir', ascending=True)
        df = df.set_index('subdir')
        path = os.path.join(Home,
                            material,
                            geometry,
                            'E{}'.format(elongation),
                            'plots',
                            'clusters_{}.txt'.format(str(size)))

        #print(path)
        #path = 'D:\\Taenite\\jupyter\\data_{}\\E{}\\plots\\{}\\{}.csv'.format(geometry,elongation, str(size),str(size))
        df.to_csv(path)
        #else:
            #print('file does not exist!!')

        #print(data_frame)
