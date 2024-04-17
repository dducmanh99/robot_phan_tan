from utlis.utlis import *
from manager.task_generate import TaskGenFromData
from manager.task_allocation import TaskAllocation
from env.env import Environment

class RDSServer:
    def __init__(self, env: Environment, task_data_path: str, num_task_in_queue: int, 
                num_zone_in_cols: int, num_zone_in_rows: int, model_folder: str):
        self.env: Environment = env
        self.factory_graph = self.env.graph
        self.factory_graph.createZone(self.env.factory_map.map_center[0], self.env.factory_map.map_center[1], 
                                        self.env.factory_map.map_length, self.env.factory_map.map_width, 
                                        num_zone_in_cols, num_zone_in_rows)
        self.robots = self.env.robots
        self.task_generator = TaskGenFromData(task_data_path, num_task_in_queue, self.factory_graph)
        self.task_allocation = TaskAllocation(self.robots, self.task_generator, self.factory_graph, model_folder)
    
    def allocationTesting(self):
        return self.task_allocation.testing()
    def allocationTraining(self, iter: int, save_interval: int = 10):
        self.task_allocation.training(iter, save_interval)