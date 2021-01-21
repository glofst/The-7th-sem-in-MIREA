import numpy as np

class RBFNetwork:
    def __init__(self, neurons_count, sigma=1.0):
        self.neurons_count = neurons_count
        self.sigma = sigma
        self.weights = None
        self.centers = None


    def calculate_weights(self, X, Y):
        self.centers = self._choose_centers(X)
        G = self._calculate_matrix(X)
        self.weights = np.dot(np.linalg.pinv(G), Y)


    def prediction(self, X):
        G = self._calculate_matrix(X)
        predictions = np.dot(G, self.weights)
        return predictions


    def _calculate_matrix(self, X):
        G = np.zeros((len(X), self.neurons_count))
        for data_point_arg, data_point in enumerate(X):
            for center_arg, center in enumerate(self.centers):
                G[data_point_arg, center_arg] = self._gauss_function(
                        center, data_point)
        return G


    def _choose_centers(self, X):
        random_args = np.random.choice(len(X), self.neurons_count)
        centers = X[random_args]
        return centers


    def _gauss_function(self, center, data_point):
        return np.exp(-self.sigma*np.linalg.norm(center-data_point)**2)