from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask import render_template
import os
from mysql.connector import connect, Error

load_dotenv()
db_user = os.getenv("MYSQL_USERNAME")
db_password = os.getenv("MYSQL_PASSWORD")
db_port = os.getenv("MYSQL_PORT")
db_database = os.getenv("MYSQL_DATABASE")

app = Flask(__name__)

try:
    connection = connect(
        host="localhost",
        user=db_user,
        password=db_password,
        database=db_database
    )
    print("Connected:", connection.is_connected())
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

@app.route('/')
def home():
    tables = find_tables()
    table_datas = []
    for i in range(0, len(tables)):
        tables[i]=str(tables[i])[2:-3]
        table_datas.append(show_table(tables[i]))
    return render_template('index.html', database=db_database, tables=tables, len=len(tables), table_datas=table_datas)

if __name__ == '__main__':
    app.run()