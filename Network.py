from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np
import pickle,math

class Network:
	def __init__(self):
		self.reg = LinearRegression()
		self.last_accuracy = '0%'

	def __sigmoid(self, x):
		return 1/(1+math.exp(-x))

	def train(self, x, y):
		# xa = []
		# for v in x.values:
		# 	# b = np.array(v)
		# 	b = 0
		# 	b1 = list(filter(lambda x: x <= 1, v))
		# 	b2 = list(filter(lambda x: x > 1, v))
		# 	# # b1 = b1.dot(2**np.arange(b1.size)[::-1]) or 1
		# 	for n in b2:
		# 		b += n
		# 	xa.append(b1.count(1) + b)
		# 	# xa.append(b.dot(2**np.arange(b.size)[::-1]) or 1)
		# xn = np.array(np.array(xa))
		# yn = np.array(np.array(y.values))
		# weights = list(map(self.__sigmoid, list(yn/xn)))

		# self.reg.fit(x, y, sample_weight=weights)
		self.reg.fit(x,y)

	def save(self, path='network.sav'):
		with open(path, 'wb') as f:
			pickle.dump(self.reg, f)

	def load(self, path='network.sav'):
		with open(path, 'rb') as f:
			self.reg = pickle.load(f)

	def tts(self, x,y, *args, **kwargs):
		return train_test_split(x, y, *args, **kwargs)

	def __check_predict(self, x):
		x = abs(x)
		if x > 4000:
			x = 4000 * self.__sigmoid(x)
		return x

	def test(self, x, y=[]):
		pred = list(map(self.__check_predict, self.reg.predict(x)))

		if len(y) > 0:
			self.last_accuracy = f'{(r2_score(y, pred)*100):.3f}%'
			print(f'R^2 score: {self.last_accuracy}')
		return pred
