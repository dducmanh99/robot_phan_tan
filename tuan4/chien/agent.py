from ultis import *
from a import Agent
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from typing import List

color = ['red', 'green', 'blue', 'black', 'orange', 'purple', 'brown'] 

num_of_agents = 10
radius = 10
angle_step = math.pi * 2 / num_of_agents

fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)
ax.set_title('{} agent visualization'.format(num_of_agents))
ax.grid(True)

agents: List[Agent] = []
robot_visuals = []
trajectory_visuals = []
for i in range(num_of_agents):
    x = radius * math.cos(angle_step * i)
    y = radius * math.sin(angle_step * i)
    agents.append(Agent(i, np.array([x, y]), np.array([-x, -y])))
    robot_visuals.append(agents[-1].circle)
    trajectory = np.array(agents[-1].trajectory)
    line = ax.plot(trajectory[:, 0], trajectory[:, 1], '-', c= agents[-1].color)[0]
    trajectory_visuals.append(line)
    ax.add_patch(agents[-1].circle)

#Update functions for the animation
def update(frame):
    agent_pos: List[np.ndarray] = []
    for agent in agents:
        agent_pos.append(agent.getCurrent())
    for agent in agents:
        agent.updatePose(agent_pos)
    for i, visual in enumerate(robot_visuals):
        visual.center = (agents[i].getCurrentX(), agents[i].getCurrentY())  # Update circle center position
    for i, visual in enumerate(trajectory_visuals):  
        trajectory = np.array(agents[i].trajectory)
        visual.set_xdata(trajectory[:, 0])
        visual.set_ydata(trajectory[:, 1])

# Create the animation
ani = FuncAnimation(fig=fig, func=update, frames=1500, interval=50)
# ani.save(filename="{}_agent.gif".format(num_of_agents), writer="pillow")
plt.show()