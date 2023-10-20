import unittest
import pkmodel as pk


class SolutionTest(unittest.TestCase):
    """
    Tests the :class:`Solution` class.
    """
    def test_create(self):
        """
        Tests Solution creation.
        """
        t_sol = [0.,1.]
        y_sol = [[0.1, 0.2],[0.3,0.4]]
        delivery = "intravenous"
        solution = pk.Solution(t_sol, y_sol, delivery)
        self.assertEqual(solution.t_sol, t_sol)

    def test_plot(self):
        """
        Tests Solution creation.
        """
        t_sol = [0.,1.]
        y_sol = [[0.1, 0.2],[0.3,0.4]]
        delivery = "intravenous"
        solution = pk.Solution(t_sol, y_sol, delivery)
        solution.plot_data()

