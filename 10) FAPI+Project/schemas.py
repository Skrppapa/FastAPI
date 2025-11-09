from pydantic import BaseModel, ConfigDict
from typing import Optional

class STaskAdd(BaseModel):
    name: str
    description: Optional[str] = None   # По идее должно было сработать str | None


class STask(STaskAdd):
    id: int

class STaskId(BaseModel):
    ok: bool = True
    task_id: int