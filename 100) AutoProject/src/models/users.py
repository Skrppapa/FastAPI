from sqlalchemy import Column, Integer, String
from src.database import Base


# Модель для таблицы users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    credit_rating = Column(Integer)
    work_place = Column(String, nullable=True)