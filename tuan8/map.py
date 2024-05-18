from utlis import *

class Map:
    def __init__(self, map_height: int, map_width: int, corridor_length: int):
        self.map_height = map_height
        self.map_width = map_width
        self.corridor_length = corridor_length
        self.map = np.zeros((map_height, map_width))
        for i in range(map_height):
            self.map[i, 0] = WALL_POWER
            self.map[i, map_width-1] = WALL_POWER
        for j in range(map_width):
            self.map[0, j] = WALL_POWER
            self.map[map_height-1, j] = WALL_POWER
        self.createCorridor()
        self.createRoom()

    def createCorridor(self):
        zoom_center_y = int(self.map_height/2)
        for i in range(self.map_width):
            self.map[zoom_center_y + int(self.corridor_length/2), i] = WALL_POWER
            self.map[zoom_center_y - int(self.corridor_length/2), i] = WALL_POWER
    
    def createRoom(self):
        zoom_center_y = int(self.map_height/2)
        start_x = 0
        while True:
            zoom_width = 20
            start_x += zoom_width
            if start_x > self.map_width - int(self.map_width/6): break 
            for i in range(0, zoom_center_y - int(self.corridor_length/2)):
                self.map[i, start_x] = WALL_POWER
        
        start_x = 0
        while True:
            zoom_width = 20
            start_x += zoom_width
            if start_x > self.map_width - int(self.map_width/6): break 
            for i in range(zoom_center_y + int(self.corridor_length/2), self.map_height):
                self.map[i, start_x] = WALL_POWER

    # def createZoom(self):
    #     zoom_center_y = int(self.map_height/2)
    #     for i in range(self.map_width):
    #         self.map[zoom_center_y + int(self.corridor_length/2), i] = WALL_POWER
    #         self.map[zoom_center_y - int(self.corridor_length/2), i] = WALL_POWER
    #     start_x = 0
    #     while True:
    #         zoom_width = np.random.randint(int(self.map_width/6), int(self.map_width/4))
    #         start_x += zoom_width
    #         if start_x > self.map_width - int(self.map_width/6): break 
    #         for i in range(0, zoom_center_y - int(self.corridor_length/2)):
    #             self.map[i, start_x] = WALL_POWER
    #     start_x = 0
    #     while True:
    #         zoom_width = np.random.randint(int(self.map_width/6), int(self.map_width/4))
    #         start_x += zoom_width
    #         if start_x > self.map_width - int(self.map_width/6): break 
    #         for i in range(zoom_center_y + int(self.corridor_length/2), self.map_height):
    #             self.map[i, start_x] = WALL_POWER