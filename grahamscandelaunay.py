from point import *
from polygon import *
from collections import deque

class HalfEdge:
    def __init__(self, point, link = None, prev = None, twin = None):
        self.point = point
        self.link = link
        self.prev = prev
        self.twin = twin

class GrahamScanDelaunay:
    def __init__(self, V):
        # Sort the points and construct base convex hull
        n = len(V)
        V = sortbyx(V)
        V = sortbyslope(V)
        P = Polygon({V[0], V[1], V[2]})

        # Initializing Data Structures
        stack = deque() # Graham Scan Point Stack
        q = deque() # Delaunay Edge Queue

        # Convert convex hull into half-edges
        self._handle = {}
        inside = [HalfEdge(p) for p in P]
        outside = [HalfEdge(p) for p in P]
        for i in range(3):
            self._handle[P[i]] = inside[i]
            inside[i - 1].twin = outside[i]
            outside[i].twin = inside[i - 1]

            inside[i - 1].link = inside[i]
            inside[i].prev = inside[i - 1]

            outside[i].link = outside[i - 1]
            outside[i-1].prev = outside[i]
            stack.append(outside[i])

        

        # Incrementally add to the triangulation
        for i in range(3, n):
            self.convexhull(V[i])
            while len(q) != 0:
                self.isdelaunay(q.popleft())

    def points(self):
        return iter(self._handle)

    def addedge_halfedges(self, a, b):
        """
        Add an edge that goes from `a.point` to `b.point`.
        It is assumed that `a` and `b` are on the face that
        will contain the new edge.

        Note: we did this one in class.
        """
        c = HalfEdge(a.point, b, a.prev)
        d = HalfEdge(b.point, a, b.prev, c)
        c.twin = d
        a.prev.link = c
        b.prev.link = d
        a.prev = d
        b.prev = c

    def addedge(self, a, b):
        pass

    def addleaf(self, a, p):
        pass
    
    # Use the convex hull algorithm to add edges to the triangulation
    def convexhull(self, p):
        # Push any new edges into the Delaunay Edge Queue
        pass
    
    # check if edge is locally delaunay
    def isdelaunay(self, h):
        # if not locally delaunay, flip the edge
        pass

    # Flip the current edge
    def flipedge(self, h):
        # flip the edge and push neighbor edges into the Delaunay Edge Queue
        pass

# Sort the points by their x-coordinates
def sortbyx(P):
    return []

# Sort the points by their slope relative to the first entry
def sortbyslope(P):
    return []