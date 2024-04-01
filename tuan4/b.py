import numpy as np
import matplotlib.pyplot as plt
SIM_TIME = 5
dt = 0.1

def main():
    time = 0
    ix = 0
    iy = 2
    plt.gcf().canvas.mpl_connect('key_release_event',
                                     lambda event: [exit(0) if event.key == 'escape' else None])
    while SIM_TIME>time:
        time+=dt
        ix += 0.2
        iy += 0.2

        plt.plot(iy,ix,".b")


        plt.plot(ix,iy,".r")
        plt.pause(0.12)
    
    plt.show()

if __name__ == '__main__':
    main()