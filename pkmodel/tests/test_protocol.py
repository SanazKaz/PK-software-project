import unittest
import pkmodel as pk
import pytest


class ProtocolTest(unittest.TestCase):
    """
    Tests the :class:`Protocol` class.
    """
    def test_create(self):
        """
        Tests Protocol creation.
        """
        protocol = pk.Protocol('intravenous', [(2, 4), (3, 1)], (0, 5), 4)
        self.assertEqual(protocol.type_dosing, 'intravenous')
        self.assertEqual(protocol.instantaneous_application, [(2, 4), (3, 1)])
        self.assertEqual(protocol.steady_application, (0, 5))
        self.assertEqual(protocol.steady_dose, 4)
        self.assertEqual(protocol.current, 0)


    def test_next_application(self):
        """
        Test next application works for a protocol object with a instantaneous_application list of lengh 2
        
        """
        protocol = pk.Protocol('intravenous', [(2, 4), (3, 1)], (0, 5), 4)
        first_application_time_dose = protocol.next_application()
        self.assertEqual(first_application_time_dose, (2, 4))
        self.assertEqual(self.current, 1)
        second_application_time_dose = protocol.next_application()
        self.assertEqual(second_application_time_dose, (3, 1))
        self.assertEqual(self.current, 2)
        third_application_time_dose = protocol.next_application()
        self.assertEqual(third_application_time_dose, (None, None))
        self.assertEqual(self.current, 2)





    def test_dose_function(self):
        """
        Test dose_function return the steady_dose when t is inside the time interval (t0, t1), 
        and returns 0 if t is not in the interval (t0, t1)

        """
        protocol = pk.Protocol('intravenous', [(2, 4), (3, 1)], (0, 5), 4)

        self.assertEqual(protocol.dose_function(2), 4)
        self.assertEqual(protocol.dose_function(-1), 0)
        self.assertEqual(protocol.dose_function(7), 0)

