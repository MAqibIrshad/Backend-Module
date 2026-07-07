
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from models import Task
from schemas import TaskResponse, TaskCreate, TaskPatch, TaskPut
from crud import get_user_by_name, update_user_field, update_user, delete_user, get_all_users, register_user
from database import get_session
from schemas import UserCreate, UserPatch, UserPut, UserResponse, UserRead, UserLogin, Token
from auth import create_access_token, get_current_user, verifyPassword
from models import User


user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@user_router.get("/")
def get_users(current_user= Depends(get_current_user), session: Session = Depends(get_session)):
    return get_all_users(current_user, session)

@user_router.post("/create-user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    return register_user(user, session)

@user_router.post("/login", response_model=Token, status_code=status.HTTP_202_ACCEPTED)
def login_user(user: UserLogin, session=Depends(get_session)):
    db_user = session.exec(
        select(User).where(User.user_name == user.user_name)
    ).first()
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    if not verifyPassword(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid Username or Password"
        )
    access_token = create_access_token(
        data={"sub": db_user.user_name}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@user_router.put("/update-user/{user_id}", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)    
def update_existing_user(
    user_id: int,
    user: UserPut,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return update_user(user_id, user, current_user, session)

@user_router.patch("/update-user-field/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def patch_user(
    user_id: int,
    task: UserPatch,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return update_user_field(user_id, task, current_user, session)

@user_router.get("/search", response_model=UserResponse)
def search_user(
    user_name: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_user_by_name(user_name, current_user, session)

@user_router.delete("/delete/{user_id}", response_model=UserResponse)
def remove_user(
    user_id: int,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return delete_user(user_id, current_user, session)



    





