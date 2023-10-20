#
# Solution class
#
import matplotlib.pylab as plt
import numpy as np
import scipy.integrate

"""
This class represents the solution of a basic PK model for drug distribution in the body.
It models both intravenous (iv) and subcutaneous (sc) drug administration routes.

"""

class Solution:

    def __init__(self, t_sol, y_sol, type_dosing):
        self.type_dosing = type_dosing
        self.t_sol = t_sol
        self.y_sol = y_sol

    def plot_data(self, path = None):

        """ Plots the results of the model"""
        fig = plt.figure()
        if (self.type_dosing == "intravenous"):
            plt.plot(self.t_sol, self.y_sol[0, :], label = 'compartment' + '- q_c')
            plt.plot(self.t_sol, self.y_sol[1, :], label = 'compartment' + '- q_p1')
        elif (self.type_dosing == "subcutaneous"):
            plt.plot(self.t_sol, self.y_sol[0, :], label = 'compartment' + '- q_c')
            plt.plot(self.t_sol, self.y_sol[1, :], label = 'compartment' + '- q_p1')
            plt.plot(self.t_sol, self.y_sol[1, :], label = 'compartment' + '- q_p0')
        else:
            raise Exception('type_dosing must be either "intravenous" or "subcutaneous"')
        plt.legend()
        plt.ylabel('drug mass [ng]')
        plt.xlabel('time [h]')
        if (path == None): plt.show()
        else:
            plt.savefig(path)
            plt.close(fig)