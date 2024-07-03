import streamlit as st
import requests
import json
from datetime import date

st.title("Task Manager")

API_URL = "http://127.0.0.1:8000"

st.sidebar.header("Operations")
operation = st.sidebar.radio("Select operation", ("Add Task", "Delete Task", "Update Task", "Search Task", "View Tasks"))

def format_date(d):
    return d.strftime("%Y-%m-%d")

if operation == "Add Task":
    st.header("Add Task")
    task_name = st.text_input("Task Name")
    description = st.text_area("Description")
    limit_date = st.date_input("Limit Date")
    priority = st.selectbox("Priority", ["Low", "Mid", "High"])
    if st.button("Add Task"):
        if task_name and limit_date:  # Verifica se os campos obrigatórios estão preenchidos
            task_data = {
                "task_name": task_name,
                "description": description,
                "limit_date": format_date(limit_date),
                "priority": priority,
                "status": "Pending"
            }
            response = requests.post(f"{API_URL}/tasks/", json=task_data)
            if response.status_code == 200:
                st.success("Task added successfully!")
            else:
                st.error(f"Error adding task: {response.text}")

elif operation == "Delete Task":
    st.header("Delete Task")
    response = requests.get(f"{API_URL}/tasks/")
    tasks = response.json()
    selected_task = st.selectbox("Select Task to Delete", [f"{task['task_name']} (ID: {task['id']})" for task in tasks])
    if selected_task:
        task_id = int(selected_task.split("ID: ")[1].rstrip(")"))
        if st.button("Delete Task"):
            response = requests.delete(f"{API_URL}/tasks/{task_id}")
            if response.status_code == 200:
                st.success(f"Task with ID {task_id} deleted successfully!")
            else:
                st.error("Error deleting task")

elif operation == "Update Task":
    st.header("Update Task")
    response = requests.get(f"{API_URL}/tasks/")
    tasks = response.json()
    selected_task = st.selectbox("Select Task to Update", [f"{task['task_name']} (ID: {task['id']})" for task in tasks])
    
    if selected_task:
        task_id = int(selected_task.split("ID: ")[1].rstrip(")"))
        current_task = next(task for task in tasks if task['id'] == task_id)
        
        task_name = st.text_input("Task Name", value=current_task['task_name'])
        description = st.text_area("Description", value=current_task['description'])
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed"], index=["Pending", "In Progress", "Completed"].index(current_task['status']))
        limit_date = st.date_input("Limit Date", value=date.fromisoformat(current_task['limit_date']) if current_task['limit_date'] else date.today())
        priority = st.selectbox("Priority", ["Low", "Mid", "High"], index=["Low", "Mid", "High"].index(current_task['priority']))

        if st.button("Update Task"):
            task_data = {
                "task_name": task_name,
                "description": description,
                "status": status,
                "limit_date": format_date(limit_date),
                "priority": priority
            }
            response = requests.put(f"{API_URL}/tasks/{task_id}", json=task_data)
            if response.status_code == 200:
                st.success(f"Task with ID {task_id} updated successfully!")
            else:
                st.error(f"Error updating task: {response.text}")

elif operation == "Search Task":
    st.header("Search Tasks")
    task_name = st.text_input("Task Name")
    if st.button("Search Tasks"):
        response = requests.get(f"{API_URL}/tasks/search/", params={"task_name": task_name})
        tasks = response.json()
        if tasks:
            st.table(tasks)
        else:
            st.warning("No tasks found.")

elif operation == "View Tasks":
    st.header("View All Tasks")
    order_by = st.selectbox("Order by", ["task_name", "description", "status", "limit_date", "priority"])
    response = requests.get(f"{API_URL}/tasks/", params={"order_by": order_by})
    tasks = response.json()
    if tasks:
        st.table(tasks)
    else:
        st.info("No tasks available.")
