import pytest
from httpx import AsyncClient, ASGITransport # httpx позволяет тестировать API не поднимая uvicorn. То есть не запуская приложение
from main import app # Ждя асинхронных тестов нужно импортировать само приложение



def func (num):
    return 1 / num  # Может быть ошибка что мы делим на 0

def test_func():   # Тестовые функции пишутся test_(название фкнкции)
    assert func(1) == 1   # Буквально говорим - убедись что при вызове с 1 результат будет 1
    assert func(2) == 0.5 # убедись что при вызове с 2 результат будет 0.5

# При вводе в терминале pytest он сам находит все функции которые мы тестируем, все папки в которых они лежат и тестирует. Ничего указывать не надо

# Запустить можно через терминал командой pytest
# Для более красивого вывода - pytest -v
# Не маловажно - по умолчанию pytest принты не отображает. Поэтому есть команда pytest -s


#  === Основные тесты===

@pytest.mark.asyncio  # Для асинхронных тестов всегда помечаем этим декоратором @pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/books")  # response в данном случае просто переменная
        assert response.status_code == 200   # Убедись что код статуса будет ок

        data = response.json()   # print(response)
        assert len(data) == 2   # Убедись что длинна списка 2 (т.к. у нас внесено 2 книги в main)
        # Можно так же тестировать, например что взвращаемый объект соответствует pydentic схеме или имеет все необходимые поля


# Мы не можем просто делать запрос к нашей API - для этого нам нужен контекстный мнеджер (with)
# AsyncClient - это клиент который будет делать запросы
# В ASGITransport нужно обязательно передать приложение


@pytest.mark.asyncio
async def test_add_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/books", json = {
            "title": "Title",
            "author": "Author"
        })
        assert response.status_code == 200

        data = response.json()
        assert data == {"success": True, "message": "Книга добавлена"}  # Убедись что data содержит ровно такой ответ как в приложении


# Лучше всего использовать pytest -s -v


# Важно!
# Выше написаны 1 юнит-тест и 2 интеграционных теста.
# Юнит тест - тестирование одной отдельно взятой функции, которую можно внедрить в другой проект с другой инфраструктурой и он заработает
# Интеграционный (чаще всего тестирование API относят к ним) - тетсирование модуля (ручки) интегрированной в определенную инфраструктуру приложения