
# -- --------------------------------------------------------------------------------------------------- -- #
# -- MarketMaker-BackTest                                                                                -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- file: main.py                                                                                       -- #
# -- Description: Main execution logic for the project                                                   -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Author: IFFranciscoME - if.francisco.me@gmail.com                                                   -- #
# -- license: MIT License                                                                                -- #
# -- Repository: https://github.com/IFFranciscoME/MarketMaker-BackTest                                   -- #
# --------------------------------------------------------------------------------------------------------- #

# -- Load Packages for this script
import pandas as pd
import pandas as np
from pandas._libs.tslibs import timestamps
import plotly.express as px
import plotly.graph_objects as go
# -- Load other scripts
from data import fees_schedule, order_book
import data as d
import importlib
importlib.reload(d)

# Small test
exchanges =  [ "bitfinex","kraken","ftx", "currencycom", 'coinmate']
symbol = 'BTC/EUR'
expected_volume = 0

# Get fee schedule
# fees = fees_schedule(exchange='kraken', symbol=symbol, expected_volume=expected_volume)

# Massive download of OrderBook data
data = d.order_book(symbol=symbol, exchanges=exchanges, output='inplace', stop=None, verbose=True)
dict_lst = []
for exchange in exchanges:
    for i in range(len(list(data[exchange].keys()))):
        timeStamp = list(data[exchange].keys())[i]
        dict_lst.append(
            {
                'exchange': exchange,
                'timeStamp' : timeStamp,
                'levels': len(data[exchange][timeStamp]),
                'ask_volume' : sum(data[exchange][timeStamp].ask_size),
                'bid_volume' : sum(data[exchange][timeStamp].bid_size),
                'total_volume' : sum(data[exchange][timeStamp].ask_size) + 
                                 sum(data[exchange][timeStamp].bid_size),
                'mid_price' : (data[exchange][timeStamp].iloc[0].ask + 
                               data[exchange][timeStamp].iloc[0].bid) / 2,
                'vwap' :  (sum(data[exchange][timeStamp].ask * 
                              data[exchange][timeStamp].ask_size) / 
                              sum(data[exchange][timeStamp].ask_size) + 
                          sum(data[exchange][timeStamp].bid * 
                              data[exchange][timeStamp].bid_size) / 
                              sum(data[exchange][timeStamp].bid_size)) / 2 
            }
        )
tmp = pd.DataFrame(dict_lst)
fig = px.line(tmp, x="timeStamp", y=['mid_price','vwap'],
                 color='exchange', line_dash ='exchange' , 
                 title='custom tick labels')
fig.show()

plot = go.Figure()
plot.add_trace(go.Scatter(
    x = tmp['timeStamp'],
    y = tmp['vwap'],
    color = tmp['exchange']
))
plot.show()
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=random_x, y=random_y0,
#                     mode='lines',
#                     name='lines'))
# fig.add_trace(go.Scatter(x=random_x, y=random_y1,
#                     mode='lines+markers',
#                     name='lines+markers'))
# fig.add_trace(go.Scatter(x=random_x, y=random_y2,
#                     mode='markers', name='markers'))

# fig.show()

# Test
# data['kraken'][list(data['kraken'].keys())[2]]

# Read previously downloaded file
ob_data = pd.read_json('files/orderbooks_06jun2021.json', orient='values', typ='series')

# OrderBooks
pd.DataFrame(ob_data['bitfinex']['2021-07-06T18:02:31.524Z'])



# -- Simulation of trades (Pending)

"""
- Type A: Make a BID in Kraken, then Take BID in Bitfinex

Check Signal_BID
    Difference between BIDs on Origin and Destination is greater than Maker_Margin_BID
    Make on Destination and Take on Origin

kr_maker_bid * (1 + kr_maker_fee) = bf_taker_bid * (1 - bf_taker_fee)
e.g. -> 5942.5638 * (1 + 0.0016) = 5964.00 * (1 - 0.0020) = 0

- Type B: Take an ASK on Bitfinex, then Make an ASK in Kraken

Check Signal_ASK
    Difference between ASKs on Origin and Destination is greater than Maker_Margin_ASK
    Take on Origin and Maker on Destination

bf_taker_ask * (1 + bf_taker_fee) = kr_maker_ask * (1 - kr_maker_fee)
e.g. -> 6000 * (1 + 0.0020) - 6021.6346 * (1 - 0.0016) = 0
"""
