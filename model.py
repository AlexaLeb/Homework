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


class SeenPeople(Base):
    __tablename__ = 'seenpeople'
    id_seen = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.Integer, unique=True, nullable=False)
    bot_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_vk_id'))

    def __str__(self) -> str:
        return f'{self.id_seen}: {self.user_vk_id}'


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


def db_chek_user_seen(id_vk, main_id) -> bool:
    new = session.query(SeenPeople).join(User, SeenPeople.bot_id == User.user_vk_id).filter_by(user_vk_id=main_id).first()
    user = new.__str__().split()
    print(int(user[1]))
    if int(user[1]) == id_vk:
        print('нашел')
        return True
    else:
        print('не нашел')
        return False


def db_add_to_seen(vk_id, bot_id):
    new = SeenPeople(
        user_vk_id=vk_id,
        bot_id=bot_id
    )
    session.add(new)
    session.commit()
    return True


def creator():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return True
