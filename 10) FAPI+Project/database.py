from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    "sqlite+aiosqlite:///task.db"   # название бд + драйвер далее :///название файла БД
)

session = async_sessionmaker(engine, expire_on_commit = False)

class Model(DeclarativeBase):
    pass


class TaskOrm(Model):  # Здесь описали таблицу, но ее еще нужно создать
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str]
    description: Mapped[Optional[str]]


async def create_tables():   # Функция создания всех тадлиц
    async with engine.begin() as conn:
        await  conn.run_sync(Model.metadata.create_all)


async def delete_tables():   # Функция удаления всех тадлиц
    async with engine.begin() as conn:
        await  conn.run_sync(Model.metadata.drop_all)