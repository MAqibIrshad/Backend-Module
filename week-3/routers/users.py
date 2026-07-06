
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from models import Task
from schemas import TaskResponse, TaskCreate, TaskPatch, TaskPut
from crud import create_new_user, get_user_by_name, update_user_field, update_user, delete_user, get_all_users
from database import get_session
from schemas import User, UserCreate, UserPatch, UserPut, UserResponse
user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@user_router.get("/")
def get_users(session: Session = Depends(get_session)):
    return get_all_users(session)

@user_router.post("/create-user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    return create_new_user(user, session)

@user_router.put("/update-user/{user_id}", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)    
def update_existing_user(
    user_id: int,
    user: UserPut,
    session: Session = Depends(get_session)
):
    return update_user(user_id, user, session)

@user_router.patch("/update-user-field/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def patch_user(
    user_id: int,
    task: UserPatch,
    session: Session = Depends(get_session)
):
    return update_user_field(user_id, task, session)

@user_router.get("/search", response_model=UserResponse)
def search_user(
    user_name: str,
    session: Session = Depends(get_session)
):
    return get_user_by_name(user_name, session)

@user_router.delete("/delete/{user_id}", response_model=UserResponse)
def remove_task(
    user_id: int,
    session: Session = Depends(get_session)
):
    return delete_user(user_id, session)



    





