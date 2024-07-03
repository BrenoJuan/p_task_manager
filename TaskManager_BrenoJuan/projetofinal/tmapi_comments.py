'''

from fastapi import FastAPI  # Importa o FastAPI para criar a API
from pydantic import BaseModel  # Importa o BaseModel do Pydantic para validação de dados
from typing import List, Optional  # Importa tipos para tipagem das funções
from datetime import date  # Importa a classe date para trabalhar com datas
from .task_manager_db import create_database, add_task, delete_task, update_task, view_tasks, search_task  # Importa funções do módulo task_manager_db

app = FastAPI()  # Cria uma instância do FastAPI

class Task(BaseModel):
    id: Optional[int]  # Define o campo 'id' como opcional
    task_name: str  # Define o campo 'task_name' como obrigatório
    description: Optional[str]  # Define o campo 'description' como opcional
    status: Optional[str]  # Define o campo 'status' como opcional
    limit_date: Optional[date]  # Define o campo 'limit_date' como opcional
    priority: Optional[str]  # Define o campo 'priority' como opcional

class TaskCreate(BaseModel):
    task_name: str  # Define o campo 'task_name' como obrigatório
    description: Optional[str]  # Define o campo 'description' como opcional
    status: Optional[str]  # Define o campo 'status' como opcional
    limit_date: Optional[date]  # Define o campo 'limit_date' como opcional
    priority: Optional[str]  # Define o campo 'priority' como opcional

class TaskUpdate(BaseModel):
    task_name: str  # Define o campo 'task_name' como obrigatório
    description: Optional[str]  # Define o campo 'description' como opcional
    status: Optional[str]  # Define o campo 'status' como opcional
    limit_date: Optional[date]  # Define o campo 'limit_date' como opcional
    priority: Optional[str]  # Define o campo 'priority' como opcional

@app.on_event("startup")
def startup():
    create_database()  # Cria o banco de dados quando o aplicativo FastAPI é iniciado

@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    add_task(task.task_name, task.description, task.limit_date, task.priority, task.status)  # Adiciona uma nova tarefa
    # Recuperar a tarefa criada para retornar com o ID gerado
    tasks = search_task(task.task_name)  # Busca a tarefa pelo nome
    created_task = tasks[-1]  # Assume que a última tarefa com o nome corresponde à recém-criada
    return Task(id=created_task[0], task_name=created_task[1], description=created_task[2], status=created_task[3], limit_date=created_task[4], priority=created_task[5])  # Retorna a tarefa criada com o ID

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    delete_task(task_id)  # Deleta a tarefa pelo ID
    return {"message": f"Task with ID {task_id} deleted"}  # Retorna uma mensagem de sucesso

@app.put("/tasks/{task_id}", response_model=Task)
def modify_task(task_id: int, task: TaskUpdate):
    update_task(task_id, task.task_name, task.description, task.status, task.limit_date, task.priority)  # Atualiza a tarefa pelo ID
    return Task(id=task_id, task_name=task.task_name, description=task.description, status=task.status, limit_date=task.limit_date, priority=task.priority)  # Retorna a tarefa atualizada

@app.get("/tasks/", response_model=List[Task])
def get_tasks(order_by: Optional[str] = None):
    tasks = view_tasks(order_by)  # Recupera todas as tarefas, possivelmente ordenadas
    return [Task(id=task[0], task_name=task[1], description=task[2], status=task[3], limit_date=task[4], priority=task[5]) for task in tasks]  # Retorna a lista de tarefas

@app.get("/tasks/search/", response_model=List[Task])
def search_tasks(task_name: str):
    tasks = search_task(task_name)  # Busca tarefas pelo nome
    return [Task(id=task[0], task_name=task[1], description=task[2], status=task[3], limit_date=task[4], priority=task[5]) for task in tasks]  # Retorna a lista de tarefas encontradas

'''