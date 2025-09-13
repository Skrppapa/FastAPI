from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database import Base

# Модель для таблицы cars
class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True) # index=True - Создает индекс для быстрого поиска и определения уникальности
    brand = Column(String, index=True)
    model = Column(String)
    price = Column(Integer)
    year_release = Column(Integer)
    color = Column(String)
    added = Column(String, nullable=True)

# Модель для таблицы users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    credit_rating = Column(Integer)
    work_place = Column(String, nullable=True)