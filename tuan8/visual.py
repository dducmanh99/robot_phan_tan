from utlis import *

num_aps = 2
max_iter = 30
g_best_value = np.loadtxt("g_best_value_{}_aps.txt".format(num_aps), dtype=np.int16)
g_best_map = np.loadtxt("g_best_map_{}_aps.txt".format(num_aps))

plt.imshow(g_best_map, cmap='gist_rainbow_r', interpolation='nearest') 

# Add colorbar 
plt.colorbar() 
ax = plt.gca()  # Get current axes
ax.set_aspect('equal')
plt.title("Độ bao phủ = {} %".format(100 - round(g_best_value[-1]/(g_best_map.shape[0]*g_best_map.shape[1])*100, 5)))
plt.tight_layout()
# plt.xticks(np.arange(0, map_width, 20))
# plt.yticks(np.arange(0, map_height, 20))
plt.show()
g_best_values = []
for i in range(max_iter):
    if i < g_best_value.shape[0]:
        g_best_values.append(g_best_value[i])
    else:
        g_best_values.append(g_best_value[-1])
x = [1]
for i in range(10, max_iter+1,10):
    x.append(i)
plt.plot(np.arange(1, max_iter+1), g_best_values, 'r')
plt.xlabel("Số lần lặp")
plt.ylabel("Giá trị gBest")

plt.xticks(x)
plt.grid()
plt.show()