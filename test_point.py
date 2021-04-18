import unittest
from point import *

class TestPoint(unittest.TestCase):

    def test_in_circle(self):
        p1 = Point(5,0)
        p2 = Point(8,5)
        p3 = Point(5,10)
        p4 = Point(2,5)
        p5 = Point(5,7)

        self.assertEqual(incircle(p1,p2,p3,p4), 1)
        self.assertEqual(incircle(p2,p1,p3,p4), 1)
        self.assertEqual(incircle(p3,p2,p1,p4), 1)
        self.assertEqual(incircle(p1,p3,p4,p2), 1)
        self.assertEqual(incircle(p2,p3,p4,p5), 1)
        self.assertEqual(incircle(p1,p2,p4,p3), -1)
        self.assertEqual(incircle(p2,p4,p5,p3), -1)
        self.assertEqual(incircle(p3,p4,p5,p2), -1)
        self.assertEqual(incircle(p2,p3,p5,p4), -1)

    def test_in_circle2(self):
        p1 = Point(800,500)
        p2 = Point(400,300)
        p3 = Point(300,200)
        p4 = Point(700,300)

        self.assertEqual(incircle(p1,p2,p3,p4), 1)


if __name__ == '__main__':
    unittest.main()