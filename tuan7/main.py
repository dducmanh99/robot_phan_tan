from env import Environment
from swarm import Swarm
from utility import *

fig, map_visual = plt.subplots(subplot_kw={'aspect': 'equal'})
map_visual: Axes = map_visual

map_width = 10
map_length = 20
corridor_width: float = 2.5
zoom_length: float= 2
num_up_zoom: int = 4
num_down_zoom: int = 3 
env = Environment(map_length, map_width, corridor_width, zoom_length, num_up_zoom, num_down_zoom, map_visual)

num_agent: int = 20
agent_in_rows: int = 2
agent_init_distance: float = 0.7
coverage_range: float = 2
first_agent_pose: np.ndarray = np.array([-3.0, -0.5])
max_velocity: float = 1.0

swarm = Swarm(env, num_agent, first_agent_pose, agent_in_rows, coverage_range, max_velocity, agent_init_distance, map_visual)
def update(frame):
    if frame % 200 == 199:
        print("Time {} s".format((frame + 1)*0.1))
    swarm.run()
    swarm.visualize()
ani = FuncAnimation(fig=fig, func=update, frames=2000, interval= 50, repeat= False) # type:ignore

plt.show()