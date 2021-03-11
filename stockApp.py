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
import tensorflow as tf
import csv

#from flask_paginate import Pagination, get_page_parameter

#from pandas_datareader import data, wb

import requests
from yahoo_fin import stock_info as si
from yahoo_fin.stock_info import get_data
from dividdb import set_dividdb
from view import HistoricalTicker
from trains import TrainTicker

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
#graph = tf.get_default_graph()
graph = tf.compat.v1.get_default_graph()

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

#---------------------------------------------

@app.route('/<hists>', methods=('GET', 'POST'))
def stocks(hists):
    if hists == "post":
        titles = "Historical Price & Dividend"
    else:
        titles = "Prediction of Price"
    if request.method == 'POST':
        ticker = request.form['Shares']
        print("hists: ", hists, ticker)
        return redirect(url_for(hists, ticker=ticker, checks='index'))
    return render_template('shares.html', titles=titles)


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

#        dow_list = si.tickers_dow()
        dow_list = get_dowjones()
#        dow_list = pd.read_csv('dow_jones.csv')
#        dow_list = [list(row) for row in df.values]

        for ticker in dow_list:
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

    divid = request.args.get('divid')
    conn =get_db_connection()
    posts = conn.execute('SELECT * FROM dividends').fetchall()
    conn.close()
    if request.method == 'POST':

        return redirect(url_for('dividend'))

    return render_template('filter.html', posts=posts)

#------------------------------------------------

@app.route('/<ticker>/<checks>', methods=('GET', 'POST'))
def post(ticker, checks):

    if request.method == 'POST':
        start = request.form['Starts']
        end = request.form['Ends']
    else:
        start = "01/01/2021"
        end = datetime.date.today()

    mastervalue = HistoricalTicker(ticker)
    values, quotes = mastervalue.build_history(start, end)
    tvalues = []
    for i in values["pricevalues"]:
        tvalues.append(round(i,2))
    values['pricevalues'] = tvalues

    return render_template('chart.html',  values = values, quotes=quotes, checks=checks)

#------------------------------------------------

@app.route('/timeseries/<ticker>', methods=('GET', 'POST'))
def timeseries(ticker):
    global graph
    with graph.as_default():
        masterinfo = TrainTicker(ticker)
        info = masterinfo.build_history("5y")

        info["actualprice"] = info["actualprice"].reshape(-1)
        info["predictprice"] = info["predictprice"].reshape(-1)
        return render_template('predicted.html', info=info)
#        return render_template('plot.html', plot_url=info)


#-------------------------------------------------
#@app.route('/timeseries/<ticker>', methods=('GET', 'POST'))
#def timeseries(ticker):
#    if request.method == 'POST':
#        ticker = request.form['Shares']
#    masterinfo = TrainTicker(ticker)
#    plot_url = masterinfo.build_history("5y")
#        return redirect(url_for('stocks', page=ticker, checks='index'))
#    return render_template('plot.html', plot_url=plot_url)

#-------------------------------------------

def get_dowjones():

    dow_list = []
    with open('database/dow_jones.csv') as f:
        line = csv.reader(f)
        for row in line:
            dow_list.append(row[0])

    f.close()
    return dow_list
