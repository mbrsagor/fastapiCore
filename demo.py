"""
FastAPI CRUD Application
------------------------
- Database: PostgreSQL
- ORM: SQLAlchemy
- Validation: Pydantic
- Entity: Note (id, title, content)
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# -------------------------------------------------------------------
# DATABASE CONFIGURATION
# -------------------------------------------------------------------

# Update with your PostgreSQL credentials
DATABASE_URL = "postgresql://postgres:password@localhost:5432/note"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# -------------------------------------------------------------------
# DATABASE MODEL
# -------------------------------------------------------------------

class Note(Base):
    """
    SQLAlchemy model for the notes table
    """
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)


# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


# -------------------------------------------------------------------
# PYDANTIC SCHEMAS
# -------------------------------------------------------------------

class NoteCreate(BaseModel):
    """
    Schema for creating a note
    """
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)


class NoteUpdate(BaseModel):
    """
    Schema for updating a note
    """
    title: str | None = Field(None, min_length=1, max_length=255)
    content: str | None = Field(None, min_length=1)


class NoteResponse(BaseModel):
    """
    Schema for returning note data
    """
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True


# -------------------------------------------------------------------
# DEPENDENCY
# -------------------------------------------------------------------

def get_db():
    """
    Provides a database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------------------------
# FASTAPI APP
# -------------------------------------------------------------------

app = FastAPI(title="Notes CRUD API", version="1.0.0")


# -------------------------------------------------------------------
# CRUD ENDPOINTS
# -------------------------------------------------------------------

@app.post("/notes", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    """
    Create a new note
    """
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@app.get("/notes", response_model=List[NoteResponse])
def get_all_notes(db: Session = Depends(get_db)):
    """
    Retrieve all notes
    """
    return db.query(Note).all()


@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a note by ID
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_data: NoteUpdate, db: Session = Depends(get_db)):
    """
    Update an existing note
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content

    db.commit()
    db.refresh(note)
    return note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """
    Delete a note
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}
