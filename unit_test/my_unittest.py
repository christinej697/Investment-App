#----------------------------------------------------------
# White Box Testing technique
# Performs basic unit tests for the stockApp flask application
# using the built-in Python library "unittest"
# Testing flow and functionality
#----------------------------------------------------------
import unittest
import os
from stocksmart.stockApp import stockApp
     
class FlaskTest(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['BASEDIR'], TEST_DB)
        #conn.drop_all()
        #conn.create_all()

    # executed after each test
    def tearDown(self):
        pass

    ###############    
    #### tests ####
    ###############

    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the index html page loads correctly
    def test_index_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        # Ensure the page text loads correctly
        self.assertTrue(b'Welcome to StockSmart' in response.data)
        self.assertTrue(b'Simple Reccomendation for Beginners' in response.data)
        self.assertTrue(b'Historical Price & Dividend for Favored Shares' in response.data)
        self.assertTrue(b'Time Series Machine Learning to Predict Stock Price' in response.data)

    # Ensure that the about html page loads correctly
    def test_about_loads(self):
        tester = app.test_client(self)
        response = tester.get('/about', content_type='html/text')
        # Ensure the page text loads correctly
        self.assertTrue(b'About' in response.data)
        self.assertTrue(b'StockSmart is an independently developed web application designed by Yuehchen Tsou and Christine Johnson. The purpose of the application is to provide begginning investors with suggestions on which investment options would best suit their needs. The options given are based on a users income and their option of with or without dividend companies. Our hope is that with the support of this application, investor will make wiser decisions for their current situations!' in response.data)

    # Ensure that the users html page loads correctly
    def test_user_loads(self):
        tester = app.test_client(self)
        response = tester.get('/signIn', content_type='html/text')
        # Ensure the page text loads correctly
        self.assertTrue(b'Welcome to StockSmart' in response.data)
        self.assertTrue(b'Enter your information and we will help you start your investment journey' in response.data)

    # Ensure signin behaves correctly given the correct credentials
    def test_sign_corr(self):
        tester = app.test_client(self)
        response = tester.get('/signIn', content_type='html/text')

    # Ensure signin behaves correctly given incorrect credentials
    def test_sign_incorr(self):
        tester = app.test_client(self)
        response = tester.get('/signIn', content_type='html/text')

    # Ensure that the advice html page loads correctly
    def test_advice_loads(self):
        tester = app.test_client(self)
        response = tester.get('/signIn/advice', content_type='html/text')
        # Ensure the page text loads correctly
        self.assertTrue(b'Income Recommendation' in response.data)
        self.assertTrue(b'Based on your income we recommend to invest..' in response.data)
        self.assertTrue(b'per month' in response.data)
        self.assertTrue(b'This is a great starting point!' in response.data)

    # Ensure that the dividend html page loads correctly
    def test_dividend_loads(self):
        tester = app.test_client(self)
        response = tester.get('/signIn/advice/dividend', content_type='html/text')
        # Ensure the page text loads correctly
        self.assertTrue(b'Types of Investments' in response.data)
        self.assertTrue(b'Choose the type of stock you would like to invest in. There are no wrong choices!' in response.data)

    # Ensure that the filter html page loads correctly
    def test_filter_loads(self):
        tester = app.test_client(self)
        response = tester.get('/signIn/advice/dividend/display', content_type='html/text')
        # Ensure the page text loads correctly
        self.assertTrue(b'Welcome to StockSmart' in response.data)            

###################################################################################

    # Ensure that the shares html page loads correctly
    def test_shares_loads(self):
        tester = app.test_client(self)
        response = tester.get('/<hists>', content_type='html/text')
        # Ensure the page text loads correctly
        self.assertTrue(b'Welcome to StockSmart' in response.data)
        self.assertTrue(b'Enter your favorite stock to see its historical price & dividend' in response.data)            

    # Ensure that the predicted html page loads correctly
    def test_predicted_loads(self):
        tester = app.test_client(self)
        response = tester.get('/<ticker>/<checks>', content_type='html/text')
        # Ensure the page text loads correctly
        self.assertTrue(b'Stock Price Prediction' in response.data) 

    # Ensure that the chart html page loads correctly
    def test_chart_loads(self):
        tester = app.test_client(self)
        response = tester.get('/timeseries/<ticker>', content_type='html/text')
        # Ensure the page text loads correctly
        self.assertTrue(b'Historical Price and Dividend' in response.data) 


if __name__ == '__main__':
unittest.main()
