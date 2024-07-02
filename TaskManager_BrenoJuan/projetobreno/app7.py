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
        task_name TEXT,
        description TEXT,
        status TEXT,
        limit_date DATE,
        priority TEXT
    )
    ''')
    
    # Verifica se as colunas 'limit_date' e 'priority' existem, caso contrário adiciona-as
    c.execute("PRAGMA table_info(tasks)")
    columns = [column[1] for column in c.fetchall()]
    if 'limit_date' not in columns:
        c.execute("ALTER TABLE tasks ADD COLUMN limit_date DATE")
    if 'priority' not in columns:
        c.execute("ALTER TABLE tasks ADD COLUMN priority TEXT")
    
    conn.commit()
    conn.close()

def add_task(task_name, description, limit_date, priority='Mid', status='Pending'):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task_name, description, status, limit_date, priority) VALUES (?, ?, ?, ?, ?)", (task_name, description, status, limit_date, priority))
    conn.commit()
    conn.close()

def delete_task(task_name):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE task_name=?", (task_name,))
    conn.commit()
    conn.close()

def update_task(task_name, description, status, limit_date, priority):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET description = ?, status = ?, limit_date = ?, priority = ? WHERE task_name = ?", (description, status, limit_date, priority, task_name))
    conn.commit()
    conn.close()

def view_tasks(order_by=None):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    if order_by:
        c.execute(f"SELECT task_name, description, status, limit_date, priority FROM tasks ORDER BY {order_by}")
    else:
        c.execute("SELECT task_name, description, status, limit_date, priority FROM tasks")
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
            add_task(task_name, description, limit_date, priority)
            st.success("Task added successfully!")

    elif operation == "Delete Task":
        st.header("Delete Task")
        tasks = view_tasks()
        selected_task = st.selectbox("Select Task to Delete", [task[0] for task in tasks])
        if selected_task:
            if st.button("Delete Task"):
                delete_task(selected_task)
                st.success(f"Task '{selected_task}' deleted successfully!")

    elif operation == "Update Task":
        st.header("Update Task")
        tasks = view_tasks()
        selected_task = st.selectbox("Select Task to Update", [task[0] for task in tasks])
        
        if selected_task:
            st.subheader(f"Update Task '{selected_task}'")
            current_description = [task[1] for task in tasks if task[0] == selected_task][0]
            current_status = [task[2] for task in tasks if task[0] == selected_task][0]
            current_limit_date = [task[3] for task in tasks if task[0] == selected_task][0]
            current_priority = [task[4] for task in tasks if task[0] == selected_task][0]

            description = st.text_area("Description", value=current_description)
            status = st.selectbox("Status", ["Pending", "In Progress", "Completed"], index=["Pending", "In Progress", "Completed"].index(current_status))
            limit_date = st.date_input("Limit Date", value=datetime.strptime(current_limit_date, "%Y-%m-%d").date() if current_limit_date else datetime.now().date())
            priority = st.selectbox("Priority", ["Low", "Mid", "High"], index=["Low", "Mid", "High"].index(current_priority))

            if st.button("Update Task"):
                update_task(selected_task, description, status, limit_date, priority)
                st.success(f"Task '{selected_task}' updated successfully!")

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
            task_table = [(task[0], task[1], task[2], task[3], task[4]) if len(task) == 5 else (task[0], "", "") for task in tasks]
            st.table(task_table)
        else:
            st.info("No tasks available.")

if __name__ == '__main__':
    main()