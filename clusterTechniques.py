import sqlite3
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from bokeh.plotting import figure, ColumnDataSource, show
from bokeh.models import HoverTool
import numpy as np
import scipy as sp
from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq
import matplotlib.pyplot as plt

database = './database.sqlite'
conn = sqlite3.connect(database)
cur = conn.cursor()

playerTsnePos = {}

def bookehPlottsne(tmp):
    _tools = 'box_zoom,pan,save,resize,reset,tap,wheel_zoom'
    fig = figure(tools=_tools, title='t-SNE of Players (FIFA stats)', responsive=True,
             x_axis_label='Component 1', y_axis_label='Component 2')
    source = ColumnDataSource(tmp)
    hover = HoverTool()
    hover.tooltips=[('Player','@player_name'),]
    fig.scatter(tmp['comp1'], tmp['comp2'], source=source, size=8, alpha=0.6,
            line_color='red', fill_color='red')

    fig.add_tools(hover)

    show(fig)
    return True

def getPlayersData():
    query = """SELECT * FROM Player_Attributes a
               INNER JOIN (SELECT player_name, player_api_id AS p_id FROM Player) b ON a.player_api_id = b.p_id;"""

    drop_cols = ['id','date','preferred_foot',
                 'attacking_work_rate','defensive_work_rate']

    global players
    global stats_cols
    global cols

    players = pd.read_sql(query, conn)
    players['date'] = pd.to_datetime(players['date'])
    players = players[players.date > pd.datetime(2015,1,1)]
    players = players[~players.overall_rating.isnull()].sort('date', ascending=False)
    players = players.drop_duplicates(cols='player_api_id')
    players = players.drop(drop_cols, axis=1)
    players = players.fillna(0)

    cols = ['player_api_id','player_name','overall_rating','potential']
    stats_cols = [col for col in players.columns if col not in (cols)]

def tsneDimReduction(val):
    ss = StandardScaler()
    tmp = ss.fit_transform(players[stats_cols])
    model = TSNE(n_components=2, random_state=0)
    tsne_comp = model.fit_transform(tmp)

    i = 0
    for player_id in players['player_api_id']:
        playerTsnePos[player_id] = (tsne_comp[:,0][i], tsne_comp[:,1][i])
        i += 1
    tmp = players[cols]
    tmp['comp1'], tmp['comp2'] = tsne_comp[:,0], tsne_comp[:,1]
    tmp = tmp[tmp.overall_rating >= val]
    X = (tmp['comp1'], tmp['comp2'])

    X2 = np.array(tmp['comp1'])
    X2.ndim
    X2.shape
    Y2 = np.array(tmp['comp2'])
    Y2.ndim
    Y2.shape

    X1 = np.vstack((X2,Y2)).T
    X1.ndim
    X1.shape
    return tmp, X1

def clusteringKMeans(XVal):
    kmeans = KMeans(n_clusters=4, random_state=0)
    kmeans.fit(XVal)
    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_
    colors = ["g.","r.","y.","c.","b."]

    for i in range(len(XVal)):
        plt.plot(XVal[i][0],XVal[i][1],colors[labels[i]], markersize = 10)
    plt.scatter(centroids[:, 0], centroids[:, 1], marker="x", s=150, linewidth = 5, zorder = 10)
    return kmeans, plt, labels

def playerPredict_KMeans(player_id):
    kmeans1, plt, labels = clusteringKMeans(X10)

    X2 = np.array(playerTsnePos[player_id][0])
    X2.ndim
    X2.shape
    Y2 = np.array(playerTsnePos[player_id][1])
    Y2.ndim
    Y2.shape

    Xz = np.vstack((X2,Y2)).T
    Xz.ndim
    Xz.shape

    return kmeans1.predict(Xz)[0]

getPlayersData()
tmp, X10 = tsneDimReduction(80)

def clusteringDBSCAN(XVal):
    XVal = StandardScaler().fit_transform(XVal)

    db = DBSCAN(eps=0.3, min_samples=10).fit(XVal)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)


    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)

        xy = XVal[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=14)

        xy = XVal[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)

    return db

def DBscan(dbscan_model, player_id, metric=sp.spatial.distance.cosine):
    X2 = np.array(playerTsnePos[player_id][0])
    X2.ndim
    X2.shape
    Y2 = np.array(playerTsnePos[player_id][1])
    Y2.ndim
    Y2.shape

    X_new = np.vstack((X2,Y2)).T
    X_new.ndim
    X_new.shape
    # Result is noise by default
    y_new = np.ones(shape=len(X_new), dtype=int)*-1

    # Find a core sample closer than EPS
    for i, x_core in enumerate(dbscan_model.components_):
        if metric(X_new, x_core) < dbscan_model.eps:
            # Assign label of x_core to x_new
            y_new = dbscan_model.labels_[dbscan_model.core_sample_indices_[i]]
            break

    return y_new

def playerPredict_DBscan(player_id):
    db = clusteringDBSCAN(X10)
    return DBscan(db, player_id)
