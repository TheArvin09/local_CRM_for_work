from pydantic import BaseModel
from datetime import datetime

class NoteCreate(BaseModel):
    text: str

class NoteUpdate(BaseModel):
    text: str | None = None

class NoteOut(BaseModel):
    id: int
    text: str
    update_time: datetime | None = None
    create_time: datetime
    class Config:
        from_attributes = True