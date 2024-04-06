from utility import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from typing import List

class Agent: 
    def __init__(self, id: int, key:bool, init_pose: np.ndarray, goal_pose: np.ndarray ,color: str, 
                 robot_radius:float=0.3, goal_gain:float=0.5, avoid_gain:float=0.5, friend_gain=2.0):
        self.id = id
        self.key = key
        self.robot_pose = init_pose.copy()
        self.goal_pose = goal_pose.copy()
        self.robot_radius = robot_radius
        self.range_avoid = 5 * self.robot_radius
        self.range_static = 7 * self.robot_radius
        self.range_friend = 9 * self.robot_radius
        
        self.color = color
        self.circle = Circle((self.robot_pose[0], self.robot_pose[1]), radius= self.robot_radius,
                             edgecolor= self.color, facecolor= self.color)
        self.path = [[init_pose[0], init_pose[1]]]
        
        self.angle = 0.0
        self.velocity = 0.0


        self.max_mag = 0.15
        self.goal_gain = goal_gain
        self.avoid_gain = avoid_gain
        self.friend_gain = friend_gain
        

    def updatePose(self, agent_position: List[np.ndarray]):
        # print(self.id)
        if self.goalReached():
            return
        # print (self.key)
        if (self.key == True):
            vector_list = [self.goalVector()]
        else:
            vector_list = [np.array([0.0, 0.0])]
        # print(vector_list)
        random_flag=False
        for i in range(len(agent_position)):
            if i == self.id: continue
            dist = computeDistance(self.robot_pose, agent_position[i], 0.0)
            if dist < self.range_avoid: 
                vector_list.append(self.avoidanceVector(agent_position[i]))
                random_flag = True
            if self.range_static < dist and dist < self.range_friend:
                vector_list.append(self.friendVector(agent_position[i]))
        # if random_flag == True:
        #     if np.random.rand() < 0.1:
        #         vector_list.append(np.array([self.max_mag * 0.5, np.random.uniform(-math.pi, math.pi)]))
        # print (vector_list)
        total_vector = sumOfListVectors(vector_list)
        # print(total_vector)
        self.robot_pose[0] += total_vector[0] * math.cos(total_vector[1])
        self.robot_pose[1] += total_vector[0] * math.sin(total_vector[1])
        self.angle = total_vector[1]
        self.velocity = total_vector[0]
        self.path.append([self.robot_pose[0], self.robot_pose[1]])
    
    def goalVector(self):
        mag = computeDistance(self.robot_pose, self.goal_pose, 0.0)

        if mag > self.max_mag: mag = self.max_mag
        if mag < -self.max_mag: mag = -self.max_mag
        angle = computeAngle(self.goal_pose, self.robot_pose)
        # angle =  math.atan2(self.goal_pose[1] - self.robot_pose[1], self.goal_pose[0] - self.robot_pose[0])

        return np.array([mag * self.goal_gain, angle])

    def avoidanceVector(self, other_pose: np.ndarray):
        dist = computeDistance(self.robot_pose, other_pose, 0.0)
        mag = (self.range_avoid - dist)/ (self.range_avoid - 2 * self.robot_radius)
        if mag > self.max_mag: mag = self.max_mag
        if mag < -self.max_mag: mag = -self.max_mag
        angle = computeAngle(self.robot_pose, other_pose)
        # angle = math.atan2(self.robot_pose[1] - other_pose[1], self.robot_pose[0] - other_pose[0])
        # print('avoid:{}'.format(mag * self.avoid_gain))
        return np.array([mag * self.avoid_gain, angle])

    def friendVector(self, other_pose: np.ndarray):
        mag = computeDistance(self.robot_pose, other_pose, self.range_avoid)

        if mag > self.max_mag: mag = self.max_mag
        if mag < -self.max_mag: mag = -self.max_mag

        angle = computeAngle(other_pose , self.robot_pose)/2
        # print('friend:{}'.format(mag * self.friend_gain))
        return np.array([mag * self.friend_gain, angle])

    def goalReached(self):
        if computeDistance(self.robot_pose, self.goal_pose, 0.0) < 1:
            return True
    
    def getCurrent(self): return self.robot_pose.copy()
    def getCurrentX(self): return self.robot_pose[0]
    def getCurrentY(self): return self.robot_pose[1]