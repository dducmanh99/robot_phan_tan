from utility import *
from agent import Agent
from mtt import MTT

goal_rows = 3
goal_cols = 15

resolution = [3,3]
start_range = [0,8]

for i in range(goal_cols):
    x = 5 * math.cos(i*2*math.pi/goal_cols)
    y = 5 * math.sin(i*2*math.pi/goal_cols)


fig, ax = plt.subplots(subplot_kw={'aspect':'equal'})
ax.set_xlim(-15,40)
ax.set_ylim(-18,35)

# map
num_goal = 0
goal_poses = []
# for i in range(goal_rows):
#     for j in range(goal_cols):
#         offset = np.random.rand(2)
#         goal_pose =np.array([resolution[0]*j+offset[0], resolution[1]*i+start_range[1]+offset[1]])
#         goal = Circle(goal_pose, radius=0.6, color="pink")
#         goal_poses.append(goal_pose)
#         ax.add_patch(goal)
#         ax.text(goal_pose[0], goal_pose[1], str(num_goal), c='black', size=5.0)
#         num_goal +=1
for i in range(goal_rows):
    for j in range(goal_cols):
        offset = np.random.rand(2)
        angles = np.random.uniform(0, math.pi/10, 2)
        
        x = (13 + i*resolution[0] ) * math.cos(j*2*math.pi/goal_cols +  angles[0] ) + 12.0 +  offset[0]
        y = (13 + i*resolution[0] )* math.sin(j*2*math.pi/goal_cols +  angles[1] ) +10.0 + offset[1]
        goal_pos = np.array([x,y])
        goal = Circle(goal_pos, radius=0.6, color="pink")
        goal_poses.append(goal_pos)
        ax.add_patch(goal)
        ax.text(goal_pos[0], goal_pos[1], str(num_goal), c='black', size=5.0)
        num_goal +=1

#
num_of_agents = goal_cols*goal_rows
agents_in_row = goal_rows
agents_dis = 2.0
agent_first_pos:np.ndarray = np.array([12.0, 10.0])
goals:np.ndarray = np.array(goal_poses)
mtt = MTT(goals=goals,num_agents=num_of_agents,agent_first_pos=agent_first_pos,agents_in_row=agents_in_row,
              agents_dis=agents_dis, map_visual=ax) 

def update(frame):
    if frame % 200 == 199:
        print("Time {} s".format((frame + 1)*0.1))
    mtt.run()
    mtt.visualize()

ani = FuncAnimation(fig=fig, func=update, frames=2000, interval= 50, repeat= False) # type:ignore
# ani.save(filename="./tuan9/MTT_{}_agents_map2.gif".format(num_of_agents), writer="pillow")
# plt.grid(True)
plt.show()