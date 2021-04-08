<h1 align = "center"> Investment Web Application: StockSmart </h1>

_Main Contributors: Yuehchen Tsou and Christine Johnson
<br>This directory contains code for the StockSmart website application. The application is being created as a capstone project for Montana State University. The main code for the application is written in Python using the Flask framework and html to format the website. SQL is used for data manipulation._

# Table of Contents
1. [Technologies Used](#Technologies)
2. [Project's Main Functions](#Three)
3. [Workflow Diagram](#Workflow)
4. [Project Demo](#Demo)
5. [Running the Project](#Running)
6. [Unit Tests](#Testing)
8. [Citations](#Citations)

## Technologies used <a name="Technologies"></a>
<li>Python 3.6+
<li>Web App library: Flask
<li>Data and array libraries: Pandas and Numpy
<li>Financial data library: Yfinance
<li>Machine learning libraries: Tensorflow, Keras
<li>Machine learning models: LSTM
<li>Plotting library: Chart.js
<li>Database: MySQL is a relational database management system
<li>HTML, CSS, and JavaScript are used to control presentation, formatting, and layout 
  
## Three main functions of the project <a name="Three"></a>
1. Simple Stock Recommendation List for Beginners
2. Historical Price & Dividend for Favored Shares
3. Times Series Machine Learning to Predict Stock Price
  
## Workflow
![workflow](https://user-images.githubusercontent.com/50720457/113912170-10f13b00-9798-11eb-9fbc-9619462402b2.png)

  
## Demo of our Project <a name="Demo"></a>
https://user-images.githubusercontent.com/50720457/113515834-0cc4e380-9534-11eb-8b5c-d15dcdf39395.mp4

## How to Run the Project <a name="Running"></a>
After downloading source code from the github page, which will download as "Investment-App-main", open the folder within a running Python environment. To start the StockSmart Flask website, run the following three commands: (1) `export FLASK_APP=stockApp`, (2) `export FLASK_ENV=development`, and (3) `flask run`. Then click the resulting website link, or manually enter `http://127.0.0.1:5000/`, to see the website in action.

## Unit Testing the Flask Application <a name="Testing"></a>
We used the python built-in framework `unittest`, to write the unit tests for our Python flask application. Our unit test are contained in the file `test.py`. We tested to make sure that flask was set up correctly, that each html page loads correctly, and that each page’s functions work correctly.

## Citations
“Yahoo Finance API - A Complete Guide - AlgoTrading101 Blog.” Quantitative Trading Ideas and Guides - AlgoTrading101 Blog, 11 Jan. 2021 
<br> https://algotrading101.com/learn/yahoo-finance-api-guide/

How To Make a Web Application Using Flask in Python 
<br> By Abdelhadi Dyouri, Published onApril 16, 2020
<br> https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3#step-6-%E2%80%94-displaying-a-single-post

Creating Charts with Chart.js in a Flask Application
<br> JANUARY 1, 2017 / PATKENNEDY79@GMAIL.COM
<br> https://www.patricksoftwareblog.com/creating-charts-with-chart-js-in-a-flask-application/

Feature Selection for Time Series Forecasting with Python by Jason Brownlee on March 29, 2017 in Time Series
<br> https://machinelearningmastery.com/feature-selection-time-series-forecasting-python/

Stock Market Predictions with LSTM in Python by Thushan Ganegedara January 1st, 2020
<br> https://www.datacamp.com/community/tutorials/lstm-python-stock-market

Flask Paginate Doc
<br> https://pythonhosted.org/Flask-paginate/

The Flask Mega-Tutorial Part IX: Pagination
<br> https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination

Unit Testing a Flask Application
<br> https://www.patricksoftwareblog.com/unit-testing-a-flask-application/
