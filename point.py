from numpy import array, append, cross
from numpy.linalg import det, solve

def point(*coords, z = 1):
    return append(coords, z)

def dist(p,q):
    return (sum((p.array()-q.array())**2))**0.5

def orient(*points):
    points = [p.array() for p in points]
    d = det(array(points))
    if d > 0:
        return 1
    elif d < 0:
        return -1
    else:
        return 0

def intersection(a,b,c,d):
    ab = cross(a.array(),b.array())
    cd = cross(c.array(),d.array())
    A = array([ab, cd, [0,0,1]])
    x, y, _ = solve(A, [0,0,1])
    return Point(x, y)


def crosscount(a,b,c,d):
    abc = orient(a,b,c)
    abd = orient(a,b,d)
    cda = orient(c,d,a)
    cdb = orient(c,d,b)
    return (abc - abd) * (abs(cda - cdb)) / 4

'''
def presort(points):
#bubble sort based Graham-Scan points sort. Using cos value
	p_0=points[0]
	for p in points:
		if p[0]<p_0[0]:
			p_0=p
	rank=[]
	cos_list=[]
	norm_list=[]
	for i in range(len(points)):
		p=points[i]
		rank.append(i)
		q=p.copy()
		q[0]=p_0[0]
		norm_value=dist(p_0,p)
		norm_list.append(norm_value)
		if norm_value==0:
			cos_list.append(1)
		else:
			cos_value=dist(q,p_0)/norm_value
			if orient(p_0,q,p) == -1:
				cos_value = cos_value*-1
			cos_list.append(cos_value)
			
		
	for i in range(len(points)):
		for j in range(i+1,len(points)):
			if cos_list[j]>cos_list[j-1] or (cos_list[j]==cos_list[j-1] and norm_list[j] > norm_list[j-1]):
				swap(cos_list[j],cos_list[j-1])
				swap(rank[j],rank[j-1])
				swap(norm_list[j],norm_list[j-1])
	sorted=[]
	for i in rank:
		sorted.append(points[i])
	return sorted
'''

class Point:
    def __init__(self, *coordinates, z = 1):
        self._p = append(coordinates, z)

    def __sub__(self, other):
        return Point(self._p[:2] - other._p[:2], z = 0)

    def __iter__(self):
        return iter(self._p)

    def array(self):
        return self._p

    def __eq__(self, other):
        return all(self._p == other._p)

    def __lt__(self, other):
        if (self._p[0] != other._p[0]):
            return self._p[0] < other._p[0]
        else:
            return self._p[1] < other._p[1]

    def __hash__(self):
        return hash(tuple(self._p))

    def __str__(self):
        return str(self._p[:2])

    def __getitem__(self, index):
        return self._p[index]



