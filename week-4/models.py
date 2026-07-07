from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
class Task(SQLModel, table=True):
    task_id: Optional[int] = Field(primary_key=True, default=None)
    task_name: str
    task_status: bool = False
    #The value stored in Task.user_id must exist in the User.user_id column.
    user_id:int = Field(foreign_key="user.user_id")
    user: Optional["User"] = Relationship(back_populates="tasks") 
    #"These two attributes represent the same relationship."
    #SQLModel doesn't know that each task should also point back to this same user object.



# class TaskCreate(SQLModel):
#     task_name: str
#     status: bool = False

# class TaskPatch(SQLModel):
#     task_name: Optional[str] = None
#     task_status: Optional[bool] = None

# class TaskPut(SQLModel):
#     task_name:str
#     task_status: bool


class User(SQLModel, table=True):
    user_id: Optional[int] = Field(primary_key=True, default=None)
    user_name: str
    user_status: bool = False
    email:str
    password: str
    tasks: list["Task"] = Relationship(back_populates="user")
