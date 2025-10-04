from fastapi import APIRouter, HTTPException, Depends
from src.schemas.cars import CarSchema # Валидация
from src.models.cars import Car # Модели таблиц
from src.database import get_session, Session


router = APIRouter()  # Вместо app используем router


@router.get("/cars/", tags = ["Cars"], summary = "Список всех автомобилей", response_model=list[CarSchema])
def read_cars(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    cars = db.query(Car).offset(skip).limit(limit).all()
    return cars
    # skip: int = 0 - сколько записей нужно пропустить перед отображением
    # limit: int = 10 - максимум 10 записей
    # db: Session = Depends(get_session) - говорит вызвать функцию из database.py

# db.query(Car) - метод создает запрос к таблице cars. Он возвращает объект запроса.
# .offset(skip) - метод указывает, сколько записей нужно пропустить.
# .limit(limit) - метод указывает максимальное количество записей, которые нужно вернуть.
# .all() - выполняет запрос и возвращает все результаты в виде списка объектов Car.


@router.post("/cars/", tags = ["Cars"], summary = "Добавить автомобиль")
def add_car(car: CarSchema, db: Session = Depends(get_session)): # car: CarSchema - валидация FAPI под капотом валидирует через схему CarSchema
    # db: Session = Depends(get_session) - через get_session получает сессию. В рамках этой сессии мы и будем действовать

    # Проверка существования автомобиля с таким ID
    existing_car = db.query(Car).filter(Car.id == car.id).first()

    if existing_car:
        raise HTTPException(
            status_code=400,
            detail=f"Автомобиль с ID {car.id} уже существует"
        )

    db_car = Car(**car.dict()) # car.dict() - преобразует объект car (это объект из pydantic уже провалидированный) в словарь.
    # Car(**car.dict()) - создаем новый объект Car (уже для алхимии он пригоден для добавления в БД) и в него распаковываем словарь

    # Можно было написать db_car = Car.model_validate(car)  через model_validate() который преобразует объект Pydantic в модель SQLAlchemy, при это дополнительно валидирует.
    # Или db_car = Car(**car.model_dump())

    db.add(db_car) # Добавляет объект Car в сессию. состояние готовое к коммиту.
    db.commit()
    db.refresh(db_car) # Обновление
    return {"ok": True, "msg": "Автомобоиль успешно добавлен!"}


@router.delete("/cars/{car_id}", tags=["Cars"], summary="Удалить автомобиль по ID")
def delete_car(car_id: int, db: Session = Depends(get_session)):
    # Ищем машину в базе
    db_car = db.query(Car).filter(Car.id == car_id).first()

    # Методы query и first - из алхимии и под капотом превращшаются в SQL.
    # query - создает новый запрос и говорит, что мы хотим работать с таблицей обекта Car
    # filter(Car.id == car_id) по сути добавляет условие WHERE к SQL-запросу
    # .first() выполняет запрос и возвращает только первый результат или None, если результатов нет. (без него падает ошибка)

    # Если машина не найдена
    if not db_car:
        raise HTTPException(status_code=404, detail="Автомобиль не найден")

    # Удаляем машину
    db.delete(db_car)
    db.commit()

    return {"ok": True, "msg": f"Автомобиль с ID {car_id} успешно удален"}



@router.put("/cars/{car_id}", tags=["Cars"], summary="Обновить автомобиль по ID")
def update_car(
    car_id: int,
    car_update: CarSchema,  # Данные для обновления
    db: Session = Depends(get_session)
):

    db_car = db.query(Car).filter(Car.id == car_id).first() # Ищем в БД авто

    if not db_car:
        raise HTTPException(status_code=404, detail=f"Автомобиль с ID {car_id} не найден")

    update_data = car_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_car, field, value)


    db.commit()
    db.refresh(db_car)

    return { "ok": True, "msg": f"Автомобиль с ID {car_id} успешно обновлен", "car": db_car}