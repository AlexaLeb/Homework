import sqlalchemy as sq
import json
from model import Publisher, Shop, Book, Sale, Stock, Base
from sqlalchemy.orm import relationship, sessionmaker
from DBconnect import session
from Uploader import uploader

def name_shop():
    name = input('Введите имя или id автора: ')
    if name.isdigit():
        query = session.query(Shop).join(Stock, Shop.id == Stock.id_shop).join(Book, Stock.id_book == Book.id).\
            join(Publisher, Book.id_publisher == Publisher.id).filter(Publisher.id == int(name)).all()
    else:
        query = session.query(Shop).join(Stock, Shop.id == Stock.id_shop).join(Book, Stock.id_book == Book.id).join(
            Publisher, Book.id_publisher == Publisher.id).filter(Publisher.name == name).all()
    return query



b = uploader('info.json')
for s in name_shop():
    print(s)

session.close()

