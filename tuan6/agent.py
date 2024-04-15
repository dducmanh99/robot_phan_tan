from utility import *
import sys 

key_color = 'black'

class Agent:
    def __init__(self,  id: int, init_pose:np.ndarray, color: str,
                 robot_radius:float=0.5):
        
        self.id = id 
        self.robot_pose = init_pose.copy()
        
        self.color = color
        self.robot_radius = robot_radius

        self.path = [[init_pose[0], init_pose[1]]]
        self.key_pos = []

        if (self.id == 0):
            self.circle = Circle((self.robot_pose[0], self.robot_pose[1]), radius= self.robot_radius,
                             edgecolor= key_color, facecolor= key_color) 
            angle = - math.pi/2 
            
            self.key_pos = [init_pose[0], init_pose[1], angle]
            
        else:
            self.circle = Circle((self.robot_pose[0], self.robot_pose[1]), radius= self.robot_radius,
                             edgecolor= self.color, facecolor= self.color)
            
        
        self.goalReach_flag = False
        self.goal_gain = 0.001
        self.angle = 0.0
        
        
    def update_pose(self,key_pos, goal):
        if self.goalReached(goal):
            print("\n-----Reach Goal!!-----\n")
            # sys.exit(1)
            return
        
        V_pos = self.cal_V_pos(key_pos)
        # print(key_pos)
        # print (V_pos)

        if self.id == 0:
            vector_list = self.nextVector(self.robot_pose, goal)
            # total_vector = sumOfListVectors(vector_list)
            total_vector = vector_list
            if total_vector[0] < 0.15 :
                total_vector[0] = 0.15
            # print(f'pre: {self.robot_pose}')
            self.robot_pose[0] += total_vector[0] * math.cos(total_vector[1])
            self.robot_pose[1] += total_vector[0] * math.sin(total_vector[1])
            # print(total_vector[0] * math.cos(total_vector[1]))
            # print(f'cur: {self.robot_pose}')
            self.angle = total_vector[1] -  math.pi/2
            self.key_pos = [self.robot_pose[0], self.robot_pose[1], self.angle]
            # print (self.key_pos)
            self.path.append([self.robot_pose[0], self.robot_pose[1]])
            
        else:
            # print(V_pos)
            scale = 200
            next = np.array([V_pos[self.id][0], V_pos[self.id][1]])

            # print (f'next: {next}')
            vector_list = self.nextVector(self.robot_pose, next)
                # total_vector = sumOfListVectors(vector_list)
            total_vector = vector_list
            # print(total_vector)
            self.robot_pose[0] += total_vector[0] * math.cos(total_vector[1])*scale
            self.robot_pose[1] += total_vector[0] * math.sin(total_vector[1])*scale
            self.angle = total_vector[1]
            self.path.append([self.robot_pose[0], self.robot_pose[1]])
            # print(10)
            # self.path.append([self.robot_pose[0], self.robot_pose[1]])
        # print(f'robot:{self.robot_pose}')

    def nextVector(self, cur, next):
        mag = computeDistance(cur, next, 0.0)
        angle = computeAngle(next,cur) 


        return np.array([mag * self.goal_gain, angle])
        
        
    def cal_V_pos(self, key_pos):
        V_pos = []
        V_pos.append(self.rotMatrix(key_pos[2], key_pos[0], key_pos[1]) @ np.array([0, 0, 1]) )
        V_pos.append(self.rotMatrix(key_pos[2], key_pos[0], key_pos[1]) @ np.array([-3, -3, 1]) )
        V_pos.append(self.rotMatrix(key_pos[2], key_pos[0], key_pos[1]) @ np.array([-1.5, -1.5, 1]) )
        
        V_pos.append(self.rotMatrix(key_pos[2], key_pos[0], key_pos[1]) @ np.array([1.5, -1.5, 1]) )
        V_pos.append(self.rotMatrix(key_pos[2], key_pos[0], key_pos[1]) @ np.array([3, -3, 1]) )
        return V_pos
    
    def rotMatrix(self, theta: float, h:float, k:float):
        return np.array([[math.cos(theta), -math.sin(theta), h],
                         [math.sin(theta), math.cos(theta), k],
                         [0, 0, 1]])

    def goalReached(self, goal):
        if computeDistance(self.robot_pose, goal, 0.0) < 0.5:
            self.goalReach_flag = True
            return True
        else:
            self.goalReach_flag = False
    def getCurrent(self): return self.robot_pose.copy()
    def getCurrentX(self): return self.robot_pose[0]
    def getCurrentY(self): return self.robot_pose[1]




        
    
