import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from typing import List
from matplotlib.axes import Axes
from matplotlib.text import Text

# State
OCCUPIED = 0
ASSIGNED = 1
NOT_ASSIGNED = 2
# Root
ROOT = 0
LEAF = 1

MAX_SAME_DIST = 0.02

agent_color = 'red'
structure_color = 'green'
sensing_color = 'blue'

def EuclideanDistance(p1: np.ndarray, p2: np.ndarray):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def EuclidDistance(p1: np.ndarray, p2: np.ndarray):
    return round(math.hypot(p1[0] - p2[0], p1[1] - p2[1]), 2)

def isSamePoint(p1: np.ndarray, p2: np.ndarray):
    if EuclidDistance(p1, p2) < MAX_SAME_DIST:
        return True
    return False

def calculatePathCost(path: np.ndarray):
    cost = 0.0
    if path.shape[0] == 1:
        return cost
    for i in range(path.shape[0] - 1):
        cost += EuclidDistance(path[i], path[i+1])
    
    return round(cost, 2)

def ManhattanDistance(p1: np.ndarray, p2: np.ndarray):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) 

def normalizeAngle(angle: float):
    return round(math.atan2(math.sin(angle), math.cos(angle)), 2)

def angleByTwoPoint(p1: np.ndarray, p2: np.ndarray):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def calculateDifferenceOrientation(angle1: float, angle2: float):
    angle1 = normalizeAngle(angle1)
    angle2 = normalizeAngle(angle2)
    
    if 0 <= angle1 <= math.pi and 0 <= angle2 <= math.pi:
        return angle2 - angle1
    elif -math.pi < angle1 < 0 and -math.pi < angle2 < 0:
        return angle2 - angle1
    elif 0 <= angle1 <= math.pi and -math.pi < angle2 < 0:
        turn = angle2 - angle1
        if turn < -math.pi:
            turn += 2 * math.pi
        return turn
    elif -math.pi < angle1 < 0 and 0 <= angle2 <= math.pi:
        turn = angle2 - angle1
        if turn > math.pi:
            turn -= 2 * math.pi
        return turn
    
    return angle2 - angle1

def are_points_collinear(point1: np.ndarray, point2: np.ndarray, point3: np.ndarray):
    # Calculate slopes
    slope1 = (point2[1] - point1[1]) * (point3[0] - point2[0])
    slope2 = (point3[1] - point2[1]) * (point2[0] - point1[0])
    
    # Check if slopes are equal (or close enough, considering floating-point arithmetic)
    return abs(slope1 - slope2) < 1e-10

def distanceBetweenPointAndLine(start_point: np.ndarray, end_point: np.ndarray, point: np.ndarray):
    px = end_point[0] - start_point[0]
    py = end_point[1] - start_point[1]

    norm = px*px + py*py
    if norm == 0.0: return EuclidDistance(start_point, point)

    u =  ((point[0] - start_point[0]) * px + (point[1] - start_point[1]) * py) / float(norm)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = start_point[0] + u * px
    y = start_point[1] + u * py

    dx = x - point[0]
    dy = y - point[1]

    dist = (dx*dx + dy*dy)**.5

    return dist

def pointIsBetweenALine(start: np.ndarray, end: np.ndarray, point: np.ndarray): 
    if isSamePoint(point, end): return True
    distance_to_start = EuclidDistance(point, start)
    distance_to_end = EuclidDistance(point, end)
    segment_length = EuclidDistance(start, end)
    
    return  segment_length - 0.01 <= distance_to_start + distance_to_end <= segment_length + 0.01 and distance_to_start > 0.01

def find_intersection_point(line1_start: np.ndarray, line1_end: np.ndarray, 
                            line2_start: np.ndarray, line2_end: np.ndarray):
    """
    Finds the intersection point of two lines defined by two points each.
    """
    x1, y1 = line1_start
    x2, y2 = line1_end
    x3, y3 = line2_start
    x4, y4 = line2_end

    # Calculate the intersection point
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
        return None  # Lines are parallel
    else:
        intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
        intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator
        return intersect_x, intersect_y

def check_line_segments_intersection_2d(line1_start: np.ndarray, line1_end: np.ndarray, 
                                        line2_start: np.ndarray, line2_end: np.ndarray):
    # http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    line1 = line1_end - line1_start
    line2 = line2_end - line2_start
    
    if isSamePoint(line1_end, line2_end) and isSamePoint(line1_start, line2_start) == False:
        return True, line1_end
    if isSamePoint(line1_end, line2_start) and isSamePoint(line1_start, line2_end) == False:
        return True, line1_end
    if isSamePoint(line1_start, line2_start) and isSamePoint(line1_end, line2_end) == False:
        return True, line1_start
    if isSamePoint(line1_start, line2_end) and isSamePoint(line1_end, line2_start) == False:
        return True, line1_start
    if are_points_collinear(line1_start, line1_end, line2_start) and  pointIsBetweenALine(line1_start, line1_end, line2_start):
        return True, line2_start
    if are_points_collinear(line1_start, line1_end, line2_end) and  pointIsBetweenALine(line1_start, line1_end, line2_end):
        return True, line2_end
    if are_points_collinear(line2_start, line2_end, line1_start) and  pointIsBetweenALine(line2_start, line2_end, line1_start):
        return True, line1_start
    if are_points_collinear(line2_start, line2_end, line1_end) and  pointIsBetweenALine(line2_start, line2_end, line1_end):
        return True, line1_end

    denom = line1[0] * line2[1] - line2[0] * line1[1]
    if denom == 0: 
        return False, np.zeros(2)  # Collinear
    denom_positive = denom > 0
    
    aux = line1_start - line2_start
    
    s_numer = line1[0] * aux[1] - line1[1] * aux[0]
    if (s_numer < 0) == denom_positive: 
        return False, np.zeros(2)  # No collision
    
    t_numer = line2[0] * aux[1] - line2[1] * aux[0]
    if (t_numer < 0) == denom_positive:  
        return False, np.zeros(2)  # No collision
    
    if ((s_numer > denom) == denom_positive) or ((t_numer > denom) == denom_positive): 
        return False, np.zeros(2)  # No collision
    
    # Otherwise collision detected
    t = t_numer / denom
    
    return True, line1_start + t * line1

def calculateRectangleCoordinate(center_x: float, center_y: float, angle: float, length: float, width: float):
    halfLength = length/2
    halfWidth = width/2
    sinAngle = math.sin(angle)
    cosAngle = math.cos(angle)
    agent_shape = []
    # Bottom left
    agent_shape.append([center_x + (cosAngle * -halfLength) - (sinAngle * halfWidth), 
                        center_y + (sinAngle * -halfLength) + (cosAngle * halfWidth)])
    # Top left corner
    agent_shape.append([center_x + (cosAngle * -halfLength) - (sinAngle * -halfWidth),
                        center_y + (sinAngle * -halfLength) + (cosAngle * -halfWidth)])
    # Top right 
    agent_shape.append([center_x + (cosAngle * halfLength) - (sinAngle * -halfWidth),
                        center_y + (sinAngle * halfLength) + (cosAngle * -halfWidth)])
    # Bottom right
    agent_shape.append([center_x + (cosAngle * halfLength) - (sinAngle * halfWidth), 
                        center_y + (sinAngle * halfLength) + (cosAngle * halfWidth)])
    # Bottom left
    agent_shape.append([center_x + (cosAngle * -halfLength) - (sinAngle * halfWidth), 
                        center_y + (sinAngle * -halfLength) + (cosAngle * halfWidth)])
    return agent_shape

def line_circle_intersection(start_point, end_point, circle_center, radius):
    # Calculate the direction vector of the line
    direction = np.array(end_point) - np.array(start_point)
    
    # Calculate the coefficients of the quadratic equation
    a = np.dot(direction, direction)
    b = 2 * np.dot(direction, np.array(start_point) - np.array(circle_center))
    c = np.dot(np.array(start_point) - np.array(circle_center), np.array(start_point) - np.array(circle_center)) - radius**2
    
    # Calculate the discriminant
    discriminant = b**2 - 4*a*c
    
    # Check if the line intersects the circle
    if discriminant < 0:
        return np.array(start_point)  # No intersection
    
    # Calculate the intersection point(s)
    t1 = (-b + np.sqrt(discriminant)) / (2*a)
    t2 = (-b - np.sqrt(discriminant)) / (2*a)
    
    intersection1 = np.array(start_point) + t1 * direction
    intersection2 = np.array(start_point) + t2 * direction
    if EuclidDistance(start_point, intersection1) > EuclidDistance(start_point, intersection2):
        return intersection2
    else:
        return intersection1