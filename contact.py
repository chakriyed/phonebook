#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 12:59:41 2024

@author: akshathaaavinashannadhani
"""

# app.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('contacts.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS contacts
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         name TEXT, 
                         phone INTEGER, 
                         email TEXT, 
                         birthday TEXT)''')

@app.route('/')
def home():
    with sqlite3.connect('contacts.db') as conn:
        contacts = conn.execute('SELECT * FROM contacts').fetchall()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form['name']
    phone = int(request.form['phone'])
    email = request.form['email']
    birthday = request.form['birthday']
    with sqlite3.connect('contacts.db') as conn:
        conn.execute('INSERT INTO contacts (name, phone, email, birthday) VALUES (?, ?, ?, ?)', (name, phone, email, birthday))
    return 'Contact added successfully!'

@app.route('/update', methods=['POST'])
def update_contact():
    try:
        name = request.form['name']
        phone = int(request.form['phone'])
        email = request.form['email']
        birthday = request.form['birthday']
        with sqlite3.connect('contacts.db') as conn:
            result = conn.execute('UPDATE contacts SET phone = ?, email = ?, birthday = ? WHERE name = ?', (phone, email, birthday, name))
            if result.rowcount == 0:
                return 'Error: Contact does not exist!'
        return 'Contact updated successfully!'
    except Exception as e:
        return f'Error: {e}'

@app.route('/delete', methods=['POST'])
def delete_contact():
    try:
        name = request.form['name']
        with sqlite3.connect('contacts.db') as conn:
            result = conn.execute('DELETE FROM contacts WHERE name = ?', (name,))
            if result.rowcount == 0:
                return 'Error: Contact does not exist!'
        return 'Contact deleted successfully!'
    except Exception as e:
        return f'Error: {e}'

@app.route('/search', methods=['GET'])
def search_contact():
    search_query = request.args.get('query', '')
    with sqlite3.connect('contacts.db') as conn:
        cursor = conn.execute('SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?', ('%{}%'.format(search_query), '%{}%'.format(search_query)))
        results = cursor.fetchall()
    return jsonify(results)

if __name__ == '__main__':
    init_db()
    app.run(port=9001)
