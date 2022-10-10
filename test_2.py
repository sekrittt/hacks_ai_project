import csv,re, pymorphy2, itertools, time, os
from collections import Counter
words_list = []
numbers_list = []
path = 'train.csv'
morph = pymorphy2.MorphAnalyzer(lang='ru')
counter = {}
result = []
os.system('cls||clear')
print('Start!')
start = time.time()
def get_combs(s:str, l: int):
    global morph
    for i in itertools.combinations_with_replacement(s, l):
        for j in range(l):
            out = ''.join(i)[:j]
            if not out.isdigit():
                if not morph.word_is_known(out):
                    continue
            yield out

with open(path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    lines = list(reader)[1:]
    for i, row in enumerate(lines):
        words_list.append(re.sub(r'\s+', ' ', re.sub(r'[^a-zA-Zа-яёА-ЯЁ\d]', ' ', row[1])).strip())
        numbers_list.append(re.sub(r'\s+', ' ', re.sub(r'[^\d]', ' ', row[1])).strip())
    # text = dict(Counter())
    l = max(list(map(lambda x: len(x), (' '.join(words_list)).lower().split(' '))))
    n = max(list(map(lambda x: len(x), (' '.join(numbers_list)).lower().split(' '))))
    text = (' '.join(words_list)).lower()
    for i in get_combs('0123456789', n):
        counter[i] = text.count(i)
    for i in get_combs('абвгдеёжзийклмнопрстуфхцчшщъыьэюя', l):
        counter[i] = text.count(i)


for key, value in counter.items():
    if value > 100:
        result.append(key)

print(result)
print(f'Time for adaptive filters: {time.time() - start}s')
