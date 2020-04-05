import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from _indicators import *
from _functions import create_single_signal, combination_maker, moving_average
from _performance_measurements import multi_signal_long_short, first_signal_long_short


data = pd.read_csv("historical_price_data/bistamp_hourly_since_beginning.csv",
                  usecols=['date','close','volume'])
close = data['close'].to_numpy()

iterations = 2500
max_data_points = int(len(data) / 2)


indicators = ['MA_indicator','BB_indicator','RSI_indicator','OBV_indicator']


return_list = pd.DataFrame(columns=['first_sharpe','multi_sharpe',
                                    'norm_return_first','cum_return_first',
                                    'norm_return_multi','cum_return_multi',
                                    'MA_indicator','BB_indicator','BB_indicator_breakout','RSI_indicator','OBV_indicator',
                                    'nr of trades', 'nr of indicators'
                                    ],index=np.arange(iterations))

for i in range(iterations):

        included_indicators = combination_maker(indicators, min=1)
        signals = []

        if 'BB_indicator_breakout' in included_indicators:
                BB_BO_range = random.randint(1, max_data_points)
                BB_BO_std_multiple = random.uniform(0.3, 10)
                signals.append(BB_indicator(close, BB_BO_range, BB_BO_std_multiple, breakout=True))

        if 'BB_indicator' in included_indicators:
                BB_range = random.randint(1, max_data_points)
                std_multiple = random.uniform(0.3, 10)
                signals.append(BB_indicator(close, BB_range, std_multiple))   

        if 'MA_indicator' in included_indicators:
                MA_short = random.randint(1, max_data_points-10)
                MA_long = random.randint(MA_short, max_data_points)
                MA_signal_extender = random.randint(2, 15)
                signals.append(MA_indicator(close, MA_short, MA_long, MA_signal_extender))
 
        if 'RSI_indicator' in included_indicators:
                RSI_time_frame = random.randint(10, max_data_points)
                buy_level = random.randint(1,60)
                sell_level = random.randint(buy_level,100)
                signals.append(RSI_indicator(close, RSI_time_frame, buy_level, sell_level))
        
        if 'OBV_indicator' in included_indicators:
                OBV_MA_short = random.randint(1, max_data_points-10)
                OBV_MA_long = random.randint(OBV_MA_short, max_data_points)
                OBV_signal_extender = random.randint(2, 15)
                signals.append(OBV_indicator(data, OBV_MA_short, OBV_MA_long, OBV_signal_extender))

        strength = np.sum(signals, axis=0)
        strength_level = len(signals)

        all_yes = np.where(strength >= strength_level, 1.0, 
                  np.where(strength <= -strength_level, -1, 0))
        
        if any(all_yes):

                all_yes = create_single_signal(all_yes)

                sharpe_first, cum_first, norm_first = first_signal_long_short(close, all_yes, 100000, normalized=True)
                sharpe_multi, cum_multi, norm_multi = multi_signal_long_short(close, all_yes, 100000, normalized=True)

                return_list['first_sharpe'][i] = sharpe_first
                return_list['multi_sharpe'][i] = sharpe_multi
                return_list['norm_return_first'][i] = norm_first
                return_list['cum_return_first'][i] = cum_first
                return_list['norm_return_multi'][i] = norm_multi
                return_list['cum_return_multi'][i] = cum_multi
                return_list['nr of trades'][i] = all_yes.astype(bool).sum(axis=0)
                return_list['nr of indicators'][i] = len(included_indicators)

                if 'BB_indicator_breakout' in included_indicators: return_list['BB_indicator_breakout'][i] = {'BB_BO_range':BB_BO_range, 'BB_BO_std_multiple':BB_BO_std_multiple}
                if 'BB_indicator' in included_indicators: return_list['BB_indicator'][i] = {'BB_range':BB_range, 'std_multiple':std_multiple}
                if 'MA_indicator' in included_indicators: return_list['MA_indicator'][i] = {'MA_short':MA_short, 'MA_long':MA_long, 'MA_extender':MA_signal_extender}
                if 'RSI_indicator' in included_indicators: return_list['RSI_indicator'][i] = {'RSI_time_frame':RSI_time_frame, 'RSI_buy_level':buy_level, 'RSI_sell_level':sell_level}
                if 'OBV_indicator' in included_indicators: return_list['OBV_indicator'][i] = {'OBV_MA_short':OBV_MA_short,'OBV_MA_long':OBV_MA_long,'OBV_extender':OBV_signal_extender}
                

        
        print(i)


return_list.sort_values(by=['norm_return_first'], ascending=False, inplace=True)
return_list.to_csv('returns.csv')