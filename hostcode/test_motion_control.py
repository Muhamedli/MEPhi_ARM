import taking as tk
import serialPort as sp
import time
import numpy as np

sp.serialBegin(baytrate = 921600)

traj = tk.trajFromCurToGiven(tk.robot.qr)
sp.sendTraj(traj)

traj = tk.trajFromCurToGiven(tk.SolFinder([0, 0, 0.1], np.eye(3), q =  tk.robot.q))
sp.sendTraj(traj)

tk.env.hold()

#
# deg = [0.0, 0, 0, -0.85, 0, 0.0]
# speed = [1.0] * 6
#
# sp.serialSend(deg, speed)
# sp.serialRead()
#
# data = "101a"
# sp.ser.write(data.encode('raw_unicode_escape'))
# print(data.encode('raw_unicode_escape'))
# output = sp.ser.read().decode()
# print(output)
