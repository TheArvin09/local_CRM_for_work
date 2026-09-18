from app.schemas.notes import NoteCreate, NoteUpdate, NoteOut
from app.data_bases.sessions import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.data_bases.models import TasksBase, NotesBase

router = APIRouter()

@router.get("/tasks/{task_id}/notes", response_model=list[NoteOut])
def get_notes(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TasksBase).filter(TasksBase.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    notes = db.query(NotesBase).filter(NotesBase.task_id == task_id).all()
    return notes

@router.get("/notes/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(NotesBase).filter(NotesBase.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.post("/tasks/{task_id}/notes", response_model=NoteOut)
def create_note(task_id: int,note: NoteCreate, db: Session = Depends(get_db)):
    task = db.query(TasksBase).filter(TasksBase.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    new_note = NotesBase(
        task_id=task_id,
        text=note.text
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.put("/tasks/{task_id}/notes/{note_id}", response_model=NoteOut)
def update_note(task_id: int, note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db)):
    task = db.query(TasksBase).filter(TasksBase.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    note = db.query(NotesBase).filter(NotesBase.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    if note_update.text is not None:
        note.text = note_update.text

    db.commit()
    db.refresh(note)
    return note

@router.delete("/tasks/{task_id}/notes/{note_id}")
def delete_note(task_id: int, note_id: int, db: Session = Depends(get_db)):
    task = db.query(TasksBase).filter(TasksBase.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    note = db.query(NotesBase).filter(NotesBase.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()