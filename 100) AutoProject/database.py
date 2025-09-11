from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

# create_engine создает "движок" базы данных, который позволяет приложению взаимодействовать с БД. 
# Управляет подключениями к БД и предоставляет интерфейс для выполнения SQL-запросов.

# declarative_base создает базовый класс для моделей. Позволяет определять модели как классы Python, которые будут автоматически сопоставлены с таблицами в БД.

# sessionmaker создает сессии для работы с БД. Сессия - временное хранилище для объектов, которые мы хотим сохранить в БД. 

# Создание базы данных SQLite
DATABASE_URL = "sqlite:///./cars.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# check_same_thread=False для разрешения использования одного и того же соединения из разных потоков. Параметр позволяет избежать ошибок, при работе в многопоточном режиме.

# autocommit=False - коммиты прописываем вручную, так больше контроля
# autoflush=False - изменения в сессии не будут автоматически отправляться в БД пока не будет вызвано flush() или commit()


# Функция для получения сессии
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Создание всех таблиц
def init_db():
    Base.metadata.create_all(bind=engine)

