#from point import point, orient, crosscount
from point import orient, crosscount

class Polygon:
    def __init__(self, points):
        """
        Create a polygon with the given `points`.
        Points may not be repeated.  If duplicate points appear, there is no
        guarantee that any of the other methods will work.
        """
        self.points = list(points)
        if len(set(str(p) for p in self.points)) != len(self.points):
            raise ValueError

    def __eq__(self, other):
        """
        Return `True` iff `self` and `other` are the same polygon with the same
        orientation.  The vertices must be in correspondence.

        The running time should be linear in the number of points.

        *Beware that cyclic shifts of the vertices of a polygon result in the
        same polygon.*
        """
        if len(self) != len(other):
            return False

        align = None
        for i, p in enumerate(other.points):
            if all(p == self[0]):
                align = i
        if align is None:
            return False
        return all(all(other[i + align] == p) for i,p in enumerate(self.points))

    def is_simple(self):
        """
        Return `True` iff the Polygon is simple, i.e., two edges can only
        intersect at a shared vertex.
        """
        n = len(self)
        for i in range(n):
            for j in range(i+2, n + i - 1):
                if crosscount(self[i], self[i+1], self[j], self[j+1]) != 0:
                    return False
        return True

    def equal_up_to_translation(self, other):
        """
        Return `True` iff `self` and `other` are the same polygon up to some
        translation.
        """
        sv = Polygon([self[i+1] - self[i] for i in range(len(self))])
        ov = Polygon([other[i+1] - other[i] for i in range(len(other))])
        return sv == ov

    def __getitem__(self, index):
        """
        Return the vertex number `index` in the polygon.
        This method supports a wraparound, so for an $n$-gon, we have vertex
        $n$ is also vertex $0$.  This makes it easier, for example, to
        iterate over edges.
        """
        n = len(self)
        return self.points[index % n]

    def __len__(self):
        """
        Return the number of vertices in the polygon.
        """
        return len(self.points)

    def is_convex(self):
        """
        Return `True` iff the polygon is convex.
        """
        n = len(self)
        sorted_left = all(orient(self[0], self[i], self[i+1]) >= 0 for i in range(1,n-1))
        sorted_right = all(orient(self[0], self[i], self[i+1]) <= 0 for i in range(1, n-1))
        all_left_turns = all(orient(self[i], self[i+1], self[i+2]) >= 0 for i in range(n))
        all_right_turns = all(orient(self[i], self[i+1], self[i+2]) <= 0 for i in range(n))

        return (sorted_left and all_left_turns) or (sorted_right and all_right_turns)

    def __contains__(self, p):
        """
        Return `True` iff `point` is contained in the polygon.
        This is only guaranteed to work if the polygon is simple.
        """
        n = len(self)
        v = point(19/7, 11/13, z = 0)
        crossings = sum(crosscount(p, v, self[i], self[i+1]) for i in range(n))
        return crossings % 2 == 1

    def __iter__(self):
        """
        Return an iterator over the vertices of the polygon.
        """
        return iter(self.points)
