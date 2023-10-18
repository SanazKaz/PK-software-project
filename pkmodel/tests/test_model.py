import unittest
import pkmodel as pk


class ModelTest(unittest.TestCase):
    """
    Tests the :class:`Model` class.
    """
    def dose_dummy(self, t):
        return 1.0

    def test_create(self):
        """
        Tests Model creation.
        """
        model = pk.Model(self.dose_dummy)
        self.assertEqual(model.parameters["CL"], 1.0)
        #self.assertEqual(model)

    def test_model_defaults(self):
        """
        Tests Model defaults run and the solver returns successfully.
        """
        for i in ["intravenous", "subcutaneous"]:
            with self.subTest(i=i):
                model = pk.Model(self.dose_dummy, delivery = i)
                sol = model.solve()
                self.assertTrue(sol.success)
        #self.assertEqual(model)

if __name__ == '__main__':
    unittest.main()