from map import Map
from utlis import *
from pso import PSO
import time
print("###----Start----###")
print(time.time())
map_height_meter = 20
map_width_meter = 15
corridor_width_meter = 3
resolution = 0.1
map_height = int(map_height_meter/resolution)
map_width = int(map_width_meter/resolution)
corridor_width = int(corridor_width_meter/resolution)
num_aps = 1
num_agents = 30
wavelength = 0.12 #lamda
transmitter_gain = 1.0 #Gt
receiver_gain = 1.0 #Gr
transmitter_power = 1e-3 # mini watt #Pt
vel_gain = 0.5 # 
p_best_gain = 1.0 #pbest
g_best_gain = 2.0 #gbest
env = Map(map_height, map_width, corridor_width)
pso = PSO(env, num_agents, num_aps, transmitter_power, wavelength, transmitter_gain, receiver_gain, 
            vel_gain, p_best_gain, g_best_gain, resolution)
pso.run(15)
plt.imshow(pso.g_best_map, cmap='gist_rainbow_r', interpolation='nearest') 

# Add colorbar 
plt.colorbar() 
ax = plt.gca()  # Get current axes
ax.set_aspect('equal')
plt.title("Wifi coverage areas") 
plt.tight_layout()
# plt.xticks(np.arange(0, map_width, 20))
# plt.yticks(np.arange(0, map_height, 20))
plt.show() 