from utility import*
from beacon import Beacon
from aodv import AODV


START = 0
GOAL = 48
figure, ax = plt.subplots(subplot_kw={'aspect': 'equal'})


map_width = 50
map_length = 50
ax.set_xlim(-2.5, 21)
ax.set_ylim(-2.5, 21)

start_range = [0, 0]
sensing_range = 4
resolution = 3
num_beacons = 49

num_beacon = 0
beacons_pos = []
beacons: List[Beacon] = []
for i in range (int(math.sqrt(num_beacons))):
    for j in range (int(math.sqrt(num_beacons))):
        offset = np.random.rand(2)
        beacon_pos = np.array([resolution*j+start_range[0]+offset[0], resolution*i+start_range[1]+offset[1]])
        beacons.append(Beacon(id=num_beacon, start=START, goal=GOAL, pos=beacon_pos, sensing_range=sensing_range, visual=ax))
        # beacon = Circle(beacon_pos, radius=0.6, color='pink')
        # beacons_pos.append(beacon_pos)
        # ax.add_patch(beacon)
        # ax.text(beacon_pos[0], beacon_pos[1], str(num_beacon), c='black', size=5.0)
        num_beacon +=1
for beacon in beacons:
    beacon.beacons = beacons

Aodv = AODV(start=START, goal=GOAL, beacons=beacons, sensing_range=sensing_range, visual=ax)
Aodv.run()


ax.grid()
# plt.tight_layout()
# ani = FuncAnimation(fig=figure, func=update, frames= 100, interval=500, repeat= False) # type:ignore
plt.title(f"Đường đi từ beacon {START} đến beacon {GOAL}")
plt.savefig("D:/C/uet_4_2/rbpt/tuan10/results.png", dpi=600)
# plt.show()
