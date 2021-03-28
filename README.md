# graham-scan-based-incremental-delaunay

Graham Scan-Based Incremental Delaunay Triangulation:
- Sort the input points by x-coordinate
- Select the leftmost, bottommost point as the pivot point
- Sort the other points by angle relative to the pivot point their slopes relative to the pivot
- Construct the base convex hull using the pivot point and the first two points sorted by angle
- Incrementally add the next sorted point and use Graham Scan to get the convex hull, saving any edges that were made
- Flip the current triangulation to Delaunay and repeat until done
