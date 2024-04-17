import numpy as np
import matplotlib.pyplot as plt
import cv2
from typing import List
from working_zone import *
from storage_zone import *
from waiting_zone import *
from charging_zone import *

class GraphVertex:
    def __init__(self, id: int, type: int, center: np.ndarray, line_type: int = -1):
        self.id = id
        self.type: int = type
        self.center: np.ndarray = center
        self.line_type: int = line_type
        # self.horizontal_id: int = horizontal_id
        # self.vertical_id: int = vertical_id

class GraphEdge:
    def __init__(self, directed: bool, start_vertex: GraphVertex, end_vertex: GraphVertex, edge_vel: float):
        self.directed: bool = directed
        self.start_vertex: GraphVertex = start_vertex
        self.end_vertex: GraphVertex = end_vertex
        self.edge_vel: float = edge_vel
        self.edge_distance: float = math.hypot(self.end_vertex.center[0] - self.start_vertex.center[0], 
                                                self.end_vertex.center[1] - self.start_vertex.center[1])

class FactoryMap:
    def __init__(self):
        self.factory_parameters()
        self.factory_bounding = np.array(calculateRectangleCoordinate(self.factory_center_x, self.factory_center_y, 0, 
                                                                    self.factory_length, self.factory_width))
        self.working_zone = WorkingZone(self.working_zone_length, self.working_zone_width, self.num_of_double_vertical_line,
                                        self.num_of_double_horizon_line, self.min_num_between_horizon, self.max_num_between_horizon,
                                        self.min_num_between_vertical, self.max_num_between_vertical, self.additional_length,
                                        self.working_two_points_dist, self.single_line_width, self.double_line_width, self.robot_length)
        self.storage_zone = StorageZone(self.working_zone_length, self.working_zone_width, self.storage_length, self.storage_width, 
                                        self.num_storage_point, self.storage_additional_length, self.single_line_width, 
                                        self.robot_length, self.robot_width)
        self.waiting_zone = WaitingZone(self.working_zone_length, self.working_zone_width, self.waiting_length, self.waiting_width,
                                        self.num_waiting_col, self.waiting_additional_length, self.single_line_width, self.waiting_point_dist,
                                        self.robot_length, self.robot_width)
        self.charging_zone = ChargingZone(self.working_zone_length, self.working_zone_width, self.charging_length, self.charging_width,
                                        self.num_charging_point, self.charging_additional_length, self.single_line_width,
                                        self.robot_length, self.robot_width)
    
    def save_line_data(self, data_folder):
        line_data = []
        for i in range(self.working_zone.horizontal_double_centers.shape[0]):
            line_data.append([DOUBLE_HORIZONTAL, self.working_zone.horizontal_double_centers[i, 0],
                            self.working_zone.horizontal_double_centers[i, 1], self.working_zone.map_length_meters])
            
        for i in range(self.working_zone.horizontal_single_centers.shape[0]):
            line_data.append([SINGLE_HORIZONTAL, self.working_zone.horizontal_single_centers[i, 0],
                            self.working_zone.horizontal_single_centers[i, 1], self.working_zone.map_length_meters])
            
        for i in range(self.working_zone.vertical_double_centers.shape[0]):
            line_data.append([DOUBLE_VERTICAL, self.working_zone.vertical_double_centers[i, 0],
                            self.working_zone.vertical_double_centers[i, 1], self.working_zone.map_width_meters])
            
        for i in range(self.working_zone.vertical_single_centers.shape[0]):
            length = max(abs(self.working_zone.vertical_single_coords[i, 0, 1] - self.working_zone.vertical_single_coords[i, 1, 1]),
                    abs(abs(self.working_zone.vertical_single_coords[i, 1, 1] - self.working_zone.vertical_single_coords[i, 2, 1])))
            line_data.append([SINGLE_VERTICAL, self.working_zone.vertical_single_centers[i, 0],
                            self.working_zone.vertical_single_centers[i, 1], length])
        np.savetxt(data_folder + "/line_data.txt", np.array(line_data), fmt='%.2f')
    
    def save_zone_data(self, data_folder):
        zone_data = []
        for i in range(self.working_zone.working_zone_centers.shape[0]):
            length = max(abs(self.working_zone.working_zone_coords[i, 0, 0] - self.working_zone.working_zone_coords[i, 1, 0]),
                    abs(abs(self.working_zone.working_zone_coords[i, 1, 0] - self.working_zone.working_zone_coords[i, 2, 0])))
            width = max(abs(self.working_zone.working_zone_coords[i, 0, 1] - self.working_zone.working_zone_coords[i, 1, 1]),
                    abs(abs(self.working_zone.working_zone_coords[i, 1, 1] - self.working_zone.working_zone_coords[i, 2, 1])))
            zone_data.append([WORKING_ZONE, self.working_zone.working_zone_centers[i, 0],
                            self.working_zone.working_zone_centers[i, 1], length, width])
            
        for i in range(self.storage_zone.storage_centers.shape[0]):
            length = max(abs(self.storage_zone.storage_coords[i, 0, 0] - self.storage_zone.storage_coords[i, 1, 0]),
                    abs(abs(self.storage_zone.storage_coords[i, 1, 0] - self.storage_zone.storage_coords[i, 2, 0])))
            width = max(abs(self.storage_zone.storage_coords[i, 0, 1] - self.storage_zone.storage_coords[i, 1, 1]),
                    abs(abs(self.storage_zone.storage_coords[i, 1, 1] - self.storage_zone.storage_coords[i, 2, 1])))
            zone_data.append([STORAGE_ZONE, self.storage_zone.storage_centers[i, 0],
                            self.storage_zone.storage_centers[i, 1], length, width])
            
        for i in range(self.waiting_zone.waiting_centers.shape[0]):
            length = max(abs(self.waiting_zone.waiting_coords[i, 0, 0] - self.waiting_zone.waiting_coords[i, 1, 0]),
                    abs(abs(self.waiting_zone.waiting_coords[i, 1, 0] - self.waiting_zone.waiting_coords[i, 2, 0])))
            width = max(abs(self.waiting_zone.waiting_coords[i, 0, 1] - self.waiting_zone.waiting_coords[i, 1, 1]),
                    abs(abs(self.waiting_zone.waiting_coords[i, 1, 1] - self.waiting_zone.waiting_coords[i, 2, 1])))
            zone_data.append([WAITING_ZONE, self.waiting_zone.waiting_centers[i, 0],
                            self.waiting_zone.waiting_centers[i, 1], length, width])
            
        for i in range(self.charging_zone.charging_centers.shape[0]):
            length = max(abs(self.charging_zone.charging_coords[i, 0, 0] - self.charging_zone.charging_coords[i, 1, 0]),
                    abs(abs(self.charging_zone.charging_coords[i, 1, 0] - self.charging_zone.charging_coords[i, 2, 0])))
            width = max(abs(self.charging_zone.charging_coords[i, 0, 1] - self.charging_zone.charging_coords[i, 1, 1]),
                    abs(abs(self.charging_zone.charging_coords[i, 1, 1] - self.charging_zone.charging_coords[i, 2, 1])))
            zone_data.append([CHARGING_ZONE, self.charging_zone.charging_centers[i, 0],
                            self.charging_zone.charging_centers[i, 1], length, width])
            
        np.savetxt(data_folder + "/zone_data.txt", np.array(zone_data), fmt='%.2f')
    
    def save_point_data(self, data_folder):
        point_data = []
        for i in range(self.working_zone.working_point_centers.shape[0]):
            length = max(abs(self.working_zone.working_point_coords[i, 0, 0] - self.working_zone.working_point_coords[i, 1, 0]),
                    abs(abs(self.working_zone.working_point_coords[i, 1, 0] - self.working_zone.working_point_coords[i, 2, 0])))
            width = max(abs(self.working_zone.working_point_coords[i, 0, 1] - self.working_zone.working_point_coords[i, 1, 1]),
                    abs(abs(self.working_zone.working_point_coords[i, 1, 1] - self.working_zone.working_point_coords[i, 2, 1])))
            point_data.append([WORKING_POINT, self.working_zone.working_point_type[i], self.working_zone.working_point_centers[i, 0],
                                self.working_zone.working_point_centers[i, 1], max(length, width), min(length, width)])
        
        for i in range(self.storage_zone.storage_point_centers.shape[0]):
            length = max(abs(self.storage_zone.storage_point_coords[i, 0, 0] - self.storage_zone.storage_point_coords[i, 1, 0]),
                    abs(abs(self.storage_zone.storage_point_coords[i, 1, 0] - self.storage_zone.storage_point_coords[i, 2, 0])))
            width = max(abs(self.storage_zone.storage_point_coords[i, 0, 1] - self.storage_zone.storage_point_coords[i, 1, 1]),
                    abs(abs(self.storage_zone.storage_point_coords[i, 1, 1] - self.storage_zone.storage_point_coords[i, 2, 1])))
            point_data.append([STORAGE_POINT, DOUBLE_HORIZONTAL, self.storage_zone.storage_point_centers[i, 0],
                            self.storage_zone.storage_point_centers[i, 1], max(length, width), min(length, width)])
            
        for i in range(self.waiting_zone.waiting_point_centers.shape[0]):
            length = max(abs(self.waiting_zone.waiting_point_coords[i, 0, 0] - self.waiting_zone.waiting_point_coords[i, 1, 0]),
                    abs(abs(self.waiting_zone.waiting_point_coords[i, 1, 0] - self.waiting_zone.waiting_point_coords[i, 2, 0])))
            width = max(abs(self.waiting_zone.waiting_point_coords[i, 0, 1] - self.waiting_zone.waiting_point_coords[i, 1, 1]),
                    abs(abs(self.waiting_zone.waiting_point_coords[i, 1, 1] - self.waiting_zone.waiting_point_coords[i, 2, 1])))
            point_data.append([WAITING_POINT,DOUBLE_HORIZONTAL, self.waiting_zone.waiting_point_centers[i, 0],
                            self.waiting_zone.waiting_point_centers[i, 1], max(length, width), min(length, width)])
            
        for i in range(self.charging_zone.charging_point_centers.shape[0]):
            length = max(abs(self.charging_zone.charging_point_coords[i, 0, 0] - self.charging_zone.charging_point_coords[i, 1, 0]),
                    abs(abs(self.charging_zone.charging_point_coords[i, 1, 0] - self.charging_zone.charging_point_coords[i, 2, 0])))
            width = max(abs(self.charging_zone.charging_point_coords[i, 0, 1] - self.charging_zone.charging_point_coords[i, 1, 1]),
                    abs(abs(self.charging_zone.charging_point_coords[i, 1, 1] - self.charging_zone.charging_point_coords[i, 2, 1])))
            point_data.append([CHARGING_POINT, DOUBLE_HORIZONTAL, self.charging_zone.charging_point_centers[i, 0],
                            self.charging_zone.charging_point_centers[i, 1], max(length, width), min(length, width)])
        np.savetxt(data_folder + "/point_data.txt", np.array(point_data), fmt= '%.2f')
        
    def updateFactoryMap(self):
        self.working_zone.updateWorkingZone()
        self.storage_zone.updateStorageZone()
        self.waiting_zone.updateWaitingZone()
        self.charging_zone.updateChargingZone()
        self.getFactoryGraphMap()
    
    def getFactoryGraphMap(self):
        self.id = 0
        self.working_points = self.working_zone.working_point_centers.copy()
        self.storage_points = self.storage_zone.storage_point_centers.copy()
        self.waiting_points = self.waiting_zone.waiting_point_centers.copy()
        self.charging_points = self.charging_zone.charging_point_centers.copy()
        self.zone_points = np.concatenate((self.working_points, self.storage_points, self.waiting_points, self.charging_points), axis= 0)
        # Create the vertices of the graph
        self.double_vertical_vertices: List[List[GraphVertex]] = [[] for _ in range(self.working_zone.vertical_double_centers.shape[0])]
        self.single_vertical_vertices: List[List[GraphVertex]] = [[] for _ in range(self.working_zone.vertical_single_centers.shape[0])]
        self.double_horizontal_vertices: List[List[GraphVertex]] = [[] for _ in range(self.working_zone.horizontal_double_centers.shape[0])]
        self.single_horizontal_vertices: List[List[GraphVertex]] = [[] for _ in range(self.working_zone.horizontal_single_centers.shape[0])]
        self.zone_vertices: List[GraphVertex] = []
        
        # Create the graph
        # self.getGraphVertices()
        # self.getGraphEdges()
        
    def getGraphVertices(self):
        self.graph_vertices: List[GraphVertex] = []
        self.waiting_vertices: List[List[GraphVertex]] = [[], []]
        for point in self.working_points:
            self.zone_vertices.append(GraphVertex(self.id, WORKING_POINT, point))
            self.graph_vertices.append(GraphVertex(self.id, WORKING_POINT, point))
            self.id += 1
        for point in self.storage_points:
            self.zone_vertices.append(GraphVertex(self.id, STORAGE_POINT, point))
            self.graph_vertices.append(GraphVertex(self.id, STORAGE_POINT, point))
            self.id += 1
        for point in self.waiting_points:
            if point[1] < 0: 
                self.waiting_vertices[0].append(GraphVertex(self.id, WAITING_POINT, point))
            else:
                self.waiting_vertices[1].append(GraphVertex(self.id, WAITING_POINT, point))
            self.zone_vertices.append(GraphVertex(self.id, WAITING_POINT, point))
            self.graph_vertices.append(GraphVertex(self.id, WAITING_POINT, point))
            self.id += 1
        for point in self.charging_points:
            self.zone_vertices.append(GraphVertex(self.id, CHARGING_POINT, point))
            self.graph_vertices.append(GraphVertex(self.id, CHARGING_POINT, point))
            self.id += 1
        # Get vertices in each line
        self.getLineIntersectionPoints()
        self.getVertexInDoubleVerticalLine()
        self.getVertexInSingleVerticalLine()
        self.getVertexInDoubleHorizontalLine()
        self.getVertexInSingleHorizontalLine()

    def getGraphEdges(self):
        self.adjacency_matrix: np.ndarray = np.zeros((len(self.graph_vertices), len(self.graph_vertices)), dtype=np.bool_)
        self.graph_edges: List[GraphEdge] = [] 
        self.getGraphEdgesBetweenZoneLine()
        self.getGraphEdgeInDoubleHorizontalLine()
        self.getGraphEdgeInDoubleVerticalLine()
        self.getGraphEdgeInSingleHorizontalLine()
        self.getGraphEdgeInSingleVerticalLine()
        
    def getGraphEdgesBetweenZoneLine(self):
        for v_list in self.waiting_vertices:
            for v1 in v_list:
                for v2 in v_list:
                    if v1.center[0] == v2.center[0] and v1.center[1] != v2.center[1] and abs(v2.center[1] - v1.center[1]) < self.waiting_zone.two_point_dist + self.waiting_zone.point_length + 0.1:
                        self.adjacency_matrix[v1.id, v2.id] = True
        
        for v_list in self.double_horizontal_vertices:
            for v in v_list:
                for z_v in self.zone_vertices:
                    if self.isGraphEdgeBetweenZoneLine(v, z_v) == True:
                        self.adjacency_matrix[v.id, z_v.id] = True
                        self.adjacency_matrix[z_v.id, v.id] = True
        for v_list in self.single_horizontal_vertices:
            for v in v_list:
                for z_v in self.zone_vertices:
                    if self.isGraphEdgeBetweenZoneLine(v, z_v) == True:
                        self.adjacency_matrix[v.id, z_v.id] = True
                        self.adjacency_matrix[z_v.id, v.id] = True
        for v_list in self.double_vertical_vertices:
            for v in v_list:
                for z_v in self.zone_vertices:
                    if self.isGraphEdgeBetweenZoneLine(v, z_v) == True:
                        self.adjacency_matrix[v.id, z_v.id] = True
                        self.adjacency_matrix[z_v.id, v.id] = True
        for v_list in self.single_vertical_vertices:
            for v in v_list:
                for z_v in self.zone_vertices:
                    if self.isGraphEdgeBetweenZoneLine(v, z_v) == True:
                        self.adjacency_matrix[v.id, z_v.id] = True
                        self.adjacency_matrix[z_v.id, v.id] = True
    
    def getGraphEdgeInDoubleHorizontalLine(self):
        for v_list in self.double_horizontal_vertices:
            first_list = [v_list[0]]
            second_list = []
            for i in range(1, len(v_list)):
                if round(v_list[i].center[1], 1) == round(v_list[0].center[1], 1):
                    first_list.append(v_list[i])
                else:
                    second_list.append(v_list[i])
            first_sorted_list = sorted(first_list, key=lambda vertex: vertex.center[0])
            second_sorted_list = sorted(second_list, key=lambda vertex: vertex.center[0])
            for i in range(len(first_sorted_list) - 1 ):
                self.adjacency_matrix[first_sorted_list[i].id, first_sorted_list[i+1].id] = True
            for i in range(len(second_sorted_list) - 1):
                self.adjacency_matrix[second_sorted_list[i+1].id, second_sorted_list[i].id] = True
            for v1 in first_sorted_list:
                for v2 in second_sorted_list:
                    if round(v1.center[0], 1) == round(v2.center[0], 1):
                        self.adjacency_matrix[v1.id, v2.id] = True
                        self.adjacency_matrix[v2.id, v1.id] = True
                        
    def getGraphEdgeInDoubleVerticalLine(self):
        for v_list in self.double_vertical_vertices:
            first_list = [v_list[0]]
            second_list = []
            for i in range(1, len(v_list)):
                if round(v_list[i].center[0], 1) == round(v_list[0].center[0], 1):
                    first_list.append(v_list[i])
                else:
                    second_list.append(v_list[i])
            first_sorted_list = sorted(first_list, key=lambda vertex: vertex.center[1])
            second_sorted_list = sorted(second_list, key=lambda vertex: vertex.center[1])
            for i in range(len(first_sorted_list) - 1 ):
                self.adjacency_matrix[first_sorted_list[i].id, first_sorted_list[i+1].id] = True
            for i in range(len(second_sorted_list) - 1):
                self.adjacency_matrix[second_sorted_list[i+1].id, second_sorted_list[i].id] = True
            for v1 in first_sorted_list:
                for v2 in second_sorted_list:
                    if round(v1.center[1], 1) == round(v2.center[1], 1):
                        self.adjacency_matrix[v1.id, v2.id] = True
                        self.adjacency_matrix[v2.id, v1.id] = True
                        
    def getGraphEdgeInSingleHorizontalLine(self):
        for v_list in self.single_horizontal_vertices:
            sorted_list = sorted(v_list, key=lambda vertex: vertex.center[0])
            for i in range(len(sorted_list) - 1 ):
                self.adjacency_matrix[sorted_list[i].id, sorted_list[i+1].id] = True
                self.adjacency_matrix[sorted_list[i+1].id, sorted_list[i].id] = True
    
    def getGraphEdgeInSingleVerticalLine(self):
        for v_list in self.single_vertical_vertices:
            sorted_list = sorted(v_list, key=lambda vertex: vertex.center[1])
            for i in range(len(sorted_list) - 1 ):
                self.adjacency_matrix[sorted_list[i].id, sorted_list[i+1].id] = True
                self.adjacency_matrix[sorted_list[i+1].id, sorted_list[i].id] = True
    
    
    def isGraphEdgeBetweenZoneLine(self, vertex1: GraphVertex, vertex2: GraphVertex):
        condition1 = round(vertex1.center[0], 2) == round(vertex2.center[0], 2)
        condition2 = round(vertex1.center[1], 2) == round(vertex2.center[1], 2)
        max_dist = self.single_line_width + max(self.working_zone.point_length/2, self.storage_zone.point_length/2,
                                                self.waiting_zone.point_length/2, self.charging_zone.point_length/2)
        if condition1 or condition2:
            if vertex1.line_type == DOUBLE_HORIZONTAL or vertex1.line_type == SINGLE_HORIZONTAL:
                if abs(vertex1.center[1] - vertex2.center[1]) < max_dist:
                    return True
            elif vertex1.line_type == DOUBLE_VERTICAL or vertex1.line_type == SINGLE_VERTICAL:
                if abs(vertex1.center[0] - vertex2.center[0]) < max_dist:
                    return True
        return False
    

    def getLineIntersectionPoints(self):
        line_intersection_points = []
        double_vertical_id = 0
        for vertical_center in self.working_zone.vertical_double_centers:
            x1 = vertical_center[0] - self.double_line_width/4
            x2 = vertical_center[0] + self.double_line_width/4
            single_horizontal_id = 0
            for single_center in self.working_zone.horizontal_single_centers:
                line_intersection_points.append([x1, single_center[1]])
                self.single_horizontal_vertices[single_horizontal_id].append(GraphVertex(self.id, LINE_POINT, 
                                                                                        np.array([x1, single_center[1]]), 
                                                                                        SINGLE_HORIZONTAL))
                
                self.double_vertical_vertices[double_vertical_id].append(GraphVertex(self.id, LINE_POINT, 
                                                                                    np.array([x1, single_center[1]]), 
                                                                                    DOUBLE_VERTICAL))
                self.graph_vertices.append(GraphVertex(self.id, LINE_POINT, np.array([x1, single_center[1]])))
                line_intersection_points.append([x2, single_center[1]])
                
                self.single_horizontal_vertices[single_horizontal_id].append(GraphVertex(self.id+1, LINE_POINT, 
                                                                                        np.array([x2, single_center[1]]), 
                                                                                        SINGLE_HORIZONTAL))
                self.double_vertical_vertices[double_vertical_id].append(GraphVertex(self.id+1, LINE_POINT, 
                                                                                    np.array([x2, single_center[1]]), 
                                                                                    DOUBLE_VERTICAL))
                self.graph_vertices.append(GraphVertex(self.id+1, LINE_POINT, np.array([x2, single_center[1]])))
                self.id += 2
                single_horizontal_id += 1
            double_horizontal_id = 0
            for double_center in self.working_zone.horizontal_double_centers:
                line_intersection_points.append([x1, double_center[1] - self.double_line_width/4])
                self.double_horizontal_vertices[double_horizontal_id].append(GraphVertex(self.id, LINE_POINT, 
                                                                                        np.array([x1, double_center[1] - 
                                                                                                self.double_line_width/4]), 
                                                                                        DOUBLE_HORIZONTAL))
                self.double_vertical_vertices[double_vertical_id].append(GraphVertex(self.id, LINE_POINT, 
                                                                                    np.array([x1, double_center[1] - 
                                                                                            self.double_line_width/4]), 
                                                                                    DOUBLE_VERTICAL))
                self.graph_vertices.append(GraphVertex(self.id, LINE_POINT, np.array([x1, double_center[1] - 
                                                                                    self.double_line_width/4])))
                
                line_intersection_points.append([x2, double_center[1] - self.double_line_width/4])
                self.double_horizontal_vertices[double_horizontal_id].append(GraphVertex(self.id + 1, LINE_POINT, 
                                                                                        np.array([x2, double_center[1] - 
                                                                                                self.double_line_width/4]), 
                                                                                        DOUBLE_HORIZONTAL))
                self.double_vertical_vertices[double_vertical_id].append(GraphVertex(self.id + 1, LINE_POINT, 
                                                                                    np.array([x2, double_center[1] - 
                                                                                            self.double_line_width/4]), 
                                                                                    DOUBLE_VERTICAL))
                self.graph_vertices.append(GraphVertex(self.id + 1, LINE_POINT, np.array([x2, double_center[1] - 
                                                                                    self.double_line_width/4])))
                
                line_intersection_points.append([x1, double_center[1] + self.double_line_width/4])
                self.double_horizontal_vertices[double_horizontal_id].append(GraphVertex(self.id + 2, LINE_POINT, 
                                                                                        np.array([x1, double_center[1] + 
                                                                                                self.double_line_width/4]), 
                                                                                        DOUBLE_HORIZONTAL))
                self.double_vertical_vertices[double_vertical_id].append(GraphVertex(self.id + 2, LINE_POINT, 
                                                                                    np.array([x1, double_center[1] + 
                                                                                            self.double_line_width/4]), 
                                                                                    DOUBLE_VERTICAL))
                self.graph_vertices.append(GraphVertex(self.id + 2, LINE_POINT, np.array([x1, double_center[1] + 
                                                                                        self.double_line_width/4])))
                
                line_intersection_points.append([x2, double_center[1] + self.double_line_width/4])
                self.double_horizontal_vertices[double_horizontal_id].append(GraphVertex(self.id + 3, LINE_POINT, 
                                                                                        np.array([x2, double_center[1] + 
                                                                                                self.double_line_width/4]), 
                                                                                        DOUBLE_HORIZONTAL))
                self.double_vertical_vertices[double_vertical_id].append(GraphVertex(self.id + 3, LINE_POINT, 
                                                                                    np.array([x2, double_center[1] + 
                                                                                            self.double_line_width/4]), 
                                                                                    DOUBLE_VERTICAL))
                self.graph_vertices.append(GraphVertex(self.id + 3, LINE_POINT, np.array([x2, double_center[1] + 
                                                                                        self.double_line_width/4])))
                double_horizontal_id += 1
                self.id += 4
            double_vertical_id += 1
            
        single_vertical_id = 0
        for vertical_center, vertical_coords in zip(self.working_zone.vertical_single_centers, self.working_zone.vertical_single_coords):
            single_horizontal_id = 0
            for single_center in self.working_zone.horizontal_single_centers:
                if vertical_coords[1, 1] - self.single_line_width <= single_center[1] <= vertical_coords[2, 1] + self.single_line_width:
                    line_intersection_points.append([vertical_center[0], single_center[1]])
                    self.single_horizontal_vertices[single_horizontal_id].append(GraphVertex(self.id, LINE_POINT, 
                                                                    np.array([vertical_center[0], single_center[1]]), 
                                                                    SINGLE_HORIZONTAL))
                    self.single_vertical_vertices[single_vertical_id].append(GraphVertex(self.id, LINE_POINT, 
                                                                    np.array([vertical_center[0], single_center[1]]), 
                                                                    SINGLE_VERTICAL))
                    self.graph_vertices.append(GraphVertex(self.id, LINE_POINT, np.array([vertical_center[0], single_center[1]])))
                    self.id += 1
                single_horizontal_id += 1

            double_horizontal_id = 0
            for double_center in self.working_zone.horizontal_double_centers:
                if vertical_coords[1, 1] - self.double_line_width/2 - 0.1 <= double_center[1] - self.double_line_width/4 <= vertical_coords[2, 1] + self.double_line_width/2 + 0.1:
                    line_intersection_points.append([vertical_center[0], double_center[1] - self.double_line_width/4])
                    self.double_horizontal_vertices[double_horizontal_id].append(GraphVertex(self.id, LINE_POINT, 
                                                                                            np.array([vertical_center[0], 
                                                                                                    double_center[1] - 
                                                                                                    self.double_line_width/4]), 
                                                                                            DOUBLE_HORIZONTAL))
                    self.single_vertical_vertices[single_vertical_id].append(GraphVertex(self.id, LINE_POINT, 
                                                                                        np.array([vertical_center[0], 
                                                                                                double_center[1] - 
                                                                                                self.double_line_width/4]), 
                                                                                        SINGLE_VERTICAL))
                    self.graph_vertices.append(GraphVertex(self.id, LINE_POINT, np.array([vertical_center[0], 
                                                                                        double_center[1] -
                                                                                        self.double_line_width/4])))
                    self.id += 1
                if vertical_coords[1, 1] - self.double_line_width<= double_center[1] + self.double_line_width/4 <= vertical_coords[2, 1] + self.double_line_width:
                    line_intersection_points.append([vertical_center[0], double_center[1] + self.double_line_width/4])
                    self.double_horizontal_vertices[double_horizontal_id].append(GraphVertex(self.id, LINE_POINT, 
                                                                                            np.array([vertical_center[0], 
                                                                                                    double_center[1] + 
                                                                                                    self.double_line_width/4]), 
                                                                                            DOUBLE_HORIZONTAL))
                    self.single_vertical_vertices[single_vertical_id].append(GraphVertex(self.id, LINE_POINT, 
                                                                                        np.array([vertical_center[0], 
                                                                                                double_center[1] + 
                                                                                                self.double_line_width/4]), 
                                                                                        SINGLE_VERTICAL))
                    self.graph_vertices.append(GraphVertex(self.id, LINE_POINT, np.array([vertical_center[0], 
                                                                                        double_center[1] + 
                                                                                        self.double_line_width/4])))
                    self.id += 1
                double_horizontal_id += 1
            single_vertical_id += 1
        self.line_intersection_points = np.array(line_intersection_points)
        
    def getVertexInDoubleVerticalLine(self):
        double_vertical_points = []
        
        id = 0
        for center in self.working_zone.vertical_double_centers:
            origin_x1 = center[0] - self.double_line_width/4
            origin_x2 = center[0] + self.double_line_width/4 
            point_x1 = round(center[0] + self.double_line_width/2 + self.working_zone.point_length/2, 1)
            point_x2 = round(center[0] - self.double_line_width/2 - self.working_zone.point_length/2, 1)
            x1 = np.where(np.round(self.working_points[:, 0], 1) == point_x1)
            x2 = np.where(np.round(self.working_points[:, 0], 1) == point_x2)
            for index in x1[0]:
                double_vertical_points.append([origin_x1, self.working_points[index, 1]])
                double_vertical_points.append([origin_x2, self.working_points[index, 1]])
                self.double_vertical_vertices[id].append(GraphVertex(self.id, LINE_POINT, 
                                                                    np.array([origin_x1, self.working_points[index, 1]]), 
                                                                    DOUBLE_VERTICAL))
                self.double_vertical_vertices[id].append(GraphVertex(self.id + 1, LINE_POINT, 
                                                                    np.array([origin_x2, self.working_points[index, 1]]), 
                                                                    DOUBLE_VERTICAL))
                self.graph_vertices.append(GraphVertex(self.id, LINE_POINT, np.array([origin_x1, self.working_points[index, 1]])))
                self.graph_vertices.append(GraphVertex(self.id+1, LINE_POINT, np.array([origin_x2, self.working_points[index, 1]])))
                self.id += 2            
            for index in x2[0]:
                double_vertical_points.append([origin_x1, self.working_points[index, 1]])
                double_vertical_points.append([origin_x2, self.working_points[index, 1]])
                self.double_vertical_vertices[id].append(GraphVertex(self.id, LINE_POINT, 
                                                                    np.array([origin_x1, self.working_points[index, 1]]), 
                                                                    DOUBLE_VERTICAL))
                self.double_vertical_vertices[id].append(GraphVertex(self.id + 1, LINE_POINT, 
                                                                    np.array([origin_x2, self.working_points[index, 1]]), 
                                                                    DOUBLE_VERTICAL))
                self.graph_vertices.append(GraphVertex(self.id, LINE_POINT, np.array([origin_x1, self.working_points[index, 1]])))
                self.graph_vertices.append(GraphVertex(self.id+1, LINE_POINT, np.array([origin_x2, self.working_points[index, 1]])))
                self.id += 2
            id += 1
        
        self.double_vertical_points = np.array(double_vertical_points)
        
    def getVertexInSingleVerticalLine(self):
        single_vertical_points = []
        id = 0
        for center, coords in zip(self.working_zone.vertical_single_centers, self.working_zone.vertical_single_coords):
            point_x1 = round(center[0] + self.single_line_width/2 + self.working_zone.point_length/2, 1)
            point_x2 = round(center[0] - self.single_line_width/2 - self.working_zone.point_length/2, 1)
            x1 = np.where(np.round(self.working_points[:, 0], 1) == point_x1)
            x2 = np.where(np.round(self.working_points[:, 0], 1) == point_x2)
            for index in x1[0]:
                if coords[1, 1] <= self.working_points[index, 1] <= coords[2, 1]:
                    single_vertical_points.append([center[0], self.working_points[index, 1]])
                    self.single_vertical_vertices[id].append(GraphVertex(self.id, LINE_POINT, 
                                                                        np.array([center[0], 
                                                                                self.working_points[index, 1]]), 
                                                                        SINGLE_VERTICAL))
                    self.graph_vertices.append(GraphVertex(self.id, LINE_POINT, np.array([center[0], 
                                                                                self.working_points[index, 1]])))                
                    self.id += 1
            for index in x2[0]:
                if coords[1, 1] <= self.working_points[index, 1] <= coords[2, 1]:
                    single_vertical_points.append([center[0], self.working_points[index, 1]])
                    self.single_vertical_vertices[id].append(GraphVertex(self.id, LINE_POINT, 
                                                                        np.array([center[0], 
                                                                                self.working_points[index, 1]]), 
                                                                        SINGLE_VERTICAL))
                    self.graph_vertices.append(GraphVertex(self.id, LINE_POINT, np.array([center[0], 
                                                                                self.working_points[index, 1]])))
                    self.id += 1
            id += 1
        
        self.single_vertical_points = np.array(single_vertical_points)
    
    def getVertexInDoubleHorizontalLine(self):
        double_horizontal_points = []
        id = 0
        for center in self.working_zone.horizontal_double_centers:
            origin_y1 = center[1] - self.double_line_width/4
            origin_y2 = center[1] + self.double_line_width/4 
            point_y1 = round(center[1] + self.double_line_width/2 + self.working_zone.point_length/2, 1)
            point_y2 = round(center[1] - self.double_line_width/2 - self.working_zone.point_length/2, 1)
            y1 = np.where(np.round(self.zone_points[:, 1], 1) == point_y1)
            y2 = np.where(np.round(self.zone_points[:, 1], 1) == point_y2)
            for index in y1[0]:
                double_horizontal_points.append([self.zone_points[index, 0], origin_y1])
                double_horizontal_points.append([self.zone_points[index, 0], origin_y2])
                self.double_horizontal_vertices[id].append(GraphVertex(self.id, LINE_POINT, 
                                                                        np.array([self.zone_points[index, 0], 
                                                                                origin_y1]), 
                                                                        DOUBLE_HORIZONTAL))
                self.double_horizontal_vertices[id].append(GraphVertex(self.id + 1, LINE_POINT, 
                                                                        np.array([self.zone_points[index, 0], 
                                                                                origin_y2]), 
                                                                        DOUBLE_HORIZONTAL))
                self.graph_vertices.append(GraphVertex(self.id, LINE_POINT, np.array([self.zone_points[index, 0], origin_y1])))
                self.graph_vertices.append(GraphVertex(self.id+1, LINE_POINT, np.array([self.zone_points[index, 0], origin_y2])))
                self.id += 2
            for index in y2[0]:
                double_horizontal_points.append([self.zone_points[index, 0], origin_y1])
                double_horizontal_points.append([self.zone_points[index, 0], origin_y2])
                self.double_horizontal_vertices[id].append(GraphVertex(self.id, LINE_POINT, 
                                                                        np.array([self.zone_points[index, 0], 
                                                                                origin_y1]), 
                                                                        DOUBLE_HORIZONTAL))
                self.double_horizontal_vertices[id].append(GraphVertex(self.id + 1, LINE_POINT, 
                                                                        np.array([self.zone_points[index, 0], 
                                                                                origin_y2]), 
                                                                        DOUBLE_HORIZONTAL))
                self.graph_vertices.append(GraphVertex(self.id, LINE_POINT, np.array([self.zone_points[index, 0], origin_y1])))
                self.graph_vertices.append(GraphVertex(self.id+1, LINE_POINT, np.array([self.zone_points[index, 0], origin_y2])))
                self.id += 2
            id += 1
        self.double_horizontal_points = np.array(double_horizontal_points)
    
    def getVertexInSingleHorizontalLine(self):
        single_horizontal_points = []
        id = 0
        for center in self.working_zone.horizontal_single_centers:
            point_y1 = round(center[1] + self.single_line_width/2 + self.working_zone.point_length/2, 1)
            point_y2 = round(center[1] - self.single_line_width/2 - self.working_zone.point_length/2, 1)
            y1 = np.where(np.round(self.working_points[:, 1], 1) == point_y1)
            y2 = np.where(np.round(self.working_points[:, 1], 1) == point_y2)
            for index in y1[0]:
                single_horizontal_points.append([self.working_points[index, 0], center[1]])
                self.single_horizontal_vertices[id].append(GraphVertex(self.id, LINE_POINT, 
                                                                        np.array([self.working_points[index, 0], 
                                                                                    center[1]]), 
                                                                        SINGLE_HORIZONTAL))
                self.graph_vertices.append(GraphVertex(self.id, LINE_POINT, np.array([self.working_points[index, 0], center[1]])))
                self.id += 1
            for index in y2[0]:
                single_horizontal_points.append([self.working_points[index, 0], center[1]])
                self.single_horizontal_vertices[id].append(GraphVertex(self.id, LINE_POINT, 
                                                                        np.array([self.working_points[index, 0], 
                                                                                    center[1]]), 
                                                                        SINGLE_HORIZONTAL))
                self.graph_vertices.append(GraphVertex(self.id, LINE_POINT, np.array([self.working_points[index, 0], center[1]])))
                self.id += 1
            id += 1
        self.single_horizontal_points = np.array(single_horizontal_points)
    
    def visualizeFactoryMap(self):
        plt.fill(self.factory_bounding[:, 0], self.factory_bounding[:,1], c= self.factory_color)
        plt.plot(self.factory_bounding[:, 0], self.factory_bounding[:,1], '-', c= self.factory_wall_color)
        for zone in self.working_zone.working_zone_coords:
            plt.fill(zone[:, 0], zone[:, 1], c= self.working_zone_color)
        for point in self.working_zone.working_point_coords:
            plt.fill(point[:, 0], point[:, 1], c= self.working_point_color)
        for zone in self.storage_zone.storage_coords:
            plt.fill(zone[:, 0], zone[:, 1], c= self.storage_zone_color)
        for point in self.storage_zone.storage_point_coords:
            plt.fill(point[:, 0], point[:, 1], c= self.storage_point_color)
        for zone in self.waiting_zone.waiting_coords:
            plt.fill(zone[:, 0], zone[:, 1], c= self.waiting_zone_color)
        for point in self.waiting_zone.waiting_point_coords:
            plt.fill(point[:, 0], point[:, 1], c= self.waiting_point_color)
        for point in self.waiting_zone.waiting_line_coords:
            plt.fill(point[:, 0], point[:, 1], c= self.waiting_line_color)
        for zone in self.charging_zone.charging_coords:
            plt.fill(zone[:, 0], zone[:, 1],'-', c= self.charging_zone_color)
        for point in self.charging_zone.charging_point_coords:
            plt.fill(point[:, 0], point[:, 1], c = self.charging_point_color)
        plt.gca().set_aspect('equal', adjustable='box')
    
    def visualizeGraphFactoryMap(self):
        for i in range(self.adjacency_matrix.shape[0]):
            for j in range(self.adjacency_matrix.shape[0]):
                if self.adjacency_matrix[i, j] == True:
                    x1 = self.graph_vertices[i].center[0]
                    y1 = self.graph_vertices[i].center[1]
                    x2 = self.graph_vertices[j].center[0]
                    y2 = self.graph_vertices[j].center[1]
                    plt.arrow(x1, y1, x2 - x1, y2 - y1, head_width=0.1, head_length=0.1, fc='black', ec='red')
        plt.gca().set_aspect('equal', adjustable='box')
    
    def visualizePointMap(self):
        for point in self.working_zone.working_point_centers:
            plt.plot(point[0], point[1], 'g.')
        for point in self.storage_zone.storage_point_centers:
            plt.plot(point[0], point[1], 'g.')
        for point in self.waiting_zone.waiting_point_centers:
            plt.plot(point[0], point[1], 'g.')
        for point in self.charging_zone.charging_point_centers:
            plt.plot(point[0], point[1], 'g.')
        # for point in self.line_intersection_points:
        #     plt.plot(point[0], point[1], 'g.')
        # for point in self.double_vertical_points:
        #     plt.plot(point[0], point[1], 'g.')
        # for point in self.single_vertical_points:
        #     plt.plot(point[0], point[1], 'g.')
        # for point in self.double_horizontal_points:
        #     plt.plot(point[0], point[1], 'g.')
        # for point in self.single_horizontal_points:
        #     plt.plot(point[0], point[1], 'g.')
        
        plt.gca().set_aspect('equal', adjustable='box')
        
    def factory_parameters(self):
        self.robot_length = 0.98
        self.robot_width = 0.61
        self.single_line_width = 0.9 # m
        self.double_line_width = 2.0
        self.working_zone_parameters()
        self.storage_zone_parameters()
        self.waiting_zone_parameters()
        self.charging_zone_parameters()
        self.storage_length = self.charging_length = (self.working_zone_length - self.waiting_length)/2
        self.factory_length = self.working_zone_length
        self.factory_width = self.working_zone_width + 2 * max(self.storage_width, self.waiting_width, self.charging_width)
        self.factory_center_x = self.factory_length/2
        self.factory_center_y = self.factory_width/2 - max(self.storage_width, self.waiting_width, self.charging_width)
        self.factory_color = 'white'
        self.factory_wall_color = 'black'
        
    def working_zone_parameters(self):
        self.working_zone_length = 100
        self.working_zone_width = 50
        self.num_of_double_vertical_line = 0
        self.num_of_double_horizon_line = 0
        self.min_num_between_horizon = 1
        self.max_num_between_horizon = 3
        self.min_num_between_vertical = 1
        self.max_num_between_vertical = 3
        self.additional_length = 0.1
        self.working_two_points_dist = 0.75
        self.working_zone_color = 'black'
        self.working_point_color = 'white'

    def storage_zone_parameters(self):
        # self.storage_length = 20
        self.storage_width = 5
        self.num_storage_point = 5
        self.storage_additional_length = 0.1
        self.storage_zone_color = 'black'
        self.storage_point_color = 'white'
        
    def waiting_zone_parameters(self):
        self.waiting_length = 8
        self.waiting_width = 5
        self.num_waiting_col = 4
        self.waiting_additional_length = 0.1
        self.waiting_point_dist = 0.8
        self.waiting_zone_color = 'black'
        self.waiting_point_color = 'white'
        self.waiting_line_color = 'white'
        
    def charging_zone_parameters(self):
        # self.charging_length = 20
        self.charging_width = 5
        self.num_charging_point = 5
        self.charging_additional_length = 0.1
        self.charging_zone_color = 'black'
        self.charging_point_color = 'white'