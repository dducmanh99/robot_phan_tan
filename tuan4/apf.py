import numpy as np
import matplotlib.pyplot as plt
import math
from collections import deque

show_animation = True
SIM_TIME = 5
DT = 0.1
S = 1 #pham vi anh huong cua chuong ngai vat
R = 10 #ban kinh vat can
G = 2 #he so
reso = 0.5
alpha = 1
beta = 1
AREA_WIDTH = 30.0
KP = 5.0  # attractive potential gain
ETA = 100.0  # repulsive potential gain

def cal_pose(x0, y0, x0g, y0g, obs_x, obs_y, start_x0, start_y0):
    # print(x0,y0)
    x_cal = x0
    y_cal = y0
    pmap, minx, miny = calc_potential_field(x0, y0, x0g, y0g, obs_x, obs_y, start_x0, start_y0)

    d = np.hypot(x0 - x0g, y0 - y0g)
    ix = round((x0 - minx) / reso)
    iy = round((y0 - miny) / reso)
    gix = round((x0g - minx) / reso)
    giy = round((y0g - miny) / reso)

    motion = get_motion_model()
    previous_ids = deque()

    if d >= reso:
        minp = float("inf")
        minix, miniy = -1, -1
        for i, _ in enumerate(motion):
            inx = int(ix + motion[i][0])
            iny = int(iy + motion[i][1])
            # print(inx, iny)
            # print (ix, iy, inx, len(pmap), iny, len(pmap[0]))
            if inx >= len(pmap) or iny >= len(pmap[0]) or inx < 0 or iny < 0:
                
                p = float("inf")  # outside area
                print("outside potential!")
            else:
                p = pmap[inx][iny]
            if minp > p:
                minp = p
                minix = inx
                miniy = iny
        ix = minix
        iy = miniy
        x_cal = ix * reso + minx
        y_cal = iy * reso + miny

    return x_cal, y_cal

def get_motion_model():
    # dx, dy
    # all the 8 neighbouring cells to be checked
    motion = [[1, 0],
              [0, 1],
              [-1, 0],
              [0, -1],
              [-1, -1],
              [-1, 1],
              [1, -1],
              [1, 1]]

    return motion

def calc_potential_field(x0, y0, x0g, y0g, obs_x, obs_y, start_x0, start_y0):
    minx = min(x0, x0g, min(obs_x), start_x0) - AREA_WIDTH / 2.0
    miny = min(y0, y0g, min(obs_y), start_y0) - AREA_WIDTH / 2.0
    maxx = max(x0, x0g, max(obs_x), start_x0) + AREA_WIDTH / 2.0
    maxy = max(y0, y0g, max(obs_y), start_y0) + AREA_WIDTH / 2.0
    xw = int(round((maxx-minx)/reso))
    yw = int(round((maxy-miny)/reso))

    pmap = [[0.0 for i in range(yw)] for i in range(xw)]
    for ix in range(xw):
        x = ix * reso + minx

        for iy in range(yw):
            y = iy * reso + miny
            ug = calc_attractive_potential(x, y, x0g, y0g)
            uo = calc_repulsive_potential(x, y, obs_x, obs_y, R)
            uf = ug + uo
            pmap[ix][iy] = uf
    return pmap, minx, miny

def calc_attractive_potential(x, y, xg, yg):
    return KP * np.hypot(x - xg, y - yg)

def calc_repulsive_potential(x, y, obstacle_x, obstacle_y, rr):
    minid = -1
    
    dmin = float("inf")
    for i, _ in enumerate(obstacle_x):
        d = np.hypot(x - obstacle_x[i], y - obstacle_y[i])
        if dmin >= d:
            dmin = d
            minid = i

    # calc repulsive potential
    dq = np.hypot(x - obstacle_x[minid], y - obstacle_y[minid])

    if dq <= rr:
        if dq <= 0.1:
            dq = 0.1

        return 0.5 * ETA * (1.0 / dq - 1.0 / rr) ** 2
    else:
        return 0.0

def main():
    time = 0.0
    #start
    start_x0 = 0.0
    start_y0 = 0.0
    start_x1 = 20.0
    start_y1 = 20.0

    x0 = start_x0
    y0 = start_y0
    x1 = start_x1
    y1 = start_y1
    #goal
    x0g = 20.0
    y0g = 20.0
    x1g = 0.0
    y1g = 0.0
    plt.gcf().canvas.mpl_connect('key_release_event',
                                     lambda event: [exit(0) if event.key == 'escape' else None])
    while SIM_TIME>=time:
        time+=DT

        
        x0, y0 = cal_pose(x0, y0, x0g, y0g, [x1], [y1], start_x0, start_y0)
        # print(x0,y0)
        x1, y1 = cal_pose(x1, y1, x1g, y1g, [x0], [y0], start_x1, start_y1)

        # print(x0, y0, x1, y1)

        plt.annotate("A",xy=(x0g + 0.2, y0g + 0.2))
        plt.annotate("B",xy=(x1g - 0.8, y1g))
        plt.plot(x0,y0,".r")
        plt.plot(x1,y1,".b")
        plt.axis("equal")

        plt.pause(0.05)

    plt.show()
            

if __name__ == '__main__':
    main()