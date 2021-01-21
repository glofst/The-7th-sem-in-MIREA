import random as rd
import numpy as np
import matplotlib.pyplot as plt


def find_centroids(X, clusters, data_size, max_iters):
    centroids = np.array([]).reshape(2,0)
    for i in range(clusters):
        rand = rd.randint(0, data_size-1)
        centroids = np.c_[centroids, X[rand]]

    Y = {}
    for i in range(max_iters):
        euclidian_distance = np.array([]).reshape(data_size, 0)
        for k in range(clusters):
            tmp_distance = np.sum((X - centroids[:, k])**2, axis = 1)
            euclidian_distance = np.c_[euclidian_distance, tmp_distance]
        C = np.argmin(euclidian_distance, axis = 1) + 1

        for k in range(clusters):
            Y[k + 1] = np.array([]).reshape(2, 0)
        for i in range(data_size):
            Y[C[i]] = np.c_[Y[C[i]], X[i]]
        for k in range(clusters):
            Y[k + 1] = Y[k + 1].T
        for k in range(clusters):
            centroids[:, k] = np.mean(Y[k + 1], axis = 0)
    
    return Y, centroids


def build_plots(X, Y, centroids, clusters):
    plt.subplot(121)
    plt.scatter(X[:, 0], X[:, 1], c = 'black', label = 'raw data')
    plt.legend(loc='upper right')
    plt.title('Raw Data')

    color=['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'orange', 'purple', 'pink']
    plt.subplot(122)
    for k in range(clusters):
        plt.scatter(Y[k + 1][:, 0], Y[k + 1][:, 1], c = color[k], label = 'Cluster ' + str(k + 1))
    plt.scatter(centroids[0, :], centroids[1, :], s = 50, c = 'black',label = 'Centroid')
    plt.legend(loc='upper right')
    plt.title('Clustered Data')
    plt.show()


def gen_raw_data(data_size):
    return np.random.randint(100, size=(data_size, 2))


def main():
    data_size = 200
    X = gen_raw_data(data_size)
    clusters = int(input('Choose number of clusters (4-9): '))
    max_iters = 100

    Y, centroids = find_centroids(X, clusters, data_size, max_iters)
    build_plots(X, Y, centroids, clusters)

    
if __name__ == '__main__':
    main()