# Delta Rule
# Trying to build source sin(x) by displaced dots


from random import uniform, choice
from math import sin, cos
import matplotlib.pyplot as plt
from numpy import arange
 

plotSize = 10           # x is [-10, 10], y is [-10, 10]
displacedFactor = 1.0   # How mach shifts dots from their original positions
dotsNumber = 20         # Number of neurons 
maxIterations = 10000
rate = 0.0001           # Educational speed


def proceed(x, k, c):
    return k * sin(x) + c


def genReferencePlot():
    c = uniform(-plotSize, plotSize)
    k = uniform(-plotSize, plotSize)
    return k, c
    

class Dot:

    def __init__(self, x, k, c):
        self.x = x
        self.c = c
        self.k = k

        self.y = proceed(x, k, c)


def genRefPlotDots(k, c, rand):
    return [
        Dot(
            i, 
            k + uniform(-displacedFactor, displacedFactor) * rand, 
            c + uniform(-displacedFactor, displacedFactor) * rand 
        ) for i in arange(-plotSize, plotSize, plotSize/dotsNumber)
    ]

 
if __name__ == '__main__':
    k = uniform(-plotSize, plotSize)
    c = uniform(-plotSize, plotSize)

    refK, refC = genReferencePlot()
    dots = genRefPlotDots(refK, refC, 1)
    plt.grid()
    plt.plot(
        [dot.x for dot in dots], 
        [dot.y for dot in dots],
        'o',
        color = 'black'
    )

    for i in range(maxIterations):
        for dot in dots:
            out = proceed(dot.x, k, c)
            delta = dot.y - out
            k += delta*rate*dot.x
            c += delta*rate


    print(f'{refK} * sin(x) + {refC}')
    print(f'{k} * sin(x) + {c}')
    newplot = genRefPlotDots(k, c, 0)
    plt.plot(
        [dot.x for dot in newplot], 
        [dot.y for dot in newplot],
        color = 'red'
    )
    plt.show()

