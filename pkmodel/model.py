#
# Model class
#

class Model:
    """A Pharmokinetic (PK) model

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """

    model1_args = {
        'name': 'model1',
        'Q_p1': 1.0,
        'V_c': 1.0,
        'V_p1': 1.0,
        'CL': 1.0,
        'X': 1.0,
    }

    def __init__(self, Q_p1 = 1.0, V_c = 1.0, V_p1 = 1.0, CL = 1.0, X = 1.0):
        self.value = value
        model1_args = {
            'name': 'model1',
            'Q_p1': Q_p1,
            'V_c': V_c,
            'V_p1': V_p1,
            'CL': CL,
            'X': X,
        }

    def rhs(t, y, Q_p1, V_c, V_p1, CL, X):
    q_c, q_p1 = y
    transition = Q_p1 * (q_c / V_c - q_p1 / V_p1)
    dqc_dt = dose(t, X) - q_c / V_c * CL - transition
    dqp1_dt = transition
    return [dqc_dt, dqp1_dt]

   

