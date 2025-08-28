import time
import webbrowser
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask import render_template
import os
from mysql.connector import connect, Error
from flask_socketio import SocketIO

load_dotenv()
db_user = os.getenv("MYSQL_USERNAME")
db_host = os.getenv("MYSQL_HOST")
db_password = os.getenv("MYSQL_PASSWORD")
db_port = os.getenv("MYSQL_PORT")
db_database = os.getenv("MYSQL_DATABASE")

app = Flask(__name__)
socketio = SocketIO(app)

try:
    connection = connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )
    print(f"Connected to database {db_database}")
except Error as e:
    print(e)
    exit()

def find_tables():
    # Fetch all table names in the database
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        return tables


def show_table(table):
    show_table_query = f"DESCRIBE {table}"
    with connection.cursor() as cursor:
        cursor.execute(show_table_query)
        # Fetch rows from last executed query
        result = []
        for row in cursor.fetchall():
            result.append(str(row))
        return result

# Grab the tables and their data from the database
tables = find_tables()
table_datas = []
for i in range(0, len(tables)):
    tables[i]=str(tables[i])[2:-3]
    table_datas.append(show_table(tables[i]))

# Function to run user inputted sql code
def execute_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        table = cursor.fetchall()
        return table

clients = 0

# Event triggered when a client connects
@socketio.on('connect')
def handle_connect():
    print("Connected to web client")
    global clients
    clients += 1

def checkRefresh():
    time.sleep(2)
    return (clients > 0)

# Event triggered when a client disconnects
@socketio.on('disconnect')
def handle_disconnect():
    global clients
    clients -= 1
    if(checkRefresh()):
        print("Client refereshed OR another client still connected")
    else: 
        print("Web client disconnected")
        os._exit(0)

@app.route('/')
def index():
    return render_template('index.html', form_text="", database=db_database, tables=tables, len=len(tables), table_datas=table_datas)

@app.route('/sql_results', methods=['POST'])
def sql_results():
    query = request.form.get('chat-input')
    try:
        result = execute_sql(query)
    except Exception:
        return render_template('sql_fail.html', form_text=query, database=db_database, tables=tables, len=len(tables), table_datas=table_datas)
    else:
        # Only SELECT statements
        if query[0:6].upper() != "SELECT":
            return render_template('sql_fail.html', form_text=query, database=db_database, tables=tables, len=len(tables), table_datas=table_datas)
        # Check is Result is emptty
        if(not result):
            return render_template('sql_empty.html', form_text=query, database=db_database, tables=tables, len=len(tables), table_datas=table_datas)
        table_height = len(result)
        table_width = len(result[0])
        return render_template('sql_results.html', form_text=query, width=table_width, height=table_height, result=result, database=db_database, tables=tables, len=len(tables), table_datas=table_datas)

if __name__ == '__main__':
    webbrowser.open_new(f'http://127.0.0.1:5000/')
    socketio.run(app, host="127.0.0.1", port=5000)