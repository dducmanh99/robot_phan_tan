import numpy as np
import matplotlib.pyplot as plt
import math
from typing import List
WALL_POWER = -100

def EuclideanDistance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def bresenham_line(x0, y0, x1, y1):
    """
    Calculates cells in a segment using Bresenham's Line Algorithm.

    Args:
        x0: X-coordinate of the first point.
        y0: Y-coordinate of the first point.
        x1: X-coordinate of the second point.
        y1: Y-coordinate of the second point.

    Returns:
        List of cells (tuples of x, y coordinates) in the segment.
    """
    sx = 1 if x1 >= x0 else -1
    sy = 1 if y1 >= y0 else -1
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    err = dx - dy

    cells = []
    while True:
        cells.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return cells

def bresenham(start, end):
    """
    Bresenham's Line Generation Algorithm
    https://www.youtube.com/watch?v=76gp2IAazV4
    """
    # step 1 get end-points of line 
    (x0, y0) = start
    (x1, y1) = end

    # step 2 calculate difference
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    m = dy/(dx + 0.000001)
    
    # step 3 perform test to check if pk < 0
    flag = True
    
    line_pixel = []
    line_pixel.append((x0,y0))
    
    step = 1
    if x0>x1 or y0>y1:
        step = -1

    mm = False   
    if m < 1:
        x0, x1 ,y0 ,y1 = y0, y1, x0, x1
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        mm = True
        
    p0 = 2*dx - dy
    x = x0
    y = y0
    
    for i in range(abs(y1-y0)):
        if flag:
            x_previous = x0
            p_previous = p0
            p = p0
            flag = False
        else:
            x_previous = x
            p_previous = p
            
        if p >= 0:
            x = x + step

        p = p_previous + 2*dx -2*dy*(abs(x-x_previous))
        y = y + 1
        
        if mm:
            line_pixel.append((y,x))
        else:
            line_pixel.append((x,y))
            
    line_pixel = np.array(line_pixel)
    
    return line_pixel