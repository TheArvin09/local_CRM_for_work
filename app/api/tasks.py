from app.data_bases.sessions import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.tasks import TaskCreate, TaskUpdate, TaskOut
from sqlalchemy.orm import Session
from app.data_bases.models import TasksBase

router = APIRouter()

@router.get("/tasks", response_model=list[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TasksBase).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TasksBase).filter(TasksBase.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    newtask = TasksBase(
        name=task.name,
        priority=task.priority,
        status=False
    )
    db.add(newtask)
    db.commit()
    db.refresh(newtask)
    return newtask

@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(TasksBase).filter(TasksBase.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_update.status is not None:
        task.status = task_update.status

    if task_update.priority is not None:
        task.priority = task_update.priority

    if task_update.name is not None:
        task.name = task_update.name

    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TasksBase).filter(TasksBase.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
