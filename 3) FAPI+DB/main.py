from fastapi import FastAPI, Depends # Depends Для инъекции зависимостей
import uvicorn
from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# create_async_engeine - асинхронный движок
# async_sessionmaker - для создания сессий
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from pydantic import BaseModel, Field


# БД в этом примере будет жить прям в проекте в файлике
engine = create_async_engine('sqlite+aiosqlite:///book.db')
# указываем бд sqlite
# указываем асинхронный драйвер aiosqlite
# book.db - это название самой базы

app = FastAPI()


new_session = async_sessionmaker(engine, expire_on_commit=False) # async_sessionmaker - это фабрика сессий для бд
# Сессия это по сути транзакция для работы с БД, что бы ее можно бло отскрыть, сделать нужные запросы и закрыть. (Сессия работы с БД)

# Создаем асинхронный генератор, который создает и автоматически закрывает сессию для работы

async def get_session():  # async - Это значит функция асинхронная, она может "ставить на паузу" свое выполнение
    async with new_session() as session: # new_session() Это как раз новая сессия
        yield session

# async with - асинхронный менеджер контекста. Он: автоматом открывает сессию при входе и автоматом закрывает сессию при выходе (очень важно!)
# А так же он работает асинхронно (не блокирует другие операции)
# yield - ключевое слово генератора. Функция не возвращает (return), а "отдает" (yield) сессию
# После yield функция ставится на паузу, пока не потребуется следующее значение
# А теперь в целом get_session() - это такой ассихронный генератор который отдает нам сессию на время пока работает ручка
# Допустим - юзер прислдал нам в API запрос, мы его получили и затем запросили у генератора сессию. И вот до момента пока мв не вернем ответ пользователю, сессия будет открыта.
# Мы можем делать разного рода запросы, сложыне, простые, может быть несколько транзакций в рамках этой сессии. Но классика это 1 ручка - 1 транзакция. И грубо говоря сессия = транзакция

SessionDep = Annotated[AsyncSession, Depends(get_session)]
# Здесь мы делаем абстракцию от которой и будем зависеть, а не от конкретной реализации
# Аналогия
# AsyncSession - это просто "сковородка"
# get_session - это повар, который приносит вам сковородку
# Depends(get_session) - означает "зависит от повара, который принесет сковородку"
# Annotated[AsyncSession, Depends(get_session)] - это "сковородка, которую принес повар"
# SessionDep - это ярлык "сковородка_от_повара"
# Теперь вместо того чтобы говорить каждый раз "принеси мне сковородку от повара", вы просто говорите "сковородка_от_повара".

class Base(DeclarativeBase): # Базовый класс мы создаем сами и он тоже всегда наследуется от DeclartiveBase
    pass

class BookModel(Base): # Всегда наследуемся от базового класса
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]


@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    return {"ok": True}


class BookAddSchema(BaseModel):
    title: str
    author: str

class BookSchema(BookAddSchema):
    id: int

class BookGetSchema(BaseModel):
    id: int
    title: str
    author: str


@app.post("/books") # Добавляем новую книгу
async def add_book(data: BookAddSchema, session: SessionDep): # Вот тут мы уже прописали, как раз эту абстракцию она нам и открывает сессию
    # На этом моменте, благодаря session: SessionDep - сессия уже открыта, можем отправлять запросы в БД
    new_book = BookModel(
        title = data.title,
        author = data.author
    )
    session.add(new_book)  # Просим АЛхимию добавить объект выше. Но с БД пока не общаемся, т.к. нет await
    await session.commit() # Это уже обращение к БД
    return {'ok': True}


@app.get("/books") # Выводим все книги
async def get_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query) # Так работает алхимия - возвращается итератор
    return result.scalars().all()



#==================================Продолжение - урок про Depends===============================

# Тут делаем ручку с пагинацией - то есть порционной выдачей контента

@app.get("/books/limit")
async def traning_get_books_limit(
    session: SessionDep,
    limit: int,   # Лимит, сколько мы хотим получить, например объектов
    offset: int   # Сдвиг - если например хотим начать посмотр с 4 страницы - укажем сдвиг на 4
    ) -> list[BookGetSchema]:
    query = select(BookModel).limit(limit).offset(offset)

    result = await session.execute(query)
    return result.scalars().all()


# Пагинация - удобно. Но вот проблема, допустимм у нас 100 ручек в проекте и в каждой из них я хочу реализовать пагинацию.
# Каждый раз подобное прописывать - глупо, к тому же это нарушает принццип DRY
# Выход - это все добро что мы написали можно вынести в зависимости и ипереиспользовать. Как мы это делаем? Через Pydantic (идем к классу PaginationParams)

class PaginationParams(BaseModel): # Можно и через функцию
    limit: int = Field(5, ge = 0, le = 100, description="Кол-во элементов на странице")
    offset: int = Field(0, ge = 0, description="Смещение для пагинации")


PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)] # Шаблон "Название = Annotated[класс/функция, Depends(класс/функция)]"
# Это и есть Depend и ее мы можеи использовать сколько угодно раз

@app.get("/books/limited")
async def get_books_limit(
    session: SessionDep,
    pagination: PaginationDep
    ) -> list[BookGetSchema]:
    query = select(BookModel).limit(pagination.limit).offset(pagination.offset)

    result = await session.execute(query)
    return result.scalars().all()


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)


# Перейти cd "3) FAPI+DB"
# Активация окружения . fapibd\Scripts\activate
# Запуск python main.py


# uvicorn main:app --reload
