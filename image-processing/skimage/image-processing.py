from skimage import io, color
from scipy.fftpack import dct, idct
import numpy as np
import intersection
 
img = io.imread('../images/receipt_00065.png')
gray = color.rgb2gray(img)
 
frequencies = dct(dct(gray, axis=0), axis=1)
frequencies[:2,:2] = 0
gray = idct(idct(frequencies, axis=1), axis=0)
 
gray = (gray - gray.min()) / (gray.max() - gray.min()) # renormalize to range [0:1]

from skimage import filters, morphology, measure
from scipy.ndimage.morphology import binary_fill_holes
 
mask = filters.gaussian(gray, 2) > 0.6
mask = morphology.binary_closing(mask, selem=morphology.disk(2, bool))
mask = binary_fill_holes(mask, structure=morphology.disk(3, bool))
mask = measure.label(mask)
mask = (mask == 1 + np.argmax([r.filled_area for r in measure.regionprops(mask)]))

io.imsave('../images/processed_image.png', mask)

from skimage import transform
 
edges = mask ^ morphology.binary_erosion(mask, selem=morphology.disk(2, bool))
segments = np.array(transform.probabilistic_hough_line(edges))
angles = np.array([np.abs(np.arctan2(a[1]-b[1], a[0]-b[0]) - np.pi/2) for a,b in segments])
verticalSegments = segments[angles < np.pi/4] 
horizontalSegments = segments[angles >= np.pi/4]

from sklearn import cluster
intersections = [intersection.lineIntersection(vs, hs) for vs in verticalSegments for hs in horizontalSegments]
# print(intersections)
bw = cluster.estimate_bandwidth(intersections, 0.1)
corners = cluster.MeanShift(bandwidth=bw).fit(intersections).cluster_centers_

from scipy.spatial import distance

d = distance.pdist(coordinates)
w = int(max(d[0], d[5])) # = max(dist(p1, p2), dist(p3, p4))
h = int(max(d[2], d[3])) # = max(dist(p1, p4), dist(p2, p3))

tr = transform.ProjectiveTransform()
tr.estimate(array([[0,0], [w,0], [w,h], [0,h]]), coords)
receipt = transform.warp(img, tr, output_shape=(h, w), order=1, mode="reflect")
