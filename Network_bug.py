from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np
import pickle, math, time

class Network:
	def __init__(self):
		self.reg = LinearRegression()
		self.last_accuracy = '0%'

	def __sigmoid(self, x):
		return 1/(1+math.exp(-x))

	def train(self, x, y):
		start = time.time()
		# xa = []
		# for v in x.values:
		# 	b = 0
		# 	b1 = list(filter(lambda x: x <= 1, v))
		# 	b2 = list(filter(lambda x: x > 1, v))
		# 	for n in b2:
		# 		b += n
		# 	xa.append(b1.count(1) + b)
		# xn = np.array(np.array(xa))
		# yn = np.array(np.array(y.values))
		# weights = list(map(self.__sigmoid, list(yn/xn)))

		# self.reg.fit(x, y, sample_weight=weights)
		self.reg.fit(x,y)
		print(f'Time for training: {time.time() - start}')

	def save(self, path='network.sav'):
		with open(path, 'wb') as f:
			pickle.dump(self.reg, f)

	def load(self, path='network.sav'):
		with open(path, 'rb') as f:
			self.reg = pickle.load(f)

	def tts(self, x,y, *args, **kwargs):
		return train_test_split(x, y, *args, **kwargs)

	def test(self, x, y=[]):
		pred = list(map(lambda x: abs(x), self.reg.predict(x)))
		# pred = self.reg.predict(x)

		if len(y) > 0:
			self.last_accuracy = f'{(r2_score(y, pred)*100):.3f}%'
			print(f'R^2 score: {self.last_accuracy}')
		return pred
