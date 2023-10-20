import unittest
import pkmodel as pk


class ModelTest(unittest.TestCase):
    """
    Tests the :class:`Model` class.
    """
    def dose_dummy(self, t)->float:
        """
        Dummy dose function that returns constant float for testing.
        """
        return 1.0

    def test_create(self):
        """
        Tests Model creation.
        """
        model = pk.Model(self.dose_dummy)
        self.assertEqual(model.parameters["CL"], 1.0)
        #self.assertEqual(model)

    def test_model_defaults(self):
        """Tests Model defaults run and the solver returns successfully, as well as expected solution.
        """
        sol_iv = {
            't': 1.0,
            'y': [4.859e-01, 2.134e-01]
        }
        sol_sc = {
            't': 1.0,
            'y': [2.134e-01, 6.720e-02, 6.321e-01]
        }
        for i in ["intravenous", "subcutaneous"]:
            with self.subTest(i=i):
                model = pk.Model(self.dose_dummy, delivery = i)
                sol = model.solve()
                if(i=="intravenous"):
                    self.assertAlmostEqual(sol.y[0,-1], sol_iv["y"][0], delta=0.01)
                    self.assertAlmostEqual(sol.y[1,-1], sol_iv["y"][1], delta=0.01)
                if(i=="subcutaneous"):
                    self.assertAlmostEqual(sol.y[0,-1], sol_sc["y"][0], delta=0.01)
                    self.assertAlmostEqual(sol.y[1,-1], sol_sc["y"][1], delta=0.01)
                    self.assertAlmostEqual(sol.y[2,-1], sol_sc["y"][2], delta=0.01)
                self.assertTrue(sol.success)
        #self.assertEqual(model)

if __name__ == '__main__':
    unittest.main()