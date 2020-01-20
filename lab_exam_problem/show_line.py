import matplotlib.pyplot as plt
import numpy as np


def show_line(data, m, c):
    data = np.array(data)
    plt.plot(data[:,0], data[:,1], 'C1o', label="Data")
    plt.plot([np.min(data[:,0]), np.max(data[:,0])],
             [m*np.min(data[:,0])+c, m*np.max(data[:,0])+c], label="Line")
    plt.legend()
    plt.title(f"Line fit m={m:.2f} c={c:.2f}")

def show_many_lines(data, fits, ranges):
    data = np.array(data)
    plt.plot(data[:,0], data[:,1], 'C1o', label="Data")
    for fit, (start, end) in zip(fits, ranges):
        m, c = fit
        if start!=end:
            plt.plot([np.min(data[start:end,0]), np.max(data[start:end,0])],
                     [m*np.min(data[start:end,0])+c, m*np.max(data[start:end,0])+c], c='C2', marker='.', alpha=0.2)
    
    plt.title(f"Partial fits")

