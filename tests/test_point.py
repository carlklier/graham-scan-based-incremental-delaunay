import unittest
import numpy
from point import *

class TestPoint(unittest.TestCase):
    def setUp(self):
        self.p0 = Point()
        self.p1 = Point(2, 4)
        self.p2 = Point(2, 4)
        self.p3 = Point(1, 1)
        self.p4 = Point(1, 3, 2)

    def test_init(self):
        self.assertListEqual(list(self.p1.array()), [2, 4, 1])
    
    def test_init_no_points(self):
        self.assertListEqual(list(self.p0.array()), [1])
    
    def test_equals(self):
        self.assertTrue(self.p1 == self.p2)
        self.assertFalse(self.p1 == self.p3)
        self.assertFalse(self.p1 == self.p4)
        self.assertFalse(self.p0 == self.p4)

    def test_get_item(self):
        self.assertTrue(self.p1[0] == 2)

    def test_slope(self):
        p1 = Point(0,0)
        p2 = Point(2,4)
        p3 = Point(0,4)

        # 0/0 should throw runtime warning or FloatingPointException and return float(inf)
        self.assertEqual(slope(p1, p2), 2)
        self.assertEqual(slope(p2, p1), 2)

        self.assertEqual(slope(p1, p3), float("inf"))

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

    def test_in_circle3(self):
        p1 = Point(0,0)
        p2 = Point(1,0)
        p3 = Point(1,1)
        p4 = Point(0,1)

        self.assertEqual(incircle(p1, p2, p3, p4), 0)

    def test_dist(self):
        p1 = Point(0,0)
        p2 = Point(1,0)
        p3 = Point(0,5)

        self.assertEqual(dist(p1, p2), 1)
        self.assertEqual(dist(p1, p3), 5)
        self.assertEqual(dist(p3, p3), 0)

    def test_orient(self):
        p1 = Point(0,0)
        p2 = Point(1,0)
        p3 = Point(1,1)
        p4 = Point(0,1)


        self.assertEqual(orient(p1, p4, p3), -1)
        self.assertEqual(orient(p1, p2, p3), 1)
        self.assertEqual(orient(p1, p1, p1), 0)


if __name__ == '__main__':
    unittest.main()