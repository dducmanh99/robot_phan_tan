from utility import *
from agent import Agent
from mtt import MTT

goal_rows = 3
goal_cols = 15

resolution = [3,3]
start_range = [0,8]

fig, ax = plt.subplots(subplot_kw={'aspect':'equal'})
ax.set_xlim(-5,(goal_cols-1)*resolution[0] +5)
ax.set_ylim(-2, (goal_rows+1)*resolution[1]+5)

# map
num_goal = 0
goal_poses = []
for i in range(goal_rows):
    for j in range(goal_cols):
        offset = np.random.rand(2)
        goal_pose =np.array([resolution[0]*j+offset[0], resolution[1]*i+start_range[1]+offset[1]])
        goal = Circle(goal_pose, radius=0.6, color="pink")
        goal_poses.append(goal_pose)
        ax.add_patch(goal)
        ax.text(goal_pose[0], goal_pose[1], str(num_goal), c='black', size=5.0)
        num_goal +=1

#
num_of_agents = goal_cols*goal_rows
agents_in_row = goal_rows
agents_dis = 2.0
agent_first_pos:np.ndarray = np.array([4.0, 1.0])
goals:np.ndarray = np.array(goal_poses)
mtt = MTT(goals=goals,num_agents=num_of_agents,agent_first_pos=agent_first_pos,agents_in_row=agents_in_row,
              agents_dis=agents_dis, map_visual=ax) 

def update(frame):
    if frame % 200 == 199:
        print("Time {} s".format((frame + 1)*0.1))
    mtt.run()
    mtt.visualize()

ani = FuncAnimation(fig=fig, func=update, frames=2000, interval= 50, repeat= False) # type:ignore
# ani.save(filename="./tuan9/MTT_{}_agents.gif".format(num_of_agents), writer="pillow")
# plt.grid(True)
plt.show()