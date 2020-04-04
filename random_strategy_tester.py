import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from _indicators import *
from _functions import create_single_signal, combination_maker, moving_average
from _performance_measurements import multi_signal_long_short, first_signal_long_short


data = pd.read_csv("historical_price_data/bistamp_hourly_since_beginning.csv",
                  usecols=['date','close','volume'])
                  
#'BB_strat_breakout','BB_strat','RSI_strat'
all_strats = ['MA_strat','BB_strat','RSI_strat','OBV_strat']

iterations = 10000
max_data_points = int(len(data) / 2)

close = data['close'].to_numpy()

return_list = pd.DataFrame(columns=['first_sharpe','multi_sharpe',
                                    'norm_return_first','cum_return_first',
                                    'norm_return_multi','cum_return_multi',
                                    'MA_strat','BB_strat','BB_strat_breakout','RSI_strat','OBV_strat',
                                    'nr of trades', 'nr of indicators'
                                    ],index=np.arange(iterations))

for i in range(iterations):

        strats = combination_maker(all_strats, min=1)
        signals = []

        if 'BB_strat_breakout' in strats:
                BA_BB_range = random.randint(1, max_data_points)
                BA_std_multiple = random.uniform(0.3, 10)
                signals.append(BB_indicator(close, BA_BB_range, BA_std_multiple, breakout=True))

        if 'BB_strat' in strats:
                BB_range = random.randint(1, max_data_points)
                std_multiple = random.uniform(0.3, 10)
                signals.append(BB_indicator(close, BB_range, std_multiple))   

        if 'MA_strat' in strats:
                MA_short = random.randint(1, max_data_points-10)
                MA_long = random.randint(MA_short, max_data_points)
                MA_signal_extender = random.randint(2, 15)
                signals.append(MA_indicator(close, MA_short, MA_long, MA_signal_extender))
 
        if 'RSI_strat' in strats:
                RSI_time_frame = random.randint(10, max_data_points)
                buy_level = random.randint(1,60)
                sell_level = random.randint(buy_level,100)
                signals.append(RSI_indicator(close, RSI_time_frame, buy_level, sell_level))
        
        if 'OBV_strat' in strats:
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
                return_list['nr of indicators'][i] = len(strats)

                if 'BB_strat_breakout' in strats: return_list['BA_BB_strat'][i] = {'BA_BB_range':BA_BB_range, 'BA_std_multiple':BA_std_multiple}
                if 'BB_strat' in strats: return_list['BB_strat'][i] = {'BB_range':BB_range, 'std_multiple':std_multiple}
                if 'MA_strat' in strats: return_list['MA_strat'][i] = {'MA_short':MA_short, 'MA_long':MA_long, 'extender':MA_signal_extender}
                if 'RSI_strat' in strats: return_list['RSI_strat'][i] = {'time_frame':RSI_time_frame, 'buy_level':buy_level, 'sell_level':sell_level}
                if 'OBV_strat' in strats: return_list['OBV_strat'][i] = {'OBV_short_MA':OBV_MA_short,'OBV_long_MA':OBV_MA_long,'Extender':OBV_signal_extender}
                

        
        print(i)

return_list.sort_values(by=['norm_return_first'], ascending=False, inplace=True)

return_list.to_excel('RETRUNS_TST.xlsx')
return_list.to_csv('returns.csv')