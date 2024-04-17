from utlis.utlis import *
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
class Robot:
    def __init__(self, dt: float, id: int, home: Vertex, home_theta: float, max_speed: float, max_payload: float, 
                map_visual: axs.Axes, robot_length: float = 0.98, robot_width: float = 0.62):
        self.dt = dt
        self.id = id
        self.state = FREE
        self.home: Vertex = home
        self.graph_id: int = home.getID()
        self.pose: np.ndarray = np.append(home.getCenter(), home_theta)
        self.payload: float = 0.0
        self.max_speed = max_speed
        self.max_payload = max_payload
        self.task: Task = Task()
        self.task_list: List[Task] = []
        self.route: Route = Route()
        self.route_id: int = 1
        self.route_done = False
        self.robot_length = robot_length
        self.robot_width = robot_width
        robot_coords = np.array(calculateRectangleCoordinate(home.getCenterX(), home.getCenterY(), home_theta, 
                                                            robot_length, robot_width))
        self.map_visual = map_visual
        self.robot_visual: Polygon = map_visual.fill(robot_coords[:, 0], robot_coords[:, 1], c= state_color[self.getState()])[0]
        self.waiting_counter: int = 1
        self.waiting_time: int = 30
    
    def aStarControl(self, waiting_time: int):
        self.waiting_time = waiting_time
        if self.task.isTask() == False:
            return False
        if self.route.getType() == TO_TARGET:
            if self.taskIsDone() == True:
                if self.waitForPicking(waiting_time) == False:
                    return False
                else:
                    self.setState(FREE)
                    self.route_id = 1
                    self.route.clearRoute()
                    self.task.clearTask()
                    return True
        if self.route.isRoute() == False:
            return False
        if self.route_done == False:
            self.route_done = self.routeFollowing()
            return False
        else:
            if self.waitForPicking(waiting_time) == False:
                return False
            self.route.clearRoute()
            self.setRoute(self.task.getRoute())
            return True
        
    def control(self, waiting_time: int):
        self.waiting_time = waiting_time
        if self.task.isTask() == False:
            return False
        if self.taskIsDone() == True:
            self.route.clearRoute()
            self.task.clearTask()
            return False
        if self.route.isRoute() == False:
            return True
        if self.route_done == False:
            self.route_done = self.routeFollowing()
            return False
        else:
            if self.waitForPicking(waiting_time) == False:
                return False
            self.route.clearRoute()
            return True

    def waitForPicking(self, waiting_time: int):
        if self.waiting_counter < waiting_time:
            self.setState(PICKING_UP)
            self.waiting_counter += 1
        if self.waiting_counter >= waiting_time:
            self.setState(BUSY)
            return True
        return False
        
    def routeFollowing(self):
        if self.routeDone() == True:
            return True
        point_reached = self.gotoPointAndAvoidance(self.route.getCoord(self.route_id))
        if point_reached == True:
            self.route_id += 1
        if self.route.getType() == TO_START:
            self.setState(ON_WAY_TO_START)
        if self.route.getType() == TO_TARGET:
            self.setState(ON_WAY_TO_TARGET)
        if self.route.getType() == TO_WAITING:
            self.setState(ON_WAY_TO_WAITING)
        if self.route.getType() == TO_CHARGING:
            self.setState(ON_WAY_TO_CHARGING)
        return False
    
    def routeDone(self):
        if EuclidDistance(self.getPosition(), self.route.getCoord(-1)) < MAX_SAME_DIST:
            return True
        return False
    
    def gotoPointAndAvoidance(self, target_point: np.ndarray):
        if EuclidDistance(self.getPosition(), target_point) < MAX_SAME_DIST:
            return True
        else:
            vel = self.limitVelocity((target_point - self.getPosition())/self.dt) 
            self.pose[0]+= vel[0] * self.dt
            self.pose[1]+= vel[1] * self.dt
            self.pose[2] = math.atan2(vel[1], vel[0])
            return False
        
    def limitVelocity(self, vel:np.ndarray):
        speed = math.hypot(vel[0], vel[1])
        if speed > self.max_speed:
            limited_speed = (vel / speed) * self.max_speed
            return limited_speed
        return vel
    
    def taskIsDone(self):
        if self.task.isTask() == True:
            if EuclidDistance(self.task.getTarget().getCenter(), self.getPose()) < MAX_SAME_DIST:
                self.setState(FREE)
                return True
        return False
    
    def getRouteType(self): return self.route.getType()
    def getRouteVertices(self): return self.route.getVertices()
    def getRouteVertex(self, id: int): return self.route.getVertex(id)
    def getRouteCoords(self): return self.route.getCoords()
    def getRouteCoord(self, id: int): return self.route.getCoord(id)
    def getRouteX(self, id: int): return self.route.getCoordX(id)
    def getRouteY(self, id: int): return self.route.getCoordY(id)
    def getRouteXList(self): return self.route.getCoordXList()
    def getRouteYList(self): return self.route.getCoordYList()
    def getRouteCost(self): return self.route.getRouteCost()
    def hasRoute(self): return self.route.isRoute()
    def hasTask(self): return self.task.isTask()
    
    def setRoute(self, route: Route):
        self.route = route.copy()
        self.route_id = 1
        self.route_done = False
        self.waiting_counter = 1

    def getNextPoint(self): return self.route_id
    def getWaitingTime(self): return self.waiting_time
    
    def getID(self): return self.id
    def getHome(self): return self.home.copy()
    def getGraphID(self): return self.graph_id
    def getX(self): return self.pose[0]
    def getY(self): return self.pose[1]
    def getPosition(self): return self.pose[0:2].copy()
    def getTheta(self): return self.pose[2]
    def getPose(self): return self.pose.copy()
    def getPayload(self): return self.payload
    def getRestPayload(self): return self.max_payload - self.payload
    def getState(self): return self.state
    def getTask(self): return self.task
    def setTask(self, task: Task): 
        self.task = task.copy()
        self.payload += task.getMass()
    def setGraphID(self, id: int): self.graph_id = id
    def setState(self, state: int): self.state = state
    def setPose(self, x: float, y: float, theta: float):
        self.pose[0] = x
        self.pose[1] = y
        self.pose[2] = theta
    def robotVisualization(self):
        self.robot_visual.set_xy(np.array(calculateRectangleCoordinate(self.pose[0], self.pose[1],
                                                                        self.pose[2], self.robot_length,
                                                                        self.robot_width)))
        self.robot_visual.set_color(state_color[self.getState()])