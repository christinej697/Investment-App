import datetime
import yfinance as yf
from yahoo_fin import stock_info as si

#----------------------------------------

class HistoricalTicker():

    def __init__(self, ticker):

        self.ticker = ticker

        self.info = {
            "quotename": "", 
            "pricelabels": "",
            "pricevalues": "",
            "dividlabels": "",
            "dividvalues": ""
        }

    def build_history(self, start, end):

        self.quote = yf.Ticker(self.ticker)
        self.info["quotename"] = self.quote.info["shortName"]
        his_divid = self.quote.history(period="max").Dividends
        self.info["dividlabels"], self.info["dividvalues"] = self.catch_data(his_divid)

        historical_datas = si.get_data(self.ticker, start_date=start, end_date=end)
        his_close = historical_datas.close

        self.info["pricelabels"], self.info["pricevalues"] = self.catch_data(his_close)
        quotetable = si.get_quote_table(self.ticker)
        quotetable["Quote Price"] = round(quotetable["Quote Price"], 2)

        return self.info, quotetable

#-------------------------------------------------

    def catch_data(self, his_data):

        tlabels = []
        tvalues = []
        index_data = his_data.index

        k=0
        for i in his_data:
            if i > 0:
                tvalues.append(i)
                tlabels.append(index_data[k].date())
            k = k + 1
        return tlabels, tvalues

#--------------------------------------------------
