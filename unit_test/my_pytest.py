#----------------------------------------------------------
# White Box Testing technique
# Performs basic unit tests for the stockApp flask application
# using the library pytest
# Testing flow and functionality
#----------------------------------------------------------
from flask import Flask
import json

from stockApp import stockApp, conn

# Ensure index html page loads
def test_index_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)
    assert response.get_data() == b'Welcome to StockSmart'
    assert response.status_code == 200   
    
# Ensure about html page loads correctly     
def test_about_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/about'
    
    response = client.get(url)
    assert response.status_code == 200

# Ensure users html page loads
def test_user_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/signIn'
    
    response = client.get(url)
    assert response.status_code == 200
    
# Ensure advice html page loads correctly     
def test_advice_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/signIn/advice'
    
    response = client.get(url)
    assert response.status_code == 200
    
# Ensure dividend html page loads correctly     
def test_dividend_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/signIn/advice/dividend'
    
    response = client.get(url)
    assert response.status_code == 200
    
# Ensure filter html page loads correctly     
def test_filter_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/signIn/advice/dividend/display'
    
    response = client.get(url)
    assert response.status_code == 200
    
##########################################################################

# Ensure shares html page loads correctly     
def test_shares_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/<hists>'
    
    response = client.get(url)
    assert response.status_code == 200
    
# Ensure predicted html page loads correctly     
def test_predicted_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/timeseries/<ticker>'
    
    response = client.get(url)
    assert response.status_code == 200
    
# Ensure chart html page loads correctly     
def test_chart_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/<ticker>/<checks>'
    
    response = client.get(url)
    assert response.status_code == 200