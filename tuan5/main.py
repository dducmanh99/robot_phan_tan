from utility import *
from agent import Agent
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from typing import List

#
num_of_agent = 30
start = np.array([0, -30])
goal = np.array([0, 30])
range_start = 5
size_map = 50
# robot
# goal = np.array([0, 10])
color = ['blue','green','yellow','purple','orange','pink','brown','lime','gray','cyan','yellowgreen','magenta','hotpink','skyblue']
robot_radius = 0.3
# set agents known goal
num_agent_known_goal = 5
num_agent_known_goal_ = num_agent_known_goal
status_agents = []
for i in range(num_of_agent):
    status = np.random.randint(0, 2)
    if num_agent_known_goal > 0:
        status_agents.append(1)
        num_agent_known_goal -= 1
    else:
        status_agents.append(0)

# range effects of robot
range_avoid = 3 * robot_radius
range_static = 5 * robot_radius 
range_friend = 7 * robot_radius

fig, ax = plt.subplots(subplot_kw={'aspect':'equal'})
ax.set_xlim(-size_map,size_map)
ax.set_ylim(-size_map,size_map)
ax.set_title('Boid Flocking algorithm with {} robots and {} robot known Goal'.format(num_of_agent, num_agent_known_goal_))
ax.grid(True)
# visual goal
goal_circle = Circle((goal[0], goal[1]), radius=0.4, color='red')
ax.add_patch(goal_circle)
plt.annotate("Goal", xy=(goal[0] + 0.4, goal[1]))

print('Start Boid Flocking algorithm with {} robots'.format(num_of_agent))

agents: List[Agent] = []
robot_visuals = []
path_visuals = []

for i in range(num_of_agent):
    x = np.random.uniform(start[0] - range_start, start[0] + range_start)
    y = np.random.uniform(start[1] - range_start, start[1] + range_start)
    color_ = color[np.random.randint(0,9)]
    if status_agents[i] == 1:
        agents.append(Agent(i, True, np.array([x, y]), goal, color_))
    else:
        agents.append(Agent(i, False, np.array([x, y]), goal, color_))
    robot_visuals.append(agents[-1].circle)
    path = np.array(agents[-1].path)

    # line = ax.plot(path[:, 0], path[:, 1], '-', c= agents[-1].color)[0]
    # path_visuals.append(line)
    
    ax.add_patch(agents[-1].circle)

for agent in agents:
    agent.agents = agents

def update(frame):
    agent_pose: List[np.ndarray] = []
    for agent in agents:
        agent_pose.append(agent.getCurrent())
    for agent in agents:
        # agent.updatePose()
        agent.updatePose(agent_pose)
    for i, visual in enumerate(robot_visuals):
        visual.center = (agents[i].getCurrentX(), agents[i].getCurrentY()) 
    for i, visual in enumerate(path_visuals):
        path = np.array(agents[i].path)
        visual.set_xdata(path[:,0])
        visual.set_ydata(path[:,1])

animation = FuncAnimation(fig=fig, func=update, frames=1500, interval=50)  

animation.save(filename="./tuan5/{}_agents.gif".format(num_of_agent), writer='pillow') 
# plt.tight_layout()
# plt.show()