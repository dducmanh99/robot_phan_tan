import math
import numpy as np
from typing import List
import matplotlib.pyplot as plt
import matplotlib.axes as axs
import matplotlib.figure as figure
import matplotlib.colors as mcolors
import heapq, random
# color = list(mcolors.CSS4_COLORS.keys())
color = ['red', 'green', 'blue', 'brown', 'orange', 'cyan', 'crimson']
# Line type
NONE_LINE = -1
DOUBLE_HORIZONTAL = 0
SINGLE_HORIZONTAL = 1
DOUBLE_VERTICAL = 2
SINGLE_VERTICAL = 3
MIX_LINE = 5
# Zone type
WORKING_ZONE = 0
STORAGE_ZONE = 1
WAITING_ZONE = 2
CHARGING_ZONE = 3
LINE_ZONE = 4
# Point type
NONE_POINT = -1
LINE_POINT = 0
WORKING_POINT = 1
STORAGE_POINT = 2
WAITING_POINT = 3
CHARGING_POINT = 4
AGENT_POINT = 5

def EuclidDistance(p1: np.ndarray, p2: np.ndarray):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def ManhattanDistance(p1: np.ndarray, p2: np.ndarray):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) 

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

class Line:
    def __init__(self, type: int, center: np.ndarray, length: float, width: float):
        self.center: np.ndarray = center.copy()
        self.length: float = length
        self.width: float = width
        self.type: int = type
        if type == DOUBLE_HORIZONTAL or type == SINGLE_HORIZONTAL:
            self.coords: np.ndarray = np.array(calculateRectangleCoordinate(center[0], center[1], 0.0, length, width))
        else:
            self.coords: np.ndarray = np.array(calculateRectangleCoordinate(center[0], center[1], math.pi/2, length, width))
    def getCenterX(self):
        return self.center[0]
    def getCenterY(self):
        return self.center[1]
    def getCenter(self):
        return self.center.copy()
    def getLength(self):
        return self.length
    def getWidth(self):
        return self.width
    def getLineType(self):
        return self.type

class Zone:
    def __init__(self, type: int, center: np.ndarray, length: float, width: float):
        self.center: np.ndarray = center.copy()
        self.length: float = length
        self.width: float = width
        self.type: int = type
        self.coords: np.ndarray = np.array(calculateRectangleCoordinate(center[0], center[1], 0.0, length, width))
    def getCenterX(self):
        return self.center[0]
    def getCenterY(self):
        return self.center[1]
    def getCenter(self):
        return self.center.copy()
    def getLength(self):
        return self.length
    def getWidth(self):
        return self.width
    def getZoneType(self):
        return self.type

class Point:
    def __init__(self, point_type: int, line_type: int, center: np.ndarray, length: float, width: float):
        self.center: np.ndarray = center.copy()
        self.length: float = length    
        self.width: float = width
        self.point_type: int = point_type
        self.line_type: int = line_type
        if line_type == DOUBLE_HORIZONTAL or line_type == SINGLE_HORIZONTAL:
            self.coords: np.ndarray = np.array(calculateRectangleCoordinate(center[0], center[1], math.pi/2, length, width))
        else:
            self.coords: np.ndarray = np.array(calculateRectangleCoordinate(center[0], center[1], 0.0, length, width))
    
    def getCenterX(self):
        return self.center[0]
    def getCenterY(self):
        return self.center[1]
    def getCenter(self):
        return self.center.copy()
    def getLength(self):
        return self.length
    def getWidth(self):
        return self.width
    def getPointType(self):
        return self.point_type
    def getLineType(self):
        return self.line_type

class Vertex:
    def __init__(self, id: int, type: int, center: np.ndarray, line_type: int = NONE_LINE):
        self.id = id
        self.type: int = type
        self.center: np.ndarray = center
        self.line_type: int = line_type
        self.neighbors: List[int] = []
    def getID(self):
        return self.id
    def getCenterX(self):
        return self.center[0]
    def getCenterY(self):
        return self.center[1]
    def getCenter(self):
        return self.center.copy()
    def getNeighbors(self):
        return self.neighbors.copy()
    def addNeighbor(self, neighbor_id: int):
        self.neighbors.append(neighbor_id)
    def removeNeighbor(self, neighbor_id: int):
        self.neighbors.remove(neighbor_id)
    def getLineType(self):
        return self.line_type

class Edge:
    def __init__(self, id: int, start: Vertex, end: Vertex, edge_vel: float):
        self.id = id
        self.start: Vertex = start
        self.end: Vertex = end
        self.edge_vel: float = edge_vel
        self.edge_distance: float = math.hypot(self.end.center[0] - self.start.center[0], 
                                                self.end.center[1] - self.start.center[1])
        
class Graph:
    def __init__(self):
        self.vertices: List[Vertex] = []
        self.edges: List[Edge] = []
        
    def getVertex(self, id: int):
        return self.vertices[id]

    def getNeighbor(self, id: int):
        return self.vertices[id].neighbors
    
    def getVertices(self):
        return self.vertices.copy()
    
    def getEdges(self):
        return self.edges.copy()   
    
    def addVertex(self, type: int, center: np.ndarray, line_type: int = -1):
        if len(self.vertices) == 0:
            self.vertices.append(Vertex(0, type, center, line_type))
        else:
            self.vertices.append(Vertex(self.vertices[-1].id + 1, type, center, line_type))

    def addEdge(self, v1_id: int, v2_id: int, edge_vel: float = 1.0):
        if len(self.edges) == 0:
            self.edges.append(Edge(id= 0, start = self.getVertex(v1_id), end= self.getVertex(v2_id), edge_vel = edge_vel))
            self.vertices[v1_id].neighbors.append(v2_id)
        else:
            self.edges.append(Edge(id= self.edges[-1].id, start = self.getVertex(v1_id), end= self.getVertex(v2_id), edge_vel = edge_vel))
            self.vertices[v1_id].neighbors.append(v2_id)
    
    def getNeighborAStar(self, id):
        neighbors = []
        for neighbor in self.vertices[id].neighbors:
            neighbors.append((neighbor, EuclidDistance(self.vertices[id].getCenter(), self.vertices[neighbor].getCenter())))
        
        return neighbors
            
class Task:
    def __init__(self, start: np.ndarray, target: np.ndarray, type: int, priority: int, mass: float):
        self.start_id: int = 0
        self.target_id: int = 0 
        self.start: np.ndarray = start
        self.target: np.ndarray = target
        self.type: int = type
        self.priority: int = priority
        self.mass: float = mass
        self.route: np.ndarray = np.array([None])
    
    def getStartID(self): return self.start_id
    def getTargetID(self): return self.target_id
    
    def getStartX(self): return self.start[0]
    def getTargetX(self): return self.target[0]
    
    def getStartY(self): return self.start[1]
    def getTargetY(self): return self.target[1]
    
    def getStart(self): return self.start.copy()
    def getTarget(self): return self.target.copy()
    
    def getType(self): return self.type 
    def getPriority(self): return self.priority
    def getMass(self): return self.mass
    
    def getRoute(self): return self.route
    
    def setStartID(self, id): self.start_id = id
    def setTargetID(self, id): self.target_id = id  
    
    def setStart(self, start: np.ndarray): self.start = start.copy()
    def setTarget(self, target: np.ndarray): self.target = target.copy()
    
    def setType(self, type: int): self.type = type
    def setPriority(self, priority: int): self.priority = priority
    def setMass(self, mass: float): self.mass = mass
    
    def setRoute(self, route: np.ndarray): self.route = route.copy()
class PriorityQueue:
    """
        Implements a priority queue data structure. Each inserted item
        has a priority associated with it and the client is usually interested
        in quick retrieval of the lowest-priority item in the queue. This
        data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)