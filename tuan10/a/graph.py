from utility import *
from aodv import Swarm

class Node:
    def __init__(self, id: int):
        self.id = id
        self.routing_table = {}
        self.sequence_number = 0
        self.visited = set()
class AODVNetwork:
    def __init__(self, swarm: Swarm):
        self.swarm = swarm
        self.nodes: List[Node] = []
        for i in range(swarm.num_agents):
            self.nodes.append(Node(id=i))
        self.neighbors: List[List[Node]] = [[] for _ in range(swarm.num_agents)]
        self.source_node: Node = self.nodes[0]
        self.destination_node: Node = self.nodes[-1]
    
    def createLink(self):
        self.neighbors: List[List[Node]] = [[] for _ in range(self.swarm.num_agents)]
        for i in range(self.swarm.num_agents - 1):
            for j in range(i+1, self.swarm.num_agents):
                    if EuclideanDistance(self.swarm.agents[i], self.swarm.agents[j]) <= self.swarm.sensing_range:
                            self.addLink(i, j)
                            
    def addLink(self, id1: int, id2: int):
        self.neighbors[id1].append(self.nodes[id2])
        self.neighbors[id2].append(self.nodes[id1])
    
    def send_rreq(self, source: Node, destination: Node):
        queue = deque([(source, [source])])
        visited = set()
        
        while queue:
            current_node, path = queue.popleft()
            if current_node.id in visited:
                continue
            visited.add(current_node.id)
            
            if current_node.id == destination.id:
                source.visited = visited
                return path
            
            for neighbor in self.neighbors[current_node.id]:
                if neighbor.id not in visited:
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    def send_rrep(self, path):
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]
            current_node.routing_table[path[-1].id] = (next_node.id, len(path) - i - 1)
    
    def route_request(self, source: Node, destination: Node):
        path = self.send_rreq(source, destination)
        self.send_rrep(path)
        route = [source.id]
        flag = False
        node = source
        dest_id = source.id
        for dest, (next_hop, _) in node.routing_table.items():
            dest_id = dest
        while True:
            for dest, (next_hop, _) in node.routing_table.items():
                route.append(next_hop)
                if next_hop == dest_id: 
                    flag = True
                node = self.nodes[next_hop]
            if flag == True:
                break
        
        return route, source.visited
            
    def show_routing_table(self, source_node: Node):
        route = [source_node.id]
        flag = False
        node = source_node
        dest_id = source_node.id
        for dest, (next_hop, hop_count) in node.routing_table.items():
            dest_id = dest
        while True:
            for dest, (next_hop, hop_count) in node.routing_table.items():
                route.append(next_hop)
                if next_hop == dest_id: 
                    flag = True
                node = self.nodes[next_hop]
            if flag == True:
                break
        print("Routing: ",route)