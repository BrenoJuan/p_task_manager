# Última versão funcional

import sqlite3
import streamlit as st
from datetime import datetime

# Funções de interação com o banco de dados SQLite

def create_database():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    
    # Deletar a tabela existente (opcional)
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
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (task_name, description, status, limit_date, priority) VALUES (?, ?, ?, ?, ?)", (task_name, description, status, limit_date, priority))
        conn.commit()
        conn.close()
        st.success("Task added successfully!")
    except sqlite3.Error as e:
        st.error(f"Error adding task: {e}")

def delete_task(task_id):
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        st.success(f"Task with ID {task_id} deleted successfully!")
    except sqlite3.Error as e:
        st.error(f"Error deleting task: {e}")

def update_task(task_id, task_name, description, status, limit_date, priority):
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET task_name = ?, description = ?, status = ?, limit_date = ?, priority = ? WHERE id = ?", (task_name, description, status, limit_date, priority, task_id))
        conn.commit()
        conn.close()
        st.success(f"Task with ID {task_id} updated successfully!")
    except sqlite3.Error as e:
        st.error(f"Error updating task: {e}")

def view_tasks(order_by=None):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    if order_by:
        c.execute(f"SELECT id, task_name, description, status, limit_date, priority FROM tasks ORDER BY {order_by}")
    else:
        c.execute("SELECT id, task_name, description, status, limit_date, priority FROM tasks")
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

# Interface do Streamlit

def main():
    st.title("Task Manager")

    create_database()

    st.sidebar.header("Operations")
    operation = st.sidebar.radio("Select operation", ("Add Task", "Delete Task", "Update Task", "Search Task", "View Tasks"))

    if operation == "Add Task":
        st.header("Add Task")
        task_name = st.text_input("Task Name")
        description = st.text_area("Description")
        limit_date = st.date_input("Limit Date")
        priority = st.selectbox("Priority", ["Low", "Mid", "High"])
        if st.button("Add Task"):
            if task_name and limit_date:  # Verifica se os campos obrigatórios estão preenchidos
                add_task(task_name, description, limit_date, priority)
            else:
                st.warning("Task Name and Limit Date are required.")

    elif operation == "Delete Task":
        st.header("Delete Task")
        tasks = view_tasks()
        selected_task = st.selectbox("Select Task to Delete", [f"{task[1]} (ID: {task[0]})" for task in tasks])
        if selected_task:
            task_id = int(selected_task.split("ID: ")[1].rstrip(")"))
            if st.button("Delete Task"):
                delete_task(task_id)

    elif operation == "Update Task":
        st.header("Update Task")
        tasks = view_tasks()
        selected_task = st.selectbox("Select Task to Update", [f"{task[1]} (ID: {task[0]})" for task in tasks])
        
        if selected_task:
            task_id = int(selected_task.split("ID: ")[1].rstrip(")"))
            st.subheader(f"Update Task '{selected_task}'")
            current_task = [task for task in tasks if task[0] == task_id][0]
            current_name, current_description, current_status, current_limit_date, current_priority = current_task[1:]
            
            task_name = st.text_input("Task Name", value=current_name)
            description = st.text_area("Description", value=current_description)
            status = st.selectbox("Status", ["Pending", "In Progress", "Completed"], index=["Pending", "In Progress", "Completed"].index(current_status))
            limit_date = st.date_input("Limit Date", value=datetime.strptime(current_limit_date, "%Y-%m-%d").date() if current_limit_date else datetime.now().date())
            priority = st.selectbox("Priority", ["Low", "Mid", "High"], index=["Low", "Mid", "High"].index(current_priority))

            if st.button("Update Task"):
                update_task(task_id, task_name, description, status, limit_date, priority)

    elif operation == "Search Task":
        st.header("Search Tasks")
        task_name = st.text_input("Task Name")
        if st.button("Search Tasks"):
            tasks = search_task(task_name)
            if tasks:
                st.table(tasks)
            else:
                st.warning("No tasks found.")

    elif operation == "View Tasks":
        st.header("View All Tasks")
        order_by = st.selectbox("Order by", ["task_name", "description", "status", "limit_date", "priority"])
        tasks = view_tasks(order_by=order_by)
        if tasks:
            task_table = [(task[0], task[1], task[2], task[3], task[4], task[5]) if len(task) == 6 else (task[0], "", "", "", "", "") for task in tasks]
            st.table(task_table)
        else:
            st.info("No tasks available.")

if __name__ == '__main__':
    main()