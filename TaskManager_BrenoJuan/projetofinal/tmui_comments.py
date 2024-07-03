'''

import streamlit as st  # Importa a biblioteca Streamlit para a interface do usuário
import requests  # Importa a biblioteca requests para fazer requisições HTTP
import json  # Importa a biblioteca json para trabalhar com dados JSON
from datetime import date  # Importa a classe date para trabalhar com datas

st.title("Task Manager")  # Define o título da aplicação

API_URL = "http://127.0.0.1:8000"  # Define a URL da API

st.sidebar.header("Operations")  # Cria um cabeçalho na barra lateral
operation = st.sidebar.radio("Select operation", ("Add Task", "Delete Task", "Update Task", "Search Task", "View Tasks"))  # Cria um rádio para selecionar a operação

def format_date(d):
    return d.strftime("%Y-%m-%d")  # Função para formatar uma data para string

if operation == "Add Task":
    st.header("Add Task")  # Cabeçalho para adicionar uma tarefa
    task_name = st.text_input("Task Name")  # Campo de entrada para o nome da tarefa
    description = st.text_area("Description")  # Área de texto para a descrição da tarefa
    limit_date = st.date_input("Limit Date")  # Entrada de data para a data limite
    priority = st.selectbox("Priority", ["Low", "Mid", "High"])  # Caixa de seleção para a prioridade da tarefa
    if st.button("Add Task"):  # Botão para adicionar a tarefa
        if task_name and limit_date:  # Verifica se os campos obrigatórios estão preenchidos
            task_data = {
                "task_name": task_name,
                "description": description,
                "limit_date": format_date(limit_date),
                "priority": priority,
                "status": "Pending"
            }
            response = requests.post(f"{API_URL}/tasks/", json=task_data)  # Envia uma requisição POST para adicionar a tarefa
            if response.status_code == 200:  # Verifica se a requisição foi bem-sucedida
                st.success("Task added successfully!")  # Exibe uma mensagem de sucesso
            else:
                st.error(f"Error adding task: {response.text}")  # Exibe uma mensagem de erro em caso de falha

elif operation == "Delete Task":
    st.header("Delete Task")  # Cabeçalho para deletar uma tarefa
    response = requests.get(f"{API_URL}/tasks/")  # Obtém a lista de tarefas da API
    tasks = response.json()  # Converte a resposta para JSON
    selected_task = st.selectbox("Select Task to Delete", [f"{task['task_name']} (ID: {task['id']})" for task in tasks])  # Caixa de seleção para selecionar a tarefa a ser deletada
    if selected_task:  # Se uma tarefa foi selecionada
        task_id = int(selected_task.split("ID: ")[1].rstrip(")"))  # Extrai o ID da tarefa selecionada
        if st.button("Delete Task"):  # Botão para deletar a tarefa
            response = requests.delete(f"{API_URL}/tasks/{task_id}")  # Envia uma requisição DELETE para deletar a tarefa
            if response.status_code == 200:  # Verifica se a requisição foi bem-sucedida
                st.success(f"Task with ID {task_id} deleted successfully!")  # Exibe uma mensagem de sucesso
            else:
                st.error("Error deleting task")  # Exibe uma mensagem de erro em caso de falha

elif operation == "Update Task":
    st.header("Update Task")  # Cabeçalho para atualizar uma tarefa
    response = requests.get(f"{API_URL}/tasks/")  # Obtém a lista de tarefas da API
    tasks = response.json()  # Converte a resposta para JSON
    selected_task = st.selectbox("Select Task to Update", [f"{task['task_name']} (ID: {task['id']})" for task in tasks])  # Caixa de seleção para selecionar a tarefa a ser atualizada
    
    if selected_task:  # Se uma tarefa foi selecionada
        task_id = int(selected_task.split("ID: ")[1].rstrip(")"))  # Extrai o ID da tarefa selecionada
        current_task = next(task for task in tasks if task['id'] == task_id)  # Obtém os detalhes da tarefa atual

        task_name = st.text_input("Task Name", value=current_task['task_name'])  # Campo de entrada para o nome da tarefa
        description = st.text_area("Description", value=current_task['description'])  # Área de texto para a descrição da tarefa
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed"], index=["Pending", "In Progress", "Completed"].index(current_task['status']))  # Caixa de seleção para o status da tarefa
        limit_date = st.date_input("Limit Date", value=date.fromisoformat(current_task['limit_date']) if current_task['limit_date'] else date.today())  # Entrada de data para a data limite
        priority = st.selectbox("Priority", ["Low", "Mid", "High"], index=["Low", "Mid", "High"].index(current_task['priority']))  # Caixa de seleção para a prioridade da tarefa

        if st.button("Update Task"):  # Botão para atualizar a tarefa
            task_data = {
                "task_name": task_name,
                "description": description,
                "status": status,
                "limit_date": format_date(limit_date),
                "priority": priority
            }
            response = requests.put(f"{API_URL}/tasks/{task_id}", json=task_data)  # Envia uma requisição PUT para atualizar a tarefa
            if response.status_code == 200:  # Verifica se a requisição foi bem-sucedida
                st.success(f"Task with ID {task_id} updated successfully!")  # Exibe uma mensagem de sucesso
            else:
                st.error(f"Error updating task: {response.text}")  # Exibe uma mensagem de erro em caso de falha

elif operation == "Search Task":
    st.header("Search Tasks")  # Cabeçalho para buscar tarefas
    task_name = st.text_input("Task Name")  # Campo de entrada para o nome da tarefa
    if st.button("Search Tasks"):  # Botão para buscar tarefas
        response = requests.get(f"{API_URL}/tasks/search/", params={"task_name": task_name})  # Envia uma requisição GET para buscar tarefas pelo nome
        tasks = response.json()  # Converte a resposta para JSON
        if tasks:  # Se foram encontradas tarefas
            st.table(tasks)  # Exibe as tarefas encontradas em uma tabela
        else:
            st.warning("No tasks found.")  # Exibe um aviso se nenhuma tarefa for encontrada

elif operation == "View Tasks":
    st.header("View All Tasks")  # Cabeçalho para visualizar todas as tarefas
    order_by = st.selectbox("Order by", ["task_name", "description", "status", "limit_date", "priority"])  # Caixa de seleção para ordenar as tarefas
    response = requests.get(f"{API_URL}/tasks/", params={"order_by": order_by})  # Envia uma requisição GET para obter todas as tarefas possivelmente ordenadas
    tasks = response.json()  # Converte a resposta para JSON
    if tasks:  # Se há tarefas para exibir
        st.table(tasks)  # Exibe as tarefas em uma tabela
    else:
        st.info("No tasks available.")  # Exibe uma mensagem informativa se não houver tarefas disponíveis

'''