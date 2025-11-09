# Здесь будем реализовывать логику которая позволит работать с БД как с коллекцией объектов
# Автор рассматривал упрщенный вариант, поэтому на него сильнго не ориентируемся

from database import new_session, TaskOrm
from schemas import STaskAdd, STask
from sqlalchemy import select

class TaskRepository():

    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump() # model_dump перобразует к виду словаря

            task = TaskOrm(**task_dict)  # TaskOrm Описана в database.py
            session.add(task)  # Добавляем обхект task в сессию
            await session.flush()  # Это команда которая идет в БД и получает id из автоинкремента (как раз этот id мы и возвращаем в return)
            await session.commit()   # Это коммит - то есть все изменения что мы прописали выше будут добавлены в БД
            return task.id   # Возвращаем id таски что бы ее идентифицировать


    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session: # Объявляем контекстный менеджер сессии
            query = select(TaskOrm)   # Здесь отбираем все таски
            result = await session.execute(query) # В этой строке говорим: сходи в БД и исполни этот запрос (query)
            task_models = result.scalars().all()
            # task_model это результат который мы получаем в качестве ответа и он является итератором
            # Мы можем взаимодествовать по разному. Например: result.all() верни все объекты, result.first() - первый, result.one_or_none() - один или ничего
            # или result.one() верни строго 1 объект

            task_schemas = [STask.model_validate(task_model) for task_model in task_models]  # Мы говорим провалидируй таску (посмотри что она соответствует модели STask) и верни схему
            return task_schemas
