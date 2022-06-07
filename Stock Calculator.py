from google.colab import drive
drive.mount('/content/drive')
!pip install pandas_datareader --upgrade
print('Loading Google API')
#!pip install gspread -U -q
#!pip install gspread_dataframe -U -q
#!pip install gspread_formatting -U -q
!pip install yfinance

import yfinance as yf
import gspread as gs
#from gspread_dataframe import set_with_dataframe
#from gspread_formatting.dataframe import format_with_dataframe

print('Loading SmartAnalytics Colab Pack')
# to be read in and instantiated
import requests # for calling the API
from io import StringIO # string as file
import xml.etree.cElementTree as ET # parsing XML
import pandas as pd # target dataframe 
import urllib.request

import datetime
today = datetime.date.today()
yesterday = today - datetime.timedelta(days = 1)
jan_start = datetime.date(2021, 1, 4)
jan_end = datetime.date(2021, 1, 5)

# STOCK DATA FROM GOOGLE SHEETS 
#column names for spreadshet: Account Number	Investment Name	Symbol	Shares	Cost Basis
print('Reading Stock tab data')
stocks = pd.read_csv('https://docs.google.com/spreadsheets/d/yourlink' +
                   '/export?gid=0&format=csv',
                   # Set first column as rownames in data frame
                   #index_col=0,
                   # Parse column values to datetime
                   #parse_dates=['Quradate']
                  )

from IPython.core.display import display, HTML
display(HTML(""" 
<br>
<a style='font-size: 20px' target='_blank' 
href='https://docs.google.com/spreadsheets/yourlink'>
STOCK SHEET</a>
</p>
""")) 

symbols = stocks['Symbol'].tolist()
unique_symbols = list(dict.fromkeys(symbols))
unique_symbols = list(filter(None,unique_symbols))

#@title
stocks['Starting Value'] = stocks['Shares'] * stocks['Cost Basis']

new_prices = []
total_portfolio = 0

for stock_index, stock_row in stocks.iterrows(): # pandas version of spreadsheet
    if stock_index >= 0:
        
        ws_row = stock_index + 2      # mapping to the actual spreadsheet row 
        stock_symbol = stock_row[2]
        shares = stock_row[3]
        #print(ws_row, stock_symbol)
        if stock_symbol != 'VMFXX':
          try:
            stock_download = yf.download(stock_symbol, yesterday, today)
            stock_closing = stock_download['Close'][0]
            holding_value = stock_closing * shares
            total_portfolio += holding_value
            print(stock_symbol, "Shares", shares, "Share Price", stock_closing, "Holding Value", holding_value)
            new_prices.append(stock_closing)
            #starting_prices.append(starting_price)
          except:
            starting_prices.append(0)
            print("Value Not Found")
        else:
          new_prices.append(1)
          total_portfolio += shares

stocks['New Price'] = new_prices
stocks['New Holding Value'] = stocks['New Price'] * stocks['Shares']

total_portfolio

stocks['Cash Return'] = round((stocks['New Holding Value'] - stocks['Starting Value']), 2)
stocks['Percentage Return'] = round(100*(stocks['Cash Return'] / stocks ['Starting Value']), 2)
