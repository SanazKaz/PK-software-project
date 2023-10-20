#
# Model class
#

import scipy
import numpy as np
from pkmodel import solution

class Model:

    """
    A Pharmokinetic (PK) model

    Args:
         dose_function (function): steady application dose injected over time
         Q_p1 (numeric): optional, the transition rate between central compartment and peripheral compartment 1
         V_c (numeric): optional, [mL], the volume of the central compartment
         V_p1 (numeric): optional, [mL], the volume of the first peripheral compartment
         k_a (numeric): optional, [/h] is the “absorption” rate for the s.c dosing.
         CL (numeric): optional, [mL/h], the clearance/elimination rate from the central compartment

    """

    def __init__(self, Q_p1 = 1.0, V_c = 1.0, V_p1 = 1.0, CL = 1.0, k_a = 1.0):
        self.parameters = {
            'Q_p1': Q_p1,
            'V_c': V_c,
            'V_p1': V_p1,
            'CL': CL,
            'k_a': k_a
        }
            
    def rhs_iv(self, t, y, proto):
        
        """ 
        ODE model for intravenous PK model

        Args:
             t (float): timepoint
             y (float): ODE variables
             protocol (Protocol()): protocol used for the model, instance of Protocol()

        Returns:     
            [dqc_dt, dqp1_dt] (list of floats): List of differentials of amount, 
                first is central compartment, second is peripheral compartment
        """

        q_c, q_p1 = y
        transition = self.parameters["Q_p1"] * (q_c / self.parameters["V_c"] - q_p1 / self.parameters["V_p1"])
        dqc_dt = proto.dose_function(t) - q_c / self.parameters["V_c"] * self.parameters["CL"] - transition
        dqp1_dt = transition
        return [dqc_dt, dqp1_dt]
    
    def rhs_sc(self, t, y, proto):

        """ 
        ODE model for subcutaneous PK model

        Args:
            t (float): timepoint
            y (float): ODE variables
            protocol (Protocol()): protocol used for the model, instance of Protocol()

        Returns:     
            [dqc_dt, dqp1_dt, dqp0_dt] (list of floats): List of differentials of amount for central, peripheral, skin compartments
                first is central compartment, second is peripheral compartment            
        """

        q_c, q_p1, q_p0 = y
        transition = self.parameters["Q_p1"] * (q_c / self.parameters["V_c"] - q_p1 / self.parameters["V_p1"])
        dqp0_dt = proto.dose_function(t) - self.parameters["k_a"] * q_p0
        dqc_dt = self.parameters["k_a"] * q_p0 - q_c / self.parameters["V_c"] * self.parameters["CL"] - transition
        dqp1_dt = transition
        return [dqc_dt, dqp1_dt, dqp0_dt]
    
    def solve_steady(self, proto, t0 = 0, t1 = 1, steps = 1000, y0 = None):

        """ 
        Solves ODE system for supplied duration with number of steps, returns scipy.integrate.solv_ivp output

        Args:
             t0 (float): optional, start timepoint, defaults to 0
             t1 (float): optional, end timepoint, defaults to 1
             steps (int): optional, number of steps to integrate, defaults to 1000

        Returns:     
            sol (bunch object): bunch object with various fields defined, such as t (1D nparray of time series), y (N-dim nparray of solution),
                success bool - for details see scipy.integrate.solv_ivp
        """

        t_eval = np.linspace(t0, t1, steps)
        if (proto.type_dosing == "intravenous"):
            if(type(y0) == type(None)): y0 = np.array([0.0, 0.0])
            sol = scipy.integrate.solve_ivp(
                fun = lambda t, y: self.rhs_iv(t, y, proto),
                t_span = [t_eval[0], t_eval[-1]],
                y0=y0, t_eval=t_eval
            )
        elif (proto.type_dosing == "subcutaneous"):
            if(type(y0) == type(None)): y0 = np.array([0.0, 0.0, 0.0])
            sol = scipy.integrate.solve_ivp(
                fun = lambda t, y: self.rhs_sc(t, y, proto),
                t_span=[t_eval[0], t_eval[-1]],
                y0=y0, t_eval=t_eval
            )
        else:
            raise Exception('type_dosing must be either "intravenous" or "subcutaneous"')
        return sol

    def solve(self, proto, t0 = 0, t1 = 1, steps = 1000):
        remaining_steps = steps
        t_old = t0
        Y = None
        t_solutions = []
        y_solutions = []
        t_new, X = proto.next_application()
        while (X != None and t_new < t1):
            if (t_new > t_old):
                temp_steps = int(remaining_steps*(t_new - t_old)/(t1 - t_old))
                sol = self.solve_steady(proto, t0 = t_old, t1 = t_new, steps = temp_steps + 1, y0 = Y)
                remaining_steps -= temp_steps
                t_solutions += [sol.t]
                y_solutions += [sol.y]
                t_old = sol.t[-1]
                if(proto.type_dosing == "intravenous"):
                    Y = sol.y[:,-1] + np.array([X, 0.0])
                elif(proto.type_dosing == "subcutaneous"):
                    Y = sol.y[:,-1] + np.array([0.0, 0.0, X])
                else:
                    raise Exception('type_dosing must be either "intravenous" or "subcutaneous"')
            t_new, X = proto.next_application()
        sol = self.solve_steady(proto, t0 = t_old, t1 = t1, steps = remaining_steps + 1, y0 = Y)
        t_solutions += [sol.t]
        y_solutions += [sol.y]
        t_sol = np.concatenate(t_solutions)
        y_sol = np.concatenate(y_solutions, axis=-1)
        return solution.Solution(t_sol, y_sol, proto.type_dosing)

        







