import psycopg2
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(os.environ.get("postgresql://leaderboard_db_55ut_user:FlEG9AHWe6Nutq0bZZAqSsWXJlxJ0BzC@dpg-d05vvkuuk2gs73ce9sig-a.oregon-postgres.render.com/leaderboard_db_55ut"))

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/submit-score', methods=['POST'])
def submit_score():
    data = request.get_json()
    name = data['name']
    score = data['score']
    date = data['date']

    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO scores (name, score, date) VALUES (%s, %s, %s)', (name, score, date))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Score submitted successfully'}), 201

@app.route('/get-leaderboard', methods=['GET'])
def get_leaderboard():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT name, score, date FROM scores ORDER BY score DESC LIMIT 5')
    scores = c.fetchall()
    conn.close()

    leaderboard = []
    for name, score, date in scores:
        leaderboard.append({
            'name': name,
            'score': score,
            'date': date
        })

    return jsonify(leaderboard)

@app.route('/')
def home():
    return "Leaderboard Server is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)