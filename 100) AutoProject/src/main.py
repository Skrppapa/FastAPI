from fastapi import FastAPI
import uvicorn
from src.api import main_router

app = FastAPI()
app.include_router(main_router)


# Файл main.py держим наиболее лаконичным


#if __name__ == '__main__':
#    uvicorn.run('main:app')

# Переход cd '100) AutoProject'
# Активация Linux source venv_auto_linux/bin/activate
# Активация Windows . venv_auto_win\Scripts\activate

# uvicorn src.main:app --reload --host 0.0.0.0 --port 8000