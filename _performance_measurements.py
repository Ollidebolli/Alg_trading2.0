import pandas as pd
import numpy as np
from _functions import repeat_last, multi_long_short


def first_signal_long_short(close, all_yes, initial_capital, return_full=False, normalized=False):
    
    position = repeat_last(all_yes)
    pos_diff = np.ediff1d(position, to_begin=position[0])
    holdings = position * close
    cash = initial_capital - (pos_diff * close).cumsum()
    total = cash + holdings
    returns = np.diff(total) / total[:-1:]
    cum_returns = returns.cumsum()
    cum_returns = np.pad(cum_returns,(1,0))
    norm_returns = total / total[0]-1
    sharpe = returns.mean() / returns.std()
    
    if return_full and normalized: return sharpe, cum_returns, norm_returns
    elif return_full: return sharpe, cum_returns
    elif normalized: return sharpe, cum_returns[-1], norm_returns[-1]
    else: return sharpe, cum_returns[-1]

def multi_signal_long_short(close, all_yes, initial_capital, return_full=False, normalized=False):

    position = multi_long_short(all_yes)
    pos_diff = np.ediff1d(position, to_begin=position[0])
    holdings = position * close
    cash = initial_capital - (pos_diff * close).cumsum()
    total = cash + holdings
    returns = np.diff(total) / total[:-1:]
    cum_returns = returns.cumsum()
    cum_returns = np.pad(cum_returns,(1,0))
    norm_returns = total / total[0]-1
    sharpe = returns.mean() / returns.std()
    
    if return_full and normalized: return sharpe, cum_returns, norm_returns
    elif return_full: return sharpe, cum_returns
    elif normalized: return sharpe, cum_returns[-1], norm_returns[-1]
    else: return sharpe, cum_returns[-1]