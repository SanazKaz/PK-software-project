#
# Solution class
#
import matplotlib.pylab as plt
import numpy as np
import scipy.integrate
import model
"""
    A Pharmacokinetic (PK) model.
    
    This class represents a basic PK model for drug distribution in the body. It models
    both intravenous (iv) and subcutaneous (sc) drug administration routes.

    Parameters
    ----------
    dose_function : function
        A function that returns the dose given at time `t`.
    Q_p1 : float, optional
        Transition rate between central compartment and peripheral compartment 1.
    V_c : float, optional
        Volume of the central compartment [mL].
    V_p1 : float, optional
        Volume of the first peripheral compartment [mL].
    k_a : float, optional
        Absorption rate constant [1/h].
    CL : float, optional
        Clearance/elimination rate from the central compartment [mL/h].
    delivery : str, optional
        Administration route. Either "intravenous" or "subcutaneous".

    Attributes
    ----------
    parameters : dict
        Dictionary storing the parameters of the PK model.
    dose_function : function
        Function representing the drug dose over time.
    """

class Solution:
  """ solves the model with set start time, end time and steps and stores
   it in the self.solution """
    def __init__(self, model: model.Model, t0=0.0, t1=1.0, steps=1000):
        self.model = model

        self.solution=model.solve(t0, t1, steps)
        
""" Plots the results of the model"""
    def plot_data(self):
        plt.plot(self.solution.t, self.solution.y[0, :], label='model1' + '- q_c')
        plt.plot(self.solution.t, self.solution.y[1, :], label='model2' + '- q_p1')

        plt.legend()
        plt.ylabel('drug mass [ng]')
        plt.xlabel('time [h]')
        plt.show()
