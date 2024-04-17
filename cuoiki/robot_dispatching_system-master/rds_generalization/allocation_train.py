from utlis.utlis import *
from env.env import Environment
from manager.server import RDSServer
import os
data_folder = "data/30x20"
model_folder = 'data/model'
num_of_task = 1000
task_data_path = os.path.join(data_folder, 'task_data', '{}_task.txt'.format(num_of_task))
figure, map_visual = plt.subplots(subplot_kw={'aspect': 'equal'})
env = Environment(data_folder, num_of_robot= 20, robot_max_speed= 1.0, robot_max_payload= 200, figure=figure, map_visual= map_visual)
server = RDSServer(env= env, task_data_path= task_data_path, num_task_in_queue= 50, 
                    num_zone_in_cols= 5, num_zone_in_rows= 5, model_folder= model_folder)

num_of_iteration = 1000
for iter in range(num_of_iteration):
    while True:
        training_state = server.task_allocation.training(iter, 10)
        env.aStarControl(waiting_time= 30)
        if training_state == True:
            break

