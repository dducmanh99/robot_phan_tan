from utility import *

class Agent: 
    def __init__(self, id:int, init_pos:np.ndarray,
                 visual:Axes, robot_radius:float=0.3, max_vel:float=0.2):
        self.id = id 
        self.global_pos : np.ndarray = init_pos.copy()
        self.local_pos : np.ndarray = np.zeros(2)
        self.theta:float =0.0
        self.max_vel = max_vel
        self.visual:Axes = visual
        self.radius = robot_radius
        self.agent_visual: Circle = Circle((self.global_pos[0], self.global_pos[1]), radius= self.radius, color='red')
        visual.add_patch(self.agent_visual)
        self.agent_text: Text = visual.text(self.global_pos[0], self.global_pos[1], str(self.id), c='black', size=5.0)

        self.goalList :np.ndarray = np.zeros(2)
        self.vel:np.ndarray = np.zeros(2)
        self.state:int = 0 #0 free 1gotogoal 2 reachgoal
    
    
    def run(self):
        self.global_pos[0] = self.global_pos[0] + self.vel[0] * 0.1
        self.global_pos[1] = self.global_pos[1] + self.vel[1] * 0.1
        self.theta = math.atan2(self.vel[1], self.vel[0])

    def visualize(self):
        self.agent_visual.set_center((self.global_pos[0], self.global_pos[1]))
        self.agent_text.set_x(self.global_pos[0])
        self.agent_text.set_y(self.global_pos[1])

    def limitVelocity(self, vel:np.ndarray):
        speed = math.hypot(vel[0], vel[1])
        if speed > self.max_vel:
            limited_speed = (vel / speed) * self.max_vel
            return limited_speed
        return vel
    
    def checkState(self):
        dis = computeDistance(self.global_pos, self.goalList,0.0)
        if abs(dis) < 0.3:
            self.state = 2
        elif self.goalList[0] !=0 or self.goalList[1] !=0:
            self.state = 1
    
    def limitPos(self):
        if self.global_pos[0] > 33 or self.global_pos[0] < -4:
            return True
        if self.global_pos[1] > 17 or self.global_pos[0] < -5:
            return True
        return False
    
