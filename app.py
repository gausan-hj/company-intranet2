# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, hashlib

app = Flask(_name_)
app.secret_key = 'secret-key'

def check_login(username, password):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    conn.close()
    if result:
        return hashlib.sha256(password.encode()).hexdigest() == result[0]
    return False

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if check_login(u, p):
            session['user'] = u
            return redirect('/home')
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template('home.html', username=session['user'])

if _name_ == '_main_':
    app.run(debug=True)