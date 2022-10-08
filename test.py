import datetime, math, os, re, csv
import numpy as np
from DataLoader import DataLoader
from get_filters import get_filters
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

loader = DataLoader()

filters_1 = get_filters('train.csv')
filters_2 = get_filters('data.csv')
filters = list(set([*filters_1, *filters_2]))

# for filt in filters_1:
#     if filt in filters_2:
#         filters.append(filt)

x, y, y_indexes = loader.load_data('train.csv', ["description","object_img",'id'], filters)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42, shuffle=False)

os.system('cls||clear')
def sigmoid(x):
    return 1/(1+math.exp(-x))
xa = []

for v in x.values:
    b = np.array(v)
    xa.append(b.dot(2**np.arange(b.size)[::-1]) or 1)

xn = np.array(np.array(xa))
yn = np.array(np.array(y.values))

weights = list(map(sigmoid, list(yn/xn)))

reg = LinearRegression()
reg.fit(x, y, sample_weight=weights)

pred = reg.predict(X_test)

c = 0
for g, img in enumerate(pred):
    if int(img) == list(y_test)[g]:
        print(f'{int(img)} == {list(y_test)[g]}')
        c += 1

print(f'R2 score: {r2_score(y_test, pred)}, count: {c}')

# test_X, test_y, test_y_indexes = loader.load_data('data.csv', ["description",'id'], filters)

# p = reg.predict(test_X)

# data = {}
# with open('data.csv', 'r', encoding='utf-8') as f:
#     reader = csv.reader(f, delimiter=',', quotechar='"')
#     for i, row in enumerate(reader, start=-1):
#         if i == -1:
#             continue
#         if i < len(p):
#             data[row[0]] = p[i]
#         else:
#             break
# d = re.sub(r'[\-\:\.]', '_', re.sub(r'\s', 'T', str(datetime.datetime.today())))
# with open(f'solution_{d}.csv', 'w', encoding='utf-8') as f:
#     f.write('id,object_img\n')
#     for key, value in list(data.items()):
#         f.write(f'{key},{int(value)}\n')
