import time, re
import pandas as pd

class DataLoader:
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
