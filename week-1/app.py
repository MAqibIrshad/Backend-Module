"Pause this function until this task finishes, but let the server work on other requests in the meantime."
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import status
from typing import Optional
from fastapi import HTTPException

app = FastAPI()

tasks = []

class TaskRequest(BaseModel):
    task_id: int
    task_name: str
    task_status: bool

class TaskResponse(BaseModel):
    task_id: Optional[int] = None
    task_name:str
    task_status:bool


@app.post("/create-task", response_model = TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskRequest):
    tasks.append(task)
    print(tasks)
    return task


@app.get("/task/search", response_model=TaskResponse)
def get_task_by_name(name: str):

    task_found = next(
        (task for task in tasks if task.task_name == name),
        None
    )

    if task_found is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task_found


@app.get("/task/{id}", response_model = TaskResponse, status_code=status.HTTP_200_OK)
def get_task_by_id(id: int):
    if len(tasks) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # task_found = next(filter(lambda task: task["task_id"] == id, tasks), None)
    task_found = next(
    filter(lambda task: task.task_id == id, tasks),
    None
)
    return task_found
    



    

@app.get("/tasks", response_model=list[TaskResponse], status_code=status.HTTP_200_OK) 
def get_all_taks():
    return tasks
       


