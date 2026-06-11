from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import crud
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo Manager API",
    description="A professional Todo Management REST API built with FastAPI and PostgreSQL",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Todo Manager API is running", "docs": "/docs"}


@app.get("/tasks", response_model=List[schemas.TaskResponse], tags=["Tasks"])
def get_all_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all tasks, ordered by creation date (newest first)."""
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.get("/tasks/stats", response_model=schemas.TaskStats, tags=["Tasks"])
def get_stats(db: Session = Depends(get_db)):
    """Get task statistics: total, completed, and pending counts."""
    return crud.get_task_stats(db)


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a single task by ID."""
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    return task


@app.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    return crud.create_task(db, task)


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Update a task's title, description, or completion status."""
    task = crud.update_task(db, task_id, task_update)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    return task


@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def toggle_task(task_id: int, toggle: schemas.TaskToggle, db: Session = Depends(get_db)):
    """Toggle the completion status of a task."""
    task = crud.toggle_task(db, task_id, toggle)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task by ID."""
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
