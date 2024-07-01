# app.py

import sqlite3  # Importa o módulo sqlite3 para interagir com o banco de dados SQLite
import streamlit as st  # Importa o módulo Streamlit para construir a interface web

# Funções de interação com o banco de dados SQLite

def create_database():
    # Função para criar o banco de dados se não existir a tabela 'tasks'
    conn = sqlite3.connect('tasks.db')  # Conecta ao banco de dados tasks.db
    c = conn.cursor()  # Cria um cursor para executar comandos SQL

    # Verifica se a tabela 'tasks' já existe no banco de dados
    c.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'
    """)
    if not c.fetchone():  # Se não encontrar a tabela 'tasks', cria a tabela
        c.execute('''CREATE TABLE tasks
                     (task_name text, description text, status text)''')
        conn.commit()  # Realiza a operação de criação da tabela
    conn.close()  # Fecha a conexão com o banco de dados

def add_task(task_name, description, status='Pending'):
    # Função para adicionar uma nova task ao banco de dados
    conn = sqlite3.connect('tasks.db')  # Conecta ao banco de dados tasks.db
    c = conn.cursor()  # Cria um cursor para executar comandos SQL
    c.execute("INSERT INTO tasks (task_name, description, status) VALUES (?, ?, ?)", (task_name, description, status))
    conn.commit()  # Realiza a operação de inserção de dados
    conn.close()  # Fecha a conexão com o banco de dados

def delete_task(task_name):
    # Função para deletar uma task do banco de dados
    conn = sqlite3.connect('tasks.db')  # Conecta ao banco de dados tasks.db
    c = conn.cursor()  # Cria um cursor para executar comandos SQL
    c.execute("DELETE FROM tasks WHERE task_name=?", (task_name,))
    conn.commit()  # Realiza a operação de remoção de dados
    conn.close()  # Fecha a conexão com o banco de dados

def update_task(task_name, description, status):
    # Função para atualizar a descrição e o status de uma task no banco de dados
    conn = sqlite3.connect('tasks.db')  # Conecta ao banco de dados tasks.db
    c = conn.cursor()  # Cria um cursor para executar comandos SQL
    c.execute("UPDATE tasks SET description = ?, status = ? WHERE task_name = ?", (description, status, task_name))
    conn.commit()  # Realiza a operação de atualização de dados
    conn.close()  # Fecha a conexão com o banco de dados

def view_tasks(order_by=None):
    # Função para visualizar todas as tasks cadastradas no banco de dados
    conn = sqlite3.connect('tasks.db')  # Conecta ao banco de dados tasks.db
    c = conn.cursor()  # Cria um cursor para executar comandos SQL
    if order_by:
        c.execute(f"SELECT task_name, description, status FROM tasks ORDER BY {order_by}")  # Seleciona e ordena as tasks pelo campo especificado
    else:
        c.execute("SELECT task_name, description, status FROM tasks")  # Seleciona todas as tasks
    tasks = c.fetchall()  # Obtém todas as linhas resultantes da consulta SQL
    conn.close()  # Fecha a conexão com o banco de dados
    return tasks  # Retorna a lista de tasks encontradas

def search_task(task_name):
    # Função para buscar uma task específica pelo nome no banco de dados
    conn = sqlite3.connect('tasks.db')  # Conecta ao banco de dados tasks.db
    c = conn.cursor()  # Cria um cursor para executar comandos SQL
    c.execute("SELECT * FROM tasks WHERE task_name=?", (task_name,))
    tasks = c.fetchall()  # Obtém todas as linhas resultantes da consulta SQL
    conn.close()  # Fecha a conexão com o banco de dados
    return tasks  # Retorna a lista de tasks encontradas

# Interface do Streamlit

def main():
    st.title("Task Manager")  # Define o título da aplicação Streamlit como "Task Manager"

    create_database()  # Chama a função para criar o banco de dados se necessário

    st.sidebar.header("Operations")  # Cabeçalho na barra lateral para as operações disponíveis
    # Cria um seletor de operações na barra lateral com opções para adicionar, deletar, atualizar, buscar e visualizar tasks
    operation = st.sidebar.radio("Select operation", ("Add Task", "Delete Task", "Update Task", "Search Task", "View Tasks"))

    if operation == "Add Task":
        st.header("Add Task")  # Cabeçalho na página principal para adicionar uma nova task
        task_name = st.text_input("Task Name")  # Campo de entrada para o nome da task
        description = st.text_area("Description")  # Área de texto para a descrição da task
        if st.button("Add Task"):  # Botão para adicionar a task ao banco de dados
            add_task(task_name, description)  # Chama a função para adicionar a task ao banco de dados
            st.success("Task added successfully!")  # Exibe uma mensagem de sucesso

    elif operation == "Delete Task":
        st.header("Delete Task")  # Cabeçalho na página principal para deletar uma task
        tasks = view_tasks()  # Obtém a lista de todas as tasks do banco de dados
        selected_task = st.selectbox("Select Task to Delete", [task[0] for task in tasks])  # Caixa de seleção para escolher a task a ser deletada
        if selected_task:
            if st.button("Delete Task"):  # Botão para confirmar a exclusão da task selecionada
                delete_task(selected_task)  # Chama a função para deletar a task do banco de dados
                st.success(f"Task '{selected_task}' deleted successfully!")  # Exibe uma mensagem de sucesso

    elif operation == "Update Task":
        st.header("Update Task")  # Cabeçalho na página principal para atualizar uma task
        tasks = view_tasks()  # Obtém a lista de todas as tasks do banco de dados
        selected_task = st.selectbox("Select Task to Update", [task[0] for task in tasks])  # Caixa de seleção para escolher a task a ser atualizada
        
        if selected_task:
            st.subheader(f"Update Task '{selected_task}'")  # Subtítulo para mostrar qual task está sendo atualizada
            current_description = [task[1] for task in tasks if task[0] == selected_task][0]  # Busca a descrição atual da task selecionada
            current_status = [task[2] for task in tasks if task[0] == selected_task][0]  # Busca o status atual da task selecionada
            
            # Área de texto para a descrição da task, preenchida com a descrição atual da task selecionada
            description = st.text_area("Description", value=current_description)
            # Caixa de seleção para o status da task, preenchida com o status atual da task selecionada
            status = st.selectbox("Status", ["Pending", "In Progress", "Completed"], index=["Pending", "In Progress", "Completed"].index(current_status))
            
            if st.button("Update Task"):  # Botão para confirmar a atualização da task
                update_task(selected_task, description, status)  # Chama a função para atualizar a task no banco de dados
                st.success(f"Task '{selected_task}' updated successfully!")  # Exibe uma mensagem de sucesso

    elif operation == "Search Task":
        st.header("Search Tasks")  # Cabeçalho na página principal para buscar tasks
        task_name = st.text_input("Task Name")  # Campo de entrada para digitar o nome da task a ser buscada
        if st.button("Search Tasks"):  # Botão para iniciar a busca das tasks
            tasks = search_task(task_name)  # Chama a função para buscar a task no banco de dados
            if tasks:
                st.table(tasks)  # Exibe uma tabela com os resultados da busca
            else:
                st.warning("No tasks found.")  # Exibe um aviso se nenhuma task for encontrada

    elif operation == "View Tasks":
        st.header("View All Tasks")  # Cabeçalho na página principal para visualizar todas as tasks
        order_by = st.selectbox("Order by", ["task_name", "description", "status"])  # Caixa de seleção para escolher o campo de ordenação
        tasks = view_tasks(order_by=order_by)  # Obtém a lista de todas as tasks ordenadas pelo campo selecionado
        if tasks:
            # Cria uma tabela com as colunas de nome da task, descrição e status para cada task encontrada
            task_table = [(task[0], task[1], task[2]) if len(task) == 3 else (task[0], "", "") for task in tasks]
            st.table(task_table)  # Exibe a tabela com as tasks encontradas
        else:
            st.info("No tasks available.")  # Exibe uma mensagem informativa se não houver tasks no banco de dados

if __name__ == '__main__':
    main()  # Chama a função principal para iniciar a aplicação Streamlit