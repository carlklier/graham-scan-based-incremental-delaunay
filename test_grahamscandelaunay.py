import unittest
from point import *
from polygon import Polygon
from grahamscandelaunay import *
import random

class TestGrahamScanDelaunay(unittest.TestCase):

    def testsortpoints(self):
        print("Unsorted")
        V = [Point(x,y) for x,y in [(1,1),(3,0),(5,1),(6,3),(5,5),(3,6),(1,5)]]
        random.shuffle(V)
        for p in V:
            print(p.array())
        print("Sorted")
        V = sort_points(V)
        for p in V:
            print(p.array())




if __name__ == '__main__':
    unittest.main()
