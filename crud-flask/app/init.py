from flask import Flask, render_template, request, jsonify
import os
import json
import psycopg2

app = Flask(__name__)

# Configurações do banco de dados
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
        print("Erro ao conectar ao banco de dados:", e)

# Função para buscar todos os dados do banco de dados
def fetch_all_data():
    connection = create_connection()
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM clientes;"
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("Erro ao buscar dados:", e)
    finally:
        cursor.close()
        connection.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_data")
def get_data_route():
    data = fetch_all_data()
    return jsonify(data)

@app.route("/save_data", methods=["POST"])
def save_data_route():
    new_data = json.loads(request.data)
    connection = create_connection()
    try:
        cursor = connection.cursor()
        query = "INSERT INTO clientes (nome, idade, endereco) VALUES (%s, %s, %s);"
        cursor.execute(query, (new_data["nome"], new_data["idade"], new_data["endereco"]))
        connection.commit()
        return jsonify({"message": "Dados inseridos com sucesso"})
    except Exception as e:
        print("Erro ao inserir dados:", e)
        return jsonify({"message": "Erro ao inserir dados"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route("/delete_selected", methods=["POST"])
def delete_selected_data():
    selected_ids = json.loads(request.data)["ids"]
    connection = create_connection()
    try:
        cursor = connection.cursor()
        for data_id in selected_ids:
            query = f"DELETE FROM clientes WHERE id = {data_id};"
            cursor.execute(query)
        connection.commit()
        return jsonify({"message": "Dados excluídos com sucesso"})
    except Exception as e:
        print("Erro ao excluir dados:", e)
        return jsonify({"message": "Erro ao excluir dados"}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app.run(debug=True)
