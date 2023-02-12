# import sqlalchemy as sq
# from model import Base
# from sqlalchemy.orm import sessionmaker
#
#
# def create_tables(engine):
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)
#
#
# DSN = "postgresql://postgres:1207@localhost:5432/dvdrental"
# engine = sq.create_engine(DSN)
# create_tables(engine)
#
# # сессия
# Session = sessionmaker(bind=engine)
# session = Session()
#
