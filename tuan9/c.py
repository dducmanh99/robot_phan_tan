class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Node({self.x}, {self.y})"
    
def distance(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)
    
nodes = [
    Node(0, 0),  # Node 0
    Node(1, 0),  # Node 1
    Node(2, 0),  # Node 2
    Node(0, 1),  # Node 3
    Node(2, 2), # Node 4
    Node(3, 2),
    Node(5, 2),
]

start_node = nodes[0]  # Node 0
end_node = nodes[4]  # Node 4

graph = {}
for node in nodes:
    neighbors = []
    for other_node in nodes:
        if node != other_node and distance(node, other_node) <= 4:  # Giới hạn khoảng cách tối đa là 10
            neighbors.append(other_node)
    graph[node] = neighbors


def bfs(graph, start_node, end_node):
    queue = [start_node]
    visited = set()
    parents = {start_node: None}

    while queue:
        current_node = queue.pop(0)
        visited.add(current_node)

        if current_node == end_node:
            path = []
            while current_node:
                path.append(current_node)
                current_node = parents[current_node]
            path.reverse()
            return path

        for neighbor in graph[current_node]:
            if neighbor not in visited:
                queue.append(neighbor)
                parents[neighbor] = current_node

    return None

path = bfs(graph, start_node, end_node)

if path:
    print("Đường đi:", path)
else:
    print("Không tìm thấy đường đi.")