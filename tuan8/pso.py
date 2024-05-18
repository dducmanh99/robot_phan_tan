from utlis import *
from agent import Agent
from map import Map
import time
class PSO:
    def __init__(self, map: Map, num_agents: int, num_aps: int, transmitter_power: float, 
                wavelength: float, transmitter_gain: float, receiver_gain: float, vel_gain: float,
                p_best_gain: float, g_best_gain: float, resolution: float):
        self.map = map
        self.agents: List[Agent] = []
        self.num_aps: int = num_aps
        self.num_agents = num_agents

        for _ in range(num_agents):
            init_pose = []
            for _ in range(num_aps):
                init_pose.append([np.random.randint(10, map.map_width-10), np.random.randint(10, map.map_height-10)])
            self.agents.append(Agent(np.array(init_pose), map.map, vel_gain, p_best_gain, 
                                    g_best_gain, transmitter_power, wavelength, 
                                    transmitter_gain, receiver_gain, resolution))
        # print(len(self.agents))
        self.g_best_value = map.map.shape[0] * map.map.shape[1]
        self.g_best_pos = np.zeros((num_aps, 2))
        self.g_best_map = map.map.copy()
        self.getGBest()
        
    def getGBest(self):
        for agent in self.agents:
            agent.calculatePBest()
            if agent.p_best_value < self.g_best_value:
                self.g_best_value = agent.p_best_value
                self.g_best_pos = agent.pos.copy()
                self.g_best_map = agent.map.copy()
        
    def run(self, num_of_iterations):
        g_best_list = []
        for iter in range(num_of_iterations):
            self.getGBest()
            g_best_list.append(self.g_best_value)
            np.savetxt('g_best_value_{}_aps.txt'.format(self.num_aps), np.array(g_best_list), fmt='%d')
            np.savetxt('g_best_map_{}_aps.txt'.format(self.num_aps), self.g_best_map.copy(), fmt='%.2f')
            time_ = time.time()
            print(iter, time_, self.g_best_value)
            for agent in self.agents:
                agent.calculateNextPosition(self.g_best_pos.copy())
            
