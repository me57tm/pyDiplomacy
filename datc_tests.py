#Hello to anyone reading this, This file is no longer required as I'm outsourcing adjudication to backstabbr so this project doesn't take 10 trillion years

import unittest
from pyDiplomacy import *


class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

#6.A
class BasicChecks(unittest.TestCase):
    england = Player("England",False)
    england.orders = Order(unit=UnitLocation(utype="a",location:""))
    def not_neighbour(self):
        

if __name__ == '__main__':
    england = Player("England",False)
    
