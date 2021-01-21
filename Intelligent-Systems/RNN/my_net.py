import random
import math
from my_util import print_picture, picture_size

def cmp(x, y):
    if x == y:
        return 0
    if x < y:
        return -1
    if x > y:
        return 1

class HopfieldNeuroNet:

    def __init__(self, draw_steps=False):
        self.draw_steps = draw_steps
        self.pictures = []  # образы, которым обучена сеть
        self.neurons = picture_size * picture_size  # количество нейронов
        self.W = [[0 for i in range(self.neurons)] for k in range(self.neurons)]      # матрица весовых коэффицентов
        self.max_iters = 200 # максимальное число безрезультатных итераций
        self.junk_iter = 0 # текущая безрезультатная итерация


    # Обучение сети образу
    def teach(self, picture):
        self.pictures.append(picture) 
        for i in range(self.neurons):
            for j in range(self.neurons):
                if i == j:
                    self.W[i][j] = 0
                else:
                    self.W[i][j] += picture[i] * picture[j]


    # Распознать изменённый образ
    def recognize(self, picture):
        self.Y = picture
        iter = 0
        # пока не совпадёт с одним из известных...
        while(self.pictures.count(self.Y) == 0):
            self.recstep()
            iter += 1
            # ... или количество безрезультатных итераций не истечёт
            if self.junk_iter >= self.max_iters:
                return (False, self.Y, iter)
        return True, self.Y, iter


    # Шаг распознования.
    # Случайно выбирается нейрон для обновления 
    def recstep(self):
        r = random.randrange(0, self.neurons, 1)
        net = 0

        for i in range(self.neurons):
            net += self.Y[i] * self.W[i][r]
            
        signet = cmp(net, 0)
        if signet != self.Y[r]: # заменяем текущий нейрон
            self.Y[r] = signet
            if self.draw_steps:
                print(f'Picture on {self.junk_iter}')
                print_picture(self.Y)
            self.junk_iter = 0
        else:
            self.junk_iter += 1 
