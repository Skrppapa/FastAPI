from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel

app = FastAPI()

# Есть 2 оснонвых подхода работы с аутентификацией и авторизацией
# 1) Токен передается с бека на фронт и с фронта на бэк в заголовках
# 2) Чрезе куки

# Если мы разрабатываем мобильное приложение, или у нас есть и сайт и мобилка - то это точно заголовки. У мобилки нет куков
# Если же у нас только вэб сайт то можно использовать любой вариант


# ВАЖНО!
# Аутентификация - это сверка имя и пароля полдьзователя. То есть мы проверям пускаем его или нет
# Авторизация - это проверка прав пользователя внутри сайта. Имеет ли он доступ к такому то фнукционалу

# Делаем свой конфиг
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY" # Секретный ключ который позволяет создавать токены (Его никогда никому не показываем!!!)
config.JWT_ACCESS_COOKIE_NAME = "my_access_token" # Название токена
config.JWT_TOKEN_LOCATION = ["cookies"] # Указываем что JWT будет храниться в куках

security = AuthX(config=config) # Создаем экземпляр класса AuthX и говорим использовать наш конфиг

class UserLoginSchema(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(creds: UserLoginSchema, response: Response):
    if creds.username == "test" and creds.password == "test": # Здесь пишем test для примера. В реальном проекте мы берем реальные имя и пароль из БД
        token = security.create_access_token(uid="12345") # Генерация токена
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token} # Отдаем токен
    raise HTTPException(status_code=401, detail="Incorrect username or password") # Обязательно указываем 401 ошибку - Ошибка авторизации

# create_access_token() - в токене должна хранится не чувствительная информация, поскольку ее могут просмотреть другие. Точнее его можно легко декодировать (jwt.io)
# Примечательно - токены удобная вещь, но есть существенный минус, они много весят. В высоконагруженных системах это решает.
# Строка response упаковывает токен в куки, наподобии формата ключ: значение
# И вот после авторизации у нас появлятся куки - который с каждым запрособ будет посылаться в довесок, что бы сайт понимал кто вы


# Защищенная ручка
@app.get("/protected", dependencies = [Depends(security.access_token_required)]) # Прописываем, что доступ к этой ручке имеет только авторизованный пользователь
def protected():
    return {"data": "TOP_SECRET"}


if __name__ == '__main__':
    uvicorn.run('main:app')

# Активация . authvenv\Scripts\activate

# uvicorn main:app --reload