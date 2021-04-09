#----------------------------------------------------------
# White BOx Testing technique
# Performs basic unit tests for the stockApp flask application
# using the built-in Python library "unittest"
# Testing flow and functionality
#----------------------------------------------------------
import unittest
import os

    try:
        from stockApp import stockApp
        import unittest
     
    class FlaskTest(unittest.TestCase):
    
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
        
        # Ensure that the users html page loads correctly
        def test_user_loads(self):
            tester = app.test_client(self)
            response = tester.get('/signIn', content_type='html/text')
            
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
            
        # Ensure that the dividend html page loads correctly
        def test_dividend_loads(self):
            tester = app.test_client(self)
            response = tester.get('/signIn/advice/dividend', content_type='html/text')
            
        # Ensure that the filter html page loads correctly
        def test_filter_loads(self):
            tester = app.test_client(self)
            response = tester.get('/signIn/advice/dividend/display', content_type='html/text')        
        
--------------------------------------------------------------------------------
        
        # Ensure that the shares html page loads correctly
        def test_shares_loads(self):
            tester = app.test_client(self)
            response = tester.get('/<hists>', content_type='html/text')      
            
        # Ensure that the chart html page loads correctly
        def test_chart_loads(self):
            tester = app.test_client(self)
            response = tester.get('/timeseries/<ticker>', content_type='html/text')         
            
        # Ensure that the about html page loads correctly
#        def test_about_loads(self):
#            tester = app.test_client(self)
#            response = tester.get('/about', content_type='html/text')
            
    if __name__ == '__main__':
        unittest.main()
        
