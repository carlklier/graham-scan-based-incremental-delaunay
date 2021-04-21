import unittest
from point import *
from polygon import Polygon
from grahamscandelaunay import *
import random
from unittest.mock import MagicMock, patch

class TestGrahamScanDelaunay(unittest.TestCase):
    def setUp(self):
        self.p1 = Point(0, 0)
        self.p2 = Point(2, 4)

        self.p3 = Point(1, 1)
        self.p4 = Point(2, 2)

    def test_get_slope(self):
        # global variable _p1 set to Point(0,0) in grahamscandelaunay.py

        # 0/0 should throw runtime warning or FloatingPointException and return float(inf)
        self.assertEqual(get_slope(self.p1), float('inf'))
        self.assertEqual(get_slope(self.p2), 2)

    def test_sort_points(self):
        
        #sorts by x value then y value to get lowest left most point
        # global variable _p1 is set to that min point and then points are sorted by slope from _p1

        # p1 = (0,0), p3 = (1,1)
        sorted_points = sort_points([self.p1, self.p3])
        self.assertEqual(sorted_points, [self.p1, self.p3])

        # (0,0), (2,2) ,(1,1) 
        sorted_points = sort_points([self.p1, self.p4, self.p3])
        self.assertEqual(sorted_points, [self.p1, self.p3, self.p4])

        # (2,2) ,(1,1)  (0,0), 
        sorted_points = sort_points([self.p4, self.p3, self.p1])
        self.assertEqual(sorted_points, [self.p1, self.p3, self.p4])

        # make a ccw polygon
        p1 = Point(1,1)
        p2 = Point(3,0)
        p3 = Point(5,1)
        p4 = Point(6,3)
        p5 = Point(5,5)
        p6 = Point(3,6)
        p7 = Point(1,5)

        sorted_points = sort_points([p7, p6, p5, p4, p3, p2, p1])
        self.assertEqual(sorted_points, [p1, p2, p3, p4, p5, p6, p7])

    def test_HalfEdge_init(self):

        p1 = Point(0,0)
        p2 = Point(0,1)
        p3 = Point(1, 0)
        h1 = HalfEdge(p1)
        self.assertTrue(h1.point == p1)
        self.assertTrue(h1.link == None)
        self.assertTrue(h1.prev == None)
        self.assertTrue(h1.twin == None)

        h2 = HalfEdge(p2)
        h1.link = h2
        h2.prev = h1

        self.assertTrue(h2.prev == h1)
        self.assertTrue(h1.link == h2)

        h3 = HalfEdge(p3)
        h3.prev = h2
        h3.link = h1

        h3twin = HalfEdge(p3, twin=h3)
        self.assertTrue(h3twin.twin == h3)

    def test_GrahamScanDelaunay_init(self):
        p1 = Point(0,1)
        p2 = Point(1,1)
        p3 = Point(1, 0)
        p4 = Point(0,0)
        V = [p1, p2, p3, p4]
        gsd = GrahamScanDelaunay(V)

        self.assertEqual(gsd.V, [p4, p3, p2, p1])

        h1 = HalfEdge(p4)
        h2 = HalfEdge(p3)
        h3 = HalfEdge(p2)

        h1.prev = h3
        h1.link = h2
        h2.prev = h1
        h2.link = h3
        h3.prev = h2
        h3.link = h1

        self.assertEqual(gsd._handle[p4].point, h1.point)
        self.assertEqual(gsd._handle[p2].point, h3.point)
        self.assertEqual(gsd._handle[p3].point, h2.point)

    # This test needs to be re-worked once I understand how add edge is suppossed to work
    def test_addedge(self):
        p1 = Point(0,1)
        p2 = Point(1,1)
        p3 = Point(1,0)
        p4 = Point(0,0)

        V = [p1, p2, p3, p4]

        h1 = HalfEdge(p1)
        h2 = HalfEdge(p2)
        h3 = HalfEdge(p3)
        h4 = HalfEdge(p4)

        h1.prev = h4
        h1.link = h2
        h2.prev = h1
        h2.link = h3
        h3.prev = h2
        h3.link = h4
        h4.prev = h3
        h4.link = h1

        h5 = HalfEdge(p2, twin=h1)
        h6 = HalfEdge(p3, twin=h2)
        h7 = HalfEdge(p4, twin=h3)
        h8 = HalfEdge(p1, twin=h4)

        h5.prev = h6
        h5.link = h8
        h6.prev = h7
        h6.link = h5
        h7.prev = h8
        h7.link = h6
        h8.prev = h5
        h8.link = h7

        h1.twin = h5
        h2.twin = h6
        h3.twin = h7
        h4.twin = h8

        # add an edge across the diagonal from h1.point to h3.point
        gsd = GrahamScanDelaunay(V)
        #gsd.incrementhull = MagicMock(return_value=None)
        #gsd.isdelaunay = MagicMock(return_value=None)
        c = gsd.addedge(h1, h3)

        self.assertTrue(h1.link == h2)
        self.assertTrue(h1.prev == c.twin)
        self.assertTrue(h1.twin == h5)

        self.assertTrue(h2.link == c.twin)
        self.assertTrue(h2.prev == h1)
        self.assertTrue(h2.twin == h6)

        self.assertTrue(h3.link == h4)
        self.assertTrue(h3.prev == c)
        self.assertTrue(h3.twin == h7)

        self.assertTrue(h4.link == c)
        self.assertTrue(h4.prev == h3)
        self.assertTrue(h4.twin == h8)

        self.assertTrue(h5.link == c)
        self.assertTrue(h5.prev == h6)
        self.assertTrue(h5.twin == h1)

        self.assertTrue(h6.link == h5)
        self.assertTrue(h6.prev == c)
        self.assertTrue(h6.twin == h2)

        self.assertTrue(h7.link == c.twin)
        self.assertTrue(h7.prev == h8)
        self.assertTrue(h7.twin == h3)

        self.assertTrue(h8.link == h7)
        self.assertTrue(h8.prev == c.twin)
        self.assertTrue(h8.twin == h4)

        self.assertTrue(c.link == )
        self.assertTrue(h2.prev == h1)
        self.assertTrue(h2.twin == h6)

        self.assertTrue(h4.link == c)
        self.assertTrue(c.link == h3)
        self.assertTrue(c.twin == h2.link)
        self.assertTrue(h2.link == c.twin)

        self.assertTrue(len(gsd.q) == 1)

    #@patch('grahamscandelaunay.GrahamScanDelaunay')
    def test_addleaf(self):
        p1 = Point(0,1)
        p2 = Point(1,1)
        p3 = Point(1, 0)
        p4 = Point(0,0)

        V = [p1, p2, p3, p4]

        h1 = HalfEdge(p1)
        h2 = HalfEdge(p2)
        h3 = HalfEdge(p3)
        h4 = HalfEdge(p4)

        h1.prev = h4
        h1.link = h2
        h2.prev = h1
        h2.link = h3
        h3.prev = h2
        h3.link = h4
        h4.prev = h3
        h4.link = h1

        h5 = HalfEdge(p2, twin=h1)
        h6 = HalfEdge(p3, twin=h2)
        h7 = HalfEdge(p4, twin=h3)
        h8 = HalfEdge(p1, twin=h4)

        h5.prev = h6
        h5.link = h8
        h6.prev = h7
        h6.link = h5
        h7.prev = h8
        h7.link = h6
        h8.prev = h5
        h8.link = h7

        h1.twin = h5
        h2.twin = h6
        h3.twin = h7
        h4.twin = h8

        # add a leaf edge from top right point to a point further to the right
        p = Point(2,1)
        gsd = GrahamScanDelaunay(V)
        gsd.incrementhull = MagicMock(return_value=None)
        gsd.isdelaunay = MagicMock(return_value=None)
        h = gsd.addleaf(h2, p)

        self.assertTrue(h1.link == h.twin)
        self.assertTrue(h.link == h2)
        self.assertTrue(h2.prev == h)
        self.assertTrue(h.twin == h.prev)
        self.assertTrue(h.twin.link == h)

    # This test needs to be re-worked once I understand how add edge is suppossed to work
    def test_flipedge(self):
        p1 = Point(0,1)
        p2 = Point(1,1)
        p3 = Point(1, 0)
        p4 = Point(0,0)

        V = [p1, p2, p3, p4]

        h1 = HalfEdge(p1)
        h2 = HalfEdge(p2)
        h3 = HalfEdge(p3)
        h4 = HalfEdge(p4)

        h1.prev = h4
        h1.link = h2
        h2.prev = h1
        h2.link = h3
        h3.prev = h2
        h3.link = h4
        h4.prev = h3
        h4.link = h1

        h5 = HalfEdge(p2, twin=h1)
        h6 = HalfEdge(p3, twin=h2)
        h7 = HalfEdge(p4, twin=h3)
        h8 = HalfEdge(p1, twin=h4)

        h5.prev = h6
        h5.link = h8
        h6.prev = h7
        h6.link = h5
        h7.prev = h8
        h7.link = h6
        h8.prev = h5
        h8.link = h7

        h1.twin = h5
        h2.twin = h6
        h3.twin = h7
        h4.twin = h8

        gsd = GrahamScanDelaunay(V)
        gsd.incrementhull = MagicMock(return_value=None)
        gsd.isdelaunay = MagicMock(return_value=None)

        h = gsd.addedge(h4, h2)

        self.assertTrue(h1.link == h2)
        self.assertTrue(h1.prev == h4)
        self.assertTrue(h1.twin == h5)

        self.assertTrue(h2.link == h3)
        self.assertTrue(h2.prev == h1)
        self.assertTrue(h2.twin == h6)

        self.assertTrue(h3.link == h4)
        self.assertTrue(h3.prev == h2)
        self.assertTrue(h3.twin == h7)

        self.assertTrue(h4.link == h1)
        self.assertTrue(h4.prev == h3)
        self.assertTrue(h4.twin == h8)

        self.assertTrue(h5.link == h8)
        self.assertTrue(h5.prev == h)
        self.assertTrue(h5.twin == h1)

        self.assertTrue(h6.link == h.twin)
        self.assertTrue(h6.prev == h7)
        self.assertTrue(h6.twin == h2)

        self.assertTrue(h7.link == h6)
        self.assertTrue(h7.prev == h.twin)
        self.assertTrue(h7.twin == h3)

        self.assertTrue(h8.link == h7)
        self.assertTrue(h8.prev == h5)
        self.assertTrue(h8.twin == h4)

        self.assertTrue(h.link == h5)
        self.assertTrue(h.prev == h8)
        self.assertTrue(h.twin == h7.prev)

        self.assertTrue(h.twin.link == h7)
        self.assertTrue(h.twin.prev == h6)
        self.assertTrue(h.twin.twin == h)

        gsd.flipedge(h)

        self.assertTrue(h1.link == h2)
        self.assertTrue(h1.prev == h4)
        self.assertTrue(h1.twin == h5)

        self.assertTrue(h2.link == h3)
        self.assertTrue(h2.prev == h1)
        self.assertTrue(h2.twin == h6)

        self.assertTrue(h3.link == h4)
        self.assertTrue(h3.prev == h2)
        self.assertTrue(h3.twin == h7)

        self.assertTrue(h4.link == h1)
        self.assertTrue(h4.prev == h3)
        self.assertTrue(h4.twin == h8)

        self.assertTrue(h5.link == h.twin)
        self.assertTrue(h5.prev == h6)
        self.assertTrue(h5.twin == h1)

        self.assertTrue(h6.link == h5)
        self.assertTrue(h6.prev == h.twin)
        self.assertTrue(h6.twin == h2)

        self.assertTrue(h7.link == h)
        self.assertTrue(h7.prev == h8)
        self.assertTrue(h7.twin == h3)

        self.assertTrue(h8.link == h7)
        self.assertTrue(h8.prev == h)
        self.assertTrue(h8.twin == h4)

        self.assertTrue(h.link == h8)
        self.assertTrue(h.prev == h7)
        self.assertTrue(h.twin == h6.link)

        self.assertTrue(h.twin.link == h6)
        self.assertTrue(h.twin.prev == h5)
        self.assertTrue(h.twin.twin == h)

        

if __name__ == '__main__':
    unittest.main()
