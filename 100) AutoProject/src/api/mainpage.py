from fastapi import APIRouter

router = APIRouter()

@router.get('/', tags = ["Home"], summary = "Главная страница")
def root():
    return "Main Page"