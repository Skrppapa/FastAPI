from fastapi import FastAPI, HTTPException
import uvicorn # uvicorn - это вебсервер который принимает запросы
from pydantic import BaseModel # pydantic библиотека для валидации данных. BaseModel - то чем будешь пользоватся ежедневно

app = FastAPI()


@app.get('/', summary='Домашняя страница') # summary отображает в докмуентации имя ручки в у казанном виде
def root():
    return('Hello World')


books = [

    {'id': 1,
     'title': 'На западном фронте без перемен',
     'author': 'Эрих Мария Ремарк'
    },

    {'id': 2,
     'title': 'Прощай оружие',
     'author': 'Эрнест Хемингуей'
    }

]

@app.get(
        '/books',
        tags=["Книги"],
        summary="Получить все книги"
        )
def read_books():
    return books


@app.get(
        '/books/{book_id}',
        tags=["Книги"],
        summary="Получить конкретную книгу"
        )
def get_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            return book
        raise HTTPException(status_code=404, detail = "Книга не найдена") # raise возвращает ошибку


class NewBook(BaseModel): # Наследуемся от BaseModel
    title: str # Под капотом pydantic валидирует данные
    author: str

@app.post(
        '/books',
        tags=["Книги"],
        summary="Добавление новой книги"
        )
def create_book(new_book: NewBook):
    books.append({
        'id': len(books) + 1,
        'title': new_book.title,
        'author': new_book.author
    })
    return {'success': True, "message": "Книга успешно добавлена"} # Под капотом FAPI сереализует словарь в JSON


if __name__ == '__main__':
    uvicorn.run('main:app')


# Активация окружения . fastenv\Scripts\activate

# Запуск приложения fastapi dev main.py
# Запуск через вебсервер uvicorn: uvicorn main:app --reload
# Запуск стандартный. После проописанной конструкуии if __name__ == '__main__' пишем: python main.py
