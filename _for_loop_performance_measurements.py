import numpy as np
import pandas as pd




def single_signal_for(close_list, signals, initial_capital = 100, return_full = False):
    port_transaction = list(np.zeros(len(close_list)))
    port_holdings = list(np.zeros(len(close_list)))
    port_cash = list(np.zeros(len(close_list)))

    direction = 'none'

    for i in range(len(close_list)):
        
        if i == 0:
            holdings = 0
            cash = initial_capital
            
        else:
            holdings = port_holdings[i-1]
            cash = port_cash[i-1]
                
        signal = signals[i]
        close = close_list[i]
        transaction = 0
        
        if (signal == 1) & (direction == 'short'):
            direction = 'long'
            
            transaction = cash/2
            cash = 0
            holdings = transaction / close
        
        elif (signal == 1) & (direction == 'none'):
            direction = 'long'
            
            transaction = cash
            cash = cash - transaction
            holdings = (transaction / close)
        
        elif (signal == -1) & (direction == 'none'):
            direction = 'short'
            
            transaction = cash
            cash = cash + transaction
            holdings = -cash
        
        elif (signal == -1) & (direction == 'long'):
            direction = 'short'
            
            transaction = (close * holdings*2)
            cash = cash + transaction
            holdings = holdings - holdings * 2
        
        port_cash[i] = cash
        port_holdings[i] = holdings
        port_transaction[i] = transaction

    if return_full:
        df = pd.DataFrame([close_list, port_transaction, port_holdings, port_cash]).transpose()
        df.columns = ['close', 'cashflow', 'holdings', 'cash']
        df['total']= df['close'] * df['holdings'] + df['cash']
        return df
    else:
        return close_list * port_holdings + port_cash

def multi_signal_for(input_close, signals, max_pos = 10, initial_capital = 100, return_full=False):

    _close = input_close
    _signal = signals
    _pos_size = np.zeros(len(_close))
    _holdings = np.zeros(len(_close))
    _ACT_short_value = np.zeros(len(_close))
    _short_pos = np.zeros(len(_close))
    _long_pos = np.zeros(len(_close))
    _cashflow = np.zeros(len(_close))
    _holdings_diff = np.zeros(len(_close))
    _holdings = np.zeros(len(_close))
    _actual_cash = np.zeros(len(_close))
    _cash_balance = np.zeros(len(_close))

    pos_size = 0

    for i in range(len(_close)):
        
        if i == 0:
            cash = initial_capital
            close = _close[i]
            cash_balance = cash
            holdings = 0
            prev_pos_size = 0

        if (pos_size == max_pos) | (pos_size == -max_pos): pos_size = prev_pos_size
        
        prev_holdings = holdings
        prev_cash_balance = cash_balance
        prev_pos_size = pos_size
        prev_cash = cash
        
        close = _close[i]
        signal = _signal[i]
        
        if (pos_size == 0) & (signal == 0):
            
            cashflow = 0
            holdings_diff = 0
            holdings = prev_holdings
            cash = prev_cash
            cash_balance = prev_cash_balance
            
            short_pos = 0
            ACT_short = 0
            long_pos = 0
        
        #short and no signal
        elif (pos_size < 0) & (signal == 0):
            
            cashflow = 0
            holdings_diff = 0
            holdings = prev_holdings
            cash = prev_cash
            cash_balance = prev_cash_balance
            short_pos = holdings * close
            ACT_short = cash_balance - cash - short_pos
            
            long_pos = 0
        
        #long and no signal
        elif (pos_size > 0) & (signal == 0):
            
            cashflow = 0
            holdings_diff = 0
            holdings = prev_holdings
            cash = prev_cash
            cash_balance = prev_cash_balance
            long_pos = holdings * close
            
            short_pos = 0
            ACT_short = 0
        
        
        #going from none to long
        elif (pos_size == 0) & (signal == 1):
            
            cashflow = -(cash / max_pos)
            holdings_diff = -(cashflow / close)
            holdings = prev_holdings + holdings_diff
            cash = cash + cashflow
            cash_balance = prev_cash_balance - (holdings_diff * close)
            
            long_pos = holdings * close
            
            pos_size = 1
        
        #going long to longer
        elif (pos_size > 0) & (signal == 1):
            
            cashflow = -(cash / (max_pos - prev_pos_size))
            holdings_diff = -(cashflow / close)
            holdings = prev_holdings + holdings_diff
            cash = prev_cash + cashflow
            cash_balance = prev_cash_balance - ( holdings_diff * close)
            
            long_pos = holdings * close
            
            pos_size += 1

        #going long to less long
        elif (pos_size > 1 ) & (signal == -1):
            
            holdings_diff = -(holdings/prev_pos_size)
            cashflow = -(holdings_diff * close)
            holdings = holdings + holdings_diff
            cash = prev_cash + cashflow
            cash_balance = prev_cash_balance - (holdings_diff * close)
            
            long_pos = holdings * close
            
            pos_size -= 1
            
            
        #going from long to short, 1 to -1
        elif (pos_size == 1) & (signal == -1):
            
            holdings_diff = - holdings
            cashflow = -(holdings_diff * close)
            holdings = 0
            cash = prev_cash + cashflow
            cash_balance = prev_cash_balance - (holdings_diff * close)
            long_pos = holdings * close
            
            pos_size = 0
            
            cashflow = -(cash / max_pos)
            holdings_diff = cashflow / close
            holdings = holdings_diff
            cash = cash + cashflow
            cash_balance = cash_balance - (holdings * close)
            
            short_pos = holdings * close
            ACT_short = cash - cash_balance - short_pos
            
            pos_size = -1

        #going from none to short
        elif (pos_size == 0) & (signal == -1):
            
            cashflow = -(cash / max_pos)
            holdings_diff = cashflow * close
            holdings = prev_holdings + holdings_diff
            cash = cash + cashflow
            cash_balance = prev_cash_balance - (holdings_diff * close)
            
            short_pos = holdings * close
            ACT_short = cash - cash_balance - short_pos
            
            pos_size = -1
            
        
        #going from short to shorter
        elif (pos_size < 0) & (signal == -1):
            
            cashflow = -(prev_cash / (max_pos + prev_pos_size))
            holdings_diff = cashflow / close
            holdings = prev_holdings + holdings_diff
            cash = prev_cash + cashflow
            cash_balance = prev_cash_balance - (holdings_diff * close)
            short_pos = holdings * close
            ACT_short = cash - cash_balance - short_pos
            
            pos_size -= 1
            
        #going from short to less short (hardest one)
        elif (pos_size < -1) & (signal == 1):
            
            holdings_diff = prev_holdings / prev_pos_size
            cashflow = (prev_cash - prev_cash_balance-(prev_holdings*close)) / prev_pos_size
            holdings = prev_holdings + holdings_diff
            cash = prev_cash + cashflow
            cash_balance = prev_cash_balance - (holdings_diff * close)
            short_pos = holdings * close
            ACT_short = cash - cash_balance - short_pos
            
            pos_size += 1
        
        #going from short to long
        elif (pos_size == -1) & (signal == 1):
            
            holdings_diff = prev_holdings / prev_pos_size
            cashflow = (prev_cash - prev_cash_balance-(prev_holdings*close)) / prev_pos_size
            holdings = prev_holdings + holdings_diff
            cash = prev_cash + cashflow
            cash_balance = prev_cash_balance - (holdings_diff * close)
            short_pos = holdings * close
            ACT_short = cash - cash_balance - short_pos
            
            pos_size = 0
            
            cashflow = -(cash / max_pos)
            holdings_diff = -(cashflow / close)
            holdings = holdings + holdings_diff
            cash = cash + cashflow
            cash_balance = cash_balance - (holdings_diff * close)
            
            long_pos = holdings * close
            
            pos_size = 1
            
        _pos_size[i] = pos_size
        _holdings[i] = holdings
        _ACT_short_value[i] = ACT_short
        _short_pos[i] = short_pos
        _long_pos[i] = long_pos
        _cashflow[i] = cashflow
        _holdings_diff[i] = holdings_diff
        _holdings[i] = holdings
        _actual_cash[i] = cash
        _cash_balance[i] = cash_balance

        
    if return_full:
        t = [_close, _signal, _pos_size, _ACT_short_value,_short_pos,_long_pos,
        _cashflow, _holdings_diff, _holdings, _actual_cash, _cash_balance]

        df = pd.DataFrame(t).transpose().round(4)

        df.columns = ['close','signal','size','ACT_short','short','long','cashflow','holding diff','holdings','cash','cash_balance']

        df['total'] = df[['cash_balance','long','short']].sum(axis=1)

        return df

    else:
        return _cash_balance