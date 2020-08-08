from __future__ import division 

import numpy as np


def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False

def lineIntersection(horizontal_seg, vertical_seg):
    horizontal_line = line(horizontal_seg[0], horizontal_seg[1])
    vertical_line = line(vertical_seg[0], vertical_seg[1])
    result = intersection(horizontal_line, vertical_line)
    if result:
        if min(horizontal_seg[0][0], horizontal_seg[1][0]) <= result[0] <= max(horizontal_seg[0][0], horizontal_seg[1][0]) \
        and min(vertical_seg[0][0], vertical_seg[1][0]) <= result[0] <= max(vertical_seg[0][0], vertical_seg[1][0]) \
        and min(horizontal_seg[0][1], horizontal_seg[1][1]) <= result[1] <= max(horizontal_seg[0][1], horizontal_seg[1][1]) \
        and min(vertical_seg[0][1], vertical_seg[1][1]) <= result[1] <= max(vertical_seg[0][1], vertical_seg[1][1]):
            return result
        else:
            return False
    return result
    