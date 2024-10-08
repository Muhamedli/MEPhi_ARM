import taking as tk
import serialPort as sp
import time
import numpy as np

sp.serialBegin(baytrate = 921600)

traj = tk.trajFromCurToGiven(tk.robot.qr)
sp.sendTraj(traj)

traj = tk.trajFromCurToGiven(tk.SolFinder([0, 0, 0.1], np.eye(3), q =  tk.robot.q))
sp.sendTraj(traj)

for i in range(len(traj.q)-1):
    times = [0, 0, 0, 0, 0, 0]
    for j in range(6):
        if(traj.qd[i+1][j]!=0):
            times[j] = (round(traj.q[i+1][j] * np.pi/180, 3)-round(traj.q[i][j]*np.pi/180, 3))/(traj.qd[i+1][j]*np.pi/180)
        else:
            times[j] = 0
    print(times)


# deg = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# speed = [0.4] * 6
#
# for i in range(20):
#     deg[1]-=0.02
#     deg[2]+=0.02
#     deg[4]+=0.05
#
#     sp.serialSend(deg, speed)
#     sp.serialRead()
#
#
# data = "101a"
# sp.ser.write(data.encode('raw_unicode_escape'))
# print(data.encode('raw_unicode_escape'))
# output = sp.ser.read().decode()
# print(output)
