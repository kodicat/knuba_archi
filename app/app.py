from flask import Flask, render_template, request, redirect, jsonify
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
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTERGER NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS partners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# @app.route('/')
# def index():
#     conn = sqlite3.connect('flowers.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM flowers')
#     flowers = cursor.fetchall()
#     conn.close()
#     return render_template('index.html', flowers=flowers)

# @app.route('/add_flower', methods=['POST'])
# def add_flower():
#     name = request.form['name']
#     price = request.form['price']
#     conn = sqlite3.connect('flowers.db')
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO flowers (name, price) VALUES (?, ?)', (name, price))
#     conn.commit()
#     conn.close()
#     return redirect('/')

def get_db_connection():
    conn = sqlite3.connect('flowers.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

# flowers
@app.route('/api/flowers', methods=['POST'])
def api_add_flower():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO flowers (name, price) VALUES (?, ?)', (name, price))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': user_id, 'name': name, 'price': price}), 201

@app.route('/api/flowers/<int:id>', methods=['GET'])
def api_get_flower(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flowers WHERE id = ?", (id,))
    flower = cursor.fetchone()
    conn.close()
    
    if flower is None:
        return jsonify({'message': 'Flower not found'}), 404
    
    return jsonify(dict(flower))

@app.route('/api/flowers', methods=['GET'])
def api_get_flowers():
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flowers")
    flowers = cursor.fetchall()
    conn.close()

    return flowers

@app.route('/api/flowers/<int:id>', methods=['PUT'])
def api_update_flower(id):
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE flowers SET name = ?, price = ? WHERE id = ?", (name, price, int(id)))
    conn.commit()
    conn.close()
    
    return jsonify({'id': id, 'name': name, 'price': price})

@app.route('/api/flowers/<int:id>', methods=['DELETE'])
def api_delete_flowers(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM flowers WHERE id = ?", (int(id),))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Flower deleted'})

# clients
@app.route('/api/clients', methods=['POST'])
def api_add_client():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (name, age) VALUES (?, ?)', (name, age))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': user_id, 'name': name, 'age': age}), 201

@app.route('/api/clients/<int:id>', methods=['GET'])
def api_get_client(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE id = ?", (id,))
    item = cursor.fetchone()
    conn.close()
    
    if item is None:
        return jsonify({'message': 'Client not found'}), 404
    
    return jsonify(dict(item))

@app.route('/api/clients', methods=['GET'])
def api_get_clients():
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients")
    items = cursor.fetchall()
    conn.close()

    return items

@app.route('/api/clients/<int:id>', methods=['PUT'])
def api_update_client(id):
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE clients SET name = ?, age = ? WHERE id = ?", (name, age, int(id)))
    conn.commit()
    conn.close()
    
    return jsonify({'id': id, 'name': name, 'age': age})

@app.route('/api/clients/<int:id>', methods=['DELETE'])
def api_delete_clients(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id = ?", (int(id),))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Client deleted'})

# partners
@app.route('/api/partners', methods=['POST'])
def api_add_partner():
    data = request.get_json()
    name = data.get('name')
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO partners (name) VALUES (?)', (name,))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': user_id, 'name': name}), 201

@app.route('/api/partners/<int:id>', methods=['GET'])
def api_get_partner(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM partners WHERE id = ?", (id,))
    item = cursor.fetchone()
    conn.close()
    
    if item is None:
        return jsonify({'message': 'Partner not found'}), 404
    
    return jsonify(dict(item))

@app.route('/api/partners', methods=['GET'])
def api_get_partners():
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM partners")
    items = cursor.fetchall()
    conn.close()

    return items

@app.route('/api/partners/<int:id>', methods=['PUT'])
def api_update_partner(id):
    data = request.get_json()
    name = data.get('name')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE partners SET name = ? WHERE id = ?", (name, int(id)))
    conn.commit()
    conn.close()
    
    return jsonify({'id': id, 'name': name})

@app.route('/api/partners/<int:id>', methods=['DELETE'])
def api_delete_partners(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM partners WHERE id = ?", (int(id),))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Partner deleted'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
