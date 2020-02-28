import pandas as pd
import numpy as np 

#get all kinds of data from here: http://api.bitcoincharts.com/v1/csv/


colnames = ['close timestamp','price','volume']
data = pd.read_csv('historical_price_data/.bitstampUSD.csv', names=colnames, header=None)
data['date'] = pd.to_datetime(data['timestamp'],unit='s')
data = data.set_index('date', drop=True)
result = data['price'].resample('60Min').ohlc()
result['volume'] = data['volume'].resample('60Min').sum()


#drop or fill NA rows otherwise it wont work