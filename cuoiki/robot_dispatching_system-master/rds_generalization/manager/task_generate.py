from utlis.utlis import *

class TaskGenerator:
    def __init__(self, num_task_in_queue: int, num_priority: int, num_type: int, 
                min_load: float, max_load: float, graph:Graph):
        self.graph = graph.copy()
        self.num_task_in_queue: int = num_task_in_queue
        self.num_priority: int = num_priority
        self.num_type: int = num_type
        self.min_load: float = min_load
        self.max_load: float = max_load
        self.extractZonePoints(graph)
        self.task_queue: List[Task] = []
        
        self.generateTaskQueue()
    
    def getTaskQueue(self):
        return self.task_queue.copy()
    
    def removeTask(self, id: int):
        del self.task_queue[id]
        for i in range(id, len(self.task_queue)):
            self.task_queue[i].setID(i)
        self.addTask()
        
    def getHighestPriority(self):
        try:
            max_val = 0
            for i in range(len(self.task_queue)):
                if self.task_queue[i].getPriority() > self.task_queue[max_val].getPriority():
                    max_val = i
            item = self.task_queue[max_val]
            task_queue = self.getTaskQueue()
            del self.task_queue[max_val]
            self.addTask()
            return item.copy(), task_queue
        except IndexError:
            print()
            exit()
    
    def addTask(self):
        epsilon = random.random()
        type = random.randint(0, self.num_type - 1)
        priority = random.randint(1, self.num_priority)
        mass = random.uniform(self.min_load, self.max_load)
        if epsilon >= 0.75:
            start = self.working_vertices[random.randint(0, len(self.working_vertices) - 1)]
            target = self.storage_vertices[random.randint(0, len(self.storage_vertices) - 1)]
            if len(self.task_queue) == 0:
                self.task_queue.append(Task(0, start, target, type, priority, mass))
                self.task_queue[-1].setRoute(AStarPlanning(self.graph, TO_TARGET, self.task_queue[-1].getStartID(), 
                                                        self.task_queue[-1].getTargetID()))
            else:
                self.task_queue.append(Task(self.task_queue[-1].getID() + 1, start, target, type, priority, mass))
                self.task_queue[-1].setRoute(AStarPlanning(self.graph, TO_TARGET, self.task_queue[-1].getStartID(), 
                                                        self.task_queue[-1].getTargetID()))
        elif 0.5 <= epsilon < 0.75:
            id_list: np.ndarray = np.arange(0, len(self.working_vertices))
            start_id = np.random.choice(id_list)
            target_id = np.random.choice(np.delete(id_list, start_id))
            if len(self.task_queue) == 0:
                self.task_queue.append(Task(0, self.working_vertices[start_id], self.working_vertices[target_id], type, priority, mass))
                self.task_queue[-1].setRoute(AStarPlanning(self.graph, TO_TARGET, self.task_queue[-1].getStartID(), 
                                                        self.task_queue[-1].getTargetID()))
            else:
                self.task_queue.append(Task(self.task_queue[-1].getID() + 1, self.working_vertices[start_id], self.working_vertices[target_id], type, priority, mass))
                self.task_queue[-1].setRoute(AStarPlanning(self.graph, TO_TARGET, self.task_queue[-1].getStartID(), 
                                                        self.task_queue[-1].getTargetID()))
        elif 0.25 <= epsilon < 0.5:
            id_list: np.ndarray = np.arange(0, len(self.storage_vertices))
            start_id = np.random.choice(id_list)
            target_id = np.random.choice(np.delete(id_list, start_id))
            if len(self.task_queue) == 0:
                self.task_queue.append(Task(0, self.storage_vertices[start_id], self.storage_vertices[target_id], type, priority, mass))
                self.task_queue[-1].setRoute(AStarPlanning(self.graph, TO_TARGET, self.task_queue[-1].getStartID(), 
                                                            self.task_queue[-1].getTargetID()))
            else:
                self.task_queue.append(Task(self.task_queue[-1].getID() + 1, self.storage_vertices[start_id], self.storage_vertices[target_id], type, priority, mass))
                self.task_queue[-1].setRoute(AStarPlanning(self.graph, TO_TARGET, self.task_queue[-1].getStartID(), 
                                                            self.task_queue[-1].getTargetID()))
        else:
            start = self.working_vertices[random.randint(0, len(self.working_vertices) - 1)]
            target = self.storage_vertices[random.randint(0, len(self.storage_vertices) - 1)]
            if len(self.task_queue) == 0:
                self.task_queue.append(Task(0, start, target, type, priority, mass))
                self.task_queue[-1].setRoute(AStarPlanning(self.graph, TO_TARGET, self.task_queue[-1].getStartID(), 
                                                            self.task_queue[-1].getTargetID()))
            else:
                self.task_queue.append(Task(self.task_queue[-1].getID() + 1, start, target, type, priority, mass))
                self.task_queue[-1].setRoute(AStarPlanning(self.graph, TO_TARGET, self.task_queue[-1].getStartID(), 
                                                            self.task_queue[-1].getTargetID()))
    
    def extractZonePoints(self, graph:Graph):
        self.working_vertices: List[Vertex] = []
        self.storage_vertices: List[Vertex] = []
        for vertex in graph.getVertices():
            if vertex.getType() == WORKING_VERTEX:
                self.working_vertices.append(vertex)
            elif vertex.getType() == STORAGE_VERTEX:
                self.storage_vertices.append(vertex)
    
    def generateTaskQueue(self):
        for _ in range(self.num_task_in_queue):
            self.addTask()

class TaskGenFromData:
    def __init__(self, task_data_path: str, num_task_in_queue: int, graph: Graph):
        self.task_data: np.ndarray = np.loadtxt(task_data_path)
        self.task_id: int = 0
        self.num_task_in_queue = num_task_in_queue
        self.graph: Graph = graph
        self.task_queue: List[Task] = []
        self.generateTaskQueue()
    
    def getTaskQueue(self): return self.task_queue.copy()
    
    def getTask(self, id: int) -> Task:
        task = self.task_queue[id]
        del self.task_queue[id]
        for i in range(id, len(self.task_queue)):
            self.task_queue[i].setID(i)
        self.addTask()
        
        return task 
    
    def generateTaskQueue(self):
        for _ in range(self.num_task_in_queue):
            self.addTask()
            
    def addTask(self):
        start: Vertex = self.graph.getVertex(int(self.task_data[self.task_id, 0]))
        target: Vertex = self.graph.getVertex(int(self.task_data[self.task_id, 1]))
        if len(self.task_queue) == 0:
            self.task_queue.append(Task(0, start, target, int(self.task_data[self.task_id, 2]), 
                                        int(self.task_data[self.task_id, 3]), self.task_data[self.task_id, 4]))
            self.task_queue[-1].setRoute(AStarPlanning(self.graph, TO_TARGET, self.task_queue[-1].getStartID(), 
                                                        self.task_queue[-1].getTargetID()))
        else:
            self.task_queue.append(Task(self.task_queue[-1].getID() + 1, start, target, int(self.task_data[self.task_id, 2]), 
                                        int(self.task_data[self.task_id, 3]), self.task_data[self.task_id, 4]))
            self.task_queue[-1].setRoute(AStarPlanning(self.graph, TO_TARGET, self.task_queue[-1].getStartID(), 
                                                        self.task_queue[-1].getTargetID()))
        if self.task_id >= self.task_data.shape[0] - 1:
            self.task_id = 0
        else:
            self.task_id += 1