from functools import reduce
import matplotlib.pyplot as plt
import numpy as np

def create_single_signal(arr):
    """ makes [0,1,1,1,0] into [0,1,0,0,0,0]"""
    shift = np.concatenate([[0], arr[:-1]])
    return (arr!=shift) * arr

def repeat_last(arr):
    """repeats the last non zero value in a list
    has to be passed in as a numpy array"""
    prev = np.arange(len(arr))
    prev[arr == 0] = 0
    prev = np.maximum.accumulate(prev)
    return arr[prev]

def multi_long_short(arr):
    """cumsum but skips zero, pass in array for better preformance
    dont pass in an array of only zeros then it will fail!"""
    arr = arr.cumsum()
    first = arr.nonzero()[0][0]
    if arr[first] == 1:
        arr = np.where(arr<=0, arr-1, arr)
    elif arr[first] == -1:
        arr = np.where(arr>=0, arr+1, arr)
    arr[:first] = 0
    return arr

def combination_maker(strats, min=1):
    """Creates a random combination of a random amount of a list passed in"""
    return np.array(np.random.choice(strats, np.random.randint(min, len(strats)+1), replace=False))

def moving_average(a ,n=0):
    """fast numpy way of getting the moving average, pass in array"""
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    ret2 = ret[n - 1:] / n
    return np.pad(ret2,(len(a)-len(ret2),0),'constant',constant_values=(np.nan,0))

def rolling_window(a, window):
    """function to get rolling window of numpy arrays
    use like: np.std(rolling_window(close, 4), 1)"""
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)