import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from _indicators import *
from _functions import create_single_signal, combination_maker, moving_average
from _performance_measurements import multi_signal_long_short, first_signal_long_short


data = pd.read_csv("Historical_price_data/lol1.csv",
                  usecols=['close timestamp','close','volume'])
#'BB_strat_breakout','BB_strat','RSI_strat'
all_strats = ['RSI_strat','BB_strat_breakout','BB_strat','MA_strat','OBV_strat']

iterations = 100000

return_list = pd.DataFrame(columns=['first_sharpe','multi_sharpe',
                                    'norm_return_first','cum_return_first',
                                    'norm_return_multi','cum_return_multi',
                                    'MA_strat','BB_strat','BB_strat_breakout','RSI_strat','OBV_strat',
                                    'nr of trades'
                                    ],index=np.arange(iterations))

for i in range(iterations):

        combined_strats = pd.DataFrame(index=data.index)

        #create combinations of strategies and lower chance of only 1 strat by running again
        #strats = combination_maker(all_strats)
        #if len(strats) == 1:
        #        strats = combination_maker(all_strats)

        strats = all_strats

        if 'BB_strat_breakout' in strats:
                BA_BB_range = random.randint(1, 300)
                BA_std_multiple = random.uniform(0.3, 10)
                combined_strats['BB_strat_breakout'] = BB_indicator(data, BA_BB_range, BA_std_multiple, breakout=True)

        if 'BB_strat' in strats:
                BB_range = random.randint(1, 300)
                std_multiple = random.uniform(0.3, 10)
                combined_strats['BB_strat'] = BB_indicator(data, BB_range, std_multiple)     

        if 'MA_strat' in strats:
                MA_short = random.randint(1, 300)
                MA_long = MA_short + random.randint(1, 300)
                MA_signal_extender = random.randint(2, 15)
                combined_strats['MA_strat'] = MA_indicator(data, MA_short, MA_long, MA_signal_extender)
 
        if 'RSI_strat' in strats:
                RSI_time_frame = random.randint(10, 300)
                buy_level = 20
                sell_level = 80
                combined_strats['RSI_strat'] = RSI_indicator(data, RSI_time_frame, buy_level, sell_level)
        
        if 'OBV_strat' in strats:
                OBV_MA_short = random.randint(1, 300)
                OBV_MA_long = OBV_MA_short + random.randint(1, 300)
                OBV_signal_extender = random.randint(2, 15)
                combined_strats['OBV_strat'] = OBV_indicator(data, OBV_MA_short, OBV_MA_long, OBV_signal_extender)

        combined_strats['strenght'] = combined_strats.sum(axis=1)

        strength_level = len(strats)

        combined_strats['all_yes'] = np.where(combined_strats['strenght'] == strength_level, 1.0, 
                                     np.where(combined_strats['strenght'] == (strength_level *-1.0), -1, 0))

        
        combined_strats['all_yes'] = create_single_signal(np.array(combined_strats['all_yes']))

        combined_strats['close'] = data['close']
        
        if combined_strats['all_yes'].any() != 0:
                sharpe_first, cum_first, norm_first = first_signal_long_short(combined_strats, 100000, normalized=True)
                sharpe_multi, cum_multi, norm_multi = multi_signal_long_short(combined_strats, 100000, normalized=True)

                return_list['first_sharpe'][i] = sharpe_first
                return_list['multi_sharpe'][i] = sharpe_multi
                return_list['norm_return_first'][i] = norm_first
                return_list['cum_return_first'][i] = cum_first
                return_list['norm_return_multi'][i] = norm_multi
                return_list['cum_return_multi'][i] = cum_multi
                return_list['nr of trades'][i] = combined_strats['all_yes'].astype(bool).sum(axis=0)

                try:
                        return_list['BB_strat_breakout'][i] = {'BB_range':BA_BB_range, 'std_multiple':BA_std_multiple}
                        return_list['BB_strat'][i] = {'BB_range':BB_range, 'std_multiple':std_multiple}
                        return_list['MA_strat'][i] = {'MA_short':MA_short, 'MA_long':MA_long, 'extender':signal_extender}
                        return_list['RSI_strat'][i] = {'time_frame':RSI_time_frame, 'buy_level':buy_level, 'sell_level':sell_level}
                        return_list['OBV_strat'][i] = {'OBV_short_MA':OBV_MA_short,'OBV_long_MA':OBV_MA_long,'Extender':OBV_signal_extender}
                except: pass
        
        print(i)

return_list.sort_values(by=['norm_return_first'], ascending=False, inplace=True)

return_list.to_excel('RETRUNS_TST.xlsx')