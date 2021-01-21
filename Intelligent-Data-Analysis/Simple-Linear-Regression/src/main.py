import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import sqrt


def verdict(r):
    print('Verdict: ', end='')
    if r > 0.6 and r < 1 :
        print('High positive correlation ')
    elif r >= 0.3 and r <= 0.6 :
        print('Middle positive correlation ')
    elif r > -0.3 and r < 0.3 :
        print('No correlation ')
    elif r >= -0.6 and r <= -0.3 :
        print('Average negative correlation ')
    elif r > -1 and r < -0.6 :
        print('High negative correlation ')



def main():
    data = pd.read_csv('resourses/potato.txt', names=['X', 'Y'])
    X = data.iloc[:, 0].values
    Y = data.iloc[:, 1].values 

    average_X = np.mean(X)
    average_Y = np.mean(Y)
    sum_of_multiplication = sum(map(lambda x, y: x*y, X, Y))
    sum_X = np.sum(X)
    sum_Y = np.sum(Y)
    quadratic_sum_X = sum(map(lambda value: value*value, X))
    quadratic_sum_Y = sum(map(lambda value: value*value, Y))
    b1 = round((sum_of_multiplication*10 - sum_X*sum_Y) / (quadratic_sum_X*10 - sum_X**2), 2)
    b0 = average_Y - b1*average_X
    print(f'y = {b0} + ({b1}) * x')

    plt.scatter(X, Y, color='black')
    plt.plot(X, [b1*value + b0 for value in X], color='red')

    m = 1
    rms_error = 0
    for i in range(X.shape[0]) :
        rms_error = rms_error + (Y[i] - b0 - b1*X[i])**2
    rms_error = round(rms_error / (X.shape[0] - m - 1), 1)
    standart_error = round(sqrt(rms_error), 1)
    print('Standart error: ', standart_error)

    Q = 0
    for i in range(X.shape[0]) :
        Q = Q + (Y[i] - average_Y)**2
    print('Q: ', Q)

    Qr = 0
    for i in range(X.shape[0]) :
        Qr = Qr + (b0 + b1*X[i] - average_Y)**2
    print('Qr: ', Qr)

    Qe = 0
    for i in range(X.shape[0]) :
        Qe = Qe + (Y[i] - b0 - b1*X[i])**2
    print('Qe: ', Qe)

    determination = round(Qr/Q, 4)
    print('Determination: ', determination)

    n = X.shape[0]
    r = (sum_of_multiplication - sum_X*sum_Y/n) / ((quadratic_sum_X - sum_X**2 / n)**(1/2) * (quadratic_sum_Y - sum_Y**2 / n)**(1/2))
    r = round(r, 4)
    print('Correlation: ', r)

    verdict(r)
    plt.show()


if __name__ == '__main__':
    main()