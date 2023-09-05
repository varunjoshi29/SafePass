import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np


def starttraining():
    dataset = pd.read_csv('actual_data.csv')

    #area_dummy = pd.get_dummies(X['AREA NAME'])
    ##crm_dummy = pd.get_dummies(X['Crm Cd Desc'])
    sex_dummy = pd.get_dummies(dataset['Vict Sex'])
    race_dummy = pd.get_dummies(dataset['Vict Descent'])
    #Concatenating the dummy variables to the original dataset

    X_dummy_set=pd.concat([dataset,sex_dummy, race_dummy],axis=1)
    #Deleting categorical variable from the dummy set
    del X_dummy_set['AREA NAME']
    del X_dummy_set['Crm Cd Desc']
    del X_dummy_set['Vict Sex']
    del X_dummy_set['Vict Descent']

    X = X_dummy_set
    X = X.drop(X.columns[0],axis=1)
    sc_X = StandardScaler()
    X = sc_X.fit_transform(X)
    #wcss = []
    #for i in range(1, 21):
    #    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    #    print(i)
    #    kmeans.fit(X)
    #    wcss.append(kmeans.inertia_)


    #plt.plot(range(1, 21), wcss)
    #plt.title('The Elbow Method')
    #plt.xlabel('Number of clusters')
    #plt.ylabel('WCSS')
    #plt.show()
    #a = 1

    kmeans = KMeans(n_clusters = 6, init = 'k-means++', random_state = 42)
    y_kmeans = kmeans.fit_predict(X)
    cluster_count = np.bincount(y_kmeans)
    dict = {}
    for i in range(len(cluster_count)):
        dict[i] = cluster_count[i]

    dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    final_dict = {}
    i = 5
    for key,value in dict:
        final_dict[key] = i
        i-=1

    return final_dict,kmeans
