import numpy as np
import matplotlib.pyplot as plt
import math
from collections import deque

show_animation = True
SIM_TIME = 20
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
    # print("++",x0,y0, ix,minx, iy, miny)
    # gix = round((x0g - minx) / reso)
    # giy = round((y0g - miny) / reso)

    motion = get_motion_model()
    # previous_ids = deque()

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
                # print(p)
            if minp > p:
                minp = p
                minix = inx
                miniy = iny
        
        ix = minix
        iy = miniy
        # print(ix,minx, iy, miny)
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
    start_x1 = 0.0
    start_y1 = 20.0
    start_x2 = 20.0
    start_y2 = 20.0
    start_x3 = 20.0
    start_y3 = 0.0

    start_x4 = 10-10*math.sqrt(2)
    start_y4 = 10.0
    start_x5 = 10.0
    start_y5 = 10.0+10*math.sqrt(2)
    start_x6 = 10.0 + 10*math.sqrt(2)
    start_y6 = 10.0
    start_x7 = 10.0
    start_y7 = 10.0-10*math.sqrt(2)

    start_x8 = 10 - 10*math.sqrt(2)*math.cos(math.pi/8)
    start_y8 = 10 + 10*math.sqrt(2)*math.sin(math.pi/8)
    start_x9 = 10 - 10*math.sqrt(2)*math.cos(math.pi*3/8)
    start_y9 = 10 + 10*math.sqrt(2)*math.sin(math.pi*3/8)
    start_x10 = 10 + 10*math.sqrt(2)*math.cos(math.pi*3/8)
    start_y10 = 10 + 10*math.sqrt(2)*math.sin(math.pi*3/8)
    start_x11 = 10 + 10*math.sqrt(2)*math.cos(math.pi/8)
    start_y11 = 10 + 10*math.sqrt(2)*math.sin(math.pi/8)

    start_x12 = start_x11
    start_y12 = 10 - 10*math.sqrt(2)*math.sin(math.pi/8)
    start_x13 = start_x10
    start_y13 = 10 - 10*math.sqrt(2)*math.sin(math.pi*3/8)
    start_x14 = start_x9
    start_y14 = 10 - 10*math.sqrt(2)*math.sin(math.pi*3/8)
    start_x15 = start_x8
    start_y15 = 10 - 10*math.sqrt(2)*math.sin(math.pi/8)

    x0 = start_x0
    y0 = start_y0
    x1 = start_x1
    y1 = start_y1
    x2 = start_x2
    y2 = start_y2
    x3 = start_x3
    y3 = start_y3

    x4 = start_x4
    y4 = start_y4
    x5 = start_x5
    y5 = start_y5
    x6 = start_x6
    y6 = start_y6
    x7 = start_x7
    y7 = start_y7

    x8 = start_x8
    y8 = start_y8
    x9 = start_x9
    y9 = start_y9
    x10 = start_x10
    y10 = start_y10
    x11 = start_x11
    y11 = start_y11

    x12 = start_x12
    y12 = start_y12
    x13 = start_x13
    y13 = start_y13
    x14 = start_x14
    y14 = start_y14
    x15 = start_x15
    y15 = start_y15
    #goal
    x0g = 20.0
    y0g = 20.0
    x1g = 20.0
    y1g = 0.0
    x2g = 0.0
    y2g = 0.0
    x3g = 0.0
    y3g = 20.0

    x4g = start_x6
    y4g = start_y6
    x5g = start_x7
    y5g = start_y7
    x6g = start_x4
    y6g = start_y4
    x7g = start_x5
    y7g = start_y5

    x8g = start_x12
    y8g = start_y12
    x9g = start_x13
    y9g = start_y13
    x10g = start_x14
    y10g = start_y14
    x11g = start_x15
    y11g = start_y15

    x12g = start_x8
    y12g = start_y8
    x13g = start_x9
    y13g = start_y9
    x14g = start_x10
    y14g = start_y10
    x15g = start_x11
    y15g = start_y11
    
    while SIM_TIME>=time:
        time+=DT
        # print('-----')
        plt.gcf().canvas.mpl_connect('key_release_event',
                                     lambda event: [exit(0) if event.key == 'escape' else None])
        
        x0, y0 = cal_pose(x0, y0, x0g, y0g, [x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15], [y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15], start_x0, start_y0)
        # # print(x0,y0)
        x1, y1 = cal_pose(x1, y1, x1g, y1g, [x0,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15], [y0,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15], start_x1, start_y1)

        x2, y2 = cal_pose(x2, y2, x2g, y2g, [x0,x1,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15], [y0,y1,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15], start_x2, start_y2)

        x3, y3 = cal_pose(x3, y3, x3g, y3g, [x0,x1,x2,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15], [y0,y1,y2,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15], start_x3, start_y3)

        x4, y4 = cal_pose(x4, y4, x4g, y4g, [x0,x1,x2,x3,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15], [y0,y1,y2,y3,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15], start_x4, start_y4)
        # # print(x0,y0)
        x5, y5 = cal_pose(x5, y5, x5g, y5g, [x0,x1,x2,x3,x4,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15], [y0,y1,y2,y3,y4,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15], start_x5, start_y5)

        x6, y6 = cal_pose(x6, y6, x6g, y6g, [x0,x1,x2,x3,x4,x5,x7,x8,x9,x10,x11,x12,x13,x14,x15], [y0,y1,y2,y3,y4,y5,y7,y8,y9,y10,y11,y12,y13,y14,y15], start_x6, start_y6)

        x7, y7 = cal_pose(x7, y7, x7g, y7g, [x0,x1,x2,x3,x4,x5,x6,x8,x9,x10,x11,x12,x13,x14,x15], [y0,y1,y2,y3,y4,y5,y6,y8,y9,y10,y11,y12,y13,y14,y15], start_x7, start_y7)

        x8, y8 = cal_pose(x8, y8, x8g, y8g, [x0,x1,x2,x3,x4,x5,x6,x7,x9,x10,x11,x12,x13,x14,x15], [y0,y1,y2,y3,y4,y5,y6,y7,y9,y10,y11,y12,y13,y14,y15], start_x8, start_y8)

        x9, y9 = cal_pose(x9, y9, x9g, y9g, [x0,x1,x2,x3,x4,x5,x6,x8,x7,x10,x11,x12,x13,x14,x15], [y0,y1,y2,y3,y4,y5,y6,y8,y7,y10,y11,y12,y13,y14,y15], start_x9, start_y9)

        x10, y10 = cal_pose(x10, y10, x10g, y10g, [x0,x1,x2,x3,x4,x5,x6,x8,x9,x10,x11,x12,x13,x14,x15], [y0,y1,y2,y3,y4,y5,y6,y8,y9,y10,y11,y12,y13,y14,y15], start_x10, start_y10)

        x11, y11 = cal_pose(x11, y11, x11g, y11g, [x0,x1,x2,x3,x4,x5,x6,x8,x9,x10,x7,x12,x13,x14,x15], [y0,y1,y2,y3,y4,y5,y6,y8,y9,y10,y7,y12,y13,y14,y15], start_x11, start_y11)

        x12, y12 = cal_pose(x12, y12, x12g, y12g, [x0,x1,x2,x3,x4,x5,x6,x8,x9,x10,x11,x7,x13,x14,x15], [y0,y1,y2,y3,y4,y5,y6,y8,y9,y10,y11,y7,y13,y14,y15], start_x12, start_y12)

        x13, y13 = cal_pose(x13, y13, x13g, y13g, [x0,x1,x2,x3,x4,x5,x6,x8,x9,x10,x11,x12,x7,x14,x15], [y0,y1,y2,y3,y4,y5,y6,y8,y9,y10,y11,y12,y7,y14,y15], start_x13, start_y13)

        x14, y14 = cal_pose(x14, y14, x14g, y14g, [x0,x1,x2,x3,x4,x5,x6,x8,x9,x10,x11,x12,x13,x7,x15], [y0,y1,y2,y3,y4,y5,y6,y8,y9,y10,y11,y12,y13,y7,y15], start_x14, start_y14)

        x15, y15 = cal_pose(x15, y15, x15g, y15g, [x0,x1,x2,x3,x4,x5,x6,x8,x9,x10,x11,x12,x13,x14,x7], [y0,y1,y2,y3,y4,y5,y6,y8,y9,y10,y11,y12,y13,y14,y7], start_x15, start_y15)

        plt.annotate("1",xy=(start_x4 - 1, start_y4))
        plt.annotate("2",xy=(start_x8 - 1, start_y8 ))
        plt.annotate("3",xy=(start_x1 - 1, start_y1))
        plt.annotate("5",xy=(start_x5  , start_y5+1))
        plt.annotate("7",xy=(start_x2 + 1, start_y2))
        plt.annotate("9",xy=(start_x6 + 1, start_y6 ))
        plt.annotate("11",xy=(start_x3 + 1, start_y3))
        plt.annotate("13",xy=(start_x7 , start_y7-1.2))
        plt.annotate("15",xy=(start_x0 - 1, start_y0))
        plt.annotate("4",xy=(start_x9 - 1, start_y9))
        plt.annotate("6",xy=(start_x10  , start_y10+1))
        plt.annotate("8",xy=(start_x11 + 1, start_y11))
        plt.annotate("10",xy=(start_x12 + 1, start_y12 ))
        plt.annotate("12",xy=(start_x13 + 1, start_y13))
        plt.annotate("14",xy=(start_x14 , start_y14-1.2))
        plt.annotate("16",xy=(start_x15 , start_y15-1.2))
        plt.plot(x0,y0,".",color='blue')
        plt.plot(x1,y1,".",color="red")
        plt.plot(x2,y2,".",color='green')
        plt.plot(x3,y3,".",color='yellow')
        plt.plot(x4,y4,".",color='purple')
        plt.plot(x5,y5,".",color='orange')
        plt.plot(x6,y6,".",color='pink')
        plt.plot(x7,y7,".",color='brown')
        plt.plot(x8,y8,".",color='lime')
        plt.plot(x9,y9,".",color="cyan")
        plt.plot(x10,y10,".",color='yellowgreen')
        plt.plot(x11,y11,".",color='magenta')
        plt.plot(x12,y12,".",color='hotpink')
        plt.plot(x13,y13,".",color='gray')
        plt.plot(x14,y14,".",color='black')
        plt.plot(x15,y15,".",color='skyblue')
        plt.axis("equal")
        plt.grid(True)

        plt.pause(0.05)
    
    plt.savefig("D:/C/uet_4_2/rbpt/tuan4/16.png", dpi=600)
    plt.show()
            

if __name__ == '__main__':
    main()