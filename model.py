import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


DSN = "postgresql://postgres:1207@localhost:5432/dvdrental"
engine = sq.create_engine(DSN)
create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'user'
    id_user = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.Integer, unique=True, nullable=False)
    age = sq.Column(sq.Integer, nullable=False)

    def __str__(self) -> str:
        return f'{self.id_user} {self.user_vk_id} {self.age}'


class Peopleforuser(Base):
    __tablename__ = 'peopleforuser'
    id_to_see = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.Integer, nullable=False)
    user_name = sq.Column(sq.String(40), nullable=False)
    user_surname = sq.Column(sq.String(40), nullable=False)
    link = sq.Column(sq.String(40), nullable=False)
    bot_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_vk_id'))

    def __str__(self) -> str:
        return f'{self.id_to_see} {self.user_vk_id} {self.user_name} {self.user_surname} {self.link}'


def db_insert_to_see(person: list, id_vk):
    for person in person:
        if db_chek_user_exists(id_vk) is True:
            new = Peopleforuser(
                user_vk_id=person['id'],
                user_name=person['first_name'],
                user_surname=person['last_name'],
                link=('vk.com/id' + str(person['id'])),
                bot_id=id_vk
            )
            session.add(new)
            session.commit()
    return True


def select_from_seen(offset, id_vk):
    if db_chek_user_exists(id_vk) is True:
        new = session.query(Peopleforuser).filter(Peopleforuser.bot_id == id_vk).offset(offset).first()
        return new.__str__().split()


def db_add_user(id_vk, age):
    if db_chek_user_exists(id_vk) is False:
        new = User(
            user_vk_id=id_vk,
            age=age
        )
        session.add(new)
        session.commit()
        print('добавил пользователя в бд')
        return True


def db_get_age(id_vk) -> int:
    if db_chek_user_exists(id_vk) is True:
        new = session.query(User).filter_by(user_vk_id=id_vk).first()
        a = new.__str__().split()
        print('возраст из базы данных', a)
        return int(a[2])


def db_chek_user_exists(id_vk) -> bool:
    new = session.query(User).filter_by(user_vk_id=id_vk).first()
    user = new.__str__()
    if user != 'None':
        return True
    else:
        return False


def creator():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return True
