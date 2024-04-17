from sympy import true
from utlis.utlis import *
from env.env import Environment
from manager.server import RDSServer
from matplotlib.animation import FuncAnimation
import os
data_folder = "./cuoiki/robot_dispatching_system-master/data/30x20"
model_folder = './cuoiki/robot_dispatching_system-master/data/model'
num_of_task = 50
task_data_path = os.path.join(data_folder, 'task_data', '{}_task.txt'.format(num_of_task))
figure, map_visual = plt.subplots(subplot_kw={'aspect': 'equal'})
env = Environment(data_folder, num_of_robot= 20, robot_max_speed= 1.0, robot_max_payload= 200, figure=figure, map_visual= map_visual)
server = RDSServer(env= env, task_data_path= task_data_path, num_task_in_queue= 20, 
                    num_zone_in_cols= 5, num_zone_in_rows= 5, model_folder= model_folder)

def update(frame):
    testing_state, test_reward = server.allocationTesting()
    if testing_state == True:
        print("Testing reward:", test_reward)
    map_visual.set_title('Time {} s'.format(round((frame + 1) * 0.1, 1)))
    env.aStarControl(waiting_time= 30)
    env.visualize()
    
ani = FuncAnimation(fig=env.figure, func=update, frames=1000, interval=100, repeat= True) # type: ignore
plt.tight_layout()
plt.xticks([])
plt.yticks([])
plt.show()
