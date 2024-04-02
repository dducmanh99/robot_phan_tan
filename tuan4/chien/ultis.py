import math
import numpy as np  
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

def sumOfTwoVectors(vector1, vector2):
    Ax = vector1[0] * math.cos(vector1[1])
    Ay = vector1[0] * math.sin(vector1[1])
    Bx = vector2[0] * math.cos(vector2[1])
    By = vector2[0] * math.sin(vector2[1])

    Cx = Ax + Bx
    Cy = Ay + By

    magnitude = math.hypot(Cx, Cy)
    angle = math.atan2(Cy, Cx)

    return np.array([magnitude, angle])

def computeDistance(position1, position2):
    distance = math.hypot(position1[0] - position2[0], position1[1] - position2[1])
    return distance