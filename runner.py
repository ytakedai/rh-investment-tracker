import profile
import time
import pandas as pd
import os.path              # Check if file exists
import random               # Random number generator
import datetime             # Current time

SETUP = False               # True to setup .csv
LOGIN = True

PROFILE = None
rh = None
maxPrice = 0
INTERVAL_MIN = 10
STOCKS = pd.DataFrame()

def main():
    initialize()
    
    while(True):
        print('Update at: ' + str(datetime.datetime.now()))
        manage_stocks()
        time.sleep(60*INTERVAL_MIN)
    
def initialize():
    global STOCKS
    global PROFILE
    global rh

    if SETUP:
        setup_dataframe()
    
    if LOGIN:
        login_rh()
    
    # Read dataframe from CSV
    STOCKS = pd.read_csv("stocks.csv")
    update_prices()

    None

# Log into Robinhood
def login_rh():
    global PROFILE
    global rh

    PROFILE = profile.Profile()
    rh = PROFILE.rh

def setup_dataframe():
    global STOCKS
    data = {'Symbol': ['FB', 'MSFT', 'SPHD'],
            #'Data': [None, None, None],
            'Price': [0.0, 0.0, 0.0],
            'Updated': ['', '', ''],
            'LocalMax': [0.0, 0.0, 0.0],
            'LocalMin': [0.0, 0.0, 0.0],
            'Shares': [2, 1, 10]}
    STOCKS = pd.DataFrame(data)
    STOCKS.to_csv('stocks.csv', index=False)

def manage_stocks():
    # Update dynamoDB
    update_prices()
    # Check prices, buy/sell
    trade()

def update_prices():
    for symbol in STOCKS['Symbol']:
        # Current symbol data from Robinhood
        data = rh.quote_data(symbol)

        # Update current price
        price = float(data['ask_price'])
        STOCKS.loc[STOCKS['Symbol'] == symbol, 'Price'] = price

        #Update 'Updated' timestamp
        STOCKS.loc[STOCKS['Symbol'] == symbol, 'Updated'] = data['updated_at']

        # Update max/min
        shares = STOCKS.loc[STOCKS['Symbol'] == symbol, 'Shares'].tolist()[0]
        prev_min = STOCKS.loc[STOCKS['Symbol'] == symbol, 'LocalMin'].tolist()[0]
        prev_max = STOCKS.loc[STOCKS['Symbol'] == symbol, 'LocalMax'].tolist()[0]
        # No shares
        if shares == 0:
            # Set LocalMax to 0 (value not needed)
            STOCKS.loc[STOCKS['Symbol'] == symbol, 'LocalMax'] = 0
            # If price goes down
            if price < prev_min:
                STOCKS.loc[STOCKS['Symbol'] == symbol, 'LocalMin'] = price
        # 1 or more shares
        if shares > 0:
            # Set LocalMin to 0 (value not needed)
            STOCKS.loc[STOCKS['Symbol'] == symbol, 'LocalMin'] = 0
            # If price goes up
            if price > prev_max:
                STOCKS.loc[STOCKS['Symbol'] == symbol, 'LocalMax'] = price

        # randomize time between updates
        time_sleep = 2
        random.seed(1)
        for i in range(3):
            time_sleep += int(round(random.random()))
        time.sleep(time_sleep)

    STOCKS.to_csv('stocks.csv', index=False)

def trade():
    None

def buy(symbol: str, num: int):
    instrument = rh.instruments(symbol)[0]
    buy_order = rh.place_buy_order(instrument, num)

def sell(symbol: str, num: int):
    instrument = rh.instruments(symbol)[0]
    sell_order = rh.place_sell_order(instrument, num)

main()


'''
Output for quote_data()

Input:
rh.quote_data("AAPL")

Output:
{'ask_price': '255.950000', 
    'ask_size': 200, 
    'bid_price': '255.930000', 
    'bid_size': 202, 
    'last_trade_price': '255.940000', 
    'last_extended_hours_trade_price': None, 
    'previous_close': '241.410000', 
    'adjusted_previous_close': '241.410000',
    'previous_close_date': '2020-04-03', 
    'symbol': 'AAPL', 
    'trading_halted': False, 
    'has_traded': True, 
    'last_trade_price_source': 'nls', 
    'updated_at': '2020-04-06T18:59:25Z', 
    'instrument': 'https://api.robinhood.com/instruments/450dfc6d-5510-4d40-abfb-f633b7d9be3e/'}

Command for grabbing specific stock share
STOCKS.loc[STOCKS['Symbol'] == 'FB']['Shares']

Command for getting stock prices
#print('Microsoft:')
#print(robinhood.print_quote("MSFT"))
'''

'''
Day Trading restriction:
https://www.reddit.com/r/RobinHood/comments/478rwb/all_about_robinhood_instant/
'''
