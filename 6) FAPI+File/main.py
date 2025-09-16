from fastapi import FastAPI, File, UploadFile
import uvicorn

# File для работы с файлами
# UploadFile загрузка файла


app = FastAPI()


@app.post("/file") # Ручка загрузки файла
async def upload_file(uploaded_file: UploadFile): # Структура данных UploadFile
    file = uploaded_file.file
    filename = uploaded_file.filename
    with open(f"1_{filename}", "wb") as f:
        f.write(file.read())





if __name__ == '__main__':
    uvicorn.run('main:app')

# Активация . fileenv\Scripts\activate

# uvicorn main:app --reload


# Закончил урок с файлами на 4:30