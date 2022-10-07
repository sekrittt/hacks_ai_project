import csv, re
from collections import Counter

def get_filters():
    words_lists = []
    text = ''

    words = []

    with open('train.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        lines = list(reader)[1:]
        for i, row in enumerate(lines):
            line = re.sub(r'\s+', ' ', re.sub(r'\W', ' ', row[1])).strip()
            words_lists.append(line)
        text = dict(Counter((' '.join(words_lists)).lower().split(' ')))
        for key, value in text.items():
            if value > 100 and len(key) > 3 and not key.isdigit():
                words.append(key)
        return words
