import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from _indicators import BB_indicator, MA_indicator, RSI_indicator, OBV_indicator
from _functions import create_single_signal, combination_maker
from _performance_measurements import multi_signal_long_short, first_signal_long_short

data = pd.read_csv("historical_price_data/bistamp_hourly_since_beginning.csv",
                  usecols=['close','volume'])

close = data['close'].to_numpy()

combined_indicators = pd.DataFrame(index=data.index)

indicators = ['rsi_signal']

if 'bb_signal_bo' in indicators:
        BB_range = random.randint(1, 300)
        std_multiple = random.uniform(0.3, 10)
        combined_indicators[['bb_lower_bo','bb_upper_bo','bb_signal_bo']] = BB_indicator(close, BB_range, std_multiple, breakout=True, return_full=True)[['lower_band','upper_band','signals']]

if 'bb_signal' in indicators:
        BB_range = 9099
        std_multiple = 0.4661689574
        combined_indicators[['bb_lower','bb_upper','bb_signal']] = BB_indicator(close, BB_range, std_multiple, return_full=True)[['lower_band','upper_band','signals']]

if 'ma_signal' in indicators:
        MA_short = 237
        MA_long = 476
        signal_extender = 9
        combined_indicators[['ma_short','ma_long','ma_signal']] = MA_indicator(close, MA_short, MA_long, extender=signal_extender, return_full=True)[['short','long','signals']]

if 'rsi_signal' in indicators:
        time_frame = 256
        combined_indicators['rsi_buy'] = rsi_buy_level = 54
        combined_indicators['rsi_sell']  = rsi_sell_level = 78
        combined_indicators[['rsi_index','rsi_signal']] = RSI_indicator(close, time_frame, rsi_buy_level, rsi_sell_level, return_full=True)[['rsi_index','signal']]

if 'obv_signal' in indicators:
        OBV_short = 36331
        OBV_long = 36843
        signal_extender = 9
        combined_indicators[['obv_short','obv_long','obv','obv_signal']] = OBV_indicator(data, OBV_short, OBV_long, extender=signal_extender,return_full=True)[['short_ma','long_ma','OBV','signal']]


combined_indicators['strength'] = combined_indicators[indicators].sum(axis=1)
strength_level = len(indicators)
combined_indicators['all_yes'] = np.where(combined_indicators['strength'] >= strength_level, 1.0, 
                                 np.where(combined_indicators['strength'] <= -strength_level, -1, 0))
combined_indicators['all_yes'] = create_single_signal(np.array(combined_indicators['all_yes']))

fig = plt.figure(figsize=(10,10), dpi=80)
ax1 = fig.add_subplot(2,1,1) 
ax2 = fig.add_subplot(6,1,4)
ax3 = fig.add_subplot(6,1,5)
ax4 = fig.add_subplot(6,1,6)

try:
        ax1.title.set_text('BB & MA')
        ax1.plot(data['close'], 'k',
                combined_indicators['bb_lower'], 'b--',
                combined_indicators['bb_upper'], 'b--',
                combined_indicators['ma_short'], 'limegreen',
                combined_indicators['ma_long'], 'g--',)
except:pass
try:
        ax2.title.set_text('OBV')
        ax2.plot(combined_indicators['obv_short'], 'g',
                 combined_indicators['obv_long'], 'r',
                 combined_indicators['obv'], 'k',)
except:pass
try:

        ax3.title.set_text('RSI')
        ax3.plot(combined_indicators['rsi_index'], 'g',
                 combined_indicators['rsi_buy'], 'r',
                 combined_indicators['rsi_sell'], 'k',)
except:pass
try:
        ax4.title.set_text('strength')
        ax4.plot(combined_indicators['strength'], 'grey',
                 combined_indicators['all_yes'], 'b')
except:pass

plt.tight_layout()
fig.savefig('testsave.png')