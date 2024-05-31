from utility import*
from beacon import Beacon
color = ['pink', 'blue', 'red', 'green', 'gray']
class AODV:
    def __init__(self, start:int, goal:int, beacons:List[Beacon], sensing_range:float, visual:Axes):
        self.start = start
        self.goal = goal
        self.beacons = beacons
        self.sensing_range = sensing_range
        self.visited = []
        self.next = [self.start]
        self.path = []

        self.reachGoal = False
        self.reachStart = False

        self.visual: Axes = visual
        self.path_visual: Line2D = visual.plot([], [], '-', c= 'gray')[0]
        self.count = 0


    def run(self):
        # print(self.beacons[self.next[0]].pos)
        while(self.reachGoal == False):
            self.count +=1 
            self.visited.append(self.next[0])
            for index, beacon in enumerate(self.beacons):
                if beacon.id == self.next[0]: continue
                if beacon.state == 0:
                    if EuclideanDistance(beacon.pos, self.beacons[self.next[0]].pos) < self.sensing_range:
                        # print(beacon.id)
                        beacon.parent = self.next[0]
                        beacon.state = 3
                        beacon.rank = self.beacons[beacon.parent].rank + 1
                        if (beacon.id == self.goal):
                            beacon.state = 2
                            # beacon.rank += 1
                            self.reachGoal = True
                            self.visited.append(beacon.id)
                        self.next.append(beacon.id)
            self.next.pop(0)

        print(f'Visited: {self.visited}')

        self.path.append(self.goal)
        while (self.reachStart == False):
            next = self.beacons[self.path[-1]].parent
            
            if next == self.start:
                self.path.append(next)
                
                # self.beacons[next].state = 4
                self.reachStart = True
            else: 
                self.path.append(next)
                self.beacons[next].state = 4

        print(f'Path: {self.path}')
        
        self.visualize()
        

    def visualize(self):
        for beacon in self.beacons:
            self.visual_beacon = Circle((beacon.pos[0], beacon.pos[1]), radius= 0.6, color=color[beacon.state])
            self.visual.add_patch(self.visual_beacon)
            self.id_visual = self.visual.text(beacon.pos[0]-0.5, beacon.pos[1], str(beacon.rank), c='white', size=6.0)

        x_coords:List[float] = []
        y_coords:List[float] = []

        for id in self.path:
            x_coords.append(self.beacons[id].pos[0])
            y_coords.append(self.beacons[id].pos[1])
        self.path_visual.set_xdata(x_coords)
        self.path_visual.set_ydata(y_coords)

        