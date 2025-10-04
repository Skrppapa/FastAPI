from sqlalchemy import Column, Integer, String
from src.database import Base

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
