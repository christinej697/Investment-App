#----------------------------------------------------
# CSCI482-483 Capstone project
# Provide a basic stock market knowledge to teach a beginner   
# how to start their investments of stock market.
#----------------------------------------------------
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

#-----------------------------------------------------

def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row
    return conn
#------------------------------------------------------

def initial_db_connection():
    conn = sqlite3.connect('database/database.db')
    conn.execute('DELETE FROM users')
    conn.row_factory = sqlite3.Row
    return conn
#------------------------------------------------------
# Create a new Flask route with a view function and a new HTML
# template to display an individual users by ite ID.
# For example: http://127.0.0.1:5000/1
#------------------------------------------------------

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM users WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post
#-------------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


#---------------------------------------------

@app.route('/signIn', methods=('GET', 'POST'))
def signin():
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    if request.method == 'POST':
        fname = request.form['FirstName']
        lname = request.form['LastName']
        age = request.form['Age']
        street = request.form['Street']
        apt = request.form['Apartment']
        zip = request.form['Zipcode']
        state = request.form['State']
        budget = request.form['Budget']

        if not (fname or lname):
            flash('Name is required!')
        elif not budget:
            flash('Budget is required!')
        else:
            if int(budget) <= 1500:
                base = 0
            elif int(budget) > 1500 and int(budget) <= 2500:
                base = int(budget)*0.1
            elif int(budget) > 2500 and int(budget) <= 4000:
                base = int(budget)*0.12
            else:
                base = int(budget)*0.15
            conn = get_db_connection()
            conn.execute('INSERT INTO users (FirstName, LastName, Age, Street, Apartment, Zipcode, State, Budget, Base) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (fname, lname, age, street, apt, zip, state, budget, base))
            conn.commit()
            return redirect(url_for('advice'))

    return render_template('users.html', post=post)

#---------------------------------------------

@app.route('/quote', methods=('GET', 'POST'))
def home():
    return render_template('homepage.html')

#------------------------------------------------

@app.route('/signIn/advice', methods=('GET', 'POST'))
def advice():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    if request.method == 'POST':
       return redirect(url_for('divident'))
    return render_template('advice.html', posts=posts)

#------------------------------------------------

@app.route('/signIn/advice/divident', methods=('GET', 'POST'))
def divident():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    if request.method == 'POST':
        divid=request.form['divident']
        if divid=="divident":
            temp="Y"
        else:
            temp="N"
        conn = get_db_connection()
        conn.execute('UPDATE users SET Divident = ? WHERE id = 1', (temp))
        conn.commit()
        return redirect(url_for('display', divid=divid))
    return render_template('divident.html', posts=posts)

#------------------------------------------------

@app.route('/signIn/advice/divident/display', methods=('GET', 'POST'))
def display():
    divid = request.args.get('divid')
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    if request.method == 'POST':
       return redirect(url_for('index'))
    if divid=="divident":
       return render_template('bonus.html', posts=posts)
    else:
       return render_template('unbonus.html', posts=posts)
#------------------------------------------------

#@app.route('/<int:post_id>')
#def post(post_id):
#    post = get_post(post_id)
#    return render_template('post.html', post=post)
