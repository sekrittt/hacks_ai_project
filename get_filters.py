import csv, re
from collections import Counter
from pyparsing import StringEnd, oneOf, FollowedBy, Optional, ZeroOrMore, SkipTo
from pymystem3 import Mystem
import pymorphy2

morphy = pymorphy2.MorphAnalyzer(lang='ru')

def get_crossing(str1, strs):
    res = ''
    for s in str1:
        a = True
        for s1 in strs:

            if not s in s1:
                a = False
        if a:
            res += s
        else:
            break
    return res

def word_process(s: str):
    res = morphy.parse(s)[0]
    strs = list(set(map(lambda x: x.word, res.lexeme)))
    return get_crossing(s, strs)


def get_parser():
    endOfString = StringEnd()
    prefix = oneOf("под не")
    suffix = oneOf("ы а ий ей ой") + FollowedBy(endOfString)

    word = (ZeroOrMore(prefix)("prefixes") +
            SkipTo(suffix | endOfString)("root") +
            Optional(suffix)("suffix"))
    return word

def get_filters(path:str):
    global get_parser, get_crossing, word_process
    filters = []
    words_lists = []
    text = ''

    words = []
    symbols = []
    m = Mystem()

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        lines = list(reader)[1:]
        for i, row in enumerate(lines):
            line = re.sub(r'\s+', ' ', re.sub(r'[^a-zA-Zа-яёА-ЯЁ\d]', ' ', row[1])).strip()
            words_lists.append(line)
        text = dict(Counter((' '.join(words_lists)).lower().split(' ')))
        for key, value in text.items():
            if value > 30 and len(key) >= 3:
                words.append(key)
        for n, w in enumerate(words):
            if n > 500:
                break
            r = word_process(w)
            if len(r) >= 3:
                filters.append(r)

        text_2 = dict(Counter(list((re.sub(r'\s+', '', ''.join(words_lists))).lower())))
        for key, value in text_2.items():
            if value > 50 and value < 10000:
                symbols.append(key)
        for n, s in enumerate(symbols):
            if n > 3000:
                break
            filters.append(s)
        return sorted(filters)

if __name__ == "__main__":
    print(get_filters())
