#
# Model class
#

import scipy
import numpy as np
class Model:
    """A Pharmokinetic (PK) model

    Parameters
    ----------
    dose_function: function
        not sure what this should look like #TODO
    Q_p1: numeric, optional
        the transition rate between central compartment and peripheral compartment 1
    V_c: numeric, optional
        [mL], the volume of the central compartment
    V_p1: numeric, optional
        [mL], the volume of the first peripheral compartment
    k_a: numeric, optional
        [mL], the volume of the first peripheral compartment
    CL: numeric, optional
        [mL/h], the clearance/elimination rate from the central compartment
    X: numeric, optional
        [ng] the dose? Should this even be here?
    

    """

    def __init__(self, dose_function, 
                 Q_p1 = 1.0, V_c = 1.0, V_p1 = 1.0, CL = 1.0, k_a = 1.0, delivery = "intravenous"):
        delivery_types = ['intravenous', 'subcutaneous']
        if delivery not in delivery_types:
            raise ValueError("Invalid delivery type. Expected one of: %s" % delivery_types)
        self.parameters = {
            'delivery': delivery,
            'Q_p1': Q_p1,
            'V_c': V_c,
            'V_p1': V_p1,
            'CL': CL,
            'k_a': k_a
        }
        self.dose_function = dose_function


    def rhs_iv(self, t, y):
        q_c, q_p1 = y
        transition = self.parameters["Q_p1"] * (q_c / self.parameters["V_c"] - q_p1 / self.parameters["V_p1"])
        dqc_dt = self.dose_function(t) - q_c / self.parameters["V_c"] * self.parameters["CL"] - transition
        dqp1_dt = transition
        return [dqc_dt, dqp1_dt]
    
    def rhs_sc(self, t, y):
        q_c, q_p1, q_p0 = y
        transition = self.parameters["Q_p1"] * (q_c / self.parameters["V_c"] - q_p1 / self.parameters["V_p1"])
        dqp0_dt = self.dose_function(t) - self.parameters["k_a"] * q_p0
        dqc_dt = self.parameters["k_a"] * q_p0 - q_c / self.parameters["V_c"] * self.parameters["CL"] - transition
        dqp1_dt = transition
        return [dqc_dt, dqp1_dt, dqp0_dt]
    
    def solve(self, t0 = 0, t1 = 1, steps = 1000):
        t_eval = np.linspace(t0, t1, steps)
        if(self.parameters["delivery"] == "intravenous"):
            y0 = np.array([0.0, 0.0])
            sol = scipy.integrate.solve_ivp(
                fun=lambda t, y: self.rhs_iv(t, y),
                t_span=[t_eval[0], t_eval[-1]],
                y0=y0, t_eval=t_eval
            )
        elif(self.parameters["delivery"] == "subcutaneous"):
            y0 = np.array([0.0, 0.0, 0.0])
            sol = scipy.integrate.solve_ivp(
                fun = lambda t, y: self.rhs_sc(t, y),
                t_span=[t_eval[0], t_eval[-1]],
                y0=y0, t_eval=t_eval
            )
        return sol


   

