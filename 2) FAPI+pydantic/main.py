
# Пример использования библиотеки Pydantic
# Сразу рассмотрим в связке с FAPI
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, ConfigDict  # pydantic библиотека для валидации данных.
import uvicorn

# BaseModel - то чем будешь пользоватся ежедневно
# Field - аналогично, большой инструмент для валидации
# EmailStr - аналогично, валидация мэйла
# ConfigDict - Позволят регулировать поведение в отношении передаваемого словаря

app = FastAPI() # Создаем экз приложения

# Есть какой то словарь
data = {
    'mail': "abc@mail.ru",
    'bio': "Это моя биография",
    'age': 12
    }

data_without_mail = {
    'bio': "Это моя биография",
    'age': 12
    #'birthday': "2022", # Параметр который не ожидаем получить
    #'gender': 'man'     # Параметр который не ожидаем получить
    }

# Делаем класс для валидации. В названии часто прибавляют слово Schema
class UserSchema(BaseModel): # Обязательно, всегда наследуемся от класса BaseModel
    bio: str | None = Field(max_length=1000)
    age: int = Field(ge = 0, le = 130) # grated or equal (ge) больше или равен. less or equal (le) меньше или равен

    model_config = ConfigDict(extra="forbid") # Буквально - запрети дополнительные параметры


users = [] # Пустой список куда будем складывать пользователей

@app.post('/users') # Ручка на добавление юзера с валидацией (Обрати внимание на user: UserSchema. То етсь добавится только валидный юзер)
def add_user(user: UserSchema):
    users.append(user)
    return {'ok': True, 'msg': 'Юзер добавлен'}


@app.get('/users')
def add_user() -> list[UserSchema]: # За счет -> list[UserSchema] в документации отразится пример выходных данных
    return users


# Помимо подробного описания ошибки невалидных данных, удобно, что можно наследоватся от других классов
# class UserMailSchema(UserSchema): # Наследуемся уже от нашего вышесозданного класса
#    mail: EmailStr # Поля bio и age Унаследовались


# print(repr(UserSchema(**data_without_age)))
# print(repr(UserMailSchema(**data)))
# repr функция для красивого отображения объекта Python

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)


# Активация окружения . fapidantic\Scripts\activate
# Запуск python main.py