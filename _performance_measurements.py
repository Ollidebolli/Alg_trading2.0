import pandas as pd
import numpy as np
from _functions import repeat_last, multi_long_short


def first_signal_long_short(data, initial_capital, return_full=False, normalized=False):

    signals = repeat_last(np.array(data['all_yes']))
    
    performance = pd.DataFrame(index=data.index).fillna(0.0)
    portfolio = performance.copy()
    performance['positions'] = signals
    pos_diff = performance['positions'].diff()
    pos_diff[0] = 0
    portfolio['holdings'] = performance['positions'] * data['close']
    portfolio['cash'] = initial_capital - (pos_diff * data['close']).cumsum()
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()

    cum_returns = portfolio['returns'].cumsum()
    norm_returns = portfolio['total'] / portfolio.iloc[0]['total']-1

    sharpe_ratio = portfolio['returns'].mean() / portfolio['returns'].std()

    if return_full and normalized: return sharpe_ratio, cum_returns, norm_returns
    elif return_full: return sharpe_ratio, cum_returns
    elif normalized: return sharpe_ratio, cum_returns.iloc[-1], norm_returns.iloc[-1]
    else: return sharpe_ratio, cum_returns.iloc[-1]

def multi_signal_long_short(data, initial_capital, return_full=False, normalized=False):

    signals = multi_long_short(np.array(data['all_yes']))

    performance = pd.DataFrame(index=data.index).fillna(0.0)
    portfolio = performance.copy()
    performance['positions'] = signals
    pos_diff = performance['positions'].diff()
    pos_diff[0] = 0
    portfolio['holdings'] = performance['positions'] * data['close']
    portfolio['cash'] = initial_capital - (pos_diff*data['close']).cumsum()
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()
    
    cum_returns = portfolio['returns'].cumsum()
    norm_returns = portfolio['total'] / portfolio.iloc[0]['total']-1

    sharpe_ratio = portfolio['returns'].mean() / portfolio['returns'].std()

    if return_full and normalized: return sharpe_ratio, cum_returns, norm_returns
    elif return_full: return sharpe_ratio, cum_returns
    elif normalized: return sharpe_ratio, cum_returns.iloc[-1], norm_returns.iloc[-1]
    else: return sharpe_ratio, cum_returns.iloc[-1]