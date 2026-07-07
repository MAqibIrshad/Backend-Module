from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from schemas import TaskCreate, TaskPatch, TaskPut
from schemas import User, UserCreate, UserPatch, UserPut
from models import User, Task
from auth import get_current_user, hashPassword

def get_all_tasks(session: Session, current_user):
    tasks = session.exec(select(Task).where(Task.user_id == current_user.user_id)).all()
    return tasks

def create_new_task(task: TaskCreate,current_user: User,session: Session):
    new_task = Task(
        title=task.title,
        description=task.description,
        user_id=current_user.id
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task

def update_task(task_id: int, task:TaskPut, current_user: User, session: Session = Depends(get_session)):
    task_to_update = session.exec(
        select(Task).where(Task.task_id == task_id)
    ).first()

    if task_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task_to_update.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update"
        )

    # Replace the entire resource
    task_to_update.task_name = task.task_name
    task_to_update.task_status = task.task_status

    session.add(task_to_update)
    session.commit()
    session.refresh(task_to_update)

    return task_to_update


    
def update_field(task_id, task: TaskPatch, current_user:User, session: Session = Depends(get_session)):
    task_to_update = session.exec(
        select(Task).where(task.task_id == task_id)
    ).first()

    if task_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task Not Found"

        )
    
    if task_to_update.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update field"
        )

    if task.task_name is not None:
        task_to_update.task_name = task.task_name
    if task.task_status is not None:
        task_to_update.task_status = task.task_status
    session.add(task_to_update)
    session.commit()
    session.refresh(task_to_update)

    return task_to_update

    
def get_task_by_name(task_name:str,  current_user:User, session: Session=Depends(get_session)):
    task_to_get = session.exec(
        select(Task).where(Task.task_name == task_name)
    ).first()

    if task_to_get is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if task_to_get.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update"
        )

    return task_to_get

    
def delete_task(task_id: int, current_user:User, session:Session = Depends(get_session)):
    task_to_delete = session.exec(
        select(Task).where(Task.task_id == task_id)
    ).first()
    if task_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    

    if task_to_delete.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update"
        )

    session.delete(task_to_delete)
    session.commit()
    return task_to_delete



def get_all_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

def register_user(
        user:UserCreate,
        session=Depends(get_session)
):
    db_user = User(
        user_name=user.user_name,
        email=user.email,
        password=hashPassword(user.password)
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
    
# def create_new_user(user: UserCreate, session: Session = Depends(get_session)):
#     db_user = User.model_validate(user)
#     session.add(db_user)
#     session.commit() #INSERT save changes permanently
#     session.refresh(db_user)
#     return db_user

def update_user(user_id: int, user:UserPut, current_user:User, session: Session = Depends(get_session)):
    user_to_update = session.exec(
        select(User).where(User.user_id == user_id)
    ).first()

    if user_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user_to_update.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update user"
        )
    # Replace the entire resource
    user_to_update.user_name = user.user_name
    user_to_update.user_status = user.user_status

    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)

    return user_to_update


    
def update_user_field(user_id, user:UserPatch, current_user:User, session: Session = Depends(get_session)):
    user_to_update = session.exec(
        select(User).where(User.user_id == user_id)
    ).first()

    if user_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"

        )
    
    if user_to_update.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update user"
        )
    if user.user_name is not None:
        user_to_update.user_name = user.user_name
    if user.user_status is not None:
        user_to_update.user_status = user.user_status
    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)

    return user_to_update

    
def get_user_by_name(user_name:str, current_user=Depends(get_current_user), session: Session=Depends(get_session)):
    user_to_get = session.exec(
        select(User).where(User.user_name == user_name)
    ).first()
    if user_to_get is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user_to_get.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to get user by name"
        )
    
    return user_to_get

    
def delete_user(user_id: int, current_user=Depends(get_current_user),session:Session = Depends(get_session)):
    user_to_delete = session.exec(
        select(User).where(User.user_id == user_id)
    ).first()
    if user_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user_to_delete.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete user"
        )
    session.delete(user_to_delete)
    session.commit()
    return user_to_delete

def assign_task(task_id, user_id, current_user: User, session=Depends(get_session)):
    task = session.exec(
        select(Task).where(Task.task_id == task_id)
    ).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task Not Found"
        )
    user = session.exec(
        select(User).where(User.user_id == user_id)
    ).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
   

    task.user_id = current_user.user_id
    session.add(task)
    session.commit()

    #user = session.get(User, 1)
    #task.user = user   ORM WAY ASSIGNING WHOLE USER OBJECT
    #we can also get tasks of user
    # user = session.get(User, 1)
    user = session.get(User, user_id)
    print(user.tasks)
    return task
