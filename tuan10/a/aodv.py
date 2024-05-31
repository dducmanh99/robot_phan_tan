from utility import *

class Swarm:
    def __init__(self, num_agents: int, sensing_range: float, agent_distance: float, map_length: int, map_width: int, visual: Axes):
        self.num_agents = num_agents
        self.map_length = map_length
        self.map_width = map_width
        self.sensing_range = sensing_range
        self.agent_distance = agent_distance
        self.visual: Axes = visual
        self.randomPosition()
        self.agent_visual: List[Circle] = []
        self.id_visual: List[Text] = []
        self.start_id = 0
        self.target_id = num_agents - 1
        for (i, agent) in enumerate(self.agents):
            self.agent_visual.append(Circle((agent[0], agent[1]), radius= 0.3, color='black'))
            self.id_visual.append(self.visual.text(agent[0], agent[1], str(i+1), c='white', size=5.0))
            self.visual.add_patch(self.agent_visual[-1])
        self.path_visual: Line2D = visual.plot([], [], '-', c= 'orange')[0]
    def randomPosition(self):
        agents: List[List[float]] = []
        for i in range(self.num_agents):
            if i == 0:
                agents.append([np.random.uniform(-self.map_length/2 + 1, self.map_length/2 - 1),
                                np.random.uniform(-self.map_width/2 + 1, self.map_width/2 - 1)])
            else:
                while True:
                    x = np.random.uniform(-self.map_length/2 + 1, self.map_length/2 - 1)
                    y = np.random.uniform(-self.map_width/2 + 1, self.map_width/2 - 1)
                    same_flag = True
                    for agent in agents:
                        if EuclideanDistance(agent, [x, y]) < self.agent_distance:
                            same_flag = False
                            break
                    if same_flag == True:
                        connect_flag = False
                        for agent in agents:
                            if EuclideanDistance(agent, [x, y]) <= self.sensing_range:
                                connect_flag = True
                                break
                        if connect_flag == True:
                            agents.append([x, y])
                            break
        self.agents = np.array(agents, dtype=np.float32)
        self.states = [False for _ in range(self.num_agents)]
    def visualize(self, route: List[int], visited: Set):
        for i in range(self.num_agents):
            self.agent_visual[i].set_center((self.agents[i, 0], self.agents[i, 1]))
            self.agent_visual[i].set_color('black')
            self.id_visual[i].set_x(self.agents[i, 0])
            self.id_visual[i].set_y(self.agents[i, 1])
        for id in visited:
            self.agent_visual[id].set_color('blue')
        x_coords:List[float] = []
        y_coords:List[float] = []
        for i in range(len(route)):
            self.agent_visual[route[i]].set_color('orange')
            x_coords.append(self.agents[route[i]][0])
            y_coords.append(self.agents[route[i]][1])
        self.path_visual.set_xdata(x_coords)
        self.path_visual.set_ydata(y_coords)
        self.agent_visual[self.start_id].set_color('red')
        self.agent_visual[self.target_id].set_color('green')