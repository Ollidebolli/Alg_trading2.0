import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from _indicators import BB_indicator, MA_indicator, RSI_indicator, OBV_indicator
from _functions import create_single_signal, combination_maker
from _performance_measurements import multi_signal_long_short, first_signal_long_short

data = pd.read_csv("Historical_price_data/lol.csv",
                  usecols=['close timestamp','close','volume'])

combined_indicators = pd.DataFrame(index=data.index)

indicators = ['bb_signal_bo','bb_signal','ma_signal','rsi_signal','obv_signal']

if 'bb_signal_bo' in indicators:
        BB_range = random.randint(1, 300)
        std_multiple = random.uniform(0.3, 10)
        combined_indicators[['bb_lower_bo','bb_upper_bo','bb_signal_bo']] = BB_indicator(data, BB_range, std_multiple, breakout=True, return_full=True)[['lower_band','upper_band','signals']]

if 'bb_signal' in indicators:
        BB_range = random.randint(1, 300)
        std_multiple = random.uniform(0.3, 10)
        combined_indicators[['bb_lower','bb_upper','bb_signal']] = BB_indicator(data, BB_range, std_multiple, return_full=True)[['lower_band','upper_band','signals']]

if 'ma_signal' in indicators:
        MA_short = random.randint(1, 300)
        MA_long = MA_short + random.randint(1, 400)
        signal_extender = random.randint(2, 15)
        combined_indicators[['ma_short','ma_long','ma_signal']] = MA_indicator(data, MA_short, MA_long, extender=signal_extender, return_full=True)[['short','long','position']]

if 'rsi_signal' in indicators:
        time_frame = random.randint(50, 1000)
        combined_indicators['rsi_buy'] = rsi_buy_level = 20
        combined_indicators['rsi_sell']  = rsi_sell_level = 80
        combined_indicators[['rsi_index','rsi_signal']] = RSI_indicator(data, time_frame, rsi_buy_level, rsi_sell_level, return_full=True)[['rsi_index','signal']]

if 'obv_signal' in indicators:
        OBV_short = random.randint(1, 300)
        OBV_long = MA_short + random.randint(1, 400)
        signal_extender = random.randint(2, 15)
        combined_indicators[['obv_short','obv_long','obv','obv_signal']] = OBV_indicator(data, 20, 40, extender=signal_extender,return_full=True)[['short_ma','long_ma','OBV','signal']]


combined_indicators['strength'] = combined_indicators[['bb_signal','ma_signal','rsi_signal']].sum(axis=1)
strength_level = 2
combined_indicators['all_yes'] = np.where(combined_indicators['strength'] >= strength_level, 1.0, 
                             np.where(combined_indicators['strength'] <= -strength_level, -1, 0))
combined_indicators['all_yes'] = create_single_signal(np.array(combined_indicators['all_yes']))

fig = plt.figure(figsize=(10,10),dpi=80)
ax1 = fig.add_subplot(2,1,1) 
ax2 = fig.add_subplot(6,1,4)
ax3 = fig.add_subplot(6,1,5)
ax4 = fig.add_subplot(6,1,6)

ax1.title.set_text('BB & MA')
ax1.plot(data['close'], 'k',
         combined_indicators['bb_lower'], 'b--',
         combined_indicators['bb_upper'], 'b--',
         combined_indicators['ma_short'], 'limegreen',
         combined_indicators['ma_long'], 'g--',)

ax2.title.set_text('OBV')
ax2.plot(combined_indicators['obv_short'], 'g',
         combined_indicators['obv_long'], 'r',
         combined_indicators['obv'], 'k',)

ax3.title.set_text('RSI')
ax3.plot(combined_indicators['rsi_index'], 'g',
         combined_indicators['rsi_buy'], 'r',
         combined_indicators['rsi_sell'], 'k',)

ax4.title.set_text('strength')
ax4.plot(combined_indicators['strength'], 'grey',
         combined_indicators['all_yes'], 'b')

plt.tight_layout()
fig.savefig('testsave.png')