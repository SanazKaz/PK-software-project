#
# Model class
#

class Model:
    """A Pharmokinetic (PK) model

    Parameters
    ----------

    Q_p1: numeric, optional
        the transition rate between central compartment and peripheral compartment 1
    V_c: numeric, optional
        [mL], the volume of the central compartment
    V_p1: numeric, optional
        [mL], the volume of the first peripheral compartment
    CL: numeric, optional
        [mL/h], the clearance/elimination rate from the central compartment
    X: numeric, optional
        an example paramter
    

    """

    def __init__(self, Q_p1 = 1.0, V_c = 1.0, V_p1 = 1.0, CL = 1.0, X = 1.0, delivery = "intravenous"):
        delivery_types = ['intravenous', 'subcutaneous']
        if delivery not in delivery_types:
            raise ValueError("Invalid delivery type. Expected one of: %s" % delivery_types)
        self.parameters = {
            'delivery': delivery,
            'Q_p1': Q_p1,
            'V_c': V_c,
            'V_p1': V_p1,
            'CL': CL,
            'X': X,
        }

def dose(t, X):
    return X

    def rhs(self, t, y):
        q_c, q_p1 = y
        transition = self.parameters["Q_p1"] * (q_c / self.parameters["V_c"] - q_p1 / self.parameters["V_p1"])
        dqc_dt = dose(t, X) - q_c / self.parameters["V_c"] * self.parameters["CL"] - transition
        dqp1_dt = transition
        return [dqc_dt, dqp1_dt]

   

