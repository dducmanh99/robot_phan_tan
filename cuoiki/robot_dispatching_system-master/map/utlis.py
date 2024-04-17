import math
import numpy as np
DOUBLE_HORIZONTAL = 0
SINGLE_HORIZONTAL = 1
DOUBLE_VERTICAL = 2
SINGLE_VERTICAL = 3

LINE_POINT = 0
WORKING_POINT = 1
STORAGE_POINT = 2
WAITING_POINT = 3
CHARGING_POINT = 4

WORKING_ZONE = 0
STORAGE_ZONE = 1
WAITING_ZONE = 2
CHARGING_ZONE = 3

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
