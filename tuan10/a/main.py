from utility import *
from aodv import Swarm
from graph import AODVNetwork
figure, map_visual = plt.subplots(subplot_kw={'aspect': 'equal'})
map_visual: Axes = map_visual

map_width = 20
map_length = 30
map_visual.set_xlim(-map_length/2, map_length/2)
map_visual.set_ylim(-map_width/2, map_width/2)
sensing_range = 1.5
swarm_distance = 1.0
swarm = Swarm(100, sensing_range, swarm_distance, map_length, map_width, map_visual) 
# graph = AODVNetwork(swarm)
# def update(frame):
#     map_visual.set_title("Frame: " + str(frame+1))
#     swarm.randomPosition()
#     graph.createLink()
#     route, visited = graph.route_request(graph.source_node, graph.destination_node)
#     swarm.visualize(route, visited)
    # if frame < 10:
    #     figure.savefig("frame_{}.png".format(frame))
    
map_visual.grid()
plt.tight_layout()
# ani = FuncAnimation(fig=figure, func=update, frames= 100, interval=100, repeat= False) # type:ignore
# ani.save("{}_agents.gif".format(num_agents), writer="pillow")
plt.show()