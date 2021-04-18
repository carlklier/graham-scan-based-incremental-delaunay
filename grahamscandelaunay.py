from point import *
from polygon import *
from collections import deque
import numpy
numpy.seterr(all='raise')

class HalfEdge:
    def __init__(self, point, link = None, prev = None, twin = None):
        self.point = point
        self.link = link
        self.prev = prev
        self.twin = twin

class GrahamScanDelaunay:
    def __init__(self, V):
        # Assume General Position: No 3 points in V are collinear
        # and no 4 points in V are cocircular
        # Sort the points and construct base convex hull
        n = len(V)
        self.V = sort_points(V)
        P = Polygon([self.V[0], self.V[1], self.V[2]])

        # Initializing Data Structures
        self.stack = deque() # Convex Hull Half Edge Stack
        self.q = deque() # Delaunay Half Edge Queue

        # Convert triangle into half-edges
        self._handle = deque() # List of all halfedges
        outside = [HalfEdge(p) for p in P]
        inside = [HalfEdge(p) for p in P]
        for i in range(3):
            outside[i - 1].twin = inside[i]
            inside[i].twin = outside[i - 1]

            outside[i - 1].link = outside[i]
            outside[i].prev = outside[i - 1]

            inside[i].link = inside[i - 1]
            inside[i - 1].prev = inside[i]
            self.stack.append(outside[i])
            self._handle.append(outside[i])

    # Returns the current iteration, the sorted list of points, and the edges in the triangulation
    def run(self):
        n=len(self.V)
        yield self.points()
        # Incrementally add to the triangulation
        for i in range(3, n):
            self.incrementhull(self.V[i])
            yield self.points()
            while len(self.q) > 0:
                self.isdelaunay(self.q.popleft())
                yield self.points()

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
        self._handle.append(c)
        return c

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
        self._handle.append(t)
        return h
    
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
        # Add the convex hull outside halfedge to the stack
        self.q.append(h.link)
        self.q.append(self.stack.pop())
        self.stack.append(h.prev.twin.prev)
        self.stack.append(h.prev.twin)
        for h in self.stack:
            print(str(h.point) + str(h.link.point))
        return
        
    
    # check if edge is locally delaunay
    def isdelaunay(self, h):
        print("checking " + str(h.point) + str(h.link.point))
        # Outside edge, do not flip
        if h in self.stack or h.twin in self.stack:
            print("outside edge, do nothing")
            return
        # if not locally delaunay, flip the edge
        print("incircle on " + str(h.point) + str(h.prev.point) + str(h.link.point) + str(h.twin.prev.point))
        if incircle(h.point, h.prev.point, h.link.point, h.twin.prev.point) > 0:
            print("in circle passed")
            self.flipedge(h)
        print("after in circle")
        return

    # Flip the current edge
    def flipedge(self, h):
        print("flipping " + str(h.point) + str(h.link.point))
        # Link the quad toegether
        h.prev.link = h.twin.link
        h.twin.prev.link = h.link
        h.link.prev = h.twin.prev
        h.twin.link.prev = h.prev
        # Flip the edge
        h.link = h.prev
        h.twin.link = h.twin.prev
        h.prev = h.twin.link.prev
        h.twin.prev = h.link.prev
        # Link the quad back to the edge
        h.link.prev = h
        h.twin.link.prev = h.twin
        h.prev.link = h
        h.twin.prev.link = h.twin
        h.point = h.twin.link.point
        h.twin.point = h.link.point
        print("result " + str(h.point) + str(h.link.point))
        # Push the neighboring edges into the Delaunay Queue
        self.q.append(h.link)
        self.q.append(h.prev)
        self.q.append(h.twin.link)
        self.q.append(h.twin.prev)
        return

# Sort the points such that the first point of the list
# is the bottomleftmost, and the remaining points
# are sorted in ascending order of their slope
# with respect to the first point
def sort_points(V):
    n = len(V)
    # Sort by x-coordinates to get the first point
    _V = sorted(V)
    
    pairs = [(_V[0], float('-inf'))]
    for i in range(1,n):
        pairs.append((_V[i], slope(_V[0], _V[i])))
        print(slope(_V[0], _V[i]))

    pairs = pairs[0:1] + sorted(pairs[1:], key=lambda p: p[1]) # Sort by slope

    print("sorted")
    output = []
    for p in pairs:
        print(p[1])
        output.append(p[0])
    return output