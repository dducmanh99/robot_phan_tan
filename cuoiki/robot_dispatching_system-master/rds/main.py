from env.env import Environment
from utlis.utlis import *
from matplotlib.animation import FuncAnimation
data_folder = "G:/My Drive/Temas/robot_dispatching_system/rds/data/simple_rds"
figure, map_visual = plt.subplots(subplot_kw={'aspect': 'equal'})

env = Environment(data_folder, figure, map_visual)
def update(frame):
    env.system_manager.taskAllocationAndPlanning()
    for robot in env.robots:
        robot.control()
    env.map_visual.set_title("Time step {}".format(frame + 1))
    env.visualize()
    

ani = FuncAnimation(fig=env.figure, func=update, frames=1000, interval=5) # type: ignore
# ani.save(filename=data_folder + "/simulation.gif", writer="pillow")
plt.tight_layout()
plt.show()