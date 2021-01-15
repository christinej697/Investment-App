import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database/database1.db')
    conn.row_factory = sqlite3.Row
    return conn


#def get_post(post_id):
#    conn = get_db_connection()
#    post = conn.execute('SELECT * FROM users WHERE id = ?',
#                        (post_id,)).fetchone()
#    conn.close()
#    if post is None:
#        abort(404)
#    return post


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')

def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

