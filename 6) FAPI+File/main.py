from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse
import uvicorn

# File для работы с файлами
# UploadFile загрузка файла

# StreamingResponse Для работы с файлами в облаке
# FileResponse Для работы с локальными файлами


app = FastAPI()


@app.post("/file") # Ручка загрузки файла
async def upload_file(uploaded_file: UploadFile): # Структура данных UploadFile
    file = uploaded_file.file
    filename = uploaded_file.filename
    with open(f"1_{filename}", "wb") as f:
        f.write(file.read())


@app.post("/multiple_files") # Ручка загрузки нескольких файлов
async def upload_file(uploaded_files: list[UploadFile]): # Делаем список для загрузки нескольких файлов
    for uploaded_file in uploaded_files:
        file = uploaded_file.file
        filename = uploaded_file.filename
        with open(f"1_{filename}", "wb") as f:
            f.write(file.read())


# Есть 3 подхода
# 1) Когда файлы лежат на диске - мы их загружаем в память и отдаем пользователю
# 2) Когда файлы находятся в облачном хранилище. Они могут быть большого объема. И нет смысла сначала загонять в память и потом отдавать юзеру. Обычно используют стриминг

# Если файл хранится локально
@app.get("/file/{filename}")
async def get_file(filename: str):
    return FileResponse(filename)


def iterfile(filename: str):
    with open(filename, "rb") as file: # Считываем данные (режим "rb")
        # Если бы мы написали ниже yield file.read() - Это было бы равноценно полной загрузке файла в память и отдаче его юзеру
        while chunk := file.read(1024 * 1024): # Поэтому мы считываем кусочек (Часто называют chunk), например видео,и отдаем его юзеру
            yield chunk # Присваеваем этому кусочку имя chunk (строка выше, присваиваем через моржа). И отдаем.

# Если файл хранится в облаке

# Для стриминга файлов нам нужен генератор - создали его выше. Это то что будет разбивать и отдавать файл по частям.
@app.get("/file/streaming/{filename}")
async def get_streaming_file(filename: str):
    return StreamingResponse(iterfile(filename), media_type="video/mp4") # И вот теперь мы возвращаем генератор который для нашего файла (filename) выдает кусочки

# В документации не очень хорошо получается протестировать пример с видео
# Поэтому лучше ввести http://127.0.0.1:8000/file/streaming/video.mp4 и выйдет само видео. Можно увидеть что ползунок немного не догоняет прогрузку - это и есть стриминг

if __name__ == '__main__':
    uvicorn.run('main:app')

# Активация . fileenv\Scripts\activate

# uvicorn main:app --reload


# Закончил урок с файлами на 4:30