from rbf_network import RBFNetwork
import numpy as np

sigma = 1.
test_data_number = 10
neurons_number = 100

test_data = np.linspace(0, 10, test_data_number)
reference_data = np.cos(test_data)

def main():
    neuronet = RBFNetwork(neurons_number, sigma)
    neuronet.calculate_weights(test_data, reference_data)
    y_pred = neuronet.prediction(test_data)
    error = np.sqrt(np.sum(np.array([pow(x, 2) for x in (reference_data - y_pred)]))/(test_data_number- 1))
    print('Reference data: ', np.vstack(reference_data).T)
    print('\nOutput: ', np.vstack(y_pred).T)
    print('\nError value: ', error)

if __name__ == '__main__':
    main()
