from binance.client import Client
import pandas as pd
import datetime

api_key = 'GDzJuMPMgTDNRypU6zOBYwz0raxYRGUohjayDQKrSOF9yJ6RuLbgplnaSEKSGhKD'

api_secret = 'vsiflsMm4MxckFsDzJo9ptydpkc0G1fAXScI4nzxHAg9SU92liTpIwGY8YtbkWW3'

start_date = '01 Jan, 2019'

client = Client(api_key, api_secret)

klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, start_date)

data = pd.DataFrame(klines, columns=['open timestamp','open','high','low','close','volume','close timestamp','volume quote asset','nr of trades','taker buy base asset volume','taker buy quote asset volume','ignore'])

#data.to_csv(f'{start_date}-{datetime.date.today()}.csv')
data.to_csv(f'lol.csv')