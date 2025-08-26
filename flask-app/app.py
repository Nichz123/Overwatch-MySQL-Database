from flask import Flask, request, jsonify
from flask import render_template
import os
from flask_sqlalchemy import SQLAlchemy

user = os.getenv("MYSQL_USERNAME")
password = os.getenv("MYSQL_PASSWORD")
database = "Overwatch"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user}:{password}@localhost/{database}"
db = SQLAlchemy(app)

print(db)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()