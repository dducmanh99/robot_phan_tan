from utility import*
color = ['pink', 'blue', 'red', 'green', 'gray']

class Beacon: 
    def __init__(self,id: int, start:int, goal:int, pos:np.ndarray, sensing_range:float, visual:Axes):
        self.id = id
        self.start = start
        self. goal = goal 
        self.pos = pos
        self.sensing_range = sensing_range
        self.visual: Axes = visual
        
        self.parent:int = -1
        self.unicast:int = -1
        self.msg:int = -1

        self.state : int = 0 #0 free 1 start 2 goal 3sended 4path
        self.rank : int = 0
        if (self.id == self.start):
            self.state = 1
            self.msg = self.goal
            self.visual_beacon = Circle((self.pos[0], self.pos[1]), radius= 0.8, color=color[self.state])
            self.id_visual = self.visual.text(self.pos[0], self.pos[1], str(id), c='black', size=6.0)
            self.visual.add_patch(self.visual_beacon)
        elif (self.id == self.goal):
            self.visual_beacon = Circle((self.pos[0], self.pos[1]), radius= 0.8, color='red')
            self.id_visual = self.visual.text(self.pos[0], self.pos[1], str(id), c='black', size=6.0)
            self.visual.add_patch(self.visual_beacon)
        else:
            self.visual_beacon = Circle((self.pos[0], self.pos[1]), radius= 0.6, color=color[self.state])
            self.id_visual = self.visual.text(self.pos[0], self.pos[1], str(id), c='black', size=6.0)
            self.visual.add_patch(self.visual_beacon)

        self.beacons : List[Beacon] = []
        
    # def run(self):
    #     for beacon in self.beacons:
    #         if beacon.state == 2:
    #             # print('Found goal')
    #             return 
    #     # print("--------")
    #     if self.msg != -1:
    #         for beacon in self.beacons:
    #             if beacon.id == self.id: continue
    #             if beacon.state == 0:
    #                 # print(self.id, self.msg, self.state)
    #                 if EuclideanDistance(self.pos, beacon.pos) < self.sensing_range:
    #                     # print (beacon.id)
    #                     beacon.msg = self.msg
    #                     beacon.state = 3
    #                     beacon.parent = self.id
    #                     if beacon.id == self.goal:
    #                         # print(self.id, beacon.id)
    #                         beacon.state = 2
    #                         self.visualize()
    #                         return
    #     self.visualize()



    

        




        