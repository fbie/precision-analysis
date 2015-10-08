#!/usr/bin/env python

import sys
import math

import numpy as np

class Frame:
    def __init__(self, x, y, t, a):
        self._x = x
        self._y = y
        self._t = t
        self._a = a

    def x(self):
        return self._x

    def y(self):
        return self._y

    def tracking(self):
        return self._t and (self._x != 0 and self._y != 0)

    def target(self):
        return self._a

    def toCoords(self):
        return self._x, self._y

def _line_to_frame(l):
    es = l.split(";")
    c = es[-1][1:-2]
    x, y = c.split(',')
    return Frame(float(x), float(y), (es[-3] == 'true'), es[2])

def _files_to_clusters(files):
    clusters = []
    for file in files:
        frames = filter(Frame.tracking, map(_line_to_frame, [line for line in open(file)][1:]))
        last = None
        cluster = []
        for frame in frames:
            if last and last.target() != frame.target():
                clusters.append(cluster)
                cluster = []
            last = frame
            cluster.append(frame.toCoords())
        if cluster != []:
            clusters.append(cluster)
    return clusters

# Constants for screen size computation
screen_height_px = 1350.0
screen_width_px = 1550.0
#screen_diag_mm = 269.240
#screen_height_mm = screen_diag_mm * math.sqrt(screen_height_px ** 2 / (screen_width_px ** 2 + screen_height_px ** 2))
screen_height_mm = 135.0
#screen_width_mm = screen_width_px / screen_height_px * screen_height_mm
screen_width_mm = 155.0
mm_per_px = np.mean((screen_height_mm / screen_height_px, screen_width_mm / screen_width_px))

# Other constants
z_avg_mm = 336.0
d = 120.0
pi = 0.001
k = 5

# Convert pixels to millimeters
def _px_to_mm(px):
    return mm_per_px * px

def _visual_angle(a, b, z):
    return _visual_angle2(b - a, z)

def _visual_angle2(d, z):
    return 2 * math.atan(math.fabs(d) / 2 * z)

def _theta_rms(coords, z):
    return _theta_rms2([coords[i+1] - coords[i] for i in xrange(len(coords) - 1)], z)

def _theta_rms2(dists, z):
    if len(dists):
        return math.sqrt(np.mean([_visual_angle2(d, z) ** 2 for d in dists]))
    return float('nan')

def _accuracy(coords, z):
    n = len(coords) - 1
    if 0 < n:
        return np.mean([_visual_angle(coords[i], coords[i+1], z) for i in xrange(n)])
    return float('nan')

def _dist(xa, ya, xb, yb):
    return math.sqrt((xa - xb) ** 2 + (ya - yb) ** 2) ** 2

def _csv(files):
    n = 0
    aggregates = []
    for name, clusters in zip(files, [_files_to_clusters([f]) for f in files]):
        for cluster in clusters:
            aggregates.append([n,
                               name,
                               _theta_rms([_px_to_mm(x) for x, y in cluster], z_avg_mm),
                               _theta_rms([_px_to_mm(y) for x, y in cluster], z_avg_mm),
                               _accuracy([_px_to_mm(x) for x, y in cluster], z_avg_mm),
                               _accuracy([_px_to_mm(y) for x, y in cluster], z_avg_mm),
                               len(cluster)])
        n += 1
    print 'n;name;theta_RMS_x;theta_RMS_y;accuracy_x;accuracy_y;samples'
    for a in aggregates:
        print ';'.join(map(lambda x: x.replace('.', ','), map(str, a)))

def csv(files):
    _csv(files)

if __name__ == '__main__':
    files = sys.argv[1:]
    if not files:
        print >> sys.stderr, 'Empty file(s): %s' %', '.join(sys.argv[2:])
        exit(1)
    csv(files)
