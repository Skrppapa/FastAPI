from http.client import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict
import uvicorn
import sqlite3

engine = create_engine('sqlite+aiosqlite:///book.db')

app = FastAPI()


class MetaSchema(BaseModel):
    id: int = Field(ge = 1)
    
# Класс для валидации вытомобилей
class CarSchema(MetaSchema): 
    brand: str = Field(max_length=200) # Если мы не указываем | None то поле считается обязательным
    model: str = Field(max_length=200) 
    price: int = Field(gt = 0) # grated or equal (ge) больше или равен. less or equal (le) меньше или равен
    year_release: int = Field(gt = 1900)
    color: str = Field(max_length=100)
    added: str | None = Field(max_length=1000)

    model_config = ConfigDict(extra="forbid") # Буквально - запрети дополнительные параметры

class UserSchema(MetaSchema):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    age: int = Field(gt = 18)
    credit_rating: int = Field(gt = 1, le = 10)
    work_plase: str | None = Field(max_length=100)



@app.get('/')
def root():
    return "Hello World"


@app.get("/list_cars", tags = ["Автомобили"], summary = "Получить все автомобили")
def all_cars():
    return cars

@app.get("/list_cars/{car_id}", tags = ["Автомобили"], summary = "Получить конкретный автобиль")
def get_car_id(car_id: int):
    for car in cars:
        if car['id'] == car_id:
             return car 
    raise HTTPException(status_code=404, detail = "Автомобиль не найден")


@app.post("/cars", tags = ["Автомобили"], summary = "Добавление новго автомобиля")
def add_car(car: CarSchema):
    cars.append(car)
    return {"ok": "True", "msg": "Автомобиль успешно добавлен"}








if __name__ == '__main__':
    uvicorn.run('main:app')

# Переход cd '100) AutoProject'
# Активация source venv_auto_linux/bin/activate