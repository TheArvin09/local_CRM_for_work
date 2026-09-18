from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, Text
from datetime import datetime

class BaseModel(DeclarativeBase):
    pass

class TasksBase(BaseModel):
    __tablename__ = 'tasks'

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(256), nullable=False)
    priority:Mapped[int] = mapped_column(Integer, nullable=False)
    status:Mapped[bool] = mapped_column(Boolean, nullable=False)
    create_time:Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    update_time:Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default = datetime.utcnow, onupdate=datetime.utcnow)
    notes: Mapped[list["NotesBase"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan"
    )

class NotesBase(BaseModel):
    __tablename__ = 'notes'

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id:Mapped[int] = mapped_column(ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    text:Mapped[str] = mapped_column(Text, nullable=False)
    create_time:Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    update_time:Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default = datetime.utcnow, onupdate=datetime.utcnow)
    task: Mapped["TasksBase"] = relationship(back_populates="notes")