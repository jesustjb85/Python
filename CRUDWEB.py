import streamlit as st
import psycopg2

# Função para criar a conexão com o banco de dados PostgreSQL
def create_connection():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432",
            database="postgres"
        )
        return connection
    except Exception as e:
        st.error("Erro ao conectar ao banco de dados.")
        raise e

# Função para executar uma consulta no banco de dados
def run_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        st.success("Consulta executada com sucesso.")
    except Exception as e:
        st.error(f"Erro ao executar a consulta: {e}")
    finally:
        cursor.close()

# Função para buscar dados do banco de dados
def fetch_data(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
    finally:
        cursor.close()

def main():
    
    st.title("CRUD de Postgres")
    st.title("Clientes")

    # Criando a conexão com o banco de dados
    connection = create_connection()

    # Opções do CRUD
    options = ["Inserir", "Buscar", "Excluir", "Atualizar"]
    choice = st.selectbox("Ação no Banco:", options)

    if choice == "Inserir":
        st.header("Inserir Dados")

        # Campos de input para receber as informações do cliente
        nome = st.text_input("Nome:")
        idade = st.number_input("Idade:", min_value=0, step=1)
        endereco = st.text_input("Endereço:")

        # Botão para inserir os dados no banco de dados
        if st.button("Inserir"):
            # Executando a inserção no banco de dados
            query = f"INSERT INTO clientes (nome, idade, endereco) VALUES ('{nome}', {idade}, '{endereco}');"
            run_query(connection, query)
            st.success("Dados inseridos com sucesso.")

    elif choice == "Buscar":
        st.header("Buscar Dados")

        # Opções de busca
        search_option = st.radio("Buscar por:", ("ID", "Nome"))

        if search_option == "ID":
            # Campo de input para receber o ID do cliente a ser buscado
            id_busca = st.number_input("ID do cliente a ser buscado:", min_value=1, step=1)

            if st.button("Buscar"):
                query = f"SELECT * FROM clientes WHERE id = {id_busca};"
                result = fetch_data(connection, query)

                if result:
                    st.subheader("Resultado:")
                    st.write(f"ID: {result[0][0]}, Nome: {result[0][1]}, Idade: {result[0][2]}, Endereço: {result[0][3]}")
                else:
                    st.warning("Nenhum resultado encontrado.")
        elif search_option == "Nome":
            # Campo de input para receber o nome do cliente a ser buscado
            nome_busca = st.text_input("Nome do cliente a ser buscado:")

            if st.button("Buscar"):
                query = f"SELECT * FROM clientes WHERE nome ILIKE '%{nome_busca}%';"
                results = fetch_data(connection, query)

                if results:
                    st.subheader("Resultados:")
                    for result in results:
                        st.write(f"ID: {result[0]}, Nome: {result[1]}, Idade: {result[2]}, Endereço: {result[3]}")
                else:
                    st.warning("Nenhum resultado encontrado.")


    elif choice == "Atualizar":
        st.header("Atualizar Dados")

        # Campo de input para receber o ID do cliente a ser atualizado
        id_atualiza = st.number_input("ID do cliente a ser atualizado:", min_value=1, step=1)

        # Verifica se o ID informado existe no banco de dados antes de realizar a atualização
        if st.button("Verificar ID"):
            query = f"SELECT * FROM clientes WHERE id = {id_atualiza};"
            result = fetch_data(connection, query)

            if result:
                st.success("ID encontrado no banco de dados.")
            else:
                st.warning("ID não encontrado no banco de dados.")

        # Campos de input para receber as novas informações do cliente
        novo_nome = st.text_input("Novo Nome:")
        nova_idade = st.number_input("Nova Idade:", min_value=0, step=1)
        novo_endereco = st.text_input("Novo Endereço:")

        # Botão para realizar a atualização no banco de dados
        if st.button("Atualizar"):
            # Executando a atualização no banco de dados
            query = f"UPDATE clientes SET nome = '{novo_nome}', idade = {nova_idade}, endereco = '{novo_endereco}' WHERE id = {id_atualiza};"
            run_query(connection, query)
            st.success("Dados atualizados com sucesso.")

    elif choice == "Excluir":
        st.header("Excluir Dados")

        # Opções de busca
        search_option = st.radio("Buscar por:", ("ID", "Nome"))

        if search_option == "ID":
            # Campo de input para receber o ID do cliente a ser buscado
            id_busca = st.number_input("ID do cliente a ser buscado:", min_value=1, step=1)

            if st.button("Buscar"):
                query = f"SELECT * FROM clientes WHERE id = {id_busca};"
                result = fetch_data(connection, query)

                if result:
                    st.subheader("Resultado:")
                    for row in result:
                        st.write(f"ID: {row[0]}, Nome: {row[1]}, Idade: {row[2]}, Endereço: {row[3]}")
                    
                    # Campo de input para receber o ID do cliente a ser excluído
                    id_excluir = st.number_input("ID do cliente a ser excluído:", min_value=1, step=1)
                    
                    if st.button("Excluir"):
                        query = f"DELETE FROM clientes WHERE id = {id_excluir};"
                        run_query(connection, query)
                        st.success("Dados excluídos com sucesso.")
                        # Redirecionar para a seção de Buscar
                        st.experimental_rerun()

                else:
                    st.warning("Nenhum resultado encontrado.")

        elif search_option == "Nome":
            # Campo de input para receber o nome do cliente a ser buscado
            nome_busca = st.text_input("Nome do cliente a ser buscado:")

            if st.button("Buscar"):
                query = f"SELECT * FROM clientes WHERE nome ILIKE '%{nome_busca}%';"
                results = fetch_data(connection, query)

                if results:
                    st.subheader("Resultados:")
                    for result in results:
                        st.write(f"ID: {result[0]}, Nome: {result[1]}, Idade: {result[2]}, Endereço: {result[3]}")
                    
                    # Campo de input para receber o ID do cliente a ser excluído
                    id_excluir = st.number_input("ID do cliente a ser excluído:", min_value=1, step=1)
                    
                    if st.button("Excluir"):
                        query = f"DELETE FROM clientes WHERE id = {id_excluir};"
                        run_query(connection, query)
                        st.success("Dados excluídos com sucesso.")
                        # Redirecionar para a seção de Buscar
                        st.experimental_rerun()

                else:
                    st.warning("Nenhum resultado encontrado.")



if __name__ == "__main__":
    main()
