"Pause this function until this task finishes, but let the server work on other requests in the meantime."
from fastapi import FastAPI, Depends, HTTPException, status
# from pydantic import BaseModel
# from fastapi import status
# from typing import Optional
# from fastapi import HTTPException
from database import create_db_tables
from contextlib import asynccontextmanager
from database import get_session
from sqlmodel import Session, select
from models import Task, TaskCreate, TaskPut, TaskPatch


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield
    

app = FastAPI(lifespan=lifespan)
# tasks = []

    

@app.get("/tasks")
def get_all_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks


@app.post("/tasks/create-task", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_new_task(task: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit() #INSERT save changes permanently
    session.refresh(db_task)
    return db_task

@app.put("/tasks/update-task/{task_id}", response_model=Task, status_code=status.HTTP_202_ACCEPTED)
def update_task(task_id: int, task:TaskPut, session: Session = Depends(get_session)):
    task_to_update = session.exec(
        select(Task).where(Task.task_id == task_id)
    ).first()

    if task_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Replace the entire resource
    task_to_update.task_name = task.task_name
    task_to_update.task_status = task.task_status

    session.add(task_to_update)
    session.commit()
    session.refresh(task_to_update)

    return task_to_update




    

@app.patch("/tasks/update-field/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_field(task_id, task: TaskPatch, session: Session = Depends(get_session)):
    task_to_update = session.exec(
        select(Task).where(task.task_id == task_id)
    ).first()

    if task_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task Not Found"

        )
    if task.task_name is not None:
        task_to_update.task_name = task.task_name
    if task.task_status is not None:
        task_to_update.task_status = task.task_status
    session.add(task_to_update)
    session.commit()
    session.refresh(task_to_update)

    return task_to_update

@app.get("/tasks/search", response_model=Task)
def get_task_by_name(task_name:str, session: Session=Depends(get_session)):
    task_to_get = session.exec(
        select(Task).where(Task.task_name == task_name)
    ).first()
    if task_to_get is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task_to_get

@app.delete("/tasks/delete/{task_id}", response_model=Task)
def delete_task(task_id: int, session:Session = Depends(get_session)):
    task_to_delete = session.exec(
        select(Task).where(Task.task_id == task_id)
    ).first()
    if task_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    session.delete(task_to_delete)
    session.commit()
    return task_to_delete






