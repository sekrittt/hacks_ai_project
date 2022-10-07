import csv, re
from collections import Counter
from deep_translator import GoogleTranslator

def get_filters(path:str):
    translator = GoogleTranslator(source='ru', target='en')
    filters = []
    words_lists = []
    text = ''

    words = []

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        lines = list(reader)[1:]
        for i, row in enumerate(lines):
            line = re.sub(r'\s+', ' ', re.sub(r'\W', ' ', row[1])).strip()
            words_lists.append(line)
        text = dict(Counter((' '.join(words_lists)).lower().split(' ')))
        for key, value in text.items():
            # if value > 50 and len(key) > 3 and not key.isdigit():
            if value > 50:
                words.append(key)
        en_words_1 = list(map(lambda x: re.sub(r'\s', '_', x).lower(), translator.translate(', '.join(words[:(len(words)//4)])).split(', ')))
        en_words_2 = list(map(lambda x: re.sub(r'\s', '_', x).lower(), translator.translate(', '.join(words[(len(words)//4):(len(words)//2)])).split(', ')))
        en_words_3 = list(map(lambda x: re.sub(r'\s', '_', x).lower(), translator.translate(', '.join(words[(len(words)//2):((len(words)//4)*3)])).split(', ')))
        en_words_4 = list(map(lambda x: re.sub(r'\s', '_', x).lower(), translator.translate(', '.join(words[((len(words)//4)*3):])).split(', ')))
        en_words = [*en_words_1, *en_words_2, *en_words_3, *en_words_4]
        for w, ew in zip(words, en_words):
            filters.append({
                "name": ew,
                "word": w
            })
        return filters

if __name__ == "__main__":
    print(get_filters())
