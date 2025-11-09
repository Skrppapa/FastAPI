from typing import Annotated
from schemas import STaskAdd, STask, STaskId
from fastapi import Depends, APIRouter
from repository import TaskRepository


router = APIRouter(
    prefix="/tasks", # Префикс. Теперь не нужно в ручках писать /tasks
    tags=["Таски"]
)


@router.post("")
async def add_task(
    task: Annotated[STaskAdd, Depends()],  # За счет Annotated и Depends() в docs будут удобные поля для ввода
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}


@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    return list(tasks)
