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
    # "[а-я]+\.\s[а-я"\.]+
    def load_data(self, path: str, drop_fields:list, filters: list[str]):
        start = time.time()
        df = pd.read_csv(path)
        #print(list(df.values))
        # df["random"] = df.description.map(lambda x: int(len(x) > 200))
        df["len_desc"] = df.description.map(lambda x: len(x))
        # df["object"] = df["description"].map(lambda x : x.split()[0])
        # df["object"] = pd.Categorical(df["object"])
        # df["object"].astype('category').cat.codes
        # df["object"] = df["object"].cat.codes
        df['description'] = df.description.map(lambda x: x.lower())

        for i, word in enumerate(filters):
            df[f"param_{i}-0"] = df.description.map(lambda x: int(word in x))
            df[f"param_{i}-1"] = df.description.map(lambda x: int(len(re.findall(fr'[^а-яёa-z]{word}', x)) > 0))
            df[f"param_{i}-2"] = df.description.map(lambda x: int(len(re.findall(fr'{word}[^а-яёa-z]', x)) > 0))
            df[f"param_{i}-3"] = df.description.map(lambda x: int(len(re.findall(fr'[^а-яёa-z]{word}[^а-яёa-z]', x)) > 0))
            df[f"param_{i}-4"] = df.description.map(lambda x: int(f' {word}' in x))
            df[f"param_{i}-5"] = df.description.map(lambda x: int(f'{word} ' in x))
            df[f"param_{i}-6"] = df.description.map(lambda x: int(f' {word} ' in x))

        # df['фотог'] = df.description.map(lambda x: int('фото' in x))
        # df['моно'] = df.description.map(lambda x: int('монета' in x))
        # df['картина'] = df.description.map(lambda x: int('картина' in x))
        # df['форм'] = df.description.map(lambda x: int('форм' in x))
        # df['кар'] = df.description.map(lambda x: int('кар' in x))
        # df['член'] = df.description.map(lambda x: int('член' in x))
        # df['стекл'] = df.description.map(lambda x: int('стекл' in x))
        # df['мат'] = df.description.map(lambda x: int('мат' in x))
        # df['цвет'] = df.description.map(lambda x: int('цвет' in x))
        # df['ряд'] = df.description.map(lambda x: int('ряд' in x))
        # df['изо'] = df.description.map(lambda x: int('изображен' in x))
        # df['сни'] = df.description.map(lambda x: int('сни' in x))
        # df['чел'] = df.description.map(lambda x: int('человек' in x))
        # df['пейзаж'] = df.description.map(lambda x: int('пейзаж' in x))
        # df['ь'] = df.description.map(lambda x: int('ь' in x)) #
        # df['лист'] = df.description.map(lambda x: int('лист' in x))
        # df['глуб'] = df.description.map(lambda x: int('19' in x))
        # df['пер'] = df.description.map(lambda x: int('пер' in x))
        # df['фраг'] = df.description.map(lambda x: int('фрагмент' in x))
        # df['чер'] = df.description.map(lambda x: int('чернила' in x))
        # df['плен'] = df.description.map(lambda x: int('плен' in x))
        # df['дерев'] = df.description.map(lambda x: int('дерев' in x))
        # df['сталь'] = df.description.map(lambda x: int('сталь' in x))
        # df['голов'] = df.description.map(lambda x: int('голов' in x))
        # df['тон'] = df.description.map(lambda x: int('тон' in x))
        # df['объем'] = df.description.map(lambda x: int('объем' in x))
        # df['эмал'] = df.description.map(lambda x: int('эмал' in x))
        # df['крас'] = df.description.map(lambda x: int('крас' in x))
        # df['раст'] = df.description.map(lambda x: int('раст' in x))
        # df['зелен'] = df.description.map(lambda x: int('зелен' in x))
        # df['граф'] = df.description.map(lambda x: int('граф' in x))
        # df['пис'] = df.description.map(lambda x: int('пис' in x))
        # df['корон'] = df.description.map(lambda x: int('корон' in x))
        # df['глин'] = df.description.map(lambda x: int('глин' in x))
        # df['бронз'] = df.description.map(lambda x: int('бронз' in x))
        # df['сереб'] = df.description.map(lambda x: int('сереб' in x))

        # df['have_pokm'] = df.description.map(lambda x: int('покм' in x))
        # df['have_pkm'] = df.description.map(lambda x: int('пкм' in x))
        # df['stamping_or_coinage'] = df.description.map(lambda x: int('штамповка' in x or 'чеканка' in x))
        # df['paperboard'] = df.description.map(lambda x: int('картон' in x))
        # df['tree'] = df.description.map(lambda x: int('дерев' in x))
        # df['tempera'] = df.description.map(lambda x: int('темпера' in x))
        # df['three_formate'] = df.description.map(lambda x: int('лист а3' in x))
        # df['spectacle'] = df.description.map(lambda x: int('спектакл' in x))
        # df['panorama'] = df.description.map(lambda x: int('панорама' in x))
        # df['permeation'] = df.description.map(lambda x: int('пронизк' in x))
        # df['table'] = df.description.map(lambda x: int('стол' in x))
        # df['order'] = df.description.map(lambda x: int('орден' in x))
        # df['animal'] = df.description.map(lambda x: int('животны' in x))
        # df['weapon'] = df.description.map(lambda x: int('оружие' in x))
        # df['have_street'] = df.description.map(lambda x: int('улиц' in x))
        # df['is_black_and_white'] = df.description.map(lambda x: int('черно-белая' in x or 'черно-белое' in x))
        # df['have_architect'] = df.description.map(lambda x: int('архитектор' in x))
        # df['have_build'] = df.description.map(lambda x: int('дом' in x \
        #                                                     or 'школа' in x \
        #                                                     or 'школы' in x \
        #                                                     or 'изб' in x \
        #                                                     or 'завод' in x \
        #                                                     or 'театр' in x \
        #                                                     or 'училище' in x \
        #                                                     or 'химкомплекс' in x \
        #                                                     or 'дворец' in x \
        #                                                     or 'аптека' in x \
        #                                                     or 'госпитал' in x \
        #                                                     or 'завод ' in x ))
        # df['have_window'] = df.description.map(lambda x: int(' окн' in x))
        # df['have_glasses'] = df.description.map(lambda x: int(' очк' in x))
        # df['have_english'] = df.description.map(lambda x: int(not re.search(r'[a-z]', x) is None))

        # df["street"] = df["description"].map(self.__get_street)
        # df["street"] = pd.Categorical(df["street"])
        # df["street"].astype('category').cat.codes
        # df["street"] = df["street"].cat.codes

        # df['material'] = df.description.map(self.__get_m_if_monet)
        # df["material"] = pd.Categorical(df["material"])
        # df["material"].astype('category').cat.codes
        # df["material"] = df["material"].cat.codes

        # df['photograph'] = df.description.map(self.__get_photograph)
        # df["photograph"] = pd.Categorical(df["photograph"])
        # df["photograph"].astype('category').cat.codes
        # df["photograph"] = df["photograph"].cat.codes

        # df['architect'] = df.description.map(self.__get_architect)
        # df["architect"] = pd.Categorical(df["architect"])
        # df["architect"].astype('category').cat.codes
        # df["architect"] = df["architect"].cat.codes

        # df['pkm'] = df.description.map(self.__get_pkm)
        # df['tgu'] = df.description.map(self.__get_tgu)
        # df['dif'] = df.description.map(self.__get_dif)
        # df['din'] = df.description.map(self.__get_din)
        # df['dmn'] = df.description.map(self.__get_dmn)
        # df['or'] = df.description.map(self.__get_or)
        # df['arzhvs'] = df.description.map(self.__get_arzhvs)
        # df['izozhgb'] = df.description.map(self.__get_izozhgb)
        # df['have_people'] = df.description.map(self.__have_people)

        # df['double_penetration'] = df.description.map(lambda x: ','.join(re.findall(r'(?<!а3)\s([а-яё]+,[а-яё]+)+\s', x)))
        # df["double_penetration"] = pd.Categorical(df["double_penetration"])
        # df["double_penetration"].astype('category').cat.codes
        # df["double_penetration"] = df["double_penetration"].cat.codes

        ids = list(df.get('id'))
        # print(df)

        # count_pkm = len(df.get('num'))
        # count_s_pkm = len(set(df.get('num')))
        # count_z_pkm = list(df.get('num')).count(0)

        # print(f'{count_pkm=}, {count_s_pkm=}, {count_z_pkm=}')

        X = df.drop(drop_fields, axis = 1)
        y = df.get('object_img')
        if not df.get('object_img') is None:
            y_indexes = pd.Series(list(df.get('object_img')), ids)
        else:
            y_indexes = None
        print(f'Time for load data: {time.time() - start}')
        return X, y, y_indexes
