import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# create routes from the database

# activate dev in Airline folder "flask run"
# http://127.0.0.1:5000/