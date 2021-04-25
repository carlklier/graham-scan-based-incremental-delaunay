import unittest
from grahamscandelaunay.point import *
from grahamscandelaunay.grahamscandelaunay import *
import random

class TestGrahamScanDelaunay(unittest.TestCase):

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
        h3 = HalfEdge(p3, h1, h2)
        self.assertTrue(h3.link == h1)
        self.assertTrue(h3.prev == h2)

        h3twin = HalfEdge(p3, twin=h3)
        self.assertTrue(h3twin.twin == h3)

    def test_GrahamScanDelaunay_init(self):
        # create a simple box
        p1 = Point(0,1)
        p2 = Point(1,1)
        p3 = Point(1, 0)
        p4 = Point(0,0)
        V = [p1, p2, p3, p4]
        gsd = GrahamScanDelaunay(V)

        # tests the _sort_points method
        self.assertEqual(gsd.V, [p4, p3, p2, p1])

        self.assertEqual(len(gsd.q), 0)
        self.assertEqual(len(gsd.stack), 0)
        self.assertEqual(len(gsd.edges), 0)

        # create a ccw polygon
        p1 = Point(1,1)
        p2 = Point(3,0)
        p3 = Point(5,1)
        p4 = Point(6,3)
        p5 = Point(5,5)
        p6 = Point(3,6)
        p7 = Point(1,5)

        V = [p7, p5, p4, p6, p3, p1, p2]
        gsd = GrahamScanDelaunay(V)
        # tests the _sort_points method
        self.assertEqual(gsd.V, [p1, p2, p3, p4, p5, p6, p7])

    def test_addedge(self):
        p1 = Point(0,1)
        p2 = Point(1,1)
        p3 = Point(1,0)
        p4 = Point(0,0)

        V = [p1, p2, p3, p4]
        gsd = GrahamScanDelaunay(V)

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

        c = gsd._addedge(h1, h3)

        self.assertTrue(h1.link == h2)
        self.assertTrue(h1.prev == c.twin)

        self.assertTrue(h2.link == c.twin)
        self.assertTrue(h2.prev == h1)

        self.assertTrue(h3.link == h4)
        self.assertTrue(h3.prev == c)

        self.assertTrue(h4.link == c)
        self.assertTrue(h4.prev == h3)

        self.assertTrue(c.link == h3)
        self.assertTrue(c.prev == h4)
        self.assertTrue(c.twin == h1.prev)

        self.assertTrue(c.twin.link == h1)
        self.assertTrue(c.twin.prev == h2)
        self.assertTrue(c.twin.twin == c)

        self.assertTrue(len(gsd.q) == 1)
        self.assertTrue(len(gsd.edges) == 1)

    def test_addleaf(self):
        p1 = Point(0,1)
        p2 = Point(1,1)
        p3 = Point(1,0)
        p4 = Point(0,0)

        V = [p1, p2, p3, p4]
        gsd = GrahamScanDelaunay(V)

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

        # add a leaf edge from top right point to a point further to the right
        p = Point(2,1)
        h = gsd._addleaf(h2, p)

        self.assertTrue(h1.link == h.twin)
        self.assertTrue(h2.prev == h)

        self.assertTrue(h.link == h2)
        self.assertTrue(h.prev == h.twin)
        self.assertTrue(h.twin == h.prev)
 
        self.assertTrue(h.twin.link == h)
        self.assertTrue(h.twin.prev == h1)
        self.assertTrue(h.twin.twin == h)

        self.assertTrue(len(gsd.edges) == 1)
        self.assertTrue(len(gsd.q) == 1)

    def test_flipedge(self):
        p1 = Point(0,1)
        p2 = Point(1,1)
        p3 = Point(1,0)
        p4 = Point(0,0)

        V = [p1, p2, p3, p4]
        gsd = GrahamScanDelaunay(V)

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

        h = gsd._addedge(h4, h2)
        gsd._flipedge(h)

        self.assertTrue(h1.link == h2)
        self.assertTrue(h1.prev == h.twin)

        self.assertTrue(h2.link == h.twin)
        self.assertTrue(h2.prev == h1)

        self.assertTrue(h3.link == h4)
        self.assertTrue(h3.prev == h)

        self.assertTrue(h4.link == h)
        self.assertTrue(h4.prev == h3)

        self.assertTrue(h.link == h3)
        self.assertTrue(h.prev == h4)
        self.assertTrue(h.twin == h2.link)

        self.assertTrue(h.twin.link == h1)
        self.assertTrue(h.twin.prev == h2)
        self.assertTrue(h.twin.twin == h)

        # _add_edge adds 1 halfedge to the queue and _flip_edge adds 4 more for a total of 5
        self.assertEqual(len(gsd.q), 5)

    def test_run(self):
        p1 = Point(0,1)
        p2 = Point(1,1)
        p3 = Point(1,0)
        p4 = Point(0,0)

        V = [p1, p2, p3, p4]
        gsd = GrahamScanDelaunay(V)
        step = gsd.run()
        state = next(step)

        # These also test the _get_vis_data(), _current_edge(), and _getedges() methods
        self.assertEqual(state[0], None)
        self.assertEqual(len(list(state[1])), 3)
        self.assertEqual(state[2], None)

        state = next(step)

        # also tests _incrementalhull() and _isdelaunay()
        self.assertEqual(state[0], p1)
        self.assertEqual(len(list(state[1])), 5)
        self.assertEqual(state[2], gsd.q[0])

        self.assertEqual(len(gsd.q), 4)
        for i in range(4):
            # we shouldn't need to flip any edges so q should just run out after 4 steps
            state = next(step)

        with self.assertRaises(StopIteration):
            next(step)

if __name__ == '__main__':
    unittest.main()
