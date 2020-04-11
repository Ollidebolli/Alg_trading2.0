import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from _indicators import *
from _functions import create_single_signal, combination_maker, moving_average, repeat_last
from _performance_measurements import multi_signal_long_short, first_signal_long_short

data = pd.read_csv("historical_price_data/bistamp_hourly_since_beginning.csv",
                  usecols=['date','close','volume'])
close = data['close'].to_numpy()

results = pd.read_csv('returns.csv').drop('Unnamed: 0', axis=1).dropna(how='all')
results = results[(results['norm_return_first'] > 0) | (results['norm_return_multi'] > 0)]

top = 12

#get the top 12 in each category from results.csv
frames = []
for col in results.columns[:6]:
    frames.append(results.sort_values(by=col, ascending=False)[:top])
top_indicators = pd.concat(frames).drop_duplicates()

#get the indicators as long as they have _indicator in their name
indicator_index = np.nonzero((results.loc[0].index).str.count('_indicator'))

#built the signals from the results.csv file per strategy
for index, strat in top_indicators[:1].iterrows():
    signals = []
    indicators = []
    
    for i in indicator_index:
        try: math.isnan(strat[i])
        except: indicators.append(strat.index[i])
        
    if 'MA_indicator' in indicators:
        MA_info = eval(strat['MA_indicator'])
        signals.append(MA_indicator(close, MA_info['MA_short'], MA_info['MA_long'], MA_info['MA_extender']))
        
    if 'BB_indicator' in indicators:
        BB_info = eval(strat['BB_indicator'])
        signals.append(BB_indicator(close, BB_info['BB_range'], BB_info['std_multiple'])) 
        
    if 'BB_indicator_breakout' in indicators:
        BB_BO_info = eval(strat['BB_indicator_breakout'])
        signals.append(BB_indicator(close, BB_BO_info['BB_BO_range'], BB_BO_info['BB_BO_std_multiple'], breakout=True))
        
    if 'RSI_indicator' in indicators:
        RSI_info = eval(strat['RSI_indicator'])
        signals.append(RSI_indicator(close, RSI_info['RSI_timeframe'], RSI_info['RSI_buy_level'], RSI_info['RSI_sell_level']))
        
    if 'OBV_indicator' in indicators:
        OBV_info = eval(strat['OBV_indicator'])
        signals.append(OBV_indicator(data, OBV_info['OBV_MA_short'], OBV_info['OBV_MA_long'], OBV_info['OBV_extender']))

        strength = np.sum(signals, axis=0)
        strength_level = len(signals)

        all_yes = np.where(strength >= strength_level, 1.0, 
                  np.where(strength <= -strength_level, -1, 0))
        
        all_yes = create_single_signal(all_yes)


#This can only go long or short x1 in each direction no matter how many signals but stays wihtin capital given range.

#can go long and short and add and reduce positions in each direction, with respect for to initial capital


