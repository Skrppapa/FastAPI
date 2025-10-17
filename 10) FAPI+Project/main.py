from typing import Annotated, Optional
from fastapi import Depends, FastAPI
from pydantic import BaseModel
import uvicorn
from contextlib import asynccontextmanager  # Импортировали декоратор который позволяет создавать контекстный менеджер
from database import create_tables, delete_tables


# Раздел в документации https://fastapi.tiangolo.com/ru/advanced/events/#lifespan
# Собственно эту функцию мы используем для подготовки базы к работе
@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)



class STaskAdd(BaseModel):
    name: str
    description: Optional[str] = None   # По идее должно было сработать satr | None


class STask(STaskAdd):
    id: int

tasks = []

@app.post("/tasks")
async def add_task(
    task: Annotated[STaskAdd, Depends()],  # За счет Annotated и Depends() в docs будут удобные поля для ввода
):
    tasks.append(task)
    return {"ok": True}




# @app.get("/tasks")
# def get_tasks():
#     task = Task(name = "Запиши это видео", description="lalal")
#     return {"data": task}



if __name__ == '__main__':
    uvicorn.run('main:app')


# Закончил на 20:00

# pip install -r .\requirement.txt   Команда для установки библиотек из файла requirement.txt
# . projenv\Scripts\activate



# uvicorn, с помощью которого мы поднимаем приложение - поднимает небольшой, локальный веб сервер