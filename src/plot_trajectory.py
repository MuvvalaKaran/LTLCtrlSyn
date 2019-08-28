'''plot trajectory obtained from simulation in the same figure as runs
 vector t_ev and marix X are returned by function simulate_system'''
import numpy as np
import matplotlib.pyplot as plt

class PlotTrajectory():

    def __init__(self, h_fig, t_ev, X):
        self.h_fig = h_fig
        self.t_ev = t_ev
        self.X = X


    def plottrajectory(self):

        X = self.X
        t_ev = self.t_ev

        X = [np.ravel(array) for array in X]

        big_array = np.ndarray((len(X) - 1, 2))
        for counter, i in enumerate(X):
            if counter == len(X) - 1:
                continue
            big_array[counter, :] = i

        n = np.shape(big_array)[1]
        ax = self.h_fig

        if n == 2:
            plt.plot(big_array[0, 0], big_array[1, 1])
            plt.plot(big_array[0:t_ev[0], 0], big_array[0:t_ev[0], 1])
            if len(t_ev) != 1:
                plt.plot(big_array[t_ev[0]::, 0], big_array[t_ev[0]::, 1])
            else:
                plt.plot(big_array[t_ev[0], 0], big_array[t_ev[0], 1])
                plt.show()
