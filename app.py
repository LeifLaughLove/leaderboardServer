from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Set up the database (if not already set)
def init_db():
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Route to submit a new score
@app.route('/submit-score', methods=['POST'])
def submit_score():
    data = request.get_json()
    name = data['name']
    score = data['score']
    date = data['date']

    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    c.execute('INSERT INTO scores (name, score, date) VALUES (?, ?, ?)', (name, score, date))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Score submitted successfully'}), 201

# Route to get the top scores
@app.route('/get-leaderboard', methods=['GET'])
def get_leaderboard():
    conn = sqlite3.connect('leaderboard.db')
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
