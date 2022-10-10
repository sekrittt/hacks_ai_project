import csv, re, pymorphy2, itertools
from collections import Counter

morphy = pymorphy2.MorphAnalyzer(lang='ru')

roman_numbers = [
    'i', 'ii', 'iii',
    'iv', 'v', 'vi', 'vii', 'viii',
    'ix', 'x', 'xi', 'xii', 'xiii',
    'xiv', 'xv', 'xvi', 'xvii', 'xviii',
    'xix', 'xx', 'xxi', 'xxii', ' xxiii',
    'xxiv', 'xxv', 'xxvi', 'xxvii', 'xxviii',
    'xxix', 'xxx'
]

def convert_roman_if_have(desc:str):
    global roman_numbers
    for i, num in enumerate(roman_numbers):
        desc = re.sub(fr'\s({num})\s', f' {i+1} ', desc)
    return desc

def get_crossing(str1, strs):
    res = ''
    for i, s in enumerate(str1):
        a = True
        for s1 in strs:
            if i >= len(s1) or not s == s1[i]:
                a = False
        if a:
            res += s
        else:
            return res
    return res

def word_process(s: str):
    res = morphy.parse(s)[0]
    l = list(map(lambda x: x.word, res.lexeme))
    l.append(get_crossing(s, l))
    return l

def get_combs(s:str, l: int):
    global morphy
    for i in itertools.combinations_with_replacement(s, l):
        for j in range(l):
            out = ''.join(i)[:j]
            if not out.isdigit():
                if not morphy.word_is_known(out):
                    continue
            yield out

def get_filters(path:str):
    global word_process
    filters = []
    words_lists = []
    words_lists_2 = []
    text = ''

    words = []
    symbols = []

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        lines = list(reader)[1:]
        for i, row in enumerate(lines):
            words_lists.append(re.sub(r'\s+', ' ', re.sub(r'[^a-zA-Zа-яёА-ЯЁ\d]', ' ', row[1])).strip())
            words_lists_2.append(re.sub(r'\s+', ' ', row[1]).strip())
        text = dict(Counter((' '.join(words_lists)).lower().split(' ')))
        for key, value in text.items():
            if value > 30 and len(key) >= 3:
                words.append(key)
        for n, w in enumerate(words):
            # if n > 500:
            #     break
            filters.extend(word_process(w))

        text_2 = dict(Counter(list((re.sub(r'\s+', '', ''.join(words_lists))).lower())))
        for key, value in text_2.items():
            if value > 100 and value < 10000:
                symbols.append(key)
        for n, s in enumerate(symbols):
            # if n > 3000:
            #     break
            filters.append(s)
        t = (' '.join(words_lists)).lower()
        for i in get_combs('0123456789', 5):
            b = t.count(i)
            if b > 30:
                filters.append(i)
        return list(filter(lambda x: len(x.strip()) > 0, sorted(filters)))
