
from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from models import Task
from schemas import TaskResponse, TaskCreate, TaskPatch, TaskPut
from crud import create_new_task, get_task_by_name, update_field, update_task, delete_task, get_all_tasks, assign_task
from database import get_session
from fastapi import Query
from auth import get_current_user

task_router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)



@task_router.get("/")
def get_tasks(current_user=Depends(get_current_user),session: Session = Depends(get_session)):
    return get_all_tasks(session, current_user)

@task_router.post("/create-task", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return create_new_task(task, current_user, session)

@task_router.put("/update-task/{task_id}", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)    
def update_existing_task(
    task_id: int,
    task: TaskPut,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return update_task(task_id, task,current_user, session)

@task_router.patch("/update-field/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def patch_task(
    task_id: int,
    task: TaskPatch,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return update_field(task_id, task, current_user, session)

@task_router.get("/search", response_model=TaskResponse)
def search_task(
    task_name: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_task_by_name(task_name, current_user, session)

@task_router.delete("/delete/{task_id}", response_model=TaskResponse)
def remove_task(
    task_id: int,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return delete_task(task_id, current_user, session)

    


#PATCH /tasks/5/assign/1
@task_router.patch("/{task_id}/assign/{user_id}")
def assign_task_to_user(
    task_id, user_id, 
    current_user=Depends(get_current_user),
    session=Depends(get_session)
):
    return assign_task(task_id, user_id, current_user, session)


#pagination
@task_router.get("/all-tasks/")
def pagination(
        skip:int = Query(0, ge=0), limit:int=Query(10, ge=1, le=100), current_user=Depends(get_current_user), session=Depends(get_session)
):
   tasks = session.exec(
        select(Task).where(Task.user_id == current_user.id).offset(skip).limit(limit)
    ).all()
   
   return tasks
@task_router.get("/query")
def get_non_completed_tasks(
    completed:bool,
    current_user=Depends(get_current_user),
    session=Depends(get_session)
):
    tasks_not_completed = session.exec(
        select(Task).where(Task.user_id == current_user.id,Task.task_status == completed)
    ).all()
    return tasks_not_completed
    
    
