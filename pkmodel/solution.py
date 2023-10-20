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

    def plot_data(self):

        """ Plots the results of the model"""

        if (delivery == "intravenous"):
            plt.plot(self.t_sol, self.y_sol[0, :], label = 'compartment' + '- q_c')
            plt.plot(self.t_sol, self.y_sol[1, :], label = 'compartment' + '- q_p1')
        if (delivery == "subcutaneous"):
            plt.plot(self.t_sol, self.y_sol[0, :], label = 'compartment' + '- q_c')
            plt.plot(self.t_sol, self.y_sol[1, :], label = 'compartment' + '- q_p1')
            plt.plot(self.t_sol, self.y_sol[1, :], label = 'compartment' + '- q_p0')
        plt.legend()
        plt.ylabel('drug mass [ng]')
        plt.xlabel('time [h]')
        plt.show()
