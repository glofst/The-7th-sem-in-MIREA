import time
from math import sqrt, exp
import random
import numpy as np
import matplotlib.pyplot as plt

class SOMNetwork():
	def __init__(self, input_dim, dim=10, sigma=None, learning_rate=0.1, min_learning_rate=0.01, tay2=1000):
		if not sigma:
			sigma = dim / 2.0
		# constants
		self.dim = dim
		self.learning_rate = learning_rate
		self.min_learning_rate = min_learning_rate
		self.sigma = sigma
		self.tay1 = 1000/np.log(sigma)
		self.minsigma = sigma * np.exp(-1000/(1000/np.log(sigma)))
		self.tay2 = tay2
		self.input_dim = input_dim
		# iteration number
		self.n = 0
		# weights net of neurons
		self.w = [[random.uniform(0, 1) for i in range(input_dim)] for j in range(dim*dim)]


	def __competition(self, input):
		neurons_dists = []
		for neuron in self.w:
			sum = 0
			for i in range(self.input_dim):
				sum += pow(abs(input[i] - neuron[i]), 2)
			neurons_dists.append(sqrt(sum))
		return neurons_dists.index(min(neurons_dists))


	def training_op(self, x):
		win_index = self.__competition(x)
		win_coords = [
		 	win_index % self.dim,
		 	win_index // self.dim
		]
		sigma = self.sigma * exp(-self.n * self.tay1)
		if sigma < self.minsigma:
			sigma = self.minsigma

		lr = self.learning_rate * exp(-self.n / self.tay2)
		if lr < self.min_learning_rate:
			lr = self.min_learning_rate

		for neuron in self.w:
			neuron_coords = [
				self.w.index(neuron) % self.dim, 
				self.w.index(neuron) // self.dim
			]
			coop_dist = sqrt(sum([
				pow(neuron_coords[i] - win_coords[i], 2)
				for i in range(len(win_coords))
			]))
			tnh = exp(-(coop_dist ** 2) / (2 * (sigma ** 2)))

			for i in range(self.input_dim):
				neuron[i] += lr * tnh * (x[i] - neuron[i])


	def next_iteration(self):
		self.n += 1
			

def tester():
	tests_number = 300000
	tests_dim = 3
	som_dim = 100

	som = SOMNetwork(input_dim=tests_dim, dim=som_dim, sigma=3)
	test_data = np.random.uniform(0, 1, (tests_number, tests_dim))

	img1 = np.reshape(som.w, (som_dim, som_dim, tests_dim))
	plt.figure(1)
	plt.subplot(121)
	plt.imshow(img1)

	for i, test in enumerate(test_data):
		if i % 100 == 0:
		 	print('iter: ', i)
		som.training_op(test)
		som.next_iteration()

	img2 = np.reshape(som.w, (som_dim, som_dim, tests_dim))
	plt.subplot(122)
	plt.imshow(img2)
	plt.show()		

tester()
