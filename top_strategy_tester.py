import pandas as pd
import numpy as np
import math
from _indicators import *
from _functions import create_single_signal, combination_maker, moving_average, repeat_last
from _for_loop_performance_measurements import multi_signal_for, single_signal_for

data = pd.read_csv("historical_price_data/lol.csv",
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

top_results = pd.DataFrame(columns=['indicator_id','strategy_type','norm_return','cum_return','sharpe','draw_down','bankrupt?',
                                    'MA_indicator','BB_indicator','BB_indicator_breakout','RSI_indicator','OBV_indicator',
                                    'nr of trades', 'nr of indicators'
                                    ],index=np.arange(len(top_indicators) * 5))

#get the indicators as long as they have _indicator in their name
indicator_index = np.nonzero((results.loc[0].index).str.count('_indicator'))

#built the signals from the results.csv file per strategy
nr = 0
for index, strat in top_indicators.iterrows():
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
        signals.append(RSI_indicator(close, RSI_info['RSI_time_frame'], RSI_info['RSI_buy_level'], RSI_info['RSI_sell_level']))
        
    if 'OBV_indicator' in indicators:
        OBV_info = eval(strat['OBV_indicator'])
        signals.append(OBV_indicator(data, OBV_info['OBV_MA_short'], OBV_info['OBV_MA_long'], OBV_info['OBV_extender']))

    strength = np.sum(signals, axis=0)
    strength_level = len(signals)

    all_yes = np.where(strength >= strength_level, 1.0, 
                np.where(strength <= -strength_level, -1, 0))
    
    signals = create_single_signal(all_yes)

    #strategy 1

    df = single_signal_for(close, signals, initial_capital = 100, return_full=True)

    norm_return = (df['total'].iloc[-1] / df['total'].iloc[0])-1
    cum_return = df['total'].pct_change().cumsum().iloc[-1]
    sharpe = df['total'].pct_change().mean() / df['total'].pct_change().std()
    annual_sharpe = (365**0.5) * sharpe
    mini = df['total'].min()
    
    total = df['total'].to_numpy()
    bot = np.argmax(np.maximum.accumulate(total) - total) # end of the period
    top = np.argmax(total[:bot]) # start of period
    max_down = (total[top] - total[bot]) / total[bot]

    top_results['indicator_id'][nr] = index
    top_results['strategy_type'][nr] = '1_direction'
    top_results['sharpe'][nr] = sharpe
    top_results['norm_return'][nr] = norm_return
    top_results['cum_return'][nr] = cum_return
    top_results['draw_down'][nr] = max_down
    top_results['bankrupt?'][nr] = mini
    top_results['nr of trades'][nr] = 'unable'
    top_results['nr of indicators'][nr] = len(indicators)

    if 'BB_indicator_breakout' in indicators: top_results['BB_indicator_breakout'][nr] = BB_BO_info
    if 'BB_indicator' in indicators: top_results['BB_indicator'][nr] = BB_info
    if 'MA_indicator' in indicators: top_results['MA_indicator'][nr] = MA_info
    if 'RSI_indicator' in indicators: top_results['RSI_indicator'][nr] = RSI_info
    if 'OBV_indicator' in indicators: top_results['OBV_indicator'][nr] = OBV_info

    nr +=1

    #multi direction (3)
    df = multi_signal_for(close, signals, max_pos=3, initial_capital = 100, return_full=True)

    norm_return = (df['total'].iloc[-1] / df['total'].iloc[0])-1
    cum_return = df['total'].pct_change().cumsum().iloc[-1]
    sharpe = df['total'].pct_change().mean() / df['total'].pct_change().std()
    annual_sharpe = (365**0.5) * sharpe
    mini = df['total'].min()
    
    total = df['total'].to_numpy()
    bot = np.argmax(np.maximum.accumulate(total) - total) # end of the period
    top = np.argmax(total[:bot]) # start of period
    max_down = (total[top] - total[bot]) / total[bot]

    top_results['indicator_id'][nr] = index
    top_results['strategy_type'][nr] = '3_direction'
    top_results['sharpe'][nr] = sharpe
    top_results['norm_return'][nr] = norm_return
    top_results['cum_return'][nr] = cum_return
    top_results['draw_down'][nr] = max_down
    top_results['bankrupt?'][nr] = mini
    top_results['nr of trades'][nr] = df['size'].diff().astype(bool).sum(axis=0)
    top_results['nr of indicators'][nr] = len(indicators)

    if 'BB_indicator_breakout' in indicators: top_results['BB_indicator_breakout'][nr] = BB_BO_info
    if 'BB_indicator' in indicators: top_results['BB_indicator'][nr] = BB_info
    if 'MA_indicator' in indicators: top_results['MA_indicator'][nr] = MA_info
    if 'RSI_indicator' in indicators: top_results['RSI_indicator'][nr] = RSI_info
    if 'OBV_indicator' in indicators: top_results['OBV_indicator'][nr] = OBV_info

    nr +=1

    #multi direction (10)
    df = multi_signal_for(close, signals, max_pos=10, initial_capital = 100, return_full=True)

    norm_return = (df['total'].iloc[-1] / df['total'].iloc[0])-1
    cum_return = df['total'].pct_change().cumsum().iloc[-1]
    sharpe = df['total'].pct_change().mean() / df['total'].pct_change().std()
    annual_sharpe = (365**0.5) * sharpe
    mini = df['total'].min()
    
    total = df['total'].to_numpy()
    bot = np.argmax(np.maximum.accumulate(total) - total) # end of the period
    top = np.argmax(total[:bot]) # start of period
    max_down = (total[top] - total[bot]) / total[bot]

    top_results['indicator_id'][nr] = index
    top_results['strategy_type'][nr] = '10_direction'
    top_results['sharpe'][nr] = sharpe
    top_results['norm_return'][nr] = norm_return
    top_results['cum_return'][nr] = cum_return
    top_results['draw_down'][nr] = max_down
    top_results['bankrupt?'][nr] = mini
    top_results['nr of trades'][nr] = df['size'].diff().astype(bool).sum(axis=0)
    top_results['nr of indicators'][nr] = len(indicators)

    if 'BB_indicator_breakout' in indicators: top_results['BB_indicator_breakout'][nr] = BB_BO_info
    if 'BB_indicator' in indicators: top_results['BB_indicator'][nr] = BB_info
    if 'MA_indicator' in indicators: top_results['MA_indicator'][nr] = MA_info
    if 'RSI_indicator' in indicators: top_results['RSI_indicator'][nr] = RSI_info
    if 'OBV_indicator' in indicators: top_results['OBV_indicator'][nr] = OBV_info

    nr +=1

    #multi direction (20)
    df = multi_signal_for(close, signals, max_pos=20, initial_capital = 100, return_full=True)

    norm_return = (df['total'].iloc[-1] / df['total'].iloc[0])-1
    cum_return = df['total'].pct_change().cumsum().iloc[-1]
    sharpe = df['total'].pct_change().mean() / df['total'].pct_change().std()
    annual_sharpe = (365**0.5) * sharpe
    mini = df['total'].min()
    
    total = df['total'].to_numpy()
    bot = np.argmax(np.maximum.accumulate(total) - total) # end of the period
    top = np.argmax(total[:bot]) # start of period
    max_down = (total[top] - total[bot]) / total[bot]

    top_results['indicator_id'][nr] = index
    top_results['strategy_type'][nr] = '20_direction'
    top_results['sharpe'][nr] = sharpe
    top_results['norm_return'][nr] = norm_return
    top_results['cum_return'][nr] = cum_return
    top_results['draw_down'][nr] = max_down
    top_results['bankrupt?'][nr] = mini
    top_results['nr of trades'][nr] = df['size'].diff().astype(bool).sum(axis=0)
    top_results['nr of indicators'][nr] = len(indicators)

    if 'BB_indicator_breakout' in indicators: top_results['BB_indicator_breakout'][nr] = BB_BO_info
    if 'BB_indicator' in indicators: top_results['BB_indicator'][nr] = BB_info
    if 'MA_indicator' in indicators: top_results['MA_indicator'][nr] = MA_info
    if 'RSI_indicator' in indicators: top_results['RSI_indicator'][nr] = RSI_info
    if 'OBV_indicator' in indicators: top_results['OBV_indicator'][nr] = OBV_info


    print(nr)


top_results.sort_values(by=['norm_return'], ascending=False, inplace=True)
top_results.to_csv('top.csv')
top_results.to_excel('top.xlsx')
top_indicators.to_excel('top_indicators.xlsx')