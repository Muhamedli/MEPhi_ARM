import traj_planning as tk
import serial_port as sp
import time
import numpy as np

sp.serialBegin(port = 3,baytrate = 115200)

traj = tk.jtrajFromCurToGiven(tk.robot.qr)
sp.sendTraj(traj)

traj = tk.jtrajFromCurToGiven(tk.SolFinder([0.0, -0.05, 0.10], np.eye(3), q =  tk.robot.q))
sp.sendTraj(traj)

traj = tk.jtrajFromCurToGiven(tk.SolFinder([0.1, 0.0, 0.0], np.eye(3), q =  tk.robot.q))
sp.sendTraj(traj)

traj = tk.jtrajFromCurToGiven(tk.SolFinder([0, -0.1, 0.0], np.eye(3), q =  tk.robot.q))
sp.sendTraj(traj)

traj = tk.jtrajFromCurToGiven(tk.SolFinder([-0.2, 0, 0.0], np.eye(3), q =  tk.robot.q))
sp.sendTraj(traj)

traj = tk.jtrajFromCurToGiven(tk.SolFinder([0, 0.1, 0.0], np.eye(3), q =  tk.robot.q))
sp.sendTraj(traj)


traj = tk.jtrajFromCurToGiven(tk.robot.qz)
sp.sendTraj(traj)


# for i in range(len(traj.q)-1):
#     times = [0, 0, 0, 0, 0, 0]
#     for j in range(6):
#         if(traj.qd[i+1][j]!=0):
#             times[j] = (round(traj.q[i+1][j] * np.pi/180, 3)-round(traj.q[i][j]*np.pi/180, 3))/(traj.qd[i+1][j]*np.pi/180)
#         else:
#             times[j] = 0
#     print(times)


# deg = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# speed = [5.0] * 6

# for i in range(20):
#     deg[1]-=0.00
#     deg[2]+=0.01
#     deg[4]+=0.00

#     sp.serialSend(deg, speed)
#     sp.serialRead()


# data = "101a"
# sp.ser.write(data.encode('raw_unicode_escape'))
# sp.serialRead()
# sp.serialRead()