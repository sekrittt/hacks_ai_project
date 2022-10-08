import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np
import os, pickle, csv, datetime, re, math
from DataLoader import DataLoader
from get_filters import get_filters

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

	def test(self, x, y=[]):
		pred = list(map(lambda x: abs(x), self.reg.predict(x)))

		if len(y) > 0:
			self.last_accuracy = f'{(r2_score(y, pred)*100):.3f}%'
			print(f'R^2 score: {self.last_accuracy}')
		return pred


if __name__ == "__main__":
	os.system('cls||clear')

	net = Network()
	loader = DataLoader()
	filters_1 = get_filters('train.csv')
	filters_2 = get_filters('data.csv')
	filters = [*filters_1, *filters_2]

	# for filt in filters_1:
	# 	if filt in filters_2:
	# 		filters.append(filt)
	X, y, y_indexes = loader.load_data('train.csv', ["description","object_img",'id'], filters)
	X_train, X_test, y_train, y_test = net.tts(X, y, test_size=0.3, random_state=42, shuffle=False)

	# if os.path.exists('network.sav'):
	# net.load()
	# else:
	os.system('cls||clear')
	net.train(X, y)

	# print(X_test.idxmin())
	# print(list(y.index))

	# net.save()

	# net.test(X_test, y_test)

	test_X, test_y, test_y_indexes = loader.load_data('data.csv', ["description",'id'], filters)

	p = net.test(test_X)
	# print(p)
	data = {}
	with open('data.csv', 'r', encoding='utf-8') as f:
		reader = csv.reader(f, delimiter=',', quotechar='"')
		for i, row in enumerate(reader, start=-1):
			if i == -1:
				continue
			if i < len(p):
				data[row[0]] = p[i]
			else:
				break
	d = re.sub(r'[\-\:\.]', '_', re.sub(r'\s', 'T', str(datetime.datetime.today())))
	with open(f'solution_{d}.csv', 'w', encoding='utf-8') as f:
		f.write('id,object_img\n')
		for key, value in list(data.items()):
			f.write(f'{key},{round(value)}\n')
	# print(data)
