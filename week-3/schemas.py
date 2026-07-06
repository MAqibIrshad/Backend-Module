from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    task_id:Optional[int]
    task_name:str
    task_status:bool = False


class TaskCreate(BaseModel):
    task_name:str
    task_status:bool = False
    user_id :int

class TaskPatch(BaseModel):
    task_name: Optional[str] = None
    task_status: Optional[bool] = None
    user_id:Optional[bool] = None

class TaskPut(BaseModel):
    task_name:str
    task_status:bool
    user_id:int

class TaskResponse(BaseModel):
    task_id: int
    task_name: str
    task_status: bool
    user_id:int

    model_config = {
        "from_attributes": True
    }

class User(BaseModel):
    user_id:Optional[int]
    user_name:str
    user_status:bool = False

class UserCreate(BaseModel):
    user_name:str
    user_status:bool = False

class UserPatch(BaseModel):
    user_id:Optional[int] = None
    user_name: Optional[str] = None
    user_status: Optional[bool] = None

class UserPut(BaseModel):
    user_name:str
    user_status:bool

class UserResponse(BaseModel):
    user_id: int
    user_name: str
    user_status: bool

    model_config = {
        "from_attributes": True
    }

class UserWithTasksResponse(UserResponse):
    tasks: list[TaskResponse] = []

    model_config = {
        "from_attributes": True
    }