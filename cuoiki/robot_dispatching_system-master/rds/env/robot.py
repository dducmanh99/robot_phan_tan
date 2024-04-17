from utlis.utlis import *
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
import random
class Robot:
    def __init__(self, dt: float, id: int, init_pose: np.ndarray, max_payload: float, map_visual: axs.Axes,
                robot_length: float = 0.98, robot_width: float = 0.62):
        self.dt = dt
        self.id = id
        self.working_state: bool = False
        self.robot_home: np.ndarray = init_pose.copy()
        self.current_pose: np.ndarray = init_pose.copy()
        self.max_speed = 2.0 # m/s
        self.max_payload = max_payload
        self.current_payload = 0.0

        self.robot_route: np.ndarray = np.array([None])
        self.task_route: np.ndarray = np.array([None])
        self.home_route: np.ndarray = np.array([None])
        self.robot_route_state: bool = False
        self.task_route_state: bool = False
        self.task_route_id: int = 1
        self.robot_route_id: int = 1
        self.home_route_id: int = 1
        
        self.robot_length = robot_length
        self.robot_width = robot_width
        self.robot_color = color[id%7]
        robot_coords = np.array(calculateRectangleCoordinate(init_pose[0], init_pose[1], init_pose[2], robot_length, robot_width))
        self.map_visual = map_visual
        self.robot_visual: Polygon = map_visual.fill(robot_coords[:, 0], robot_coords[:, 1], c=self.robot_color)[0]
        self.route_visual: Line2D = map_visual.plot([], [], '-', c= self.robot_color)[0]
        self.waiting_counter: int = 0
        self.waiting_time: int = 30
        
    def control(self, route_following: bool = False, next_point: np.ndarray = np.array([None])):
        if route_following == False:
            self.routeFollowing()
        else:
            assert next_point[0] != None
            self.goToPoint(next_point)
    
    def goHome(self):
        if self.home_route_id == self.home_route.shape[0]:
            return True
        point_reached = self.goToPoint(self.home_route[self.home_route_id])
        if point_reached == True:
            self.home_route_id += 1
    
    def routeFollowing(self):
        if self.robot_route_id == self.robot_route.shape[0]:
            self.robot_route_state = True
        if self.task_route_id == self.task_route.shape[0]:
            self.waiting_counter = 0
            self.task_route_state = True  
            return True
        
        if self.robot_route_state == False:
            point_reached = self.goToPoint(self.robot_route[self.robot_route_id])
            if point_reached == True: self.robot_route_id += 1
            return False
            
        if self.robot_route_state == True and self.waiting_counter < self.waiting_time and self.task_route_state == False:
            self.waiting_counter += 1
            return False
        else:
            point_reached = self.goToPoint(self.task_route[self.task_route_id])
            if point_reached == True: self.task_route_id += 1
            return False
            
    def goToPoint(self, targetPoint: np.ndarray):
        speed = 0.0
        if round(targetPoint[0], 2) == round(self.getCurrentX(), 2) and round(targetPoint[1], 2) != round(self.getCurrentY(), 2):
            speed = round((targetPoint[1] - self.getCurrentY())/ self.dt,2)
            if speed > self.max_speed:
                speed = self.max_speed
            if speed < - self.max_speed:
                speed = -self.max_speed
            self.current_pose[1] += speed * self.dt
            self.current_pose[2] = math.pi/2
        if round(targetPoint[1], 2) == round(self.getCurrentY(), 2) and round(targetPoint[0], 2) != round(self.getCurrentX(), 2):
            speed = round((targetPoint[0] - self.getCurrentX())/ self.dt, 2)
            if speed > self.max_speed:
                speed = self.max_speed
            if speed < -self.max_speed:
                speed = -self.max_speed
            self.current_pose[0] += speed * self.dt
            self.current_pose[2] = 0.0
        if speed == 0:
            return True
        return False
        
    def setRoute(self, robot_route: np.ndarray, task_route: np.ndarray):
        self.robot_route = robot_route.copy()
        self.task_route = task_route.copy()    
        self.robot_route_state = False
        self.task_route_state = False
        self.robot_route_id = 1
        self.task_route_id = 1
    
    def setHomeRoute(self, home_route: np.ndarray):
        self.home_route = home_route.copy() 
        self.home_route_id = 1

    def getRobotID(self): return self.id
    def getHomePose(self): return self.robot_home.copy()
    def getCurrentX(self): return self.current_pose[0]
    def getCurrentY(self): return self.current_pose[1]
    def getCurrentTheta(self): return self.current_pose[2]
    def getCurrentPose(self): return self.current_pose
    def getWorkingState(self): return self.working_state
    def setWorkingState(self, state: bool): self.working_state = state
    def setCurrentPose(self, x: float, y: float, theta: float):
        self.current_pose[0] = x
        self.current_pose[1] = y
        self.current_pose[2] = theta
    def robotVisualization(self):
        self.robot_visual.set_xy(np.array(calculateRectangleCoordinate(self.current_pose[0], self.current_pose[1],
                                                                        self.current_pose[2], self.robot_length,
                                                                        self.robot_width)))