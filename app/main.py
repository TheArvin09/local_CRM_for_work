from fastapi import FastAPI, HTTPException, Form, Request, Depends
from fastapi.responses import RedirectResponse
from app.api.tasks import router as tasks_router
from app.api.notes import router as notes_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.data_bases.sessions import get_db
from app.data_bases.models import TasksBase, NotesBase
from datetime import timezone
from zoneinfo import ZoneInfo


app = FastAPI()

app.include_router(tasks_router, prefix='/api')
app.include_router(notes_router, prefix='/api')

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

def format_local_timezone(dt):
    if dt is None:
        return "-"

    dt_utc = dt.replace(tzinfo=timezone.utc)
    dt_local = dt_utc.astimezone(ZoneInfo("Asia/Yekaterinburg"))
    return dt_local.strftime('%d.%m.%Y %H:%M')

templates.env.filters["format_local_timezone"] = format_local_timezone

def priority_label(priority: int) -> str:
    labels = {0: "Без приоритета",1: "Высокий", 2: "Средний", 3: "Низкий", 4: "Отложенная"}
    return labels.get(priority, "Неизвестно")

templates.env.filters["priority_label"] = priority_label

def status_label(status: bool) -> str:
    labels = {True: "Выполнена", False: "Не выполнена"}
    return labels.get(status, "Неизвестно")

templates.env.filters["status_label"] = status_label

@app.get("/")
def tasks_page(request: Request, priority: str = "", status: str = "", db: Session = Depends(get_db)):
    query = db.query(TasksBase)

    if priority != "":
        query = query.filter(TasksBase.priority == int(priority))

    if status != "":
        status_bool = status == "True"
        query = query.filter(TasksBase.status == status_bool)

    tasks = query.order_by(TasksBase.id).all()

    tasks_with_notes = []
    for task in tasks:
        last_note = (
            db.query(NotesBase)
            .filter(NotesBase.task_id == task.id)
            .order_by(NotesBase.create_time.desc())
            .first()
        )
        tasks_with_notes.append({"task": task, "last_note": last_note})

    return templates.TemplateResponse(request, "tasks.html", {
        "tasks_with_notes": tasks_with_notes,
        "selected_priority": priority,
        "selected_status": status
    })

@app.get("/tasks/{task_id}")
def task_page(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(TasksBase).filter(TasksBase.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    notes = db.query(NotesBase).filter(NotesBase.task_id == task_id).order_by(NotesBase.create_time.desc()).all()

    return templates.TemplateResponse(request, "task_detail.html", {"task": task, "notes": notes})

@app.post("/tasks/create")
def create_task_form(
        name: str = Form(...),
        priority: int = Form(...),
        db: Session = Depends(get_db)
):
    new_task = TasksBase(name=name, priority=priority, status=False)
    db.add(new_task)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/tasks/{task_id}/delete")
def delete_task_form(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TasksBase).filter(TasksBase.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/tasks/{task_id}/toggle_status")
def toggle_task_status(task_id: int, redirect_to: str = Form("/"), db: Session = Depends(get_db)):
    task = db.query(TasksBase).filter(TasksBase.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = not task.status
    db.commit()
    return RedirectResponse(url=redirect_to, status_code=303)

@app.post("/tasks/{task_id}/update_priority")
def update_priority(task_id: int, priority: int = Form(...), redirect_to: str = Form("/"), db: Session = Depends(get_db)):
    task = db.query(TasksBase).filter(TasksBase.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.priority = priority
    db.commit()
    return RedirectResponse(url=redirect_to, status_code=303)

@app.post("/tasks/{task_id}/notes/create")
def create_note(
        task_id: int,
        text: str = Form(...),
        db: Session = Depends(get_db)
):
    task = db.query(TasksBase).filter(TasksBase.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    note = NotesBase(text=text, task_id=task_id)
    db.add(note)
    db.commit()
    return RedirectResponse(url=f"/tasks/{task_id}", status_code=303)

@app.post("/notes/{note_id}/delete")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(NotesBase).filter(NotesBase.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    task_id = note.task_id
    db.delete(note)
    db.commit()
    return RedirectResponse(url=f"/tasks/{task_id}", status_code=303)

@app.post("/notes/{note_id}/update")
def update_note(
        note_id: int,
        text: str = Form(...),
        db: Session = Depends(get_db)
):
    note = db.query(NotesBase).filter(NotesBase.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.text = text
    task_id = note.task_id
    db.commit()
    return RedirectResponse(url=f"/tasks/{task_id}", status_code=303)