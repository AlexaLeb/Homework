from model import Publisher, Shop, Book, Sale, Stock
import json
from DBconnect import session

def uploader(fail_path):
    with open(fail_path, 'r') as fd: #Путь к файлу json
        data = json.load(fd)
        for record in data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
            }[record.get('model')]
            session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()