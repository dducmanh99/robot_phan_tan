Tin cập nhật về phím tắt … Vào Thứ Năm, 1 tháng 8, 2024, các phím tắt trong Drive sẽ được cập nhật để bạn có thể thao tác bằng chữ cái đầu tiên.Tìm hiểu thêm
from agent import Agent
from env import Environment
from utlis import *

class Swarm:
    def __init__(self, env: Environment, num_agents: int, first_agent_pose: np.ndarray, agent_in_rows: int, 
                coverage_range: float, max_velocity: float, agent_init_distance: float, map_visual: Axes):
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
        self.obstacle_range: float = 2.0
        self.collision_range: float = self.agents[0].radius * 2 + 0.05
        self.avoidance_range: float = 0.3
        self.goal_gain: float = 0.1
        self.collision_gain: float = 1.0
        self.avoidance_gain: float = 2.0
        self.determineRoot()
    def run(self):
        self.createVirtualPoint()
        self.findTarget()
        self.runToTarget()

    def runToTarget(self):
        for agent in self.agents:
            if agent.state == OCCUPIED: continue
            if agent.state == ASSIGNED:
                if EuclidDistance(agent.global_pose, agent.agent_position_hold_target) <= agent.coverage_range:
                    self.runToPoint(agent, agent.target_point_global)
                    if EuclidDistance(agent.global_pose, agent.target_point_global) < 0.01: 
                        agent.vel = np.zeros(2)
                        agent.state = OCCUPIED
                        agent.path_to_root = agent.route_to_target.copy()
                else:
                    if agent.route_id > len(agent.route_to_target) - 1:
                        agent.route_id = len(agent.route_to_target) - 1
                    else:
                        target = self.agents[agent.route_to_target[agent.route_id]].global_pose
                        if agent.route_id < len(agent.route_to_target) - 1:
                            next_target = self.agents[agent.route_to_target[agent.route_id +1]].global_pose
                        if EuclidDistance(agent.global_pose, next_target) <= agent.coverage_range:
                            agent.route_id += 1
                        else:
                            self.runToPoint(agent, target)
                        
            if agent.state == NOT_ASSIGNED:
                self.runAvoidance(agent)
                
    def runAvoidance(self, agent: Agent):
        vel_collision = np.zeros(2)
        for other in self.agents:
            if other.id == agent.id: continue
            distance = EuclideanDistance(agent.global_pose, other.global_pose)
            if distance < self.collision_range:
                vel_collision += self.collision_gain * math.exp(-(distance - self.collision_range))/(distance - self.collision_range) * (other.global_pose - agent.global_pose)/distance
        
        vel_avoidance = np.zeros(2)
        for i in range(len(self.env.obstacle_centers)):
            distance, intersection = self.distanceToObstacle(agent.global_pose, self.env.obstacle_centers[i], self.env.obstacle_coords[i])
            if distance < self.avoidance_range:
                vel_avoidance += self.avoidance_gain * (1/distance**2 - 1/self.avoidance_range**2) * (agent.global_pose - intersection)/distance
        agent.vel = agent.limitVelocity((vel_avoidance + vel_collision)/0.1)
        agent.run()
        
    def runToPoint(self, agent: Agent, point: np.ndarray):
        v_to_goal = (point - agent.global_pose) * self.goal_gain
        vel_collision = np.zeros(2)
        for other in self.agents:
            if other.id == agent.id: continue
            distance = EuclideanDistance(agent.global_pose, other.global_pose)
            if distance < self.collision_range:
                vel_collision += self.collision_gain * math.exp(-(distance - self.collision_range))/(distance - self.collision_range) * (other.global_pose - agent.global_pose)/distance
        
        vel_avoidance = np.zeros(2)
        point_obstacle = self.distanceToEnvironment(agent.global_pose, point)
        for obstacle in point_obstacle:
            distance = EuclideanDistance(agent.global_pose, obstacle)
            if distance < self.avoidance_range:
                vel_avoidance += self.avoidance_gain * (1/distance**2 - 1/self.avoidance_range**2) * (agent.global_pose - obstacle)/distance
        random_vel = np.zeros(2)
        vel = (vel_avoidance + vel_collision + v_to_goal)/0.1
        if self.checkLocalMinima(agent, point):
            random_vel = np.random.random(2)
        agent.vel = agent.limitVelocity(vel + random_vel)
        agent.run()
    
    def createVirtualPoint(self):
        for agent in self.agents:
            if agent.state == OCCUPIED:
                for i in range(6):
                    angle = normalizeAngle(i * math.pi/3)
                    virtual_point = np.array([round(agent.global_pose[0] + agent.coverage_range * math.cos(angle), 2),
                                            round(agent.global_pose[1] + agent.coverage_range * math.sin(angle), 2)],)
                    if self.virtualPointIsValid(virtual_point):
                        agent.virtual_point.append(virtual_point - agent.global_pose)
                        route = agent.path_to_root.copy()
                        route.append(agent.id)
                        agent.route_to_virtual_point.append(route)
                        agent.virtual_point_is_occupied.append(False)
                        
    
    def findTarget(self):
        id_list = []
        for agent in self.agents:
            if agent.state == NOT_ASSIGNED:
                id_list.append(agent.id)
        sorted_id_list = sorted(id_list, key=lambda id: EuclidDistance(self.agents[id].global_pose, self.root.global_pose))
        index = 0
        for agent in self.agents:
            for i in range(len(agent.virtual_point_is_occupied)):
                if agent.virtual_point_is_occupied[i] == False:
                    self.agents[sorted_id_list[index]].state = ASSIGNED
                    self.agents[sorted_id_list[index]].target_point_global = agent.virtual_point[i] + agent.global_pose
                    self.agents[sorted_id_list[index]].target_point_local = agent.virtual_point[i] + agent.global_pose
                    self.agents[sorted_id_list[index]].route_to_target = agent.route_to_virtual_point[i]
                    self.agents[sorted_id_list[index]].agent_position_hold_target = agent.global_pose
                    agent.virtual_point_is_occupied[i] = True
                    index += 1
    
    def checkLocalMinima(self, agent: Agent, target: np.ndarray):
        for other in self.agents:
            if other.id == agent.id: continue
            if are_points_collinear(other.global_pose, agent.global_pose, target):
                return True
        return False
    
    def determineRoot(self):
        agent_x = []
        for agent in self.agents:
            agent_x.append(agent.global_pose[0])
        indices = [index for index, value in enumerate(agent_x) if value == max(agent_x)]
        sorted_indices = sorted(indices, key= lambda idx: self.agents[idx].global_pose[1])
        root_id = sorted_indices[math.floor(len(sorted_indices)/2)]
        self.agents[root_id].type = ROOT
        self.agents[root_id].state = OCCUPIED
        self.agents[root_id].local_pose = np.zeros(2)
        self.root: Agent = self.agents[root_id]
        
    def distanceToObstacle(self, pose: np.ndarray, obstacle_center: np.ndarray, obstacle_coords: np.ndarray):
        for i in range(obstacle_coords.shape[0] - 1):
            intersection_bool, intersection_point = check_line_segments_intersection_2d(pose, obstacle_center,
                                                                                        obstacle_coords[i], obstacle_coords[i+1])
            if intersection_bool == True:
                return EuclideanDistance(pose, intersection_point), intersection_point
            else:
                return float('inf'), np.zeros(2)
        return float('inf'), np.zeros(2)
    
    def distanceToEnvironment(self, pose: np.ndarray, target: np.ndarray):
        point_list: List[np.ndarray] = []
        angle_range = np.arange(math.pi, -math.pi, -math.pi/3)
        angle_range = np.append(angle_range, angleByTwoPoint(pose, target))
        point_bool: List[bool] = [False for i in range(angle_range.shape[0])]
        for obstacle in self.env.obstacle_coords:
            for i in range(obstacle.shape[0] - 1):
                for idx, angle in enumerate(angle_range):
                    if point_bool[idx] == True: continue
                    angle_point = np.array([pose[0] + self.obstacle_range * math.cos(angle), pose[1] + self.obstacle_range * math.sin(angle)])
                    intersect_bool, intersect_point = check_line_segments_intersection_2d(pose, angle_point, obstacle[i], obstacle[i+1])
                    if intersect_bool == True:
                        point_bool[idx] = True
                        point_list.append(intersect_point)
        return point_list
    
    def checkPointInObstacle(self, point: np.ndarray, obstacle_coords: np.ndarray):
        min_x = obstacle_coords[:, 0].min()
        max_x = obstacle_coords[:, 0].max()
        min_y = obstacle_coords[:, 1].min()
        max_y = obstacle_coords[:, 1].max()
        if min_x <= point[0] <= max_x and min_y <= point[1] <= max_y:
            return True
        
    def virtualPointIsValid(self, virtual_point: np.ndarray):
        if virtual_point[0] >= self.env.map_length/2 or virtual_point[0] <= -self.env.map_length/2:
            return False
        if virtual_point[1] >= self.env.map_width/2 or virtual_point[1] <= -self.env.map_width/2:
            return False
        for agent in self.agents:
            for other_point in agent.virtual_point:
                if EuclidDistance(virtual_point, other_point + agent.global_pose) < 0.1:
                    return False
        point_obstacle = self.distanceToEnvironment(virtual_point, virtual_point)
        for point in point_obstacle:
            if EuclidDistance(virtual_point, point) < 0.4:
                return False
        for i in range(len(self.env.obstacle_centers)):
            if self.checkPointInObstacle(virtual_point, self.env.obstacle_coords[i]):
                return False
        return True
        
    def visualize(self):
        for agent in self.agents:
            agent.visualize()