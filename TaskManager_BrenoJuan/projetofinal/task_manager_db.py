import sqlite3
import streamlit as st
from datetime import datetime

def create_database():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    
    # Deleta a tabela existente, se houver (opcional)
    # c.execute("DROP TABLE IF EXISTS tasks")
    
    # Cria a tabela 'tasks' se não existir
    c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        description TEXT,
        status TEXT,
        limit_date DATE,
        priority TEXT
    )
    ''')
    conn.commit()
    conn.close()

def add_task(task_name, description, limit_date, priority='Mid', status='Pending'):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task_name, description, status, limit_date, priority) VALUES (?, ?, ?, ?, ?)", 
              (task_name, description, status, limit_date, priority))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, task_name, description, status, limit_date, priority):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET task_name = ?, description = ?, status = ?, limit_date = ?, priority = ? WHERE id = ?", 
              (task_name, description, status, limit_date, priority, task_id))
    conn.commit()
    conn.close()

def view_tasks(order_by=None):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    query = "SELECT id, task_name, description, status, limit_date, priority FROM tasks"
    if order_by:
        query += f" ORDER BY {order_by}"
    c.execute(query)
    tasks = c.fetchall()
    conn.close()
    return tasks

def search_task(task_name):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE task_name=?", (task_name,))
    tasks = c.fetchall()
    conn.close()
    return tasks