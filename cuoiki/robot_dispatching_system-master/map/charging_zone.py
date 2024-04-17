import matplotlib.pyplot as plt
import numpy as np
import math
from utlis import *

class ChargingZone:
    def __init__(self, working_length: float, working_width: float, charging_length: float, charging_width: float,
                num_charging_point: int, additional_length: float, single_line_width: float, robot_length: float, 
                robot_width: float):
        self.working_length = working_length
        self.working_width = working_width
        self.charging_length = charging_length
        self.charging_width = charging_width
        self.robot_length = robot_length
        self.robot_width = robot_width
        self.num_charging_point = num_charging_point
        self.additional_length = additional_length
        self.single_line_width = single_line_width
        self.point_length = self.robot_length + self.additional_length
        self.calculateChargingZone()
        self.calculateChargingPoint()

    def updateChargingZone(self):
        self.calculateChargingZone()
        self.calculateChargingPoint()

    def calculateChargingZone(self):
        charging_centers = []
        charging_coords = []

        center_x = self.charging_length/2
        center_y = 0 - self.charging_width/2
        charging_centers.append([center_x, center_y])
        charging_coords.append(calculateRectangleCoordinate(center_x, center_y, 0, self.charging_length, self.charging_width))
        center_x = self.charging_length/2
        center_y = self.working_width + self.charging_width/2
        charging_centers.append([center_x, center_y])
        charging_coords.append(calculateRectangleCoordinate(center_x, center_y, 0, self.charging_length, self.charging_width))
        self.charging_centers = np.array(charging_centers)
        self.charging_coords = np.array(charging_coords)
        
    def calculateChargingPoint(self):
        charging_point_centers = []
        charging_point_coords = []
        step = (self.charging_length - self.single_line_width)/ (self.num_charging_point + 1)
        center_y = self.charging_centers[0, 1] + self.charging_width/2 - self.point_length/2
        for i in range(1, self.num_charging_point + 1):
            center_x = self.charging_centers[0, 0] - self.charging_length/2 + self.single_line_width/2 + i * step
            charging_point_centers.append([center_x, center_y])
            charging_point_coords.append(calculateRectangleCoordinate(center_x, center_y, math.pi/2, 
                                                                    self.point_length, self.single_line_width))
        center_y = self.charging_centers[1, 1] - self.charging_width/2 + self.point_length/2
        for i in range(1, self.num_charging_point + 1):
            center_x = self.charging_centers[1, 0] - self.charging_length/2 + self.single_line_width/2 + i * step
            charging_point_centers.append([center_x, center_y])
            charging_point_coords.append(calculateRectangleCoordinate(center_x, center_y, math.pi/2, 
                                                                    self.point_length, self.single_line_width))
        
        self.charging_point_centers = np.array(charging_point_centers)
        self.charging_point_coords = np.array(charging_point_coords)