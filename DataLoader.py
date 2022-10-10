import random, time
import re, base64
import pandas as pd

class DataLoader:
    __roman_numbers = [
        'i', 'ii', 'iii',
        'iv', 'v', 'vi', 'vii', 'viii',
        'ix', 'x', 'xi', 'xii', 'xiii',
        'xiv', 'xv', 'xvi', 'xvii', 'xviii',
        'xix', 'xx', 'xxi', 'xxii', ' xxiii',
        'xxiv', 'xxv', 'xxvi', 'xxvii', 'xxviii',
        'xxix', 'xxx'
    ]

    def __get_nums(self, desc: str):
        pkm = self.__get_pkm(desc)
        tgu = self.__get_tgu(desc)
        dif = self.__get_dif(desc)
        din = self.__get_din(desc)
        didp = self.__get_didp(desc)
        dmn = self.__get_dmn(desc)
        nm = self.__get_nm(desc)
        _or = self.__get_or(desc)
        arus = self.__get_arus(desc)
        arzhvs = self.__get_arzhvs(desc)
        izozhgb = self.__get_izozhgb(desc)
        osc = len(re.findall(r'\W', desc))
        l = len(desc)
        return int(f'{l}{pkm}{tgu}{dif}{din}{didp}{dmn}{nm}{_or}{arus}{arzhvs}{izozhgb}{osc}')

    def __get_m_if_monet(self, desc:str):
        if desc.split()[0] == 'монета':
            f = re.search(r'(пкм|покм)-(\d+)/(\d+) (\w+);', desc)
            if not f is None:
                return f[4]
            f = re.search(r'(пкм|покм)-(\d+) (\w+);', desc)
            if not f is None:
                return f[3]
        return 0

    def __get_pkm(self, desc:str):
        f = re.search(r'(?:пкм|покм)-(\d+)/(\d+)', desc)
        if not f is None:
            return round(int(f'{f[1]}{f[2]}'))
        f = re.search(r'(?:пкм|покм)-(\d+)', desc)
        if not f is None:
            return int(f[1])
        return 0

    def __get_tgu(self, desc:str):
        f = re.search(r'т/гу-(\d+)', desc)
        if not f is None:
            return int(f[1])
        return 0

    def __get_dif(self, desc:str):
        f = re.search(r'ди/ф-(\d+)', desc)
        if not f is None:
            return int(f[1])
        return 0
    def __get_din(self, desc:str):
        f = re.search(r'ди/н-(\d+)', desc)
        if not f is None:
            return int(f[1])
        return 0
    def __get_didp(self, desc:str):
        f = re.search(r'ди/дп-(\d+)', desc)
        if not f is None:
            return int(f[1])
        return 0

    def __get_dmn(self, desc:str):
        f = re.search(r'дм/н-(\d+)', desc)
        if not f is None:
            return int(f[1])
        return 0
    def __get_nm(self, desc:str):
        f = re.search(r'н/м-(\d+)', desc)
        if not f is None:
            return int(f[1])
        return 0
    def __get_arus(self, desc:str):
        f = re.search(r'а/рус-(\d+)', desc)
        if not f is None:
            return int(f[1])
        return 0
    def __get_arzhvs(self, desc:str):
        f = re.search(r'а/ржвс-(\d+)', desc)
        if not f is None:
            return int(f[1])
        return 0
    def __get_izozhgb(self, desc:str):
        f = re.search(r'изо/жгб-(\d+)', desc)
        if not f is None:
            return int(f[1])
        return 0
    def __get_or(self, desc:str):
        f = re.search(r'ор-(\d+)', desc)
        if not f is None:
            return int(f[1])
        return 0

    def __get_street(self, desc:str):
        f = re.search(r'(?:ул\.|улица) (\w+)\s', desc)
        if not f is None:
            return f[1]
        return 'no_street'

    def __have_people(self, desc:str):
        res = ('женщин' in desc) \
                or ('мужчин' in desc) \
                or ('мальчик' in desc) \
                or ('девушк' in desc) \
                or ('участники' in desc) \
                or ('секретарь' in desc) \
                or ('врач' in desc) \
                or ('режиссер' in desc) \
                or ('крестьянк' in desc) \
                or ('крестьянин' in desc) \
                or ('дочь' in desc) \
                or ('член ' in desc) \
                or ('коллектив' in desc)

    #	print(res)
        return int(res)

    def __convert_roman_if_have(self, desc:str):
        for i, num in enumerate(self.__roman_numbers):
            desc = re.sub(fr'\s({num})\s', f' {i+1} ', desc)
        return desc

    def __get_plenum_num(self, desc:str):
        if 'пленум ' in desc:
            desc = self.__convert_roman_if_have(desc)
            f = re.search(r'(\d+).*?\sпленум', desc)
            if not f is None:
                return f[1]
        return 0

    def __get_congress_num(self, desc:str):
        if 'пленум ' in desc:
            desc = self.__convert_roman_if_have(desc)
            f = re.search(r'(\d+).*?съезд', desc)
            if not f is None:
                return f[1]
        return 0

    def __get_photograph(self, desc:str):
        f = re.search(r'\s((?:[\w\s\(\)]|\[[\w\s\(\)]\])+) \(фотограф\)', desc)
        # print(f)
        if not f is None:
            return f[1]
        return 'no_photograph'

    def __get_architect(self, desc:str):
        f = re.search(r'\s([\w\s\(\)]+) \(архитектор\)', desc)
        # print(f)
        if not f is None:
            return f[1]
        return 'no_architect'

    def __get_colors_if_enamel_or_clay(self, desc:str):
        f = re.findall(r'(?:глина|эмаль) \(([\w,\s]+)\)', desc)
        if len(f) > 0:
            return ', '.join(map(lambda x: x, f))
        return 'no_colors'
    def load_data(self, path: str, drop_fields:list, filters: list[str]):
        start = time.time()
        df = pd.read_csv(path)
        df["len_desc"] = df.description.map(lambda x: len(x))
        df['description'] = df.description.map(lambda x: x.lower())

        for i, word in enumerate(filters):
            df[f"param_{i}-0"] = df.description.map(lambda x: int(word in x))
            df[f"param_{i}-1"] = df.description.map(lambda x: int(len(re.findall(fr'[^а-яёa-z]{word}', x)) > 0))
            df[f"param_{i}-2"] = df.description.map(lambda x: int(len(re.findall(fr'{word}[^а-яёa-z]', x)) > 0))
            df[f"param_{i}-3"] = df.description.map(lambda x: int(len(re.findall(fr'[^а-яёa-z]{word}[^а-яёa-z]', x)) > 0))
            df[f"param_{i}-4"] = df.description.map(lambda x: int(f' {word}' in x))
            df[f"param_{i}-5"] = df.description.map(lambda x: int(f'{word} ' in x))
            df[f"param_{i}-6"] = df.description.map(lambda x: int(f' {word} ' in x))

        ids = list(df.get('id'))

        X = df.drop(drop_fields, axis = 1)
        y = df.get('object_img')
        if not df.get('object_img') is None:
            y_indexes = pd.Series(list(df.get('object_img')), ids)
        else:
            y_indexes = None
        print(f'Time for load data: {time.time() - start}')
        return X, y, y_indexes
