from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware # Пройслойка которая позволяет настроить CORS
from starlette.responses import Response

# CORS Абсолютно Всегда настраивается на Бэкенде!
# CORS - Специальный мехнизм который позволяет бекендеру конкретно прописать кто может обращатся к его API

app = FastAPI()

# Добавляем CORSMiddleware к нашему приложению
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] # * Значит что абсолютно любые сайты могут делать запросы к нашему API
)                       # Обычно прописываются конкретные адреса которые находятся в компании, например: "http://127.0.0.1:63342"

books = [
    {
        "id": 1,
        "title": "Асинхронность в Python",
        "author": "Мэттью",
    },
    {
        "id": 2,
        "title": "Backend разработка в Python",
        "author": "Артём",
    },
]


class BookSchema(BaseModel):
    title: str
    author: str


@app.get("/books",
         tags=["Книги 📚"],
         summary="Получить список книг",
         description="<h1>Отдает список всех книг</h1>",
         )
def get_books():
    return books


@app.post("/books", tags=["Книги 📚"])
def add_book(book: BookSchema, response: Response
             ):
    new_book_id = len(books) + 1
    books.append({
        "id": new_book_id,
        "title": book.title,
        "author": book.author
    })
    return {"success": True, "message": "Книга добавлена"}


@app.put("/books/{book_id}", tags=["Книги 📚"])
def change_book(book_id: int, data: BookSchema):
    match = [book for book in books if book["id"] == book_id]
    if not match:
        raise HTTPException(status_code=404, detail="Книга с таким id не найдена")
    match[0] |= data.model_dump()
    return {"success": True, "message": "Книга обновлена"}


@app.delete("/books/{book_id}", tags=["Книги 📚"])
def delete_book(book_id: int):
    match = [book for book in books if book["id"] == book_id]
    if not match:
        raise HTTPException(status_code=404, detail="Книга с таким id не найдена")
    books.remove(match[0])
    return {"success": True, "message": "Книга удалена"}





# Активация . corsenv\Scripts\activate