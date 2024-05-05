from agent import Agent
from env import Environment
from utility import *

class Swarm:
    def __init__(self, env: Environment, num_agents: int, first_agent_pose: np.ndarray, agent_in_rows: int,
                 coverage_range: float, max_velocity: float, agent_init_distance: float, map_visual: Axes) :
        self.env: Environment = env
        self.num_agents: int = num_agents   
        self.map_visual: Axes = map_visual
        assert num_agents % agent_in_rows == 0
        agent_in_cols: int = int(num_agents/ agent_in_rows)
        self.agent_init_distance: float = agent_init_distance
        self.agents: List[Agent] = []
        for i in range(agent_in_rows):
            for j in range(agent_in_cols): 
                x = first_agent_pose[0] + j * agent_init_distance
                y = first_agent_pose[1] + i * agent_init_distance
                id = (i*agent_in_cols + j)
                self.agents.append(Agent(id, np.array([x, y]), coverage_range, max_velocity, map_visual))
        self.obstacle_range: float = 4.0
        self.collision_range: float = self.agents[0].radius * 4 + 0.05
        self.avoidance_range: float = 0.3
        self.goal_gain: float = 0.1
        self.collision_gain: float = 1.0
        self.avoidance_gain: float = 5.0
        
    def run(self):
        for agent in self.agents:
            self.runAvoidance(agent)
            self.randomVel(agent)
            # self.runVirtualGoal(agent)

    def runVirtualGoal(self, agent: Agent):

        goal = np.array([(np.random.rand(1)*2-1)*self.env.map_width, (np.random.rand(1)*2-1)*self.env.map_length])


    def runAvoidance(self, agent: Agent):
        velAvoid = np.zeros(2)
        velColl = np.zeros(2)
        for other in self.agents:
            if other.id == agent.id: continue
            dis = EuclidDistance(agent.global_pose, other.global_pose)
            if dis < self.collision_range:
                velColl += self.collision_gain * math.exp(-(dis - self.collision_range))/(dis - self.collision_range) * (other.global_pose - agent.global_pose)/dis

        for i in range(len(self.env.obstacle_centers)):
            distance, intersection = self.distanceToObstacle(agent.global_pose, self.env.obstacle_centers[i], self.env.obstacle_coords[i])
            if distance < self.avoidance_range: 
                print(agent.id)
            
                velAvoid += self.avoidance_gain * (1/distance**2 - 1/self.avoidance_range**2) * (agent.global_pose - intersection)/(distance+0.01)
        
        agent.vel = agent.limitVelocity((velAvoid + velColl)/0.1)
        agent.run()

    def randomVel(self, agent: Agent):
        rand = np.random.randint(0,2)
        if rand == 0:
            return  
        else:
            agent.vel = np.array([np.random.rand(1)*2-1 , np.random.rand(1)*2-1])/5
            agent.run()

    def distanceToObstacle(self, pose: np.ndarray, obstacle_center: np.ndarray, obstacle_coords: np.ndarray):
        for i in range(obstacle_coords.shape[0] - 1):
            intersection_bool, intersection_point = check_line_segments_intersection_2d(pose, obstacle_center,
                                                                                        obstacle_coords[i], obstacle_coords[i+1])
            if intersection_bool == True:
                return EuclideanDistance(pose, intersection_point), intersection_point
            else:
                return float('inf'), np.zeros(2)
        return float('inf'), np.zeros(2)

    def visualize(self):
        for agent in self.agents:
            agent.visualize()