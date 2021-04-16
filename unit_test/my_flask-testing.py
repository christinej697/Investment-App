#----------------------------------------------------------
# White Box Testing technique
# Performs basic unit tests for the stockApp flask application
# using the library Flask-Testing
# Testing flow and functionality
#----------------------------------------------------------
import unittest
import os
from flask_testing import TestCase
from stockApp import stockApp, conn

class BaseTestCase(TestCase):
	""" A base test case """
	
	def create_app(self):
		stockApp.config.from_object('config.TestConfig')
		return stockApp
	
	def setUp(self):
		conn.create_all()
		
	def tearDown(self):
		conn.session.remove()
		conn.drop_all()
 
class FlaskTest(unittest.TestCase):

	# Ensure that flask was set up correctly
	def test_index(self):
		response = self.client.get('/', content_type='html/text')
		self.assertEqual(response.status_code, 200)
		
	# Ensure that the index html page loads correctly
	def test_index_loads(self):
		response = self.client.get('/', content_type='html/text')
		# Ensure the page text loads correctly
		self.assertTrue(b'Welcome to StockSmart' in response.data)
		
	# Ensure that the about html page loads correctly
	def test_about_loads(self):
		response = self.client.get('/about', content_type='html/text')
	
	# Ensure that the users html page loads correctly
	def test_user_loads(self):
		response = self.client.get('/signIn', content_type='html/text')
		
	# Ensure signin behaves correctly given the correct credentials
	def test_sign_corr(self):
		response = self.client.get('/signIn', content_type='html/text')
		
	# Ensure signin behaves correctly given incorrect credentials
	def test_sign_incorr(self):
		response = self.client.get('/signIn', content_type='html/text')
		
	# Ensure that the advice html page loads correctly
	def test_advice_loads(self):
		response = self.client.get('/signIn/advice', content_type='html/text')
		
	# Ensure that the dividend html page loads correctly
	def test_dividend_loads(self):
		response = self.client.get('/signIn/advice/dividend', content_type='html/text')
		
	# Ensure that the filter html page loads correctly
	def test_filter_loads(self):
		response = self.client.get('/signIn/advice/dividend/display', content_type='html/text')        
	
###################################################################################
	
	# Ensure that the shares html page loads correctly
	def test_shares_loads(self):
		response = self.client.get('/<hists>', content_type='html/text')     

	# Ensure that the predicted html page loads correctly
	def test_predicted_loads(self):
		response = self.client.get('/<ticker>/<checks>', content_type='html/text')            
		
	# Ensure that the chart html page loads correctly
	def test_chart_loads(self):
		response = self.client.get('/timeseries/<ticker>', content_type='html/text')         
		
		
if __name__ == '__main__':
	unittest.main()