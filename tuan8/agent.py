import dis
import numpy as np
from utlis import *

class Agent:
    def __init__(self, init_position: np.ndarray, env_map: np.ndarray, vel_gain: float, 
                p_best_gain: float, g_best_gain: float, transmitter_power:float = 10e-3, 
                wavelength:float = 0.125, transmitter_gain:float = 1, receiver_gain:float = 1, 
                resolution = 0.05):
        self.pos = init_position.copy().astype(np.int16)
        self.p_best_pos = init_position.copy().astype(np.int16)
        self.vel = np.random.randint(0, 5, (self.pos.shape[0], 2)).astype(np.int16)
        self.p_best_value = env_map.shape[0] * env_map.shape[1]
        self.env_map: np.ndarray = env_map.copy()
        self.map: np.ndarray = env_map.copy()
        self.transmitter_power = transmitter_power
        self.wavelength = wavelength
        self.transmitter_gain = transmitter_gain
        self.receiver_gain = receiver_gain
        self.resolution: float = resolution
        self.vel_gain = vel_gain
        self.p_best_gain = p_best_gain  
        self.g_best_gain = g_best_gain
        self.max_vel = 5
        
    def calculatePBest(self):
        counter = 0
        self.map = self.env_map.copy()
        for y in range(self.env_map.shape[0]):
            for x in range(self.env_map.shape[1]):
                if self.env_map[y, x] == WALL_POWER: continue
                self.map[y, x] = max(WALL_POWER,self.calculateRSSI(x, y))
                if max(WALL_POWER, self.calculateRSSI(x, y)) < -70: 
                    counter += 1
        if counter < self.p_best_value:
            self.p_best_pos = self.pos.copy().astype(np.int16)
            self.p_best_value = counter
            
    def calculateRSSI(self, x: int, y: int):
        rssi_list = []
        for ap in self.pos:
            dist = EuclideanDistance(ap, [x, y])*self.resolution
            if dist < 0.1:
                rssi_list.append(10*math.log10(self.transmitter_power))
            else:
                # free_loss = self.transmitter_power * self.transmitter_gain * np.random.uniform(0.8, 1) * self.receiver_gain *np.random.uniform(0.8, 1) * (self.wavelength/(4*math.pi*dist**2))
                free_loss = self.transmitter_power * self.transmitter_gain * self.receiver_gain  * (self.wavelength/(4*math.pi*dist**2))

                rssi_list.append(10*math.log10(free_loss))

        return max(rssi_list)

    def calculateNumberOfWalls(self, x1: int, y1: int, x2: int, y2:int):
        cells = bresenham([x1, y1],[x2, y2])
        if len(cells) == 0: return 0.0
        else:
            counter = 0
            p = [0, 0]
            for cell in cells:
                if cell[1] < 0 or cell[1] >= self.env_map.shape[0]: continue
                if cell[0] < 0 or cell[0] >= self.env_map.shape[1]: continue 
                if self.env_map[cell[1], cell[0]] == WALL_POWER:
                    if counter == 0:
                        p = [cell[0], cell[1]]
                        counter += 1
                    else:
                        if EuclideanDistance(p, [cell[0], cell[1]]) > 3:
                            p = [cell[0], cell[1]]
                            counter += 1
            return counter
    
    def calculateNextPosition(self, g_best_pose: np.ndarray):
        vel1 = self.vel_gain * self.vel
        vel2 = self.p_best_gain * np.random.rand()*(self.p_best_pos - self.pos)
        vel3 = self.g_best_gain * np.random.rand()*(g_best_pose - self.pos)
        self.vel = (vel1 + vel2 + vel3).astype(np.int16)
        self.pos = self.pos + self.vel
        for i in range(self.pos.shape[0]):
            if self.pos[i,0] < 0: self.pos[i,0] = 0
            if self.pos[i,1] < 0: self.pos[i,1] = 0
            if self.pos[i,0] > self.env_map.shape[1]-1: self.pos[i,0] = self.env_map.shape[1]-1
            if self.pos[i,1] > self.env_map.shape[0]-1: self.pos[i,1] = self.env_map.shape[0]-1

    
    def limitVelocity(self, vel:np.ndarray):
        speed = math.hypot(vel[0], vel[1])
        if speed > self.max_vel:
            limited_speed = (vel / speed) * self.max_vel
            return limited_speed
        return vel

    def limitVelocityList(self, vel_list: np.ndarray):
        for i in range(vel_list.shape[0]):
            vel_list[i] = self.limitVelocity(vel_list[i])
            
        return vel_list