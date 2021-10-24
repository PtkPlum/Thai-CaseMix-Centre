import pandas as pd
import numpy as np
import scipy as sp

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.metrics import silhouette_samples
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering

import numpy.matlib



'''
====================================================================================================================================================
        

        1st     :   Code of Data Cleansing and Data Preparation


====================================================================================================================================================
'''


def PlotNonCluster(X, columnList, title="", rotate=0):
    if X.shape[1] == 2:
        plt.plot(X[:,0], X[:,1], 'o', markeredgecolor='k')
        plt.title("Graph")
        plt.xlabel(columnList[0]) 
        plt.ylabel(columnList[1])
        plt.show()
        
    elif X.shape[1] == 3:
        for angle1 in range(int(0 + 30 * (1-rotate)), int(90 - 50 * (1-rotate)), 15):
            for angle2 in range(int(0 + 30 * (1-rotate)), int(90 - 50 * (1-rotate)), 15):
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                
                p = ax.scatter(X[:,0], X[:,1], X[:,2], alpha=.3)
                
                ax.view_init(angle1, angle2)
                
                ax.set_title(title + " \nwith Perspective " + str(angle1) + " degree")
                ax.set_xlabel(column[0])
                ax.set_ylabel(column[1])
                ax.set_zlabel(column[2])
        plt.show()
                
    elif X.shape[1] == 4:
        for angle1 in range(int(0 + 30 * (1-rotate)), int(90 - 50 * (1-rotate)), 15):
            for angle2 in range(int(0 + 30 * (1-rotate)), int(90 - 50 * (1-rotate)), 15):
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                
                p = ax.scatter(X[:,0], X[:,1], X[:,2], c=X[:,3] ,cmap=plt.hot(), alpha=.3)
                cbar = fig.colorbar(p)
                
                ax.view_init(angle1, angle2)
                
                ax.set_title(title + " \nwith Perspective " + str(angle1) + " degree")
                ax.set_xlabel(column[0])
                ax.set_ylabel(column[1])
                ax.set_zlabel(column[2])
                cbar.set_label(column[3])
        plt.show()
        
    else:
        print("Could not plot in higher dimension")


def StatMeasure(X, columnList, hist=0, boxplt=0):
    j = 0
    for i in columnList:
        print("Mean     of ", i, "is", np.mean(X[:,j]))
        print("Median   of ", i, "is", np.median(X[:,j]))
        print("S.D.     of ", i, "is", np.std(X[:,j]))
        print("skewness of ", i, "is", sp.stats.skew(X[:,j])) 
        print("\n")
        if boxplt == 1:
            plt.boxplot(X[:,j])
            plt.title("Boxplot of " + i)
            plt.show()
        if hist == 1:
            plt.hist(X[:,j])
            plt.title("Histrogram of " + i)
            plt.show()
        j += 1

    XEachColumn = []
    for i in range(X.shape[1]):
        XEachColumn.append(X[:,i])
        
    print("correlation coefficient is \n", np.corrcoef(XEachColumn))
    print("\n")


def GenerateArray(data, columnList, plot=0, rotate=0, LogIndex = []):
    X = data[columnList]
    X = np.array(X)
    Y = X.copy()
    X = Standardize(X, LogIndex)
    if plot == 1:
        PlotNonCluster(Y, columnList, "Visualization of Data", rotate)
        if LogIndex != []:
            PlotNonCluster(X, columnList, "Visualization of Standardized and Scaled Data", rotate)
    return Y, X


def LogTransform(X, Index):
    for i in Index:
        Min = min(X[:,i])
        Min = 0 if Min > 0 else Min
        X[:,i] = np.log(X[:,i] + 1 - Min)
    return X


def Standardize(X, LogIndex):
    if LogIndex is not None:
        X = LogTransform(X, LogIndex)
    Mean = np.mean(X,0)
    SD   = np.std(X,0)
    return (X-Mean)/SD



'''
====================================================================================================================================================
        

        2nd     :   Code of clustering algorithm


====================================================================================================================================================
'''



def Kmeans(X, K, th=0):
    centroids = X[np.random.choice(len(X), K, replace=False)]
    i = 0
    while True:
        i += 1
        D = np.zeros((K,len(X)))
        for k in range(K):
            D[k] = np.sum((X - centroids[k])**2, axis=1)
        idx = np.argmin(D, axis=0)
        old_centroids = centroids.copy()
        for k in range(K):
            centroids[k] = np.mean(X[idx == k], axis=0)
        if np.sum(np.abs(old_centroids - centroids)) <= th:
            return idx, centroids


def Kmedians(X, K, th=0):
    centroids = X[np.random.choice(len(X), K, replace=False)]
    i = 0
    while True:
        i += 1
        D = np.zeros((K,len(X)))
        for k in range(K):
            D[k] = np.sum((X - centroids[k])**2, axis=1)
        idx = np.argmin(D, axis=0)
        old_centroids = centroids.copy()
        for k in range(K):
            centroids[k] = np.median(X[idx == k], axis=0)
        if np.sum(np.abs(old_centroids - centroids)) <= th:
            return idx, centroids
        
        
def FuzzyCmeans(X, K, m=2, th=10**-6, show=False):
    centroids = X[np.random.choice(len(X), K, replace=False)]
    i = 0
    while True:
        i += 1
        D = np.zeros((K,len(X)))
        for k in range(K):
            D[k] = np.sum((X - centroids[k])**2, axis=1)
        u = 1 / D ** (1/(m-1))
        u /= np.sum(u, axis=0)
        u[np.isnan(u)] = 1      # Replace Nan with 1
        old_centroids = centroids.copy()
        for k in range(K):
            temp = u[k] ** m
            centroids[k] = np.sum(X.T * temp.T, axis=1) / np.sum(temp)
            # Use Transpose for broadcast trick
        if np.sum(np.abs(old_centroids - centroids)) <= th:
            return np.argmin(D, axis=0), centroids

    
def Linkage(X, stdX, k,linkage, x_label, y_label, plot=1):
    cluster = AgglomerativeClustering(n_clusters=k, linkage=linkage)
    cluster.fit(stdX)
    cluster = cluster.labels_
    if plot == 1:
        ClusterPlot(X, cluster, x_label, y_label, linkage)
    return cluster
    


'''
====================================================================================================================================================
        

        3rd     :   Code of Clustering Plot and Measurement


====================================================================================================================================================
'''
    
def ClusterPlot(X,cluster, x_label="x", y_label="y", label="title", rotate=0):
    ClustSet      = set(cluster)
    ClustGrp      = [[] for i in ClustSet]
    ClustGrpIndex = [[] for i in ClustSet]
    for k in ClustSet:
        for i in range(len(cluster)):
            if cluster[i] == k:
                ClustGrp[k].append(list(X[i,:]))
                ClustGrpIndex.append(i)
        ClustGrp[k] = np.array(ClustGrp[k].copy())
        
    
    if X.shape[1] == 2:
        # Black removed and is used for noise instead.
        unique_labels = set(cluster)
        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
        #print(colors)
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = [0, 0, 0, 1]
            class_member_mask = (cluster == k)        
            xy = X[class_member_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=5, label=k)
            plt.legend()
        plt.title(label)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
        
    elif X.shape[1] == 3:
        for angle1 in range(int(0 + 30 * (1-rotate)), int(90 - 50 * (1-rotate)), 15):
            for angle2 in range(int(0 + 30 * (1-rotate)), int(90 - 50 * (1-rotate)), 15):
                i = 0
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                
                for j in range(len(ClustGrp)):            
                    ax.scatter(ClustGrp[j][:,0], ClustGrp[j][:,1], ClustGrp[j][:,2], alpha=0.9, label=j)
                    ncol = 1 if len(ClustSet) < 10 else len(ClustSet)//10 
                    ax.legend(bbox_to_anchor=(0, 0., -0.2, 1.01), title="Cluster", ncol=ncol)                    
                    
                    ax.view_init(angle1, angle2)
                        
                    ax.set_title("Clustering Visualization \nwith Perspective " + str(angle1) + " degree")
                    ax.set_xlabel(column[0])
                    ax.set_ylabel(column[1])
                    ax.set_zlabel(column[2])
                
                plt.show()

          
    elif X.shape[1] == 4 and len(ClustSet) <= 31:
        marker = ('$?$', '$a$', '$b$', '$c$','$d$', '$e$', '$f$','$g$', '$h$', '$i$','$j$', '$k$', '$l$','$m$', '$n$', '$o$', r'$\checkmark$',r'$\spadesuit$', r'$\lambda$',r'$\bowtie$',r'$\circlearrowleft$', r'$\clubsuit$', 'o', 'v', '*', 'P', '>', 's', 'p', '8', 'H', 'h', '^', 'D', 'd', '<', 'X')

        for angle1 in range(int(0 + 30 * (1-rotate)), int(90 - 50 * (1-rotate)), 15):
            for angle2 in range(int(0 + 30 * (1-rotate)), int(90 - 50 * (1-rotate)), 15):
                i = 0
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')         
                    
                for x in ClustGrp:            
                    p = ax.scatter(x[:,0], x[:,1], x[:,2], c=x[:,3], marker=marker[i] ,cmap=plt.hot(), alpha=0.9, vmin=min(X[:,3]), vmax=max(X[:,3]), label=i)
                    ncol = 1 if len(ClustSet) < 10 else len(ClustSet)//10 
                    plt.legend(bbox_to_anchor=(0, 0., -.3, 1.01), title="Cluster", ncol=ncol)
                    # bbox_to_anchor used to locate the .legend 
                    i += 1
                    
                    ax.view_init(angle1, angle2)
                    
                    ax.set_title("Clustering Visualization \nwith Perspective " + str(angle1) + " degree")
                    ax.set_xlabel(column[0])
                    ax.set_ylabel(column[1])
                    ax.set_zlabel(column[2])
        
                cbar = fig.colorbar(p)
                cbar.set_label(column[3])
                plt.show()
        
    else:
        print("Could not plot in higher dimension")


def WCSS(X, cluster, Centroid = []):
    ClustSet = set(cluster)
    ClustGrp = [[] for i in ClustSet]
    for i in range(len(cluster)):
        for k in ClustSet:
            if cluster[i] == k:
                ClustGrp[k].append(i)
    if Centroid == []:
        Centroid = [[] for i in ClustSet]
        for k in ClustSet:
            Centroid[k] = np.mean(X[cluster == k], axis=0)
    WCSS = [0 for i in ClustSet]

    for i in range(len(ClustGrp)):
        for j in range(len(ClustGrp[i])):
            index = ClustGrp[i][j]
            WCSS[i] += (np.array(X[index]) - np.array(Centroid[i])) ** 2
    TotalWCSS = np.sum(WCSS)
    return TotalWCSS


def OptimalK_ByElbow(X, ClusterList, MinK, MaxK, CentroidList=[], showWCSS=0, plot=0):
    K = range(MinK, MaxK+1)
    ElbowList = []
    for k in K:
        Cluster = ClusterList[k - MinK]
        if CentroidList == []:
            Centroid = []
        else:
            Centroid = CentroidList[k - MinK]
        ElbowList.append(WCSS(X, Cluster, Centroid))
        
    if showWCSS==1:        
            print("\n\n___________________________________________________\n\n")
            print(k)
            print("WCSS is ", ElbowList[-1])
            
    if plot==1:     
        plt.plot(K, ElbowList)
        plt.ylabel("WCSS")
        plt.xlabel("K")
        plt.title("Elbow plot")
        plt.show()
        
    optK = MaxPerpendicular(ElbowList, MinK, MaxK)
    return optK


def OptK(ElbowList, MinK, MaxK):
    nPoints = len(ElbowList)
    allCoord = np.vstack((range(nPoints), ElbowList)).T
    firstPoint = allCoord[0]
    lineVec = allCoord[-1] - allCoord[0]
    lineVecNorm = lineVec / np.sqrt(np.sum(lineVec**2))
    vecFromFirst = allCoord - firstPoint
    scalarProduct = np.sum(vecFromFirst * np.matlib.repmat(lineVecNorm, nPoints, 1), axis=1)
    vecFromFirstParallel = np.outer(scalarProduct, lineVecNorm)
    vecToLine = vecFromFirst - vecFromFirstParallel
    distToLine = np.sqrt(np.sum(vecToLine ** 2, axis=1))
    idxOfBestPoint = np.argmax(distToLine)
    
    print(f'Optimum number of cluster by Elbow method: {idxOfBestPoint}')
    
    return idxOfBestPoint



def MaxPerpendicular(ElbowList, MinK, MaxK):
    x1, x2 = MinK, MaxK
    y1, y2 = ElbowList[0], ElbowList[-1]
    m  = (y2-y1)/(x2-x1)
    c1 = y1 - m * x1
    Max = 0
    MaxIndex = 0
    for i in range(len(ElbowList)):
        x3 = MinK + i
        y3 = ElbowList[i]
        c2 = y3 + m * x3
        y4 = (c1 + c2) / 2
        x4 = (c1 - c2) / (-2 * m)
        distance = ((x4 - x3) ** 2 + (y4 - y3) ** 2) ** .5
        if distance >= Max:
            Max = distance
            MaxIndex = i + MinK
    return MaxIndex
    



'''
====================================================================================================================================================
        

        4th     :   Main Code for this program


====================================================================================================================================================
'''

if __name__ == '__main__':

#   =========================================================
#
#       I.   Import data and Prepare variable before cleaning
#    

    data = pd.read_csv("dataset1To11.csv")

    Column = [i for i in data]
    Index  = [-1, 10, 8, 14]
    column = []
    for i in Index:
        column.append(Column[i])
    
#   =========================================================   
#
#       II.     Clean the data and visualize it
#    

    X, stdX = GenerateArray(data, column, plot=1, LogIndex = [0,2,3], rotate=0)
    StatMeasure(X, column, hist=0, boxplt=0)

#   =========================================================   
#
#       III.    K-Mean model run K from interval and find best K using elboe method
#               ( Optional )

    ClusterList  = []
    CentroidList = []
    
    MinK, MaxK = 2, 100
    K = range(MinK, MaxK+1)

    for k in K:
        cluster, centroids = Kmeans(X, k)
        ClusterList.append(cluster)
        CentroidList.append(centroids)        
        
    OptK = OptimalK_ByElbow(X, ClusterList, MinK, MaxK, CentroidList=[], plot=1)
    print("Optimal number of K from ", MinK," to ", MaxK, " is ", OptK)

#   =========================================================   
#
#       VI.     Run K-Mean model with given K and visualize the cluster result
# 

    K = OptK                # K mean
    cluster, centroids = Kmeans(X, K)
    ClusterPlot(X, cluster, "x", "y", "title", rotate=.5)  # rotate = 0 to 1 which 0 = No, 0.5 = Medium, 1 = High
    
#   =========================================================   
#
#       V.     Add the result as DataFrame and save it as excel
# 
    
    data["cluster"] = cluster
    data.to_csv("ClusterResult.csv", index=False)
    data.to_excel("ClusterResult.xlsx", index=False)
    
        
    
    
    
    
