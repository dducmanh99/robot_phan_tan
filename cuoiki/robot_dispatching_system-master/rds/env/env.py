from env.factory_map import FactoryMap
from env.robot import Robot
from utlis.utlis import *
from env.system_manager import SystemManager
class Environment:
    def __init__(self, data_folder:str, figure: figure.Figure, map_visual: axs.Axes):
        self.dt = 0.1
        self.single_line_width = 0.9
        self.double_line_width = 2.0
        self.point_line_length = 1.2
        self.data_folder = data_folder
        self.figure = figure 
        self.map_visual:axs.Axes = map_visual
        self.factory_map = FactoryMap(data_folder, self.single_line_width, self.double_line_width, self.point_line_length)
        self.graph = self.factory_map.graph
        self.zone_vertices = self.factory_map.zone_vertices
        self.factory_map.visualizeMap(self.map_visual)
        init_poses = np.loadtxt(self.data_folder + "/init_pose.txt")
        self.num_of_robots = init_poses.shape[0]
        self.robots: List[Robot] = []
        self.export_tasks: List[Task] = [] # provide production materials
        self.import_tasks: List[Task] = [] # pull empty pallet
        for id in range(self.num_of_robots):
            self.robots.append(Robot(self.dt, id, init_poses[id], 100, self.map_visual))
        self.system_manager: SystemManager = SystemManager(data_folder, self.robots, self.graph, self.zone_vertices)
    def visualize(self):
        for robot in self.robots:
            robot.robotVisualization()