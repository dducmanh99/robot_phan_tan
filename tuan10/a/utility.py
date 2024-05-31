import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from typing import List, Set
from matplotlib.axes import Axes
from matplotlib.text import Text
from collections import deque
import random
import string
# Define constants
INF = float('inf')
# State of agents
OCCUPIED = 0
ASSIGNED = 1
NOT_ASSIGNED = 2


def EuclideanDistance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def normalizeAngle(angle: float):
    return math.atan2(math.sin(angle), math.cos(angle))

def calculateVirtualPoint(leader_pose: np.ndarray, wing_dist: float, wing_heading: float, num_robot: int):
    alpha = math.radians(wing_heading)
    num_follow = int(num_robot/2)
    left_pose = []
    right_pose = []
    for i in range(num_follow):
        angle = normalizeAngle(leader_pose[2] + alpha/2 + math.pi)
        x = leader_pose[0] + wing_dist*(num_follow - i) * math.cos(angle)
        y = leader_pose[1] + wing_dist*(num_follow - i) * math.sin(angle)
        left_pose.append([x, y, leader_pose[2]])
        angle = normalizeAngle(leader_pose[2] - alpha/2 + math.pi)
        x = leader_pose[0] + wing_dist*(num_follow - i) * math.cos(angle)
        y = leader_pose[1] + wing_dist*(num_follow - i) * math.sin(angle)
        right_pose.append([x, y, leader_pose[2]])
    
    return np.array(left_pose)[::-1], np.array(right_pose)[::-1]