from utility import *
import sys 

key_color = 'black'

class Agent:
    def __init__(self,  id: int, init_pose:np.ndarray, init_angleKey:float, color: str,
                 robot_radius:float=0.5, range_avoid:float=1.5, 
                 goal_gain:float=0.001, avoid_gain:float=0.001):
        
        self.id = id 
        self.robot_pose = init_pose.copy()
        
        self.color = color
        self.robot_radius = robot_radius
        self.range_avoid = range_avoid
        self.goal_id = 0

        self.path = [[init_pose[0], init_pose[1]]]
        self.key_pos = []

        if (self.id == 0):
            self.circle = Circle((self.robot_pose[0], self.robot_pose[1]), radius= self.robot_radius,
                             edgecolor= key_color, facecolor= key_color) 
            angle = init_angleKey 
            
            self.key_pos = [init_pose[0], init_pose[1], angle]
            
        else:
            self.circle = Circle((self.robot_pose[0], self.robot_pose[1]), radius= self.robot_radius,
                             edgecolor= self.color, facecolor= self.color)
        
        self.angle = 0.0
        self.goalReach_flag = False
        self.goal_gain = goal_gain
        self.avoid_gain = avoid_gain
        self.agents: List[Agent] = []
         
    def update_pose(self,key_pos, goal, agents_pos: List[np.ndarray], obs: List[np.ndarray]):
        if self.goalReached(goal):
            print(f'\n-----Reach Goal {self.goal_id} !!-----\n')
            self.goal_id += 1 
            # sys.exit(1) # close
            return
        
        V_pos = self.cal_V_pos(key_pos)
        # print (V_pos)

        vector_list = []
        for i in range(len(obs)):
            dist = computeDistance(self.robot_pose, obs[i], 0.0)
            if dist < self.range_avoid:
                    vector_list.append(self.avoidVector(obs[i]))

        if self.id == 0:
            next = self.nextVector(self.robot_pose, goal)
            vector_list.append(next)

            total_vector = sumOfListVectors(vector_list)
            if total_vector[0] < 0.15 :
                total_vector[0] = 0.15
            
            self.robot_pose[0] += total_vector[0] * math.cos(total_vector[1])
            self.robot_pose[1] += total_vector[0] * math.sin(total_vector[1])
            
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
            nextV = self.nextVector(self.robot_pose, next)
            vector_list.append(nextV)
            # print(vector_list)
            for i in range(len(agents_pos)):
                if i == self.id: continue
                dist = computeDistance(self.robot_pose, agents_pos[i], 0.0)
                # print(f'dist: {dist}')
                if dist < self.range_avoid:
                    # print(f'dist:{dist}')
                    vector_list.append(self.avoidVector(agents_pos[i]))
            
            total_vector = sumOfListVectors(vector_list)
            # print(total_vector)
            self.robot_pose[0] += total_vector[0] * math.cos(total_vector[1])*scale
            self.robot_pose[1] += total_vector[0] * math.sin(total_vector[1])*scale
            self.angle = total_vector[1]
            self.path.append([self.robot_pose[0], self.robot_pose[1]])
            
            # self.path.append([self.robot_pose[0], self.robot_pose[1]])
        # print(f'robot:{self.robot_pose}')

    def avoidVector(self, other_pose: np.ndarray):
        dist = computeDistance(self.robot_pose, other_pose, 0.0)
        mag = (self.range_avoid - dist)/ (self.range_avoid - 2 * self.robot_radius)
        angle = computeAngle(self.robot_pose, other_pose)

        return np.array([mag * self.avoid_gain, angle])

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




        
    
