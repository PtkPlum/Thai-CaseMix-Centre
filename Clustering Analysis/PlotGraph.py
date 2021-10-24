import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import silhouette_samples
import seaborn as sns

def ClusterPlot(X,cluster, xcolumn, ycolumn):
    # Black removed and is used for noise instead.
    unique_labels = set(cluster)
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]
        class_member_mask = (cluster == k)
        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=5, label=k)
        plt.legend()
    plt.title("Clustering Model")
    plt.xlabel(xcolumn)
    plt.ylabel(ycolumn)
    plt.show()


def BoxPlot(Cluster, columnPlot):
    ClusterSet = set(Cluster)
    for i in columnPlot:
        sns.boxplot(Column[-1], i, data=data)
        plt.xlabel(Column[-1])
        plt.ylabel(i)
        plt.show()

data = pd.read_csv("ClusterResult.csv")

Column = [i for i in data]
ColumnIndex = [8, 10, 14, -2]

for i in range(len(ColumnIndex)):
    for j in range(i):
        X = np.array(data[[Column[ColumnIndex[i]], Column[ColumnIndex[j]]]])
        cluster = np.array(data[Column[-1]])
        
        plt.clf()
        ClusterPlot(X, cluster, Column[ColumnIndex[i]], Column[ColumnIndex[j]])

L = [Column[i] for i in ColumnIndex]

BoxPlot(data[Column[-1]], L)