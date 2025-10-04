from fastapi import APIRouter
from src.api.cars import router as car_router
from src.api.mainpage import router as mainpage_router
# from src.api.users import router as user_router   - это когда юзеры появятся


main_router = APIRouter()
main_router.include_router(car_router)  # Делаем в этой папке главный роутер в котором будут стянуты все остальные и уже его импортируем в main.py
main_router.include_router(mainpage_router)