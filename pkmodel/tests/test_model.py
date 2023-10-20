import unittest
import pkmodel as pk
import pytest
from numpy import random as rand

class ModelTest(unittest.TestCase):
    """
    Tests the :class:`Model` class.
    """
    def test_create(self):
        """
        Tests Model creation.
        """
        Q_p1, V_c, V_p1, CL, k_a = rand.rand(5)
        model = pk.Model(Q_p1 = Q_p1, V_c = V_c, V_p1 = V_p1, CL = CL, k_a = k_a)
        self.assertEqual(model.parameters["Q_p1"], Q_p1)
        self.assertEqual(model.parameters["V_c"], V_c)
        self.assertEqual(model.parameters["V_p1"], V_p1)
        self.assertEqual(model.parameters["CL"], CL)
        self.assertEqual(model.parameters["k_a"], k_a)
    
    def test_solve_steady(self):
        """
        Tests Model solver for steady application.
        """

        sol_iv = {
            't': 1.0,
            'y': [4.859e-01, 2.134e-01]
        }
        sol_sc = {
            't': 1.0,
            'y': [2.134e-01, 6.720e-02, 6.321e-01]
        }

        model = pk.Model()
        for type_dosing in ["intravenous", "subcutaneous"]:
            sol = model.solve_steady(pk.Protocol(type_dosing = type_dosing, steady_application = (1, 2), steady_dose = 1), t0 = 0, t1 = 2)
            if(type_dosing == "intravenous"):
                self.assertAlmostEqual(sol.y[0,-1], sol_iv["y"][0], delta=0.01)
                self.assertAlmostEqual(sol.y[1,-1], sol_iv["y"][1], delta=0.01)
            if(type_dosing == "subcutaneous"):
                self.assertAlmostEqual(sol.y[0,-1], sol_sc["y"][0], delta=0.01)
                self.assertAlmostEqual(sol.y[1,-1], sol_sc["y"][1], delta=0.01)
                self.assertAlmostEqual(sol.y[2,-1], sol_sc["y"][2], delta=0.01)

    def test_solve(self):
       Q_p1, V_c, V_p1, CL, k_a = rand.rand(5)
       model = pk.Model(Q_p1 = Q_p1, V_c = V_c, V_p1 = V_p1, CL = CL, k_a = k_a)
       for type_dosing in ["intravenous", "subcutaneous"]:
           protocol = pk.Protocol(type_dosing = type_dosing, instantaneous_application = [(i/4, 1) for i in range(8)], steady_application = (1, 2), steady_dose = 1)
           model.solve(protocol, t0 = 0, t1 = 2).plot_data('test_plot_' + type_dosing + '.png')

if __name__ == '__main__':
    unittest.main()