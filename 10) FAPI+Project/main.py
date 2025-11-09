from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager  # Импортировали декоратор который позволяет создавать контекстный менеджер
from database import create_tables, delete_tables
from router import router as tasks_router



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
app.include_router(tasks_router)



if __name__ == '__main__':
    uvicorn.run('main:app')


# Закончил на 30:55




# pip install -r .\requirement.txt   Команда для установки библиотек из файла requirement.txt

# cd "10) FAPI+Project"
# . projenv\Scripts\activate


# uvicorn, с помощью которого мы поднимаем приложение - поднимает небольшой, локальный веб сервер