from sqlalchemy.orm import Session
from sqlalchemy import func
import models
import schemas


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).order_by(models.Task.created_at.desc()).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=False,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def toggle_task(db: Session, task_id: int, toggle: schemas.TaskToggle):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    db_task.completed = toggle.completed
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True


def get_task_stats(db: Session):
    total = db.query(func.count(models.Task.id)).scalar()
    completed = db.query(func.count(models.Task.id)).filter(models.Task.completed == True).scalar()
    pending = total - completed
    return schemas.TaskStats(total=total, completed=completed, pending=pending)
