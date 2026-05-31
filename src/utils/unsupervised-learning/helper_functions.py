import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import multivariate_t, multivariate_normal
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples, adjusted_rand_score, jaccard_score
from sklearn.base import clone
from sklearn.utils import check_random_state
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

import warnings
warnings.simplefilter('ignore')

def hening_stability(X: np.ndarray | pd.DataFrame, estimator, y_true: np.ndarray, K: int = 2, B: int = 10, random_state: int | None = None) -> np.ndarray:
    '''
    Computes the Hening stability index for a clustering model.

    Parameters:
    -----------
    X: np.ndarray | pd.DataFrame - Data to be clustered.
    estimator: object - Clustering model to be used.
    y_true: np.ndarray - Labels from the original clusters.
    K: int - Number of clusters to be used.
    B: int - Number of bootstrap samples to be used.
    random_state: int | None - Random seed to be used.
    '''
    # Initialize random number generator
    rng = np.random.RandomState(random_state)

    if isinstance(X, np.ndarray):
        col = [f'X{i+1}' for i in np.arange(X.shape[1])]
        X = pd.DataFrame(X, columns= col)
    
    y_true = pd.Series(y_true, index=X.index)

    # Initialize lists to store labels and indices
    jaccard = np.zeros(shape=(B, K))

    # Loop over the number of iterations
    for b in np.arange(B):
        # Draw bootstrap samples and store indices
        sample = rng.randint(low=0, high=X.shape[0], size=X.shape[0])

        # Clone the estimator to make sure that we are fitting fresh models
        estimator = clone(estimator)

        # Randomize estimator if possible
        if hasattr(estimator, 'random_state'):
            estimator.random_state = random_state
        
        # Create a bootstrap sample
        X_bootstrap = X.iloc[sample, :]

        # Fit the clustering model
        estimator.fit(X_bootstrap)
        y_pred = pd.Series(estimator.labels_, index=X.index)

        max_jaccard = []
        # Store clustering outcome using original indices
        for i in np.arange(K):
            jaccard_scores = []
            for j in np.arange(K):
                intersect = np.intersect1d(y_true.index[y_true == j], y_pred.index[y_pred == i])
                union = np.union1d(y_true.index[y_true == j], y_pred.index[y_pred == i])
                
                jaccard_scores.append(len(intersect) / len(union))
            
            max_jaccard.append(np.max(jaccard_scores))
        
        jaccard[b] = max_jaccard

    return np.mean(jaccard, axis=0)


def plot_silhouette(X: np.ndarray, y: np.ndarray, ax=None, figsize: tuple = (10, 6)) -> None:
    '''
    Silhouette plot for a clustering model.

    Parameters:
    -----------
    X: np.ndarray - Data to be clustered.
    y: np.ndarray - Labels from the clustering model.
    '''
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    
    # Compute silhouette scores
    silhouette_values = silhouette_samples(X, y)

    n_clusters = len(np.unique(y))
    y_lower, y_upper = 0, 0
    yticks = []
    colors = ['#E65983', '#2D3846', '#F6AE2D', '#3C7A89', '#F2F4F7', '#A7C5EB', '#E7ECEF', '#F4D35E', '#EE964B']

    for i in np.arange(n_clusters):
        cluster_silhouette_vals = silhouette_values[y == i]
        cluster_silhouette_vals.sort()
        y_upper += len(cluster_silhouette_vals)
        ax.barh(np.arange(y_lower, y_upper), cluster_silhouette_vals, edgecolor='white', height=1, color=colors[i])
        yticks.append((y_lower + y_upper) / 2)
        y_lower += len(cluster_silhouette_vals)

    ax.axvline(x=np.mean(silhouette_values), color="black", linestyle="--")
    ax.set_yticks(yticks, [f'Cluster {i}' for i in np.arange(n_clusters)])
    ax.set_xlabel('Silhouette Coefficient')
    ax.set_title('Silhouette Plot', loc='left', fontdict={'fontsize': 16, 'fontweight': 'bold'})

def plot_clusters(data: pd.DataFrame, labels: np.ndarray, title: str = None, interactive: bool = True) -> px.scatter:
    '''
    Plots clusters using the first two principal components of the data.

    Parameters:
    -----------
    data: pd.DataFrame - Data to be plotted.
    labels: np.ndarray - Labels from the clustering model.
    '''

    pca = PCA(n_components=2).fit(data)
    columns = [f'PC{i + 1} ({pca.explained_variance_ratio_[i] * 100:.2f}%)' for i in np.arange(2)]
    pca = pca.transform(data)
    pca = pd.DataFrame(pca, columns=columns)

    if interactive:
        figure = px.scatter(
            data,
            x=data.columns[0],
            y=data.columns[1],
            color=labels.astype(str),
            color_discrete_map={'0': '#E65983', '1': '#2D3846', '2': '#3D8791', '3': '#2D3846'},
            size=[1] * data.shape[0],
        )
        figure.update_layout(
            title=title,
            title_font=dict(size=16, family='Arial', color='black', weight='bold'),
            xaxis_title=data.columns[0],
            yaxis_title=data.columns[1],
            plot_bgcolor='white',
            yaxis=dict(showgrid=True, gridcolor='LightGray', showline=True, linecolor='Black', zeroline=True, zerolinecolor='LightGray'),
            xaxis=dict(showgrid=True, gridcolor='LightGray', showline=True, linecolor='Black', zeroline=True, zerolinecolor='LightGray'),
        )
        figure.show()
    else:
        fig, ax = plt.subplots(figsize=(12, 6))

        ax.scatter(pca[columns[0]], pca[columns[1]], c=labels, cmap='viridis', s=50, alpha=0.7)
        ax.set_xlabel(columns[0])
        ax.set_ylabel(columns[1])
        ax.set_title(title, loc='left', fontdict={'fontsize': 16, 'fontweight': 'bold'})
        ax.legend()
        plt.show()

def knn_displot(data: np.ndarray | pd.DataFrame, k: int = 3, eps: int = 1) -> px.scatter:
    '''
    Plots a displot of the k-nearest neighbors distances.

    Parameters:
    -----------
    data: pd.DataFrame - Data to be used.
    k: int - Number of nearest neighbors to be used.
    eps: int - Epsilon value to be used.
    '''
    nn = NearestNeighbors(n_neighbors=k).fit(data)
    distances, indices = nn.kneighbors(data)
    distances = np.sort(distances[:, k-1])

    df = pd.DataFrame({'X': np.arange(0, len(distances)), 'Y': distances})

    # Fit the nearest neighbors model
    figure = px.scatter(df, x='X', y='Y')
    figure.update_layout(
        title='kNN-Distance',
        title_font=dict(size=16, family='Arial', color='black', weight='bold'),
        yaxis_title='kNN-Distance',
        plot_bgcolor='white',
        yaxis=dict(showgrid=True, gridcolor='LightGray', showline=True, linecolor='Black', zeroline=True, zerolinecolor='LightGray'),
        xaxis=dict(showgrid=True, gridcolor='LightGray', showline=True, linecolor='Black', zeroline=True, zerolinecolor='LightGray'),
    )
    figure.add_hline(
        y=eps,
        line=dict(color='black', width=2, dash='dash')
    )
    figure.show()

def plot_clusters3d(data: pd.DataFrame, labels: np.ndarray, title: str = None) -> px.scatter_3d:
    pca = PCA(n_components=3).fit(data)
    l = [f'PC{i + 1} ({v * 100:.3}%)' for (i, v) in enumerate(pca.explained_variance_ratio_)]
    pca = pca.transform(data)

    # Existing scatter plot
    figure = px.scatter_3d(
        x=pca[:, 0],
        y=pca[:, 1],
        z=pca[:, 2],
        color=labels.astype(str),
        color_discrete_map={'0': '#E65983', '1': '#2D3846', '2': '#3D8791', '3': '#2D3846'},
        size=[1] * len(pca[:, 0]),
    )

    # Update layout
    figure.update_layout(
        title=title,
        title_font=dict(size=16, family='Arial', color='black', weight='bold'),
        scene=dict(
            xaxis_title=l[0],
            yaxis_title=l[1],
            zaxis_title=l[2]
        ),
        plot_bgcolor='white',
        yaxis=dict(showgrid=True, gridcolor='LightGray', showline=True, linecolor='Black', zeroline=True, zerolinecolor='LightGray'),
        xaxis=dict(showgrid=True, gridcolor='LightGray', showline=True, linecolor='Black', zeroline=True, zerolinecolor='LightGray'),
    )

    figure.update_traces(marker=dict(line=dict(width=0)))
    figure.show()

def plot_data(data: pd.DataFrame, title: str = None, interactive: bool = True) -> px.scatter:
    '''
    Plots the data using the first two principal components.

    Parameters:
    -----------
    data: pd.DataFrame - Data to be plotted.
    title: str - Title of the plot.
    '''
    pca = PCA(n_components=2).fit(data)
    l = [f'PC{i + 1} ({v * 100:.3}%)' for (i, v) in enumerate(pca.explained_variance_ratio_)]
    pca = pca.transform(data)

    if interactive:
        figure = px.scatter(
            x=pca[:, 0],
            y=pca[:, 1],
            size=[1] * len(pca[:, 0]),
        )
        figure.update_layout(
            title=title,
            title_font=dict(size=16, family='Arial', color='black', weight='bold'),
            xaxis_title=l[0],
            yaxis_title=l[1],
            plot_bgcolor='white',
            yaxis=dict(showgrid=True, gridcolor='LightGray', showline=True, linecolor='Black', zeroline=True, zerolinecolor='LightGray'),
            xaxis=dict(showgrid=True, gridcolor='LightGray', showline=True, linecolor='Black', zeroline=True, zerolinecolor='LightGray'),
        )
        figure.show()
    else:
        fig, ax = plt.subplots(figsize=(12, 6))

        ax.scatter(pca[:, 0], pca[:, 1], s=50, alpha=0.7)
        ax.set_xlabel(l[0])
        ax.set_ylabel(l[1])
        ax.set_title(title, loc='left', fontdict={'fontsize': 16, 'fontweight': 'bold'})
        ax.legend()
        plt.show()

def centroids(X: np.ndarray | pd.DataFrame, labels: np.ndarray, K: int = 2) -> np.ndarray:
    '''
    Computes the centroids of a clustering model.

    Parameters:
    -----------
    X: np.ndarray | pd.DataFrame - Data to be clustered.
    labels: np.ndarray - Labels from the clustering model.
    K: int - Number of clusters to be used.
    '''
    if isinstance(X, pd.DataFrame):
        X = X.values

    centroids = np.zeros(shape=(K, X.shape[1]))
    for k in np.arange(K):
        centroids[k] = np.mean(X[labels == k], axis=0)

    return centroids

def cluster_diameter(X: np.ndarray, labels: np.ndarray, cluster_label: int, metric: str = 'euclidean') -> float:
    '''
    Computes the diameter of a cluster.

    Parameters:
    -----------
    X: np.ndarray - Data to be clustered.
    labels: np.ndarray - Labels from the clustering model.
    cluster_label: int - Cluster label to be used.
    metric: str - Distance metric to calculate the distance between clusters.
    '''
    cluster_points = X[labels == cluster_label]
    if len(cluster_points) < 2:
        return 0.0
    distances = cdist(cluster_points, cluster_points, metric=metric)
    return np.max(distances)


def dunn_index(X: np.ndarray | pd.DataFrame, labels: np.ndarray, K: int = 1, metric: str = 'euclidean') -> float:
    '''
    Computes the Dunn index for a clustering model.

    Parameters:
    -----------
    X: np.ndarray - Data to be clustered.
    labels: np.ndarray - Labels from the clustering model.
    K: int - Number of clusters to be used.
    metric: str - Distance metric to calculate the distance between clusters.
    '''
    # Compute the distance matrix
    if isinstance(X, pd.DataFrame):
        X = X.values

    # Compute the centroids of each cluster
    clusters = centroids(X, labels, K)

    # Compute the minimum inter-cluster distance
    dist = cdist(clusters, clusters, metric=metric)
    min_inter_cluster_distance = np.min(dist[np.nonzero(dist)])

    # Compute the diameter of each cluster
    diameters = np.array([cluster_diameter(X, labels, i) for i in np.arange(K)])
    max_intra_cluster_distance = np.max(diameters)

    return min_inter_cluster_distance / max_intra_cluster_distance
