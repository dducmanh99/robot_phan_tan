import matplotlib.pyplot as plt
import numpy as np
import math
from utlis import *

class StorageZone:
    def __init__(self, working_length: float, working_width: float, storage_length: float, storage_width: float,
                num_storage_point: int, additional_length: float, single_line_width: float, robot_length: float, 
                robot_width: float):
        self.working_length = working_length
        self.working_width = working_width
        self.storage_length = storage_length
        self.storage_width = storage_width
        self.robot_length = robot_length
        self.robot_width = robot_width
        self.num_storage_point = num_storage_point
        self.additional_length = additional_length
        self.single_line_width = single_line_width
        self.point_length = self.robot_length + self.additional_length
        self.calculateStorageZone()
        self.calculateStoragePoint()
    
    def updateStorageZone(self):
        self.calculateStorageZone()
        self.calculateStoragePoint()
    
    def calculateStorageZone(self):
        storage_centers = []
        storage_coords = []

        center_x = self.working_length - self.storage_length/2
        center_y = 0 - self.storage_width/2
        storage_centers.append([center_x, center_y])
        storage_coords.append(calculateRectangleCoordinate(center_x, center_y, 0, self.storage_length, self.storage_width))
        center_x = self.working_length - self.storage_length/2
        center_y = self.working_width + self.storage_width/2
        storage_centers.append([center_x, center_y])
        storage_coords.append(calculateRectangleCoordinate(center_x, center_y, 0, self.storage_length, self.storage_width))
        self.storage_centers = np.array(storage_centers)
        self.storage_coords = np.array(storage_coords)
        
    def calculateStoragePoint(self):
        storage_point_centers = []
        storage_point_coords = []
        step = (self.storage_length - self.single_line_width)/ (self.num_storage_point + 1)
        center_y = self.storage_centers[0, 1] + self.storage_width/2 - self.point_length/2
        for i in range(1, self.num_storage_point + 1):
            center_x = self.storage_centers[0, 0] - self.storage_length/2 + self.single_line_width/2 + i * step
            storage_point_centers.append([center_x, center_y])
            storage_point_coords.append(calculateRectangleCoordinate(center_x, center_y, math.pi/2, 
                                                                    self.point_length, self.single_line_width))
        center_y = self.storage_centers[1, 1] - self.storage_width/2 + self.point_length/2
        for i in range(1, self.num_storage_point + 1):
            center_x = self.storage_centers[1, 0] - self.storage_length/2 + self.single_line_width/2 + i * step
            storage_point_centers.append([center_x, center_y])
            storage_point_coords.append(calculateRectangleCoordinate(center_x, center_y, math.pi/2, 
                                                                    self.point_length, self.single_line_width))
        
        self.storage_point_centers = np.array(storage_point_centers)
        self.storage_point_coords = np.array(storage_point_coords)