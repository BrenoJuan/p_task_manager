'''

import sqlite3  # Importa a biblioteca sqlite3 para trabalhar com o banco de dados SQLite
import streamlit as st  # Importa a biblioteca Streamlit para a interface do usuário
from datetime import datetime  # Importa a classe datetime para trabalhar com datas

def create_database():
    conn = sqlite3.connect('tasks.db')  # Conecta ao banco de dados SQLite (ou cria um novo se não existir)
    c = conn.cursor()  # Cria um cursor para interagir com o banco de dados
    
    # Deleta a tabela existente, se houver (opcional)
    # c.execute("DROP TABLE IF EXISTS tasks")
    
    # Cria a tabela 'tasks' se não existir
    c.execute(''''''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        description TEXT,
        status TEXT,
        limit_date DATE,
        priority TEXT
    )
    '''''')
    conn.commit()  # Salva (commita) as alterações no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

def add_task(task_name, description, limit_date, priority='Mid', status='Pending'):
    conn = sqlite3.connect('tasks.db')  # Conecta ao banco de dados SQLite
    c = conn.cursor()  # Cria um cursor para interagir com o banco de dados
    # Insere uma nova tarefa na tabela 'tasks'
    c.execute("INSERT INTO tasks (task_name, description, status, limit_date, priority) VALUES (?, ?, ?, ?, ?)", 
              (task_name, description, status, limit_date, priority))
    conn.commit()  # Salva (commita) as alterações no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')  # Conecta ao banco de dados SQLite
    c = conn.cursor()  # Cria um cursor para interagir com o banco de dados
    # Deleta a tarefa com o ID fornecido
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()  # Salva (commita) as alterações no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

def update_task(task_id, task_name, description, status, limit_date, priority):
    conn = sqlite3.connect('tasks.db')  # Conecta ao banco de dados SQLite
    c = conn.cursor()  # Cria um cursor para interagir com o banco de dados
    # Atualiza a tarefa com o ID fornecido com os novos dados
    c.execute("UPDATE tasks SET task_name = ?, description = ?, status = ?, limit_date = ?, priority = ? WHERE id = ?", 
              (task_name, description, status, limit_date, priority, task_id))
    conn.commit()  # Salva (commita) as alterações no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

def view_tasks(order_by=None):
    conn = sqlite3.connect('tasks.db')  # Conecta ao banco de dados SQLite
    c = conn.cursor()  # Cria um cursor para interagir com o banco de dados
    query = "SELECT id, task_name, description, status, limit_date, priority FROM tasks"  # Define a consulta para selecionar todas as tarefas
    if order_by:  # Se um critério de ordenação for fornecido
        query += f" ORDER BY {order_by}"  # Adiciona a cláusula ORDER BY à consulta
    c.execute(query)  # Executa a consulta
    tasks = c.fetchall()  # Recupera todos os resultados da consulta
    conn.close()  # Fecha a conexão com o banco de dados
    return tasks  # Retorna as tarefas

def search_task(task_name):
    conn = sqlite3.connect('tasks.db')  # Conecta ao banco de dados SQLite
    c = conn.cursor()  # Cria um cursor para interagir com o banco de dados
    # Seleciona as tarefas que correspondem ao nome fornecido
    c.execute("SELECT * FROM tasks WHERE task_name=?", (task_name,))
    tasks = c.fetchall()  # Recupera todos os resultados da consulta
    conn.close()  # Fecha a conexão com o banco de dados
    return tasks  # Retorna as tarefas encontradas
    
'''