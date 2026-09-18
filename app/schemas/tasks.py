from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    name: str
    priority: int

class TaskUpdate(BaseModel):
    name: str | None = None
    priority: int | None = None
    status: bool | None = None

class TaskOut(BaseModel):
    id: int
    name: str
    priority: int
    status: bool
    create_time: datetime
    update_time: datetime | None

    class Config:
        from_attributes = True