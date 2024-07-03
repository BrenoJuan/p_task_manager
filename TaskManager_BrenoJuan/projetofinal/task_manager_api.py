from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from .task_manager_db import create_database, add_task, delete_task, update_task, view_tasks, search_task

app = FastAPI()

class Task(BaseModel):
    id: Optional[int]
    task_name: str
    description: Optional[str]
    status: Optional[str]
    limit_date: Optional[date]
    priority: Optional[str]

class TaskCreate(BaseModel):
    task_name: str
    description: Optional[str]
    status: Optional[str]
    limit_date: Optional[date]
    priority: Optional[str]

class TaskUpdate(BaseModel):
    task_name: str
    description: Optional[str]
    status: Optional[str]
    limit_date: Optional[date]
    priority: Optional[str]

@app.on_event("startup")
def startup():
    create_database()

@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    add_task(task.task_name, task.description, task.limit_date, task.priority, task.status)
    # Recuperar a tarefa criada para retornar com o ID gerado
    tasks = search_task(task.task_name)
    created_task = tasks[-1]  # assume que a última tarefa com o nome corresponde à recém-criada
    return Task(id=created_task[0], task_name=created_task[1], description=created_task[2], status=created_task[3], limit_date=created_task[4], priority=created_task[5])

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    delete_task(task_id)
    return {"message": f"Task with ID {task_id} deleted"}

@app.put("/tasks/{task_id}", response_model=Task)
def modify_task(task_id: int, task: TaskUpdate):
    update_task(task_id, task.task_name, task.description, task.status, task.limit_date, task.priority)
    return Task(id=task_id, task_name=task.task_name, description=task.description, status=task.status, limit_date=task.limit_date, priority=task.priority)

@app.get("/tasks/", response_model=List[Task])
def get_tasks(order_by: Optional[str] = None):
    tasks = view_tasks(order_by)
    return [Task(id=task[0], task_name=task[1], description=task[2], status=task[3], limit_date=task[4], priority=task[5]) for task in tasks]

@app.get("/tasks/search/", response_model=List[Task])
def search_tasks(task_name: str):
    tasks = search_task(task_name)
    return [Task(id=task[0], task_name=task[1], description=task[2], status=task[3], limit_date=task[4], priority=task[5]) for task in tasks]
