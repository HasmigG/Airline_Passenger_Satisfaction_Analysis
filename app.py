import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# create routes from the database
@app.route('/api/v1.0/airlines_reviews')
def get_reviews():
    conn = sqlite3.connect('airline_passenger_satisfaction.sqlite')
    db = conn.cursor()
    results = db.execute('SELECT * FROM airlines_reviews')

    print(results.description[0])

    return jsonify(results.fetchall())



# activate dev in Airline folder "flask run"
# http://127.0.0.1:5000/