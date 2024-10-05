import taking as tk
import serialPort as sp
import time

sp.serialBegin(baytrate = 921600)

# traj = tk.trajFromCurToGiven(tk.robot.qr)
# sp.sendTraj(traj)
#
# traj = tk.trajFromCurToGiven(tk.robot.qz)
# sp.sendTraj(traj)

#
deg = [0.0, 0, 0, 0.0, 0, 0.14]
speed = [1.0] * 6

sp.serialSend(deg, speed)
sp.serialRead()

data = "101a"
sp.ser.write(data.encode('raw_unicode_escape'))
print(data.encode('raw_unicode_escape'))
output = sp.ser.read().decode()
print(output)
