import math
from utlis.utlis import *
from env.robot import Robot
class SystemManager:
    def __init__(self, data_folder: str, robots: List[Robot], graph: Graph, zone_vertices: List[Vertex]):
        self.robots: List[Robot] = robots
        self.graph: Graph = graph
        self.zone_vertices: List[Vertex] = zone_vertices
        self.export_tasks: List[Task] = [] # provide production materials
        self.import_tasks: List[Task] = [] # pull empty pallet
        self.data_folder: str = data_folder
        export_data = np.loadtxt(self.data_folder + "/export_task.txt")
        import_data = np.loadtxt(self.data_folder + "/import_task.txt") 
        for data in export_data:
            self.export_tasks.append(Task(data[0:2], data[2:4], int(data[4]), int(data[5]), data[6]))
        for data in import_data:
            self.import_tasks.append(Task(data[0:2], data[2:4], int(data[4]), int(data[5]), data[6]))
        self.calculateIDAndRouteInTask()
        self.calculateRobotRoute(0, self.export_tasks[0])
        self.task_assignment: List[bool] = [False for _ in range(len(self.robots))]
        self.task_number: List[int] = [0 for _ in range(len(self.robots))]
        self.wait_time_counter: List[int] = [0 for _ in range(len(self.robots))]
        self.wait_time = 30
    
    def taskAllocationAndPlanning(self):
        self.taskAllocation()
        self.planning()

    def planning(self):
        for robot in self.robots:
            if self.task_assignment[robot.getRobotID()] == False:
                self.calculateRobotRoute(robot.getRobotID(), self.taskCycles[robot.getRobotID()][self.task_number[robot.getRobotID()]])
                self.task_assignment[robot.getRobotID()] = True
            elif self.task_assignment[robot.getRobotID()] == True and robot.task_route_state == True:
                if self.wait_time_counter[robot.getRobotID()] < self.wait_time:
                    self.wait_time_counter[robot.getRobotID()] += 1
                else:
                    self.wait_time_counter[robot.getRobotID()] = 0
                    self.task_assignment[robot.getRobotID()] = False
                    if self.task_number[robot.getRobotID()] == len(self.taskCycles[robot.getRobotID()] ) - 1:
                        self.task_number[robot.getRobotID()] = 0
                    else: 
                        self.task_number[robot.getRobotID()] += 1
    def taskAllocation(self):
        robot_for_task = np.array([0, 1, 1, 1, 2, 2, 3, 4])
        self.taskCycles: List[List[Task]] = []
        for robot in self.robots:
            task_list = np.where(robot_for_task == robot.getRobotID())[0]
            task_cycle: List[Task] = []
            for task_id in task_list:
                task_cycle.append(self.export_tasks[task_id])
            for task_id in task_list[::-1]:
                task_cycle.append(self.import_tasks[task_id])
            self.taskCycles.append(task_cycle)
    
    def calculateHomeRoute(self):
        for robot in self.robots:
            start_id = self.calculateIDPointInGraph(robot.getCurrentPose())
            home_id = self.calculateIDPointInGraph(robot.getHomePose())
            robot.setHomeRoute(self.routePlanning(start_id, home_id)) 

    def calculateRobotRoute(self, robot_id: int, task: Task):
        robot_id_in_graph = self.calculateIDPointInGraph(self.robots[robot_id].getCurrentPose())
        robot_route = self.routePlanning(robot_id_in_graph, task.getStartID())
        task_route = task.getRoute()
        self.robots[robot_id].setRoute(robot_route, task_route)

    def calculateIDAndRouteInTask(self):
        for task in self.export_tasks:
            cond1 = False
            cond2 = False
            for vertices in self.zone_vertices:
                if round(task.getStartX(),2) == round(vertices.getCenterX(), 2) and round(task.getStartY(), 2) == round(vertices.getCenterY(),2):
                    cond1 = True
                    task.setStartID(vertices.getID())
                if round(task.getTargetX(), 2) == round(vertices.getCenterX(), 2) and round(task.getTargetY(), 2) == round(vertices.getCenterY(), 2):
                    cond2 = True
                    task.setTargetID(vertices.getID())
                if cond1 and cond2:
                    task.setRoute(self.routePlanning(task.getStartID(), task.getTargetID()))
                    break
        for task in self.import_tasks:
            cond1 = False
            cond2 = False
            for vertices in self.zone_vertices:
                if round(task.getStartX(),2) == round(vertices.getCenterX(), 2) and round(task.getStartY(), 2) == round(vertices.getCenterY(),2):
                    cond1 = True
                    task.setStartID(vertices.getID())
                if round(task.getTargetX(), 2) == round(vertices.getCenterX(), 2) and round(task.getTargetY(), 2) == round(vertices.getCenterY(), 2):
                    cond2 = True
                    task.setTargetID(vertices.getID())
                if cond1 and cond2:
                    task.setRoute(self.routePlanning(task.getStartID(), task.getTargetID()))
                    break

    def calculateIDPointInGraph(self, point):
        for vertices in self.graph.getVertices():
            if round(point[0],2) == round(vertices.getCenterX(), 2) and round(point[1], 2) == round(vertices.getCenterY(),2):
                return vertices.getID()
        return -1
    
    def routePlanning(self, start_id: int, target_id: int):
        prior_queue = PriorityQueue()
        prior_queue.push((start_id, [start_id], 0), 0)
        visited = []
        while not prior_queue.isEmpty():
            current_state, actions, cost = prior_queue.pop()
            if current_state not in visited:
                visited.append(current_state)
                if current_state == target_id:
                    route = []
                    for id in actions:
                        route.append([self.graph.getVertex(id).getCenterX(), self.graph.getVertex(id).getCenterY()])
                    return np.array(route)
                else:
                    children = self.graph.getNeighborAStar(current_state)
                    for child in children:
                        heuristic_value = ManhattanDistance(self.graph.getVertex(child[0]).getCenter(), self.graph.getVertex(target_id).getCenter())
                        prior_queue.update((child[0], actions + [child[0]], cost + child[1]), child[1] + cost + heuristic_value)
        return np.array([None])