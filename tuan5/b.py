
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from typing import List
from matplotlib.axes import Axes

def EuclideanDistance(p1: np.ndarray, p2: np.ndarray):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
color = ['red', 'green', 'blue', 'black', 'orange', 'purple', 'brown'] 
class Agent:
    def __init__(self, id: int, init_pose: np.ndarray, separation_range: float, cohesion_range: float, alignment_range: float,
                goal_gain: float, cohesion_gain: float, separation_gain: float, alignment_gain: float, max_velocity: float, visual: Axes, 
                map_length: float, map_width: float, robot_radius:float = 0.3):
        self.id: int = id
        self.pose: np.ndarray = init_pose.copy()
        self.vel:np.ndarray = np.zeros(2)
        self.separation_range = separation_range + 2 * robot_radius
        self.cohesion_range = cohesion_range + 2 * robot_radius
        self.alignment_range = alignment_range + 2 * robot_radius
        self.goal_gain = goal_gain
        self.cohesion_gain = cohesion_gain
        self.separation_gain = separation_gain
        self.alignment_gain = alignment_gain
        self.max_vel = max_velocity
        self.visual: Axes = visual
        self.radius = robot_radius
        self.map_length = map_length
        self.map_width = map_width
        self.color: str = color[id%len(color)]
        self.circle: Circle = Circle((self.pose[0], self.pose[1]), radius= self.radius, 
                                    edgecolor=self.color, facecolor=self.color)
        visual.add_patch(self.circle)
        self.path_x = []
        self.path_y = []
        self.path_visual: Line2D = visual.plot([], [], '-', c= self.color, lw = 0.4)[0]
        self.agents: List[Agent] = []
        self.angle_list: List[float] = []
        
    def run(self, vel: np.ndarray):
        self.pose = self.pose + vel
    
    def reynoldBehavior(self, goal: np.ndarray):
        if self.id % 10 == 0:
            self.goToGoalBehavior(goal)
        self.cohesionBehavior()
        self.separationBehavior()
        self.alignmentBehavior()
        self.keepWithinBound()
        return self.limitVelocity(self.vel)
    
    def goToGoalBehavior(self, goal: np.ndarray):
        self.vel = (goal - self.pose) * self.goal_gain
    
    def separationBehavior(self):
        move = np.zeros(2)
        for agent in self.agents:
            if EuclideanDistance(self.pose, agent.pose) < self.separation_range:
                move = move + self.pose - agent.pose
        self.vel = self.vel + move * self.separation_gain
        
    def alignmentBehavior(self):
        avg = np.zeros(2)
        count = 0
        for agent in self.agents:
            if EuclideanDistance(self.pose, agent.pose) < self.alignment_range:
                avg = avg + agent.vel
                count += 1
        if count > 0:
            avg = avg / count
            self.vel = self.vel + (avg - self.vel) * self.alignment_gain
    def cohesionBehavior(self):
        center = np.zeros(2)
        count = 0
        for agent in self.agents:
            if self.separation_range < EuclideanDistance(self.pose, agent.pose) <= self.cohesion_range:
                center = center + agent.pose
                count += 1
        if count > 0:
            center = center/ count
            self.vel = self.vel + (center - self.pose) * self.cohesion_gain
    
    def keepWithinBound(self):
        turn_factor = 0.2
        if self.pose[0] < -(self.map_length - 5.0):
            self.vel[0] += turn_factor
        if self.pose[0] > (self.map_length - 5.0):
            self.vel[0] -= turn_factor
        if self.pose[1] < -(self.map_width - 5.0):
            self.vel[1] += turn_factor
        if self.pose[1] > (self.map_width - 5.0):
            self.vel[1] -= turn_factor
            
    def visualize(self):
        self.path_x.append(self.pose[0])
        self.path_y.append(self.pose[1])
        self.circle.set_center((self.pose[0], self.pose[1]))
        if self.id %10 == 0:
            self.path_visual.set_xdata(self.path_x)
            self.path_visual.set_ydata(self.path_y)
        # path_length = 20
        # if len(self.path_x) < path_length:
        #     self.path_visual.set_xdata(self.path_x)
        #     self.path_visual.set_ydata(self.path_y)
        # else:
        #     self.path_visual.set_xdata(self.path_x[len(self.path_x) - path_length:])
        #     self.path_visual.set_ydata(self.path_y[len(self.path_y) - path_length:])
    def limitVelocity(self, vel:np.ndarray):
        speed = math.hypot(vel[0], vel[1])
        if speed > self.max_vel:
            limited_speed = (vel / speed) * self.max_vel
            return limited_speed
        return vel
        
figure, map_visual = plt.subplots(subplot_kw={'aspect': 'equal'})
map_visual: Axes = map_visual
map_width = 60
map_length = 80
map_visual.set_xlim(-map_length, map_length)
map_visual.set_ylim(-map_width, map_width)

num_of_agent = 50
start_pose = [0, 0]
agents: List[Agent] = []
separation_range: float = 2.0
cohesion_range: float = 3.0
alignment_range: float = 5.0
goal_gain = 0.2
cohesion_gain: float = 0.1
separation_gain: float = 2.0
alignment_gain: float = 1.0
max_velocity: float = 1.0
radius: float = 0.3
angle_step = math.pi * 2 / num_of_agent
x_list = []
y_list = []
for i in range(num_of_agent):
    x = np.random.uniform(-10, 10)
    y = np.random.uniform(-10, 10)
    agents.append(Agent(i, np.array([x, y]), separation_range, cohesion_range, alignment_range, 
                        goal_gain, cohesion_gain, separation_gain, alignment_gain, max_velocity, 
                        map_visual, map_length, map_width, radius))
        
for agent in agents:
    agent.agents = agents

square_path = np.array([[-60, -40], [-60, 40], [60, 40], [60, -40], [-60, -40]])
path = np.array([[-60, -40], [-40, 40], [-20, -40], [0, 40], [20, -40], [40, 40], [60, -40]])
path = np.concatenate((path, np.array([[70, 0], [60, 40], [40, -40], [20, 40], [0, -40], [-20, 40], [-40, -40], [-60, 40], [-70, 0],[-60, -40]])))
waypoints = path
map_visual.plot(waypoints[:, 0], waypoints[:, 1], ls='-', marker='*', c='grey', mec='green', mfc = 'green')
waypoint_id = 0
def nextWaypoint(agents: List[Agent], waypoint: np.ndarray):
    for agent in agents:
        if EuclideanDistance(agent.pose, waypoint) < 0.5:
            return True
    return False

def update(frame):
    global waypoints, waypoint_id
    vel_list: List[np.ndarray] = []
    if nextWaypoint(agents, waypoints[waypoint_id]):
        if waypoint_id >= len(waypoints) - 1:
            waypoint_id = 0
        else:
            waypoint_id += 1
    for agent in agents:
        vel_list.append(agent.reynoldBehavior(waypoints[waypoint_id]))
    for agent in agents:
        if vel_list[agent.id][0] == 0.0  and vel_list[agent.id][1] == 0:
            agent.run(np.random.rand(2))
        else:
            agent.run(vel_list[agent.id])
        agent.visualize()
        
ani = FuncAnimation(fig=figure, func=update, frames=500, interval=20, repeat = False) # type:ignore
plt.grid(True)
plt.tight_layout()
# ani.save(filename="zic_zac_{}_agent.gif".format(num_of_agent), writer="pillow")
# plt.savefig(fname="zic_zac_{}_agent.png".format(num_of_agent), dpi= 500)
plt.show()