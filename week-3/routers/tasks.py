
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from models import Task
from schemas import TaskResponse, TaskCreate, TaskPatch, TaskPut
from crud import create_new_task, get_task_by_name, update_field, update_task, delete_task, get_all_tasks, assign_task
from database import get_session
task_router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)



@task_router.get("/")
def get_tasks(session: Session = Depends(get_session)):
    return get_all_tasks(session)

@task_router.post("/create-task", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session)
):
    return create_new_task(task, session)

@task_router.put("/update-task/{task_id}", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)    
def update_existing_task(
    task_id: int,
    task: TaskPut,
    session: Session = Depends(get_session)
):
    return update_task(task_id, task, session)

@task_router.patch("/update-field/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def patch_task(
    task_id: int,
    task: TaskPatch,
    session: Session = Depends(get_session)
):
    return update_field(task_id, task, session)

@task_router.get("/search", response_model=TaskResponse)
def search_task(
    task_name: str,
    session: Session = Depends(get_session)
):
    return get_task_by_name(task_name, session)

@task_router.delete("/delete/{task_id}", response_model=TaskResponse)
def remove_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    return delete_task(task_id, session)

    


#PATCH /tasks/5/assign/1
@task_router.patch("/{task_id}/assign/{user_id}")
def assign_task_to_user(
    task_id, user_id, session=Depends(get_session)
):
    return assign_task(task_id, user_id, session)


