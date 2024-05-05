from utility import *

class Environment:
    def __init__(self, map_length: float, map_width: float, corridor_width: float, 
                zoom_length: float, num_up_zoom: int, num_down_zoom: int, map_visual: Axes):
        self.map_length: float = map_length
        self.map_width: float = map_width
        self.map_boundary: np.ndarray = np.array(calculateRectangleCoordinate(0.0, 0.0, 0.0, map_length, map_width))
        self.corridor_boundary: np.ndarray = np.array(calculateRectangleCoordinate(0.0, 0.0, 0.0, map_length, corridor_width))
        self.corridor_width: float = corridor_width
        self.zoom_width: float = 0.5 * (map_width - corridor_width)
        self.zoom_length: float = zoom_length
        self.num_up_zoom: int = num_up_zoom
        self.num_down_zoom: int = num_down_zoom
        self.up_zoom_centers: List[np.ndarray] = []
        self.up_zoom_coords: List[np.ndarray] = []
        self.down_zoom_coords: List[np.ndarray] = []
        self.down_zoom_coords: List[np.ndarray] = []
        self.up_block_centers: List[np.ndarray] = []
        self.up_block_coords: List[np.ndarray] = []
        self.down_block_centers: List[np.ndarray] = []
        self.down_block_coords: List[np.ndarray] = []
        self.map_visual: Axes = map_visual
        self.calculateUpZoomAndBlock()
        self.calculateDownZoomAndBlock()
        self.obstacle_coords: List[np.ndarray] = []
        self.obstacle_centers: List[np.ndarray] = []
        for center, block in zip(self.up_block_centers, self.up_block_coords):
            self.obstacle_centers.append(center)
            self.obstacle_coords.append(block)
        for center, block in zip(self.down_block_centers, self.down_block_coords):
            self.obstacle_centers.append(center)
            self.obstacle_coords.append(block)
        
        self.visualize()
    def calculateUpZoomAndBlock(self):
        y = self.corridor_width/2 + self.zoom_width/2
        step_x = self.map_length/(self.num_up_zoom + 1)
        x_list = [-self.map_length/2]
        for i in range(1, self.num_up_zoom+1):
            x_zoom = step_x * i - self.map_length/2
            x_list.append(x_zoom)
            self.up_zoom_centers.append(np.array([x_zoom, y]))
            self.up_zoom_coords.append(np.array(calculateRectangleCoordinate(x_zoom, y, 0.0, self.zoom_length, self.zoom_width)))
        x_list.append(self.map_length/2)
        for i in range(len(x_list) - 1):
            x_block = 0.5*(x_list[i] + x_list[i+1])
            block_length = step_x - self.zoom_length
            if i == 0:
                x_block = 0.5*(x_list[i] + x_list[i+1]) - self.zoom_length/4
                block_length = step_x - self.zoom_length/2
            elif i == len(x_list) - 2:
                x_block = 0.5*(x_list[i] + x_list[i+1]) + self.zoom_length/4
                block_length = step_x - self.zoom_length/2
            
            self.up_block_centers.append(np.array([x_block, y]))
            self.up_block_coords.append(np.array(calculateRectangleCoordinate(x_block, y, 0.0, block_length, self.zoom_width)))
    def calculateDownZoomAndBlock(self):
        y = -self.corridor_width/2 - self.zoom_width/2
        step_x = self.map_length/(self.num_down_zoom + 1)
        x_list = [-self.map_length/2]
        for i in range(1, self.num_down_zoom+1):
            x_zoom = step_x * i - self.map_length/2
            x_list.append(x_zoom)
            self.up_zoom_centers.append(np.array([x_zoom, y]))
            self.up_zoom_coords.append(np.array(calculateRectangleCoordinate(x_zoom, y, 0.0, self.zoom_length, self.zoom_width)))
        x_list.append(self.map_length/2)
        for i in range(len(x_list) - 1):
            x_block = 0.5*(x_list[i] + x_list[i+1])
            block_length = step_x - self.zoom_length
            if i == 0:
                x_block = 0.5*(x_list[i] + x_list[i+1]) - self.zoom_length/4
                block_length = step_x - self.zoom_length/2
            elif i == len(x_list) - 2:
                x_block = 0.5*(x_list[i] + x_list[i+1]) + self.zoom_length/4
                block_length = step_x - self.zoom_length/2
            
            self.up_block_centers.append(np.array([x_block, y]))
            self.up_block_coords.append(np.array(calculateRectangleCoordinate(x_block, y, 0.0, block_length, self.zoom_width)))
    def visualize(self):
        self.map_boundary[0] = np.array([-self.map_length/2, -self.corridor_width/2])
        self.map_boundary = np.concatenate((self.map_boundary, np.array([[-self.map_length/2, self.corridor_width/2]])), axis=0)
        self.map_visual.plot(self.map_boundary[:, 0], self.map_boundary[:, 1], color='black', ls='-')
        for obstacle in self.obstacle_coords:
            self.map_visual.fill(obstacle[:, 0], obstacle[:, 1], color='black')