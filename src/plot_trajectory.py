'''plot trajectory obtained from simulation in the same figure as runs
 vector t_ev and marix X are returned by function simulate_system'''
import numpy as np
import matplotlib.pyplot as plt

def plottrajectory(h_fig, t_ev, X):
    n = np.shape(X)[1]
    plt = h_fig

    if n == 2:
        plt.plot(X[0, 0], X[1, 1])
        plt.plot(X[0:t_ev[0], 0], X[0:t_ev[1], 1])
        if len(t_ev) != 1:
            plt.plot(X[t_ev[0]::, 0], X[t_ev[0]::, 1])
        else:
            plt.plot(X[t_ev[0], 0], X[t_ev[0], 1])
