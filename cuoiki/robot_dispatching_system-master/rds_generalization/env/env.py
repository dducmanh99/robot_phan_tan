from utlis.utlis import *
from env.factory_map import FactoryMap
from env.robot import Robot
class Environment:
    def __init__(self, data_folder:str, num_of_robot: int, robot_max_speed: float, robot_max_payload: float,
                figure: figure.Figure, map_visual: axs.Axes):
        self.dt = 0.1
        self.single_line_width = 0.9
        self.double_line_width = 2.0
        self.point_line_length = 1.2
        self.data_folder = data_folder
        self.figure = figure 
        self.map_visual:axs.Axes = map_visual
        self.factory_map = FactoryMap(data_folder, self.single_line_width, self.double_line_width, self.point_line_length)
        self.graph = self.factory_map.graph.copy()
        self.home_vertices = self.factory_map.waiting_vertices.copy()
        self.factory_map.visualizeMap(self.map_visual)
        num_of_home = 0
        for vertices in self.home_vertices:
            num_of_home += len(vertices)
        assert num_of_robot <= num_of_home
        self.num_of_robot = num_of_robot
        self.robot_max_speed = robot_max_speed
        self.robot_max_payload = robot_max_payload
        home_id_list: List[np.ndarray] = []
        for i in range(len(self.home_vertices)):
            home_id_list.append(np.arange(0, len(self.home_vertices[i])))
        
        self.robots: List[Robot] = []
        for id in range(self.num_of_robot):
            for i in range(len(self.home_vertices)):
                if id % (len(self.home_vertices)) == i:
                    home_id = np.random.choice(home_id_list[i])
                    home_id_list[i] = np.delete(home_id_list[i], np.where(home_id_list[i] == home_id))
                    self.robots.append(Robot(self.dt, id, self.home_vertices[i-1][home_id], math.pi/2, 
                                    self.robot_max_speed, self.robot_max_payload, self.map_visual))

    def aStarControl(self, waiting_time: int):
        for robot in self.robots:
            robot.aStarControl(waiting_time)
    def control(self, waiting_time: int):
        for robot in self.robots:
            robot.control(waiting_time)
        
    def visualize(self):
        for robot in self.robots:
            robot.robotVisualization()