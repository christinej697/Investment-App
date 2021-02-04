#----------------------------------------------------
# CSCI482-483 Capstone project
# Provide a basic stock market knowledge to teach a beginner   
# how to start their investments of stock market.
#----------------------------------------------------
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

import yfinance as yf
import datetime
import numpy as np
import pandas as pd
from pandas_datareader import data, wb

import requests
import matplotlib
from yahoo_fin import stock_info as si
from yahoo_fin.stock_info import get_data
from dividdb import set_dividdb

basebudge = 0
#-----------------------------------------------------

def get_db_connection():
    conn = sqlite3.connect('database/database.db')

    conn.row_factory = sqlite3.Row
    return conn

#-----------------------------------------------------
# initialize users table
#-----------------------------------------------------

def initial_db_connection():
    conn = sqlite3.connect('database/database.db')
    conn.execute('DELETE FROM users')

    conn.row_factory = sqlite3.Row
    return conn
#-----------------------------------------------------
# initialize dividend table
#-----------------------------------------------------

def initial_dividdb_connection():
    conn = sqlite3.connect('database/database.db')
    conn.execute('DELETE FROM dividends')
    conn.commit()

    conn.row_factory = sqlite3.Row
    return conn

#------------------------------------------------------
# Create a new Flask route with a view function and a new HTML
# template to display an individual users by ite ID.
# For example: http://127.0.0.1:5000/1
#------------------------------------------------------

def get_post(post_symbol):
    conn = get_db_connection()

    post = conn.execute('SELECT * FROM dividends WHERE Symbol = ?',
                        (post_symbol,)).fetchone()
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

@app.route('/stocks', methods=('GET', 'POST'))
def stock():
    if request.method == 'POST':
        ticker = request.form['Shares']
        if not ticker:
            flash('A share is required!')
        else:
            return redirect(url_for('quote', ticker=ticker))
    return render_template('shares.html')


#---------------------------------------------
def fetch_price(ticker):
    data = requests.get('https://financialmodelingprep.com/api/v3/stock/real-time-price/{}'.format(ticker.upper()), params={'apikey':'demo'}).json()
    if data and "price" in data:
        return data["price"]
    else:
        return "none"

@app.route('/stocks/<ticker>')
def quote(ticker):
     stock_price = fetch_price(ticker)
#     return "This price of {} is {}".format(ticker, stock_price)


     symbol =request.args.get('symbol', default=ticker)
     period = request.args.get('period', default="1y")
     interval = request.args.get('interval', default="1mo")

	#pull the quote
     quote = yf.Ticker(symbol)	
     amazon_weekly= get_data("amzn", start_date="12/04/2009", end_date="12/04/2019", index_as_date = True, interval="1wk")

     return render_template('simple.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
#     df = amazon_weekly.values.tolist()
#     JSONP_data = jsonify(df)
#     return JSONP_data
#     dow_list = si.tickers_dow()


#     quote = yf.Ticker(symbol)
#     return quote.info
#--------------------------------------------------
# API route for pulling the stock history
#--------------------------------------------------

@app.route("/history")
def display_history():
	#get the query string parameters
	symbol = request.args.get('symbol', default="AAPL")
	period = request.args.get('period', default="1y")
	interval = request.args.get('interval', default="1mo")

	#pull the quote
	quote = yf.Ticker(symbol)	
	#use the quote to pull the historical data from Yahoo finance
	hist = quote.history(period=period, interval=interval)
	#convert the historical data to JSON
	data = hist.to_json()
	#return the JSON in the HTTP response
	return data

#---------------------------------------------

@app.route('/signIn', methods=('GET', 'POST'))
def signin():
    global basebudge
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
            basebudge = base

            conn = initial_db_connection()
            conn.execute('INSERT INTO users (FirstName, LastName, Age, Street, Apartment, Zipcode, State, Budget, Base) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (fname, lname, age, street, apt, zip, state, budget, base))
            conn.commit()
            return redirect(url_for('advice'))

    return render_template('users.html', post=post)

#------------------------------------------------
# Display the budget of recommendation
#------------------------------------------------

@app.route('/signIn/advice', methods=('GET', 'POST'))
def advice():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    if request.method == 'POST':

        return redirect(url_for('dividend'))
    return render_template('advice.html', posts=posts)

#------------------------------------------------

@app.route('/signIn/advice/dividend', methods=('GET', 'POST'))
def dividend():
    global basebudge
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    if request.method == 'POST':
        divid=request.form['dividend']
        initial_dividdb_connection()
        conn = get_db_connection()
        if divid=="dividend":
            conn.execute('UPDATE users SET Dividend = ? WHERE id = 1', "Y")
        else:
            conn.execute('UPDATE users SET Dividend = ? WHERE id = 1', "N")
        conn.commit()
        conn.close()

        dow_list = si.tickers_dow()
        print(dow_list[0:10])

        for ticker in dow_list[0:10]:
            quote_table = si.get_quote_table(ticker)
            quoteprice = round(quote_table["Quote Price"],2)
            if quoteprice <= basebudge:
                quotedivid = quote_table["Forward Dividend & Yield"]

                if divid=="dividend" and quotedivid!="N/A (N/A)":
                    quote = yf.Ticker(ticker)
                    quotename = quote.info["shortName"]
                    conn = get_db_connection()
                    conn.execute('INSERT INTO dividends (Symbol, Company, Price, DividendYield) VALUES(?, ?, ?, ?)',
                        (ticker, quotename, quoteprice, quotedivid ))
                    conn.commit()
                    conn.close()

                if divid=="without dividend" and quotedivid=="N/A (N/A)":
                    quote = yf.Ticker(ticker)
                    quotename = quote.info["shortName"]
                    conn = get_db_connection()
                    conn.execute('INSERT INTO dividends (Symbol, Company, Price, DividendYield) VALUES(?, ?, ?, ?)',
                        (ticker, quotename, quoteprice, quotedivid ))
                    conn.commit()
                    conn.close()

        return redirect(url_for('display', divid=divid))
    return render_template('dividend.html', posts=posts)

#------------------------------------------------

@app.route('/signIn/advice/dividend/display', methods=('GET', 'POST'))
def display():

#    divid = request.args.get('divid')
    conn =get_db_connection()
    posts = conn.execute('SELECT * FROM dividends').fetchall()
    conn.close()
    if request.method == 'POST':

        return redirect(url_for('dividend'))

    return render_template('filter.html', posts=posts)

#------------------------------------------------

@app.route('/<page>', methods=('GET', 'POST'))
def post(page):

    hsitorical_datas = {}
    labels = []
    values = []
    start = "01/01/2021"
    end = datetime.date.today()
    interval="1d"
    quote = yf.Ticker(page)
    quotename = quote.info["shortName"]
    legend = quotename + " Historical Stock Line Chart"

    historical_datas = si.get_data(page, start_date=start, end_date=end)
    t_labels = historical_datas.index
    for i in t_labels:
        labels.append(i.date())
    t_values = historical_datas.adjclose

    for i in t_values:
        values.append(round(i,2))

    while True:
        if request.method == 'POST':
            start = request.form['Starts']
            end = request.form['Ends']

            historical_datas = si.get_data(page, start_date=start, end_date=end)
            t_labels = historical_datas.index
            labels = []
            values = []

            for i in t_labels:
                labels.append(i.date())
            t_values = historical_datas.adjclose

            for i in t_values:
                values.append(round(i,2))

#            return redirect(url_for('display'))

        return render_template('chart.html', values=values, labels=labels, legend=legend, start=start, end=end)
