#
# Model class
#

import scipy
import numpy as np
class Model:
    """A Pharmokinetic (PK) model

    Parameters (live within parameters property, a dictionary)
    ----------
    :param dose_function: Should return dose (float) at timepoint t (float) #TODO
    :param Q_p1: the transition rate between central compartment and peripheral compartment 1, defaults to 1
    :type Q_p1: float, optional
    :param V_c: [mL], the volume of the central compartment
    :type V_c: float, optional
    :param V_p1: [mL], the volume of the first peripheral compartment, defaults to 1
    :type V_p1: float, optional
    :param k_a: [mL], the volume of the first peripheral compartment, defaults to 1
    :type k_a: float, optional    
    :param CL: [mL/h], the clearance/elimination rate from the central compartment, defaults to 1
    :type CL: float, optional    
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


    def rhs_iv(self, t, y)->list:
        """ ODE model for intravenous PK model
        :param t: timepoint
        :type t: float
        :param y: ODE variables
        :type t1: list of floats
        :return [dqc_dt, dqp1_dt]: List of differentials of amount, first is central compartment, second is peripheral comp
        :rtype [dqc_dt, dqp1_dt]: List of floats
        """
        q_c, q_p1 = y
        transition = self.parameters["Q_p1"] * (q_c / self.parameters["V_c"] - q_p1 / self.parameters["V_p1"])
        dqc_dt = self.dose_function(t) - q_c / self.parameters["V_c"] * self.parameters["CL"] - transition
        dqp1_dt = transition
        return [dqc_dt, dqp1_dt]
    
    def rhs_sc(self, t: float, y: list)->list:
        """ ODE model for subcutaneous PK model
        :param t: timepoint
        :type t: float
        :param y: ODE variables
        :type t1: list of floats
        :return [dqc_dt, dqp1_dt, dqp0_dt]: List of differentials of amounts for central, peripheral, skin compartments
        :rtype [dqc_dt, dqp1_dt, dqp0_dt]: List of floats
        """
        q_c, q_p1, q_p0 = y
        transition = self.parameters["Q_p1"] * (q_c / self.parameters["V_c"] - q_p1 / self.parameters["V_p1"])
        dqp0_dt = self.dose_function(t) - self.parameters["k_a"] * q_p0
        dqc_dt = self.parameters["k_a"] * q_p0 - q_c / self.parameters["V_c"] * self.parameters["CL"] - transition
        dqp1_dt = transition
        return [dqc_dt, dqp1_dt, dqp0_dt]
    
    def solve(self, t0 = 0.0, t1 = 1.0, steps = 1000):
        """ Solves ODE system for supplied duration with number of steps, returns scipy.integrate.solv_ivp output
        :param t0: Start timepoint, defaults to 0
        :type t0: float, optional
        :param t1: End timepoint, defaults to 1
        :type t1: float, optional
        :param steps: Number of steps to integrate, defaults to 1000
        :type t1: int, optional
        :return sol: Bunch object with various fields defined, such as t (1D nparray of time series), y (N-dim nparray of solution),
        success bool - for details see scipy.integrate.solv_ivp
        :rtype sol: Bunch object
        """

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


   

