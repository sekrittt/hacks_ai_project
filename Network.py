import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np
import os, pickle, csv, sys, datetime, re
from DataLoader import DataLoader
from get_filters import get_filters

colors = [
	'цвет морской волны',
	'аквамарин',
	'лазурный',
	'бежевый',
	'бисквитный',
	'черный',
	'синий',
	'сине-фиолетовый',
	'коричневый',
	'малиновый',
	'голубой',
	'темно-синий',
	'темно-голубой',
	'темно-золотой',
	'темно-серый',
	'темно-серый',
	'темно-зеленый',
	'темный хаки',
	'темно-пурпурный',
	'темно-оливковый',
	'темно-оранжевый',
	'темно-зеленый',
	'темно-красный',
	'темно-лососевый',
	'темно-зеленый',
	'темно-зеленый',
	'темно-зеленый',
	'темно-серый',
	'темно-сланцевый',
	'темно-бирюзовый',
	'темно-фиолетовый',
	'темно-розовый',
	'темно-синий',
	'тускло-серый',
	'тусклый',
	'фуксия',
	'золото',
	'золотарник',
	'серый',
	'серый',
	'зеленый',
	'зелено-желтый',
	'медвяная роса',
	'ярко-розовый',
	'индийский красный',
	'индиго',
	'слоновая кость',
	'хаки',
	'лаванда',
	'лимонный шифон',
	'светло-голубой',
	'светло-коралловый',
	'светло-голубой',
	'светло-золотой',
	'светло-серый',
	'светло-серый',
	'светло-зеленый',
	'светло-розовый',
	'светло-лососевый',
	'светло-зеленый',
	'светло-голубой',
	'светло-серый',
	'светло-серый',
	'светло-стальной',
	'светло-желтый',
	'лайм',
	'лимонно-зеленый',
	'льняной',
	'пурпурный',
	'бордовый',
	'средне-аквамарин',
	'средне-синий',
	'бледно-зеленый',
	'пале-бирюзовый',
	'розовый',
	'пурпурный',
	'красный',
	'розово-коричневый',
	'королевский синий',
	'песочно-коричневый',
	'морская зелень',
	'морская ракушка',
	'серебристый',
	'небесно-голубой',
	'весенне-зеленый',
	'томатный',
	'бирюзовый',
	'фиолетовый',
	'пшеничный',
	'белый',
	'дымчатый',
	'желтый',
	'желто-зеленый'
]



class Network:
	def __init__(self):
		self.reg = LinearRegression(normalize=True)
		self.last_accuracy = '0%'

	def train(self, x, y):
		self.reg.fit(x, y)

	def save(self, path='network.sav'):
		with open(path, 'wb') as f:
			pickle.dump(self.reg, f)

	def load(self, path='network.sav'):
		with open(path, 'rb') as f:
			self.reg = pickle.load(f)

	def tts(self, x,y, *args, **kwargs):
		return train_test_split(x, y, *args, **kwargs)

	def test(self, x, y=[]):
		pred = self.reg.predict(x)
		pred = list(map(lambda i: abs(int(i)), pred))

		if len(y) > 0:
			self.last_accuracy = f'{(r2_score(y, pred)*100):.3f}%'
			print(f'Accuracy: {self.last_accuracy}')
		return pred


if __name__ == "__main__":
	os.system('clear')

	net = Network()
	loader = DataLoader()
	filters_1 = get_filters('train.csv')
	filters_2 = get_filters('data.csv')
	filters = []

	for filt in filters_1:
		if filt in filters_2:
			filters.append(filt)
	X, y, y_indexes = loader.load_data('train.csv', ["description","object_img",'id'], filters)
	X_train, X_test, y_train, y_test = net.tts(X, y, test_size=0.3, random_state=42, shuffle=False)

	# if os.path.exists('network.sav'):
	# 	net.load()
	# else:
	os.system('clear')
	net.train(X, y)

	# print(X_test.idxmin())
	# print(list(y.index))

	# net.save()


	net.test(X_test, y_test)

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
			f.write(f'{key},{value}\n')
	# print(data)
