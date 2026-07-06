from sqlmodel import SQLModel, Field
from typing import Optional
class Task(SQLModel, table=True):
    task_id: Optional[int] = Field(primary_key=True, default=None)
    task_name: str
    task_status: bool = False



class TaskCreate(SQLModel):
    task_name: str
    status: bool = False

class TaskPatch(SQLModel):
    task_name: Optional[str] = None
    task_status: Optional[bool] = None

class TaskPut(SQLModel):
    task_name:str
    task_status: bool
