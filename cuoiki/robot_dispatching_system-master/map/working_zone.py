import matplotlib.pyplot as plt
import numpy as np
import math
from utlis import *

class WorkingZone:
    def __init__(self, map_length: float, map_width: float, double_vertical: float, double_horizontal: float,
                min_num_between_horizon: int, max_num_between_horizon: int, min_num_between_vertical: int, 
                max_num_between_vertical: int, additional_length: float, distance_between_points: float, 
                single_line_width: float, double_line_width: float, robot_length: float):
        self.map_length_meters = map_length
        self.map_width_meters = map_width

        self.num_double_vertical_line = double_vertical + 2
        self.num_double_horizontal_line = double_horizontal + 2
        
        self.min_num_between_horizon = min_num_between_horizon
        self.max_num_between_horizon = max_num_between_horizon
        
        self.min_num_between_vertical = min_num_between_vertical
        self.max_num_between_vertical = max_num_between_vertical
        
        self.single_line_width = single_line_width
        self.double_line_width = double_line_width
        
        self.working_zone_bounding = np.array(calculateRectangleCoordinate(map_length/2, map_width/2, 0, 
                                                                            map_length, map_width))
        self.additional_length = additional_length
        self.distance_between_points = distance_between_points
        self.point_length = robot_length + self.additional_length
        self.point_width = self.single_line_width
        self.calculateHorizontalLine()
        self.calculateWorkingZone()
        self.calculateWorkingPoint()
    
    def updateWorkingZone(self):
        self.calculateHorizontalLine()
        self.calculateWorkingZone()
        self.calculateWorkingPoint()
    
    def calculateWorkingPoint(self):
        working_point_type, working_point_centers, working_point_coords = [], [], []
        for i in range(self.working_zone_centers.shape[0]):
            working_length = self.working_zone_sizes[i, 0]
            working_width = self.working_zone_sizes[i, 1]
            origin_x = self.working_zone_centers[i, 0] - working_length / 2
            origin_y = self.working_zone_centers[i, 1] - working_width / 2
            for j in range(4):
                if j % 2 == 0:
                    num_points = int((working_length - self.point_length)/ (self.single_line_width + self.distance_between_points * 2))
                    if num_points <= 0:
                        continue
                    step = (working_length - self.point_length) / (num_points + 1)
                    for k in range(1, num_points + 1):
                        center_x = origin_x + k * step + self.point_length/2
                        if j == 0:
                            center_y = origin_y + working_width - self.point_length/2
                        else:
                            center_y = origin_y + self.point_length/2
                        working_point_type.append(DOUBLE_HORIZONTAL)
                        working_point_centers.append([center_x, center_y])
                        working_point_coords.append(calculateRectangleCoordinate(center_x, center_y, math.pi/2, 
                                                                                self.point_length, self.point_width))
                else:
                    num_points = int((working_width - self.point_length)/ (self.single_line_width + self.distance_between_points * 2))
                    if num_points <= 0:
                        continue
                    step = (working_width - self.point_length) / (num_points + 1)
                    for k in range(1, num_points + 1):
                        center_y = origin_y + k * step + self.point_length/2
                        if j == 1:
                            center_x = origin_x + working_length - self.point_length/2
                        else:
                            center_x = origin_x + self.point_length/2
                        working_point_type.append(DOUBLE_VERTICAL)
                        working_point_centers.append([center_x, center_y])
                        working_point_coords.append(calculateRectangleCoordinate(center_x, center_y, 0, 
                                                                                self.point_length, self.point_width))
        self.working_point_centers = np.array(working_point_centers)
        self.working_point_coords = np.array(working_point_coords)
        self.working_point_type = np.array(working_point_type)

    def calculateWorkingZone(self):
        double_line_centers, double_line_coords = self.calculateFixedVerticalLines()
        working_zone_centers, working_zone_coords, working_zone_sizes = [], [], []
        single_line_centers, single_line_coords = [], []
        double_single_line_centers = []
        for i in range(self.horizontal_double_centers.shape[0] - 1):
            double_single_center = [self.horizontal_double_centers[i]]
            for j in range(self.horizontal_single_centers.shape[0]):
                if self.horizon_single_line_id[j] == i:
                    double_single_center.append(self.horizontal_single_centers[j])
            double_single_center.append(self.horizontal_double_centers[i+1])
            double_single_line_centers.append(double_single_center.copy())

        for i in range(len(double_single_line_centers)):
            for j in range(len(double_single_line_centers[i])-1):
                line_length = double_single_line_centers[i][j+1][1] - double_single_line_centers[i][j][1] - self.single_line_width
                center_y = 0.5 * (double_single_line_centers[i][j+1][1] + double_single_line_centers[i][j][1])
                if len(double_single_line_centers[i]) > 2:
                    if j == 0 or j == len(double_single_line_centers[i]) - 2:
                        line_length = line_length + self.single_line_width/2 - self.double_line_width/2
                        if j == 0:
                            center_y += 0.5 * (self.double_line_width/2 - self.single_line_width/2)
                        else:
                            center_y -= 0.5 * (self.double_line_width/2 - self.single_line_width/2)
                else:
                    line_length = line_length + self.single_line_width - self.double_line_width
                
                for k in range(double_line_centers.shape[0] - 1):
                    coord_distance = double_line_centers[k+1, 0] - double_line_centers[k, 0]
                    num_of_line = np.random.randint(self.min_num_between_vertical, self.max_num_between_vertical)
                    if num_of_line == 0: continue
                    coef_distance = [0]
                    prod_coef_distance = [0]
                    for _ in range(num_of_line + 1):
                        coef_distance.append(np.random.randint(2, 5))
                        prod_coef_distance.append(sum(coef_distance))
                    step_distance = coord_distance / sum(coef_distance)
                    for line in range(num_of_line + 1):
                        working_center_x = double_line_centers[k, 0] + 0.5 * (prod_coef_distance[line] + prod_coef_distance[line+1]) * step_distance
                        working_width = step_distance * coef_distance[line + 1] - self.single_line_width
                        if line == 0:
                            working_width += self.single_line_width/2 - self.double_line_width/2
                            working_center_x += 0.5 * (self.double_line_width/2 - self.single_line_width/2)
                        if line == num_of_line:
                            working_width += self.single_line_width/2 - self.double_line_width/2
                            working_center_x -= 0.5 * (self.double_line_width/2 - self.single_line_width/2)

                        if line < num_of_line:
                            line_center_x = double_line_centers[k, 0] + prod_coef_distance[line+1] * step_distance 
                            working_zone_centers.append([working_center_x, center_y])
                            working_zone_coords.append(calculateRectangleCoordinate(working_center_x, center_y, math.pi/2,
                                                                                    line_length, working_width))
                            working_zone_sizes.append([working_width, line_length])
                            single_line_centers.append([line_center_x, center_y])
                            single_line_coords.append(calculateRectangleCoordinate(line_center_x, center_y, math.pi/2,
                                                                                    line_length, self.single_line_width))
                        else:
                            working_zone_centers.append([working_center_x, center_y])
                            working_zone_coords.append(calculateRectangleCoordinate(working_center_x, center_y, math.pi/2,
                                                                                    line_length, working_width))
                            working_zone_sizes.append([working_width, line_length])  

        self.working_zone_centers = np.array(working_zone_centers)
        self.working_zone_coords = np.array(working_zone_coords)
        self.working_zone_sizes = np.array(working_zone_sizes)
        self.vertical_double_centers = double_line_centers.copy()
        self.vertical_double_coords = double_line_coords.copy()
        self.vertical_single_centers = np.array(single_line_centers)
        self.vertical_single_coords = np.array(single_line_coords)
        
    def calculateHorizontalLine(self):
        double_line_centers, double_line_coords = self.calculateFixedHorizontalLines()
        single_line_centers, single_line_coords, single_line_id = [], [], []
        for i in range(double_line_centers.shape[0] - 1):
            distance = double_line_centers[i+1, 1] - double_line_centers[i, 1]
            num_of_line = np.random.randint(self.min_num_between_horizon, self.max_num_between_horizon)
            if num_of_line == 0: continue
            step_distance = distance / (num_of_line + 1)
            k = 1
            for _ in range(num_of_line):
                single_line_id.append(i)
                single_line_centers.append([double_line_centers[i, 0], double_line_centers[i, 1] + k * step_distance])
                single_line_coords.append(calculateRectangleCoordinate(double_line_centers[i, 0], 
                                                                        double_line_centers[i, 1] + k * step_distance, 0,
                                                                        self.map_length_meters, 
                                                                        self.single_line_width))
                k += 1
        
        self.horizontal_double_centers = double_line_centers.copy()
        self.horizontal_double_coords = double_line_coords.copy()
        self.horizontal_single_centers = np.array(single_line_centers)
        self.horizontal_single_coords = np.array(single_line_coords)
        self.horizon_single_line_id = single_line_id
            
    def calculateFixedHorizontalLines(self):
        center_line_x = self.map_length_meters / 2
        center_line_y = self.double_line_width / 2 
        coef_distance = [0]
        prod_coef_distance = [0]
        for _ in range(self.num_double_horizontal_line - 1):
            coef_distance.append(np.random.randint(2, 5))
            prod_coef_distance.append(sum(coef_distance))
        step_distance = (self.map_width_meters - self.double_line_width) / (sum(coef_distance))
        double_lines_coords = []
        double_lines_center = []
        i = 0
        for k in range(self.num_double_horizontal_line):
            double_lines_center.append([center_line_x, center_line_y + prod_coef_distance[k] * step_distance])
            double_lines_coords.append(calculateRectangleCoordinate(center_line_x, 
                                                                    center_line_y + prod_coef_distance[k] * step_distance, 0, 
                                                                    self.map_length_meters, 
                                                                    self.double_line_width))
            i += 1
            
        
        return np.array(double_lines_center), np.array(double_lines_coords)
    
    def calculateFixedVerticalLines(self):
        center_line_x = self.double_line_width / 2 
        center_line_y = self.map_width_meters / 2
        coef_distance = [0]
        prod_coef_distance = [0]
        for _ in range(self.num_double_vertical_line - 1):
            coef_distance.append(np.random.randint(2, 3))
            prod_coef_distance.append(sum(coef_distance))
        step_distance = (self.map_length_meters - self.double_line_width) / (sum(coef_distance))
        double_lines_coords = []
        double_lines_center = []
        i = 0
        for k in range(self.num_double_vertical_line):
            double_lines_center.append([center_line_x +  prod_coef_distance[k] * step_distance, center_line_y])
            double_lines_coords.append(calculateRectangleCoordinate(center_line_x +  prod_coef_distance[k] * step_distance, 
                                                                    center_line_y, math.pi/2, 
                                                                    self.map_width_meters, 
                                                                    self.double_line_width))
            i += 1
        
        return np.array(double_lines_center), np.array(double_lines_coords)