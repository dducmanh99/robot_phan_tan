import matplotlib.pyplot as plt
import numpy as np
import math
from utlis import *

class WaitingZone:
    def __init__(self, working_length: float, working_width: float, waiting_length: float, waiting_width: float,
                num_waiting_col: int, additional_length: float, single_line_width: float, two_point_dist: float, 
                robot_length: float, robot_width: float):
        self.working_length = working_length
        self.working_width = working_width
        self.waiting_length = waiting_length
        self.waiting_width = waiting_width
        self.robot_length = robot_length
        self.robot_width = robot_width
        self.num_waiting_col = num_waiting_col
        self.additional_length = additional_length
        self.single_line_width = single_line_width
        self.two_point_dist = two_point_dist
        self.point_length = self.robot_length + self.additional_length
        self.calculateWaitingZone()
        self.calculateWaitingPoint()

    def updateWaitingZone(self):
        self.calculateWaitingZone()
        self.calculateWaitingPoint()
        
    def calculateWaitingZone(self):
        waiting_centers = []
        waiting_coords = []

        center_x = self.working_length/2 
        center_y = -self.waiting_width/2
        waiting_centers.append([center_x, center_y])
        waiting_coords.append(calculateRectangleCoordinate(center_x, center_y, 0, self.waiting_length, self.waiting_width))
        center_x = self.working_length/2 
        center_y = self.working_width + self.waiting_width/2
        waiting_centers.append([center_x, center_y])
        waiting_coords.append(calculateRectangleCoordinate(center_x, center_y, 0, self.waiting_length, self.waiting_width))
        self.waiting_centers = np.array(waiting_centers)
        self.waiting_coords = np.array(waiting_coords)
        
    def calculateWaitingPoint(self):
        waiting_point_centers = []
        waiting_point_coords = []
        waiting_line_centers = []
        waiting_line_coords = []
        num_of_rows = int((self.waiting_width + self.two_point_dist) / (self.point_length + self.two_point_dist))
        step = (self.waiting_length - self.single_line_width)/ (self.num_waiting_col + 1)
        for i in range(num_of_rows):
            center_y = - self.point_length/2 - i * (self.two_point_dist + self.point_length)
            line_center_y = center_y - self.point_length/2 - self.two_point_dist/2
            for j in range(1, self.num_waiting_col + 1):
                center_x = self.waiting_centers[0, 0] - self.waiting_length/2 + self.single_line_width/2 + j * step
                line_center_x = center_x + self.single_line_width/2 + (step - self.single_line_width)/2
                waiting_point_centers.append([center_x, center_y])
                waiting_point_coords.append(calculateRectangleCoordinate(center_x, center_y, math.pi/2, 
                                                                        self.point_length, self.single_line_width))
                # if j < self.num_waiting_col:
                #     waiting_line_centers.append([line_center_x, center_y])
                #     waiting_line_coords.append(calculateRectangleCoordinate(line_center_x, center_y, 0.0, 
                #                                                             step - self.single_line_width, self.robot_width))
                if i < num_of_rows - 1:
                    waiting_line_centers.append([center_x, line_center_y])
                    waiting_line_coords.append(calculateRectangleCoordinate(center_x, line_center_y, math.pi/2, 
                                                                            self.two_point_dist, self.robot_width))
        
        for i in range(num_of_rows):
            center_y = self.working_width + self.point_length/2 + i * (self.two_point_dist + self.point_length)
            line_center_y = center_y + self.point_length/2 + self.two_point_dist/2
            for j in range(1, self.num_waiting_col + 1):
                center_x = self.waiting_centers[0, 0] - self.waiting_length/2 + self.single_line_width/2 + j * step
                line_center_x = center_x + self.single_line_width/2 + (step - self.single_line_width)/2
                waiting_point_centers.append([center_x, center_y])
                waiting_point_coords.append(calculateRectangleCoordinate(center_x, center_y, math.pi/2, 
                                                                        self.point_length, self.single_line_width))
                # if j < self.num_waiting_col:
                #     waiting_line_centers.append([line_center_x, center_y])
                #     waiting_line_coords.append(calculateRectangleCoordinate(line_center_x, center_y, 0.0, 
                #                                                             step - self.single_line_width, self.robot_width))
                if i < num_of_rows - 1:
                    waiting_line_centers.append([center_x, line_center_y])
                    waiting_line_coords.append(calculateRectangleCoordinate(center_x, line_center_y, math.pi/2, 
                                                                            self.two_point_dist, self.robot_width))
        
        self.waiting_point_centers = np.array(waiting_point_centers)
        self.waiting_point_coords = np.array(waiting_point_coords)
        self.waiting_line_centers = np.array(waiting_line_centers)
        self.waiting_line_coords = np.array(waiting_line_coords)