import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from typing import List
import math 
import numpy as np 

def rotMatrix(theta: float, h, k):
        return np.array([[math.cos(theta), -math.sin(theta), h],
                         [math.sin(theta), math.cos(theta), k],
                         [0, 0, 1]])
def computeAngle(position0, position1): #goal, robot
    angle = math.atan2(position0[1]-position1[1], position0[0]-position1[0])
    return angle

key_pos = [-20.0, 30.0, 1.46013]
# key_pos = [2.0, 1.0, -math.pi/2]
V_pos = []
V_pos.append(rotMatrix(key_pos[2], key_pos[0], key_pos[1]) @ np.array([0, 0, 1]) )
V_pos.append(rotMatrix(key_pos[2], key_pos[0], key_pos[1]) @ np.array([-2, -2, 1]) )
V_pos.append(rotMatrix(key_pos[2], key_pos[0], key_pos[1]) @ np.array([-1, -1, 1]) )
V_pos.append(rotMatrix(key_pos[2], key_pos[0], key_pos[1]) @ np.array([1, -1, 1]) )
V_pos.append(rotMatrix(key_pos[2], key_pos[0], key_pos[1]) @ np.array([2, -2, 1]) )
print (V_pos)
# print(math.cos(3.141592653589793))

fig, ax = plt.subplots(subplot_kw={'aspect':'equal'})
size_map = 50
ax.set_xlim(-size_map,size_map)
ax.set_ylim(0,size_map)
ax.grid(True)
for i in V_pos:
    # print (i)
    circle = Circle((i[0], i[1]), radius=0.3, color='blue')
    ax.add_patch(circle)

# plt.show()
a = [-20.0, 30.0]
b = [25.0, 25.0]
print(computeAngle(b,a) * 180 / math.pi)

