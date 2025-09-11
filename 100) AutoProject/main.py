import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import init_db, get_session # БД
from schemas import CarSchema, UserSchema # Валидация
from models import Car, User # Модели таблиц

app = FastAPI()

# Инициализация БД
init_db()


@app.get('/')
def root():
    return "Main Page"

@app.post("/cars/", tags = ["Автомобили"], summary = "Добавить автомобиль", response_model=CarSchema) # response_model=CarSchema - указывает, что ответ от этого эндпоинта будет соответствовать модели CarSchema
def add_car(car: CarSchema, db: Session = Depends(get_session)): # car: CarSchema - валидация FAPI под капотом валидирует через схему CarSchema
    # db: Session = Depends(get_session) - через get_session получает сессию
    db_car = Car(**car.dict()) # car.dict() - преобразует объект car в словарь. Car(**car.dict()) - создаем новый объект Car и в него распаковываем словарь
    db.add(db_car) # Добавляет объект в сессию. состояние готовое к коммиту.
    db.commit() 
    db.refresh(db_car) # Обновление
    return {"ok": True, "msg": "Автомбоиль успешно добавлен!"}


@app.get("/cars/", tags = ["Автомобили"], summary = "Список всех автомобилей", response_model=list[CarSchema])
def read_cars(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    cars = db.query(Car).offset(skip).limit(limit).all()
    return cars
    # skip: int = 0 - сколько записей нужно пропустить перед отображением
    # limit: int = 10 - максимум 10 записей
    # db: Session = Depends(get_session) - говорит вызвать функцию из database.py

# db.query(Car): Этот метод создает запрос к таблице cars в базе данных. Он возвращает объект запроса, который можно использовать для дальнейших операций.
# .offset(skip): Этот метод указывает, сколько записей нужно пропустить. Например, если skip равен 10, то первые 10 записей не будут включены в результаты.
# .limit(limit): Этот метод указывает максимальное количество записей, которые нужно вернуть. Например, если limit равен 5, то будет возвращено не более 5 записей.
# .all(): Этот метод выполняет запрос и возвращает все результаты в виде списка объектов Car.




#@app.get("/list_cars", tags = ["Автомобили"], summary = "Получить все автомобили")
#def all_cars():
#    return cars

#@app.get("/list_cars/{car_id}", tags = ["Автомобили"], summary = "Получить конкретный автобиль")
#def get_car_id(car_id: int):
#    for car in cars:
#        if car['id'] == car_id:
#             return car 
#    raise HTTPException(status_code=404, detail = "Автомобиль не найден")


#@app.post("/cars", tags = ["Автомобили"], summary = "Добавление новго автомобиля")
#def add_car(car: CarSchema):
#    cars.append(car)
#    return {"ok": "True", "msg": "Автомобиль успешно добавлен"}








if __name__ == '__main__':
    uvicorn.run('main:app')

# Переход cd '100) AutoProject'
# Активация source venv_auto_linux/bin/activate