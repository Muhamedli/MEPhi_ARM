import traj_planning as tk
import serial_port as sp
import time

sp.serialBegin(baytrate = 115200)

# traj = tk.trajFromCurToGiven(tk.robot.qr)
# sp.sendTraj(traj)
#
# traj = tk.trajFromCurToGiven(tk.robot.qz)
# sp.sendTraj(traj)

#ЕБАНЫЕ радианы!!!
deg = [0.0, 0.0, 0.0, 0.0, 0.0, -0.15]
speed = [0.5] * 6

sp.serialSend(deg, speed)
sp.serialRead()

# sp.serialSend(deg, speed)
# sp.serialRead()

sp.ser.write(bytes("101a", 'utf-8'))
sp.serialRead()
sp.serialRead()