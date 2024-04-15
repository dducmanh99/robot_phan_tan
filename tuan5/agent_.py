from utility import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from typing import List

key_color = 'black'

class Agent: 
    def __init__(self, id: int, key:bool, init_pose: np.ndarray, goal_pose: np.ndarray ,color: str, 
                 robot_radius:float=0.3, goal_gain:float=0.05, avoid_gain:float=1.0, friend_gain=0.01, align_gain=0.01):
        self.id = id
        self.key = key
        self.robot_pose = init_pose.copy()
        self.goal_pose = goal_pose.copy()
        self.vel:np.ndarray = np.zeros(2)
        
        self.robot_radius = robot_radius
        self.range_avoid = 3 * self.robot_radius
        self.range_static = 5 * self.robot_radius
        self.range_friend = 7 * self.robot_radius
        
        self.color = color
        if (self.key == True):
            self.circle = Circle((self.robot_pose[0], self.robot_pose[1]), radius= self.robot_radius,
                             edgecolor= key_color, facecolor= key_color)
        else:
            self.circle = Circle((self.robot_pose[0], self.robot_pose[1]), radius= self.robot_radius,
                                edgecolor= self.color, facecolor= self.color)
        
        self.agents: List[Agent] = []
        self.path = [[init_pose[0], init_pose[1]]]
        
        self.max_vel = 1
        
        self.max_mag = 0.15
        self.goal_gain = goal_gain
        self.avoid_gain = avoid_gain
        self.friend_gain = friend_gain
        self.align_gain = align_gain
        self.avoid_flag = False
        self.align_flag = False
        self.friend_flag = False
        
    def updatePose(self):
        
        if self.goalReached():
            print("Reach Goal!!")
            
        if self.key == True:
            self.goalVel()
        # avoid_flag = False
        # for agent in self.agents:
        #     dist = computeDistance(self.robot_pose, agent.robot_pose, 0.0)
        #     if (dist < self.range_avoid):
        #         avoid_flag = True
        #         self.avoidanceVel(agent.robot_pose)

        #     if (self.range_avoid < dist < )

        
        self.avoidanceVel()
        if self.avoid_flag == False:
            self.alignVel()
            self.friendVel()
        
        if self.avoid_flag == False and self.align_flag==False and self.friend_flag==False:
            self.vel = 0
        # self.friendVel()
        # self.limitVel()
        self.robot_pose = self.robot_pose + self.vel
        self.path.append([self.robot_pose[0], self.robot_pose[1]])

    def goalVel(self):
        self.vel = (self.goal_pose - self.robot_pose) * self.goal_gain

    def avoidanceVel(self):
        self.avoid_flag = False
        vel_avoid = np.zeros(2)
        for agent in self.agents:
            dist = computeDistance(self.robot_pose, agent.robot_pose, 0.0)
            if (dist < self.range_avoid):
                vel_avoid = vel_avoid + self.robot_pose - agent.robot_pose 
                self.avoid_flag = True
        self.vel = self.vel + vel_avoid * self.avoid_gain

    def alignVel(self):
        self.align_flag = False
        vel_align = np.zeros(2)
        count = 0
        for agent in self.agents:
            dist = computeDistance(self.robot_pose, agent.robot_pose, 0.0)
            if (self.range_avoid < dist < self.range_static):
                vel_align = vel_align + agent.vel
                count +=1
            if count > 0:
                self.vel = self.vel + (vel_align/count - self.vel) * self.align_gain
                self.align_flag = True

    def friendVel(self):
        self.friend_flag = False
        vel_friend = np.zeros(2)
        count = 0
        for agent in self.agents:
            dist = computeDistance(self.robot_pose, agent.robot_pose, 0.0)
            if (self.range_static < dist < self.range_friend):
                vel_friend = vel_friend + agent.robot_pose - self.range_static
                count +=1 
            if (count > 0):
                self.vel = self.vel + (vel_friend/count - self.robot_pose) * self.friend_gain
                self.friend_flag = True
                    
    def limitVel(self):
        speed = math.hypot(self.vel[0], self.vel[1])
        if speed > self.max_vel:
            self.vel =  self.vel/speed * self.max_vel
    
    def goalReached(self):
        if computeDistance(self.robot_pose, self.goal_pose, 0.0) < 1:
            return True
    
    def getCurrent(self): return self.robot_pose.copy()
    def getCurrentX(self): return self.robot_pose[0]
    def getCurrentY(self): return self.robot_pose[1]