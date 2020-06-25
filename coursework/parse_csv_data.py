import csv
from itertools import chain, islice

import storage

FIELDS_LIST = ('iyear', 'country_txt', 'region_txt', 'success', 'suicide', 'targtype1_txt', 'weaptype1_txt')
FIELDS_TYPE = (int, str, str, lambda x: x == '1', lambda x: x == '1', str, str)


def get_fields(source):
    data = dict()
    for field, type_ in zip(FIELDS_LIST, FIELDS_TYPE):
        piece = source[field]
        if not piece:
            return None
        data[field.replace('_txt', '').replace('1', '').replace('iyear', 'year')] = type_(piece)
    return data


def load_csv(filepath):
    rows = csv.DictReader(open(filepath, 'r', encoding='ISO-8859-1'))
    for row in rows:
        data = get_fields(row)
        if data:
            yield data


def chunk_generator(iterable, size):
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))


if __name__ == '__main__':
    collection = storage.mongo_collection()
    collection.delete_many({})
    data = load_csv('terrorism.csv')
    print('Зачекайте, йде обробка csv файлу. Це може тривати декілька хвилин...')
    count = 0
    for sublist in chunk_generator(data, size=1_000):
        sublist = list(sublist)
        collection.insert_many(sublist)
        count += len(sublist)
        print(f'{count} було записано в базу даних')
    print(f'Дані з terrorism.csv успішно записано в базу даних')
