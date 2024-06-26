from ultis import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from typing import List
color = ['red', 'green', 'blue', 'black', 'orange', 'purple', 'brown'] 
class Agent:
    def __init__(self, id: int, init_pose: np.ndarray, goal_pose: np.ndarray, robot_radius:float = 0.3):
        self.id = id
        self.robot_pose = init_pose.copy()
        self.goal_pose = goal_pose.copy()
        self.robot_radius = robot_radius
        self.effect_range = 2 * self.robot_radius + 2.0
        self.avoidance_gain = 2.0
        self.goal_gain = 0.5
        self.max_mag = 0.2
        self.random_gain = 0.5
        self.color = color[np.random.randint(0, len(color))]
        self.circle = Circle((self.robot_pose[0], self.robot_pose[1]), radius= self.robot_radius, 
                                edgecolor=self.color, facecolor=self.color)
        self.trajectory = [[init_pose[0], init_pose[1]]]
    
    def updatePose(self, agent_position: List[np.ndarray]):
        if self.goalReached():
            return
        vector_list = [self.goalVector()]
        # print(vector_list)
        random_flag = False
        for i in range(len(agent_position)):
            if i == self.id: continue
            dist = computeDistance(self.robot_pose, agent_position[i])
            if dist < self.effect_range:
                vector_list.append(self.avoidanceVector(agent_position[i]))
                # print(self.avoidanceVector(agent_position[i]))
                random_flag = True
        if random_flag == True:
            if np.random.rand() < 0.1:
                vector_list.append(np.array([self.max_mag * self.random_gain, np.random.uniform(-math.pi, math.pi)]))
    
        total_vector = sumOfListVectors(vector_list)
        self.robot_pose[0] += total_vector[0] * math.cos(total_vector[1])
        self.robot_pose[1] += total_vector[0] * math.sin(total_vector[1])
        self.trajectory.append([self.robot_pose[0], self.robot_pose[1]])
        
    def avoidanceVector(self, other_pos: np.ndarray):
        dist = computeDistance(self.robot_pose, other_pos)
        mag = (self.effect_range - dist)/ (self.effect_range - 2 * self.robot_radius)
        if mag > self.max_mag: mag = self.max_mag
        if mag < -self.max_mag: mag = -self.max_mag
        angle = math.atan2(self.robot_pose[1] - other_pos[1], self.robot_pose[0] - other_pos[0])
        return np.array([mag * self.avoidance_gain, angle])
        
    def goalVector(self):
        mag = computeDistance(self.robot_pose, self.goal_pose)
        
        if mag > self.max_mag: mag = self.max_mag
        if mag < -self.max_mag: mag = -self.max_mag
        angle =  math.atan2(self.goal_pose[1] - self.robot_pose[1], self.goal_pose[0] - self.robot_pose[0])
        
        return np.array([mag * self.goal_gain, angle])

    def goalReached(self):
        if computeDistance(self.robot_pose, self.goal_pose) < 0.1:
            return True
    def getCurrentX(self): return self.robot_pose[0]
    def getCurrentY(self): return self.robot_pose[1]
    def getGoalX(self): return self.goal_pose[0]
    def getGoalY(self): return self.goal_pose[1]
    def getGoal(self): return self.goal_pose.copy()
    def getCurrent(self): return self.robot_pose.copy()