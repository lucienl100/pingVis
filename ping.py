import os
import re
import time
import math
import threading
import numpy as np
import subprocess
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib import style

maxPointsOnGraph = 40
pingL = []
timestamps = []
y_max = 100
fig = plt.figure()
ax1 = fig.add_subplot()
axes = plt.gca()
plt.ylim([0, y_max])
maxPings = 1000
class plotUpdater(threading.Thread):

    def __init__(self, animator):
        threading.Thread.__init__(self)
        self.runnable = animator
        self.daemon = True
        self.pingL = []

    def run(self):
        self.runnable()


class Anim():

    def __init__(self, fig, **kwargs):
        self.pingCount = 0
        self.responding = True

    def testStatus(self) -> bool:
        if (self.pingCount <= 1000 and self.responding):
            return True
        else:
            return False

    def startAnimation(self):
        self.ani = anim.FuncAnimation(fig=fig, func=self.animate, frames=100, interval=100)

    def animate(self, i):
        global y_max
        output = subprocess.run(["ping", "1.1.1.1", "-n", "1"], stdout = subprocess.PIPE)
        trip_time = int(timeParamIdx(str(output.stdout)))

        if (trip_time == -1):
            self.responding = False
            
        else:
            updatePingList(trip_time)
            self.pingCount += 1
            if (trip_time > y_max):
                y_max = int(trip_time * 1.1)
        if (pingL):
            max_vis_ping = max(pingL)
            if (max_vis_ping < y_max):
                y_max = max(100, y_max - (y_max - max_vis_ping) * 0.1)
        
        self.testStatus()

        xs = timestamps
        ys = pingL
        ax1.clear()
        ax1.plot(xs, ys)
        plt.ylim(0, y_max)
        
        return


def timeParamIdx(input : str) -> int:

    time = re.search(r"time=(\d*)ms", input)
    if (time):

        return time.group(1)

    else:

        return -1


def updatePingList(ping : int):

    if (len(pingL) >= maxPointsOnGraph):

        pingL.pop(0)
        timestamps.pop(0)


    pingL.append(ping)

    if (len(timestamps)):

        timestamps.append(timestamps[-1] + 1)

    else:

        timestamps.append(0)

    return


def main():

    style.use("fivethirtyeight")
    mpl.rcParams['toolbar'] = 'None'

    anim = Anim(fig)
    anim.startAnimation()

    plt.show()

if __name__ == "__main__":
    main()