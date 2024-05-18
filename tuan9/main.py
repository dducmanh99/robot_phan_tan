from utility import *
goal_rows = 3
goal_cols = 10
resolution = [5,5]
start_range = [0,8]

fig, ax = plt.subplots(subplot_kw={'aspect':'equal'})
ax.set_xlim(-5,(goal_cols-1)*resolution[0] +5)
ax.set_ylim(0, (goal_rows+1)*resolution[1]+3)
s

num_goal = 0
for i in range(goal_rows):
    for j in range(goal_cols):
        offset = (np.random.rand(2) - 0.5) * 2
        goal_pose =[resolution[0]*j+offset[0], resolution[1]*i+start_range[1]+offset[1]]
        goal = Circle(goal_pose, radius=0.6, color="pink")
        ax.add_patch(goal)
        ax.text(goal_pose[0], goal_pose[1], str(num_goal), c='black', size=5.0)
        num_goal +=1


plt.show()