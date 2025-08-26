from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask import render_template
import os
from mysql.connector import connect, Error

load_dotenv()
db_user = os.getenv("MYSQL_USERNAME")
db_password = os.getenv("MYSQL_PASSWORD")
db_port = 3306
db_database = "Overwatch"

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

def show_table(table):
    show_table_query = f"DESCRIBE {table}"
    with connection.cursor() as cursor:
        cursor.execute(show_table_query)
        # Fetch rows from last executed query
        result = []
        for row in cursor.fetchall():
            result.append(str(row))
        print(result)
        return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/characters")
def characters():
    return render_template("table.html", table_name="characters", table=show_table("characters"))

@app.route("/affiliations")
def affiliations():
    return render_template("table.html", table_name="affiliations", table=show_table("affiliations"))

@app.route("/characteraffiliations")
def characteraffiliations():
    return render_template("table.html", table_name="characteraffiliations", table=show_table("characteraffiliations"))

if __name__ == '__main__':
    app.run()