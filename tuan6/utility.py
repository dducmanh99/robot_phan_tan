import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from typing import List
import math 
import numpy as np 

def computeDistance(position0, position1, offset):
    distance = math.hypot(position0[0] - position1[0] - offset, position0[1] - position1[1] - offset)
    return distance

def computeAngle(position0, position1): #goal, robot
    angle = math.atan2(position0[1]-position1[1], position0[0]-position1[0])
    return angle

def sumOfListVectors(vectors):
    Vx = 0.0
    Vy = 0.0
    # Compute x, y parts of vectors
    for i in range(len(vectors)):
        Vx += vectors[i][0] * math.cos(vectors[i][1])
        Vy += vectors[i][0] * math.sin(vectors[i][1])
    # Compute magnitude and angle of sum vector
    magnitude = math.sqrt(Vx ** 2 + Vy ** 2)
    angle = math.atan2(Vy, Vx + 0.0000000001)

    return np.array((magnitude, angle))