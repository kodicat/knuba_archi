from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flowers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flowers')
    flowers = cursor.fetchall()
    conn.close()
    return render_template('index.html', flowers=flowers)

@app.route('/add_flower', methods=['POST'])
def add_flower():
    name = request.form['name']
    price = request.form['price']
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO flowers (name, price) VALUES (?, ?)', (name, price))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
