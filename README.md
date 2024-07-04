# p_task_manager

'''

O projeto foi feito utilizando python, streamlit, sqlite3 e fastapi.

Para rodar o programa, se torna necessário abrir dois terminais dentro do VS Code, um para executar o arquivo api e o outro para executar o arquivo do front.

A segmentação de pastas para encontrar os arquivos finais é: p_task_manager -> TaskManager_BrenoJuan -> projetofinal -> arquivos dispostos aqui dentro.

O primeiro a ser executado é o task_manager_api, usa-se a seguinte sintaxe no primeiro terminal:

uvicorn TaskManager_BrenoJuan.projetofinal.task_manager_api:app --reload

Para o segundo, task_manager_ui, utiliza-se a sintaxe a baixo (substituindo pelo seu respectivo caminho localizado à sua escolha):

streamlit run "C:\Users\{seu usuário}\Desktop\p_task_manager\TaskManager_BrenoJuan\projetofinal\task_manager_ui.py"

Com tudo certo, caso não abra no navegador de forma padrão, é possível abrir o fastapi usando: http://127.0.0.1:8000/docs#/
E para a interface personalizada do streamlit: http://localhost:8501

>>> Pontos de observação <<<: 

Por padrão quando criar uma tarefa, ela terá o status "Pending", e caso deseje atualizar, é possível na aba "Update Task".
A funcionalidade da aba "Search Task" não funciona pesquisando apenas letras ou parte de palavras, para achar a linha registrada, é necessário que pesquise o nome inteiro da tarefa.
Os ID's são autoincrementados.

## Não utilizei **nenhum** dos códigos do professor, tudo que foi feito, foi realizado a partir de:

- Aprendizado em aula;
- Pesquisas individuais;
- Criação individual do aluno;
- Interações com variados conteúdos na internet.

*Focando exclusivamente no aprendizado individual do aluno, comprovando com o resultado positivo ao final do projeto*

'''
