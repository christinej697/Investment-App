import datetime
from datetime import date, timedelta
import yfinance as yf
from yahoo_fin import stock_info as si

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import base64
from io import BytesIO
import os
import math
from array import array

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

#----------------------------------------

class TrainTicker():

    def __init__(self, ticker):

        self.ticker = ticker

        self.info = {
                  "name": "",
                  "actualdate": "",
                  "actualprice": "",
                  "predictdate": "",
                  "predictprice": ""
                }
#-----------------------------------------------

    def build_history(self, periods):

        self.quote = yf.Ticker(self.ticker)
        self.info['name'] = self.quote.info["shortName"]
#--- parse historical data of a period from Yahoo Finacne

        df = self.quote.history(period=periods)
        fig = plt.figure(figsize=(10, 5))

        n = int(0.8*(len(df)))
        ep=50
        training_set = df.iloc[:n, 3:4].values
        test_set = df.iloc[n:, 3:4].values
#-----------------------------------------------
#  Data Normalization : Rescaling the data from the original data so that
#  all values are within the range of 0 and 1.
#-----------------------------------------------

        sc = MinMaxScaler(feature_range = (0, 1))
        training_set_scaled = sc.fit_transform(training_set)

        x_train = []
        y_train = []
        pastday = 22
        futureday = 5
        for i in range(pastday, n):
            x_train.append(training_set_scaled[i-pastday:i, 0])  # 0-21, 22-43,...
            y_train.append(training_set_scaled[i, 0])    # 22, 44,...
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

#---------------------------------------------------------
#  Create the model will neural network having 3 layers of LSTM.
#    Add the LSTM layers and some Dropout regularisation
#---------------------------------------------------------

        model = Sequential()

        model.add(LSTM(units = 100, return_sequences = True, input_shape = (x_train.shape[1], 1)))
        model.add(Dropout(0.2))

        model.add(LSTM(units = 100, return_sequences = True))
        model.add(Dropout(0.2))

        model.add(LSTM(units = 50, return_sequences = True))
        model.add(Dropout(0.2))

        model.add(LSTM(units = 50))
        model.add(Dropout(0.2))

        model.add(Dense(units = 1))

#------------------------------------------------------------
#  Compile and fit the model
#------------------------------------------------------------

        model.compile(optimizer = 'adam', loss = 'mean_squared_error')
        model.fit(x_train, y_train, epochs = ep, batch_size = 32)

#-----------------------------------------------------------------
#  Once the model is created, it can be saved. Proceeding forward,
#  then we need to find out the starting point based on the user inputs for
#  "Ahead" and "Days". The data is reshaped next.
#-----------------------------------------------------------------

        dataset_train = df.iloc[:n, 3:4]    # 1008
        dataset_test = df.iloc[n:, 3:4]     # 252

        dataset_total = df.iloc[:, 3:4]     # rows: 1260

        inputs = dataset_total[len(dataset_train) - pastday:].values   # 1008 - 22 = 986
        inputs = inputs.reshape(-1,1)
        inputs = sc.fit_transform(inputs)   # 274

        x_test = []
        for i in range(pastday, inputs.shape[0]):   # 252
            x_test.append(inputs[i-pastday:i, 0])
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

#----------------------------------------------------
#   Predict with the model on the test data
#----------------------------------------------------

        predicted_stock_price = model.predict(x_test)
        predicted_stock_price = sc.inverse_transform(predicted_stock_price)

        ndate=df.index
        tdate = []
        k=0
        for i in ndate:
            tdate.append(ndate[k].date())
            k = k + 1
        df['Date'] = tdate
        df=df.reset_index(drop=True)

        train_predict_price = np.append(dataset_train, predicted_stock_price)

#-----------------------------------------------------
#    Plot the actual and predicted data
#-----------------------------------------------------

        self.info["actualdate"] = df.loc[:, 'Date'] 
        self.info["actualprice"] = dataset_total.values
        self.info["predictdate"] = df.loc[n:, 'Date']
        self.info["predictprice"] = train_predict_price

#------------------------------------------------------
# Use matplotlib to display the graph
#------------------------------------------------------
        plt.plot(df.loc[:, 'Date'],dataset_total.values, color = 'red', label = 'Actual Price')
        plt.plot(df.loc[n:, 'Date'],predicted_stock_price, color = 'blue', label = 'Predicted Price')

        plt.title('Stock Price Prediction')
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Price', fontsize=12)

        plt.legend()
        plt.xticks(rotation=90)
        STOCK = BytesIO()
        plt.savefig(STOCK, format="png")
#--- Send the plot to plot.html

        STOCK.seek(0)
        plot_url = base64.b64encode(STOCK.getvalue()).decode('utf8')
#        return plot_url

#-----------------------------------------------------
        return self.info
#--------------------------------------------------
#        hist = self.quote.history(period=periods)
#        fig = plt.figure(figsize=(10, 5))
#        df = hist
#        train = df[:int(0.7*(len(df)))]
#        valid = df[int(0.7*(len(df))):]
# preprocessing (since arima takes univariate series as input)
#        train_xs = train.index
#        train_ys = train.Close
#        valid_xs = valid.index
#        valid_ys = valid.Close
#        plt.plot(train_xs, train_ys, color='blue', label='train values')
#        plt.plot(valid_xs, valid_ys, color='red', label='valid values')
#        close = web.DataReader(self.ticker, 'yahoo', start, end).Close
#        xs = close.index
#        ys = close
#        plt.title('Stock Price Prediction')
#        plt.xlabel('Time', fontsize=12)
#        plt.ylabel('Price', fontsize=12)
#        plt.legend()
#        plt.xticks(rotation=90)
#        STOCK = BytesIO()
#        plt.savefig(STOCK, format="png")
#        STOCK.seek(0)
#        plot_url = base64.b64encode(STOCK.getvalue()).decode('utf8')
#        return plot_url
#-------------------------------------------------------------------------
