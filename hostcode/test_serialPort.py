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
deg = [0.0, 0.0, 0.4, 0.0, 0.0, 0.0]
speed = [0.5] * 6

sp.serialSend(deg, speed)
sp.serialRead()

# sp.serialSend(deg, speed)
# sp.serialRead()

sp.ser.write(bytes("101a", 'utf-8'))
sp.serialRead()
sp.serialRead()

deg = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
speed = [0.5] * 6

sp.serialSend(deg, speed)
sp.serialRead()
sp.ser.write(bytes("101a", 'utf-8'))
sp.serialRead()
sp.serialRead()