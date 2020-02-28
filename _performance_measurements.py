import pandas as pd
import numpy as np
from _functions import repeat_last, multi_long_short


def first_signal_long_short(data, initial_capital, return_full=False, normalized=False):
    
    all_yes = data['all_yes'].to_numpy()
    close = data['close'].to_numpy()
    signals = repeat_last(all_yes)
    pos_diff = np.ediff1d(signals, to_begin=signals[0])
    holdings = signals * close
    cash = initial_capital - (pos_diff * close).cumsum()
    total = cash + holdings
    returns = np.diff(total) / total[:-1:]
    cum_returns = returns.cumsum()
    norm_returns = total / total[0]-1
    sharpe = returns.mean() / returns.std()
    
    if return_full and normalized: return sharpe, cum_returns, norm_returns
    elif return_full: return sharpe, cum_returns
    elif normalized: return sharpe, cum_returns[-1], norm_returns[-1]
    else: return sharpe, cum_returns[-1]

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