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
        # Assume General Position: No 3 points in V are collinear
        # Sort the points and construct base convex hull
        n = len(V)
        self.V = sort_points(V)
        P = Polygon([self.V[0], self.V[1], self.V[2]])

        # Initializing Data Structures
        self.stack = deque() # Convex Hull Half Edge Stack
        self.q = deque() # Delaunay Half Edge Queue

        # Convert triangle into half-edges
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
            outside[i - 1].prev = outside[i]
            self.stack.append(outside[i])

        # Incrementally add to the triangulation
        for i in range(3, n):
            self.incrementhull(V[i])
            while len(self.q) > 0:
                self.isdelaunay(self.q.popleft())

    def points(self):
        return iter(self._handle)

    # Connects an edge from a.point to b.point
    # Assumes a and b are the outside halfedges
    # During the convex hull process
    def addedge(self, a, b):
        c = HalfEdge(a.point, b, a.prev)
        d = HalfEdge(b.point, a, b.prev, c)
        c.twin = d
        a.prev.link = c
        b.prev.link = d
        a.prev = d
        b.prev = c
        # Push new edge into the Delaunay Edge Queue
        self.q.append(c)

    # Connects an edge from a.point to p
    # a is the outside halfedge and p is a point
    # Only used for the convex hull
    def addleaf(self, a, p):
        h = HalfEdge(p, a)
        t = HalfEdge(a.point, h, a.prev, h)
        h.prev = t
        h.twin = t
        a.prev.link = t
        a.prev = h
        # Push new edge into the Delaunay Edge Queue
        self.q.append(h)
    
    # Use the convex hull algorithm to add edges to the triangulation
    def incrementhull(self, p):
        # Connect the top point of the stack to the new point
        self.addleaf(self.stack[-1], p)
        h = self.q[-1] # Halfedge from p
        # Run graham scan to see if backtracking is needed
        while (orient(self.stack[-2].point, self.stack[-1].point, p) != 1):
            self.stack.pop()
            self.addedge(self.stack[-1], h)
        # Connect the new point to the first point
        self.addedge(h, self.stack[0])
        
    
    # check if edge is locally delaunay
    def isdelaunay(self, h):
        # if not locally delaunay, flip the edge
        pass

    # Flip the current edge
    def flipedge(self, h):
        # flip the edge and push neighbor edges into the Delaunay Edge Queue
        pass

_p1 = Point(0, 0)

# Sort the points such that the first point of the list
# is the bottomleftmost, and the remaining points
# are sorted in ascending order of their slope
# with respect to the first point
def sort_points(V):
    n = len(V)
    # Sort by x-coordinates to get the first point
    _V = sorted(V)
    _p1 = _V[1]
    
    # Sort remaining points by slope
    _V[1:n] = sorted(_V, key=get_slope)

    return _V

# Key function to help sort by slope
def get_slope(p):
    try:
        return (_p1[1]-p[1]) / (_p1[0]-p[0])
    except ZeroDivisionError:
        return float('inf')