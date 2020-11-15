import pandas as pd
#import datetime as dt
#from sklearn.cluster import KMeans
#import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
from matplotlib.gridspec import GridSpec

def feature_EDA(dataframe, feat1, feat2):
    data = dataframe[[feat1, feat2]]
    feat2_count = feat2 + ' Count'
    data = data.groupby([feat1]).agg({feat2: 'count'}).sort_values(feat2, ascending=False).reset_index().rename(
        columns={feat2: feat2_count})
    print(data)
    print(data.describe())

    plt.figure(figsize=(30, 10))
    plt.bar(data[feat1], data[feat2_count])
    plt.show()

# Recency scoring: higher score less concern
def r_score(var, p,d):
    if var <= d[p][0.25]:
        return 1
    elif var <= d[p][0.50]:
        return 2
    elif var <= d[p][0.75]:
        return 3
    else:
        return 4

# Frequency scoring: higher score higher concern

def f_score(var,p,d):
    if var <= d[p][0.25]:
        return 4
    elif var <= d[p][0.50]:
        return 3
    elif var <= d[p][0.75]:
        return 2
    else:
        return 1

def RF_Modeling(df):
    latest_date = df['CrimeDate'].max()
    RF_data = df.groupby('CrimeCode').agg({'CrimeDate': lambda x: (latest_date - x.max()).days,
                                           'CrimeCode': 'count'})

    RF_data.rename(columns={'CrimeDate': 'Recency',
                            'CrimeCode': 'Frequency'}, inplace=True)

    #RF_data

    i = 0
    fig = plt.figure(constrained_layout=True, figsize=(10, 5))
    gs = GridSpec(1, 2, figure=fig)

    col = ['red', 'blue']

    for var in list(RF_data):
        plt.subplot(gs[0, i])
        sns.distplot(RF_data[var], color=col[i])
        plt.title('Skewness : ' + round(RF_data[var].skew(), 2).astype(str))
        i = i + 1
    #Recency and Frequency set up
    RF_data = RF_data[RF_data.Recency <= 730]
    RF_data = RF_data[RF_data.Frequency <= 1000]

    # Visualize Recency and Frequency Distributions
    i = 0
    fig = plt.figure(constrained_layout=True, figsize=(10, 5))
    gs = GridSpec(1, 2, figure=fig)

    col = ['red', 'blue']

    for var in list(RF_data):
        plt.subplot(gs[0, i])
        sns.distplot(RF_data[var], color=col[i])
        plt.title('Skewness : ' + round(RF_data[var].skew(), 2).astype(str))
        i = i + 1

    # Segmentation of data based on quartile ranges from our .describe() output
    quantiles = RF_data.quantile(q=[0.25, 0.5, 0.75])
    quantiles.to_dict()

    RF_data['r_score'] = RF_data['Recency'].apply(r_score, args=('Recency', quantiles,))
    RF_data['f_score'] = RF_data['Frequency'].apply(f_score, args=('Frequency', quantiles,))

    RF_data['RF_Group'] = RF_data['r_score'].astype(str) + RF_data['f_score'].astype(str)

    # Score
    RF_data['RF_Score'] = RF_data[['r_score', 'f_score']].sum(axis=1)

    concern_level = ['High Concern', 'Mild Concern', 'Some Concern', 'Least Concern']

    cuts = pd.qcut(RF_data['RF_Score'], q=4, labels=concern_level)
    RF_data['RF_Concern_Level'] = cuts.values

    print(RF_data.head())

    fig = px.scatter(RF_data, x='Recency', y='Frequency', color='RF_Concern_Level')
    fig.show()

def KM_Modeling(df):
    KM_data = df.groupby(['Neighborhood', 'Description'])['Description'].count().unstack()

    KM_data = KM_data.fillna(0)

    from sklearn import preprocessing
    KM_standardized = preprocessing.scale(KM_data)
    print(KM_standardized)
    KM_standardized = pd.DataFrame(KM_standardized)

    from sklearn.cluster import KMeans
    #%matplotlib inline

    plt.figure(figsize=(10, 8))
    wcss = []
    for i in range(1, 10):
        kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
        kmeans.fit(KM_standardized)
        wcss.append(kmeans.inertia_)

    plt.plot(range(1, 10), wcss)
    plt.title('The Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()

    # I think here we want to pick 5 or 7?

    kmeans = KMeans(n_clusters=4, init='k-means++', random_state=42)
    y_kmeans = kmeans.fit_predict(KM_standardized)

    y_kmeans1 = y_kmeans + 1
    cluster = list(y_kmeans1)

    KM_data['cluster'] = cluster

    kmeans_mean_cluster = pd.DataFrame(round(KM_data.groupby('cluster').mean(), 1))
    kmeans_mean_cluster

    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=KM_data['Violent_Crime'], y=KM_data['Robbery'], hue=y_kmeans1)
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=KM_data['Auto_Crime'], y=KM_data['Violent_Crime'], hue=y_kmeans1)
    plt.show()