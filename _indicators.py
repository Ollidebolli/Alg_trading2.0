import pandas as pd
import numpy as np
from _functions import moving_average

def BB_indicator(close,time_frame, std_multiple, breakout=False, return_full=False):
    ma = moving_average(close,n=time_frame)
    std = pd.Series(close).rolling(window=time_frame).std().to_numpy()
    upper_band = ma + (std * std_multiple)
    lower_band = ma - (std * std_multiple)
    
    if breakout == False:
        signals = np.where(close > upper_band, -1.0, 
                  np.where(close < lower_band,1.0,0))
    elif breakout == True:
        signals = np.where(close > upper_band, 1.0, 
                  np.where(close < lower_band,-1.0,0))
        
    if return_full: return pd.DataFrame({'lower_band':lower_band,'upper_band':upper_band,'signals':signals})
    else: return signals

def MA_indicator(close, short_time_frame, long_time_frame, extender=0, return_full=False):
    ma_short = moving_average(close, n=short_time_frame)
    ma_long = moving_average(close, n=long_time_frame)
    signals = np.where(ma_short[long_time_frame:] > ma_long[long_time_frame:], 1.0,0)
    signals = np.pad(signals,(long_time_frame,0),'constant',constant_values=(0,0))
    signals = np.ediff1d(signals, to_begin=signals[0])

    signals = pd.Series(signals).replace({0:np.nan}).ffill(limit=extender).fillna(0)
    
    if return_full: return pd.DataFrame({'short':ma_short,'long':ma_long,'signals':signals})
    else: return signals.to_numpy()
    
def RSI_indicator(close, timeframe, buy_level, sell_level, return_full=False):
    delta = np.ediff1d(close, to_begin=close[0])
    dUp, dDown = delta.copy(), delta.copy()
    dUp[dUp < 0] = 0
    dDown[dDown > 0] = 0

    RolUp = moving_average(dUp,n=timeframe)
    RolDown = np.absolute(moving_average(dDown,n=timeframe))

    RS = RolUp[timeframe:] / RolDown[timeframe:]

    rsi_index = 100.0 - (100.0 / (1.0 + RS))
    signals = np.where(rsi_index <= buy_level, 1, np.where(rsi_index >= sell_level,-1,0))
    signals = np.pad(signals,(timeframe,0),'constant',constant_values=(0,0))
    
    if return_full: return pd.DataFrame({'rsi_index':np.pad(rsi_index,(timeframe,0),'constant',constant_values=(None,0)),'signal':signals})
    else: return signals

def OBV_indicator(data, short_ma, long_ma, extender=0, return_full=False):
    close = data['close'].to_numpy()
    volume = data['volume'].to_numpy()
    volume[0] = 0.0
    
    obv = np.where(close > np.roll(close, 1), volume,
          np.where(close < np.roll(close, 1), -volume,0)).cumsum()
    
    ma_short = moving_average(obv, n=short_ma)
    ma_long = moving_average(obv, n=long_ma)
    
    signals = np.where(ma_short > ma_long,1,0)
    signals = np.ediff1d(signals, to_begin=signals[0])
    signals = pd.Series(signals).replace({0:np.nan}).ffill(limit=extender).fillna(0)

    if return_full: return pd.DataFrame({'short_ma':ma_short,'long_ma':ma_long,'OBV':obv,'signal':signals})
    else: return signals
