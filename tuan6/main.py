# Robot doi hinh chu V 

from utility import *
from agent import Agent

## 
num_of_agent = 5
range_start = 5
start = np.array([-40.0, 25.0])
# goal = np.array([0.0, 20.0])
size_map = 50

##
color = ['green','yellow','purple','orange','pink','brown','lime','gray','cyan','yellowgreen','magenta','hotpink','skyblue']
robot_radius = 0.3

poses = np.array([[-40.0,  25.0],
 [-40.0 , 35.0],
 [-40.0 , 30.0],
 [-40.0 , 20.0],
 [-40.0 , 15.0]])
# poses = np.empty((num_of_agent,2))
# for i in range(num_of_agent):
#     poses[i][0] = start[0]
#     poses[i][1] = start[1] - int(num_of_agent/2)*range_start + range_start * i
# print(poses) #y: 15 20 25 30 35 x:-40
# print (status_agent)

range_avoid = 5 * robot_radius

## create figure
fig, ax = plt.subplots(subplot_kw={'aspect':'equal'})
ax.set_xlim(-size_map,size_map)
ax.set_ylim(0,size_map)
ax.set_title(' V-shape formation with {} robots '.format(num_of_agent))
ax.grid(True)

## Visual start - goal
start_circle = Circle((start[0], start[1]), radius=0.8, color='blue')
ax.add_patch(start_circle)
plt.annotate("Start", xy=(start[0] - 8, start[1]))

wayPoints = np.array([[-20, 10], [0, 40], [25, 25]])
# wayPoints = np.array([ [-20, 30], [25, 25]])
wayPoints_id = 0
for i in wayPoints:
    goal_circle = Circle((i[0], i[1]), radius=0.8, color='red')
    ax.add_patch(goal_circle)

plt.annotate("Goal", xy=(wayPoints[-1][0] + 2, wayPoints[-1][1]))

print('algorithm with {} robots'.format(num_of_agent))

agents: List[Agent] = []
robot_visuals = []
path_visuals = []

for i in range(num_of_agent):
    agents.append(Agent(i, poses[i], color[i]))
    robot_visuals.append(agents[-1].circle)
    ax.add_patch(agents[-1].circle)
    
    path = np.array(agents[-1].path)
    line = ax.plot(path[:, 0], path[:, 1], '-', c= agents[-1].color)[0]
    path_visuals.append(line)



def nextWaypoint (agents: List[Agent], waypoint: np.ndarray):
    for agent in agents: 
        if agent.goalReach_flag == True:
            return True
    return False

def update(frame):
    # print("--")
    global wayPoints, wayPoints_id
    if nextWaypoint(agents, wayPoints[wayPoints_id]):
        if wayPoints_id >= len(wayPoints) - 1:
            wayPoints_id = 0
        else:
            wayPoints_id += 1
    for agent in agents:
        if agent.id == 0:
            key_pos = agent.key_pos
        # agent.updatePose()
        agent.update_pose(key_pos,wayPoints[wayPoints_id])
    for i, visual in enumerate(robot_visuals):
        visual.center = (agents[i].getCurrentX(), agents[i].getCurrentY()) 
    for i, visual in enumerate(path_visuals):
        path = np.array(agents[i].path)
        visual.set_xdata(path[:,0])
        visual.set_ydata(path[:,1])
        
animation = FuncAnimation(fig=fig, func=update, frames=1500, interval=50) 
animation.save(filename="./tuan6/{}_agents.gif".format(num_of_agent), writer='pillow') 

plt.tight_layout()
plt.show()