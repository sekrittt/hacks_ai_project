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

    def __get_d_if_monet(self, desc:str):
        if desc.split()[0] == 'монета':
            f = re.search(r'(штамповка|чеканка).*?(\d+) мм', desc)
            if not f is None:
                return f[2]
        return 0

    def __get_m_if_monet(self, desc:str):
        if desc.split()[0] == 'монета':
            f = re.search(r'(пкм|покм)-(\d+)/(\d+) (\w+);', desc)
            if not f is None:
                return f[4]
            f = re.search(r'(пкм|покм)-(\d+) (\w+);', desc)
            if not f is None:
                return f[3]
        return 0

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

    def __get_pkm(self, desc:str):
        f = re.search(r'(?:пкм|покм)-(\d+)/(\d+)', desc)
        if not f is None:
            return round(int(f'{f[1]}{f[2]}'))
        f = re.search(r'(?:пкм|покм)-(\d+)', desc)
        if not f is None:
            return f[1]
        return 0

    def __get_tgu(self, desc:str):
        f = re.search(r'т/гу-(\d+)', desc)
        if not f is None:
            return f[1]
        return 0

    def __get_dif(self, desc:str):
        f = re.search(r'ди/ф-(\d+)', desc)
        if not f is None:
            return f[1]
        return 0
    def __get_din(self, desc:str):
        f = re.search(r'ди/н-(\d+)', desc)
        if not f is None:
            return f[1]
        return 0
    def __get_didp(self, desc:str):
        f = re.search(r'ди/дп-(\d+)', desc)
        if not f is None:
            return f[1]
        return 0

    def __get_dmn(self, desc:str):
        f = re.search(r'дм/н-(\d+)', desc)
        if not f is None:
            return f[1]
        return 0
    def __get_nm(self, desc:str):
        f = re.search(r'н/м-(\d+)', desc)
        if not f is None:
            return f[1]
        return 0
    def __get_arus(self, desc:str):
        f = re.search(r'а/рус-(\d+)', desc)
        if not f is None:
            return f[1]
        return 0
    def __get_arzhvs(self, desc:str):
        f = re.search(r'а/ржвс-(\d+)', desc)
        if not f is None:
            return f[1]
        return 0
    def __get_izozhgb(self, desc:str):
        f = re.search(r'изо/жгб-(\d+)', desc)
        if not f is None:
            return f[1]
        return 0
    def __get_or(self, desc:str):
        f = re.search(r'ор-(\d+)', desc)
        if not f is None:
            return f[1]
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
    def load_data(self, path: str, drop_fields:list):
        df = pd.read_csv(path)
        #print(list(df.values))
        df['description'] = df.description.map(lambda x: re.sub(r'\s+', ' ', x).lower())
        df["len_description"] = df.description.map(len)
        df["object"] = df["description"].map(lambda x : re.sub(r'\W', ' ', x.split('.')[0]).strip())
        df['othersymbolscount'] = df.description.map(lambda x: len(re.findall(r'\W', x)))

        df["object"] = pd.Categorical(df["object"])
        df["object"].astype('category').cat.codes
        df["object"] = df["object"].cat.codes

        df['have_pokm'] = df.description.map(lambda x: int('покм' in x))
        df['have_pkm'] = df.description.map(lambda x: int('пкм' in x))
        df['photo_print'] = df.description.map(lambda x: int('фотопечать' in x))
        df['stamping_or_coinage'] = df.description.map(lambda x: int('штамповка' in x or 'чеканка' in x))
        df['coinage'] = df.description.map(lambda x: int('чеканка' in x))
        df['photography'] = df.description.map(lambda x: int('фотосъемка' in x))
        df['tape'] = df.description.map(lambda x: int('плёнка' in x or 'пленочный' in x))
        df['photo_paper'] = df.description.map(lambda x: int('фотобумага' in x))
        df['paperboard'] = df.description.map(lambda x: int('картон' in x))
        df['oil'] = df.description.map(lambda x: int('масло' in x))
        df['wood'] = df.description.map(lambda x: int('дерево' in x))
        df['tree'] = df.description.map(lambda x: int('дерев' in x))
        df['is_photo'] = df.description.map(lambda x: int('фотография' in x))
        df['congress'] = df.description.map(lambda x: int('съезд' in x))
        df['congress_num'] = df.description.map(self.__get_congress_num)
        df['photo_annot'] = df.description.map(lambda x: int('фотография аннотирована' in x))
        df['plenum'] = df.description.map(lambda x: int('пленум' in x))
        df['plenum_num'] = df.description.map(self.__get_plenum_num)
        df['manuscript'] = df.description.map(lambda x: int('рукопись' in x))
        df['painting'] = df.description.map(lambda x: int('роспись' in x))
        df['pasta'] = df.description.map(lambda x: int('паста' in x))
        df['glue'] = df.description.map(lambda x: int('клей' in x))
        df['tempera'] = df.description.map(lambda x: int('темпера' in x))
        df['glass'] = df.description.map(lambda x: int('стекло' in x))
        df['forging'] = df.description.map(lambda x: int('ковка' in x))
        df['plant'] = df.description.map(lambda x: int('цветок' in x or 'плод' in x or 'растение' in x or 'ветвь' in x))
        df['three_formate'] = df.description.map(lambda x: int('лист а3' in x))
        df['spectacle'] = df.description.map(lambda x: int('спектакл' in x))
        df['panorama'] = df.description.map(lambda x: int('панорама' in x))
        df['pendant'] = df.description.map(lambda x: int('подвеск' in x))
        df['permeation'] = df.description.map(lambda x: int('пронизк' in x))
        df['table'] = df.description.map(lambda x: int('стол' in x))
        df['order'] = df.description.map(lambda x: int('орден' in x))
        df['bird'] = df.description.map(lambda x: int('птиц' in x))
        df['animal'] = df.description.map(lambda x: int('животны' in x))
        df['weapon'] = df.description.map(lambda x: int('оружие' in x))
        df['have_street'] = df.description.map(lambda x: int('улиц' in x))
        df['is_perm'] = df.description.map(lambda x: int('перм' in x))
        df['is_ussr'] = df.description.map(lambda x: int('ссср' in x))
        df['is_enamel'] = df.description.map(lambda x: int('эмаль' in x))
        df['is_black_and_white'] = df.description.map(lambda x: int('черно-белая' in x or 'черно-белое' in x))
        df['is_saint_p'] = df.description.map(lambda x: int('санкт-петербург' in x))
        df['have_photograph'] = df.description.map(lambda x: int('фотограф' in x))
        df['have_architect'] = df.description.map(lambda x: int('архитектор' in x))
        df['have_build'] = df.description.map(lambda x: int('дом' in x \
                                                            or 'школа' in x \
                                                            or 'школы' in x \
                                                            or 'изб' in x \
                                                            or 'завод' in x \
                                                            or 'театр' in x \
                                                            or 'училище' in x \
                                                            or 'химкомплекс' in x \
                                                            or 'дворец' in x \
                                                            or 'аптека' in x \
                                                            or 'госпитал' in x \
                                                            or 'завод ' in x ))
        df['have_window'] = df.description.map(lambda x: int(' окн' in x))
        df['have_glasses'] = df.description.map(lambda x: int(' очк' in x))
        df['have_paint'] = df.description.map(lambda x: int('пейзаж' in x))
        df['have_english'] = df.description.map(lambda x: int(not re.search(r'[a-z]', x) is None))

        df["street"] = df["description"].map(self.__get_street)
        df["street"] = pd.Categorical(df["street"])
        df["street"].astype('category').cat.codes
        df["street"] = df["street"].cat.codes

        df['diameter'] = df.description.map(self.__get_d_if_monet)

        df['material'] = df.description.map(self.__get_m_if_monet)
        df["material"] = pd.Categorical(df["material"])
        df["material"].astype('category').cat.codes
        df["material"] = df["material"].cat.codes

        df['photograph'] = df.description.map(self.__get_photograph)
        df["photograph"] = pd.Categorical(df["photograph"])
        df["photograph"].astype('category').cat.codes
        df["photograph"] = df["photograph"].cat.codes

        df['architect'] = df.description.map(self.__get_architect)
        df["architect"] = pd.Categorical(df["architect"])
        df["architect"].astype('category').cat.codes
        df["architect"] = df["architect"].cat.codes

        df['colors'] = df.description.map(self.__get_colors_if_enamel_or_clay)
        df["colors"] = pd.Categorical(df["colors"])
        df["colors"].astype('category').cat.codes
        df["colors"] = df["colors"].cat.codes

        # df['num'] = df.description.map(self.__get_nums)
        df['pkm'] = df.description.map(self.__get_pkm)
        df['tgu'] = df.description.map(self.__get_tgu)
        df['dif'] = df.description.map(self.__get_dif)
        df['din'] = df.description.map(self.__get_din)
        df['didp'] = df.description.map(self.__get_didp)
        df['dmn'] = df.description.map(self.__get_dmn)
        df['nm'] = df.description.map(self.__get_nm)
        df['or'] = df.description.map(self.__get_or)
        df['arus'] = df.description.map(self.__get_arus)
        df['arzhvs'] = df.description.map(self.__get_arzhvs)
        df['izozhgb'] = df.description.map(self.__get_izozhgb)
        df['have_people'] = df.description.map(self.__have_people)

        df['desc'] = df.description.map(lambda x: base64.b64encode(bytes(x, 'utf-8')))
        df["desc"] = pd.Categorical(df["desc"])
        df["desc"].astype('category').cat.codes
        df["desc"] = df["desc"].cat.codes

        df['double_penetration'] = df.description.map(lambda x: ','.join(re.findall(r'(?<!а3)\s([а-яё]+,[а-яё]+)+\s', x)))
        df["double_penetration"] = pd.Categorical(df["double_penetration"])
        df["double_penetration"].astype('category').cat.codes
        df["double_penetration"] = df["double_penetration"].cat.codes

        ids = list(df.get('id'))

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

        return X, y, y_indexes
