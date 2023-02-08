import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'Publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)
    book = relationship('Book', back_populates='publisher')

    def __str__(self):
        return f'{self.id}: {self.name}'


class Book(Base):
    __tablename__ = 'Book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('Publisher.id'), nullable=False)
    publisher = relationship('Publisher', back_populates='book')


class Shop(Base):
    __tablename__ = 'Shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)

    def __str__(self):
        return f'{self.id}: {self.name}'

class Stock(Base):
    __tablename__ = 'Stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('Book.id'))
    book = relationship(Book, backref='Stock')
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('Shop.id'))
    shop = relationship(Shop, backref='Stock')
    count = sq.Column(sq.Integer, nullable=False)


class Sale(Base):
    __tablename__ = 'Sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('Stock.id'))
    stock = relationship(Stock, backref='Sale')
    count = sq.Column(sq.Integer, nullable=False)
