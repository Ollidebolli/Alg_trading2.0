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

iterations = 100000
max_data_points = len(data)-35000

return_list = pd.DataFrame(columns=['first_sharpe','multi_sharpe',
                                    'norm_return_first','cum_return_first',
                                    'norm_return_multi','cum_return_multi',
                                    'MA_strat','BB_strat','BB_strat_breakout','RSI_strat','OBV_strat',
                                    'nr of trades', 'nr of indicators'
                                    ],index=np.arange(iterations))

count = 0
for length in range(336,1200)[1::5]:
    for first in range(4,35)[::2]:
        for second in range(65,95)[::2]:
            
            combined_strats = pd.DataFrame(index=data.index)
            combined_strats['OBV'] = OBV_indicator(data,18,21,1)
            return_list['OBV_strat'][count] = {'Short_ma':18, 'Long_ma':21}

            combined_strats['RSI_strat'] = RSI_indicator(data, length, first, second)
            return_list['RSI_strat'][count] = {'time_frame':length, 'buy_level':first, 'sell_level':second}


            combined_strats['strenght'] = combined_strats.sum(axis=1)

            strength_level = 2

            combined_strats['all_yes'] = np.where(combined_strats['strenght'] == strength_level, 1.0, 
                                        np.where(combined_strats['strenght'] == (strength_level *-1.0), -1, 0))

            combined_strats['close'] = data['close']

            if any(combined_strats['all_yes']):

                sharpe_first, cum_first, norm_first = first_signal_long_short(combined_strats, 100000, normalized=True)
                sharpe_multi, cum_multi, norm_multi = multi_signal_long_short(combined_strats, 100000, normalized=True)

                return_list['first_sharpe'][count] = sharpe_first
                return_list['multi_sharpe'][count] = sharpe_multi
                return_list['norm_return_first'][count] = norm_first
                return_list['cum_return_first'][count] = cum_first
                return_list['norm_return_multi'][count] = norm_multi
                return_list['cum_return_multi'][count] = cum_multi
                return_list['nr of trades'][count] = combined_strats['all_yes'].astype(bool).sum(axis=0)
            print(count)

            count += 1

print('done')
return_list.sort_values(by=['norm_return_first'], ascending=False, inplace=True)

return_list.to_csv('RETRUNS_TST1.csv')