import numpy as np

def f(x):
    return 1 / (1 + np.exp(-x))
    
input_data = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [1, 1, 1],
    [1, 0, 0]
])
teacher_data = np.array([[1, 1, 0, 1]]).T
epsilon = 0.01
learning_rate = 0.1
max_iter = 10000
amount_of_neurons = 10


def main():
    M, N = np.shape(input_data)
    hidden_weights = 2 * np.random.random((amount_of_neurons, N)) - 1
    output_weights = 2 * np.random.random((1, amount_of_neurons)) - 1

    counter = 0
    error = epsilon + 1
    output = np.zeros((1, 4))
    while error > epsilon and counter < max_iter:
        counter += 1
        for i in range(M):
            l0 = input_data[i]
            l1 = np.array([f(x) for x in np.dot(l0, hidden_weights.T)])
            l2 = f(np.dot(l1, output_weights.T))

            l2_sigma = l2 * (1 - l2) * (teacher_data[i] - l2) 
            l1_sigma = l1 * (1 - l1) * output_weights * l2_sigma

            output_weights += learning_rate * l2_sigma * l1
            hidden_weights += learning_rate * np.array([l0 * x for x in l1_sigma[0]])

            output[0, i] = l2

        error = np.sqrt(np.sum(np.array([pow(x, 2) for x in (teacher_data - output.T)]))/(M - 1))

    print('Teacher data: ', teacher_data.T)
    print('Output: ', output)
    print('\nError value: ', error)


if __name__ == '__main__':
    main()
