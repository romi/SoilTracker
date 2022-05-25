import time
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz, firwin
import numpy as np

def filter_sample(sample):
    """
    Filters a given sample using window method
    /!\ provides unexploitable results.
    """
    b = signal.firwin(6, 0.2)
    z = signal.lfilter_zi(b, 1)
    result, z = signal.lfilter(b, 1, sample, zi=z)
    return result[-1]

def avg(liste):
    """
    List average
    """
    return sum(liste)/(len(liste))

def med(liste):
    """
    List median
    """
    liste.sort()
    return liste[int(len(liste)/2)]

def filter2(x, y):
    """
    x is the i-th raw value
    y is the i-1-th filtered value
    """
    coeff = 0.06
    return (1 - coeff)*y + coeff*x

def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y[-1]

def lowpass_win(data):
    fs = 500
    nyq = fs/2
    filt = firwin(20, cutoff = 5/nyq, window="hamming")
    return med(lfilter(filt, 1, data)[-10:])

if __name__ == "__main__":
    ## Simulate real-time data and filter it

    # Gathering data
    with open("descente_data.csv") as f:
        L = f.readlines()
        X = []
        Y = []
        for i, line in enumerate(L[1:]):
            line = line.strip().split(",")
            X.append(float(line[1]))
            Y.append(float(line[2]))

    filtered_data_avg = []
    for i, elt in enumerate(Y):
        if i == 0:
            filtered_data_avg.append(Y[i])

        else:
            if i<5:
                sample = Y[0:i]
                filtered_data_avg.append(avg(sample))
                print(sample)

            else:
                sample = Y[(i-5) : i]
                filtered_data_avg.append(avg(sample))

    plt.plot(X, Y)
    plt.plot(X, filtered_data_avg)
    plt.show()
