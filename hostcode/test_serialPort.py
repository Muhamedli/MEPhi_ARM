import taking as tk
import serialPort as sp
import time

sp.serialBegin(baytrate = 921600)

# traj = tk.trajFromCurToGiven(tk.robot.qr)
# sp.sendTraj(traj)
#
# traj = tk.trajFromCurToGiven(tk.robot.qz)
# sp.sendTraj(traj)

#ЕБАНЫЕ радианы!!!
deg = [1.6, 1.4, 2.5, 2.8, 2.7, 0.0]
speed = [1.0] * 6

sp.serialSend(deg, speed)
sp.serialRead()

# sp.serialSend(deg, speed)
# sp.serialRead()

sp.ser.write(bytes("101a", 'utf-8'))
sp.serialRead()
