import taking as tk
import serialPort as sp

sp.serialBegin(baytrate = 921600)

traj = tk.trajFromCurToWork()
sp.sendTraj(traj)

# deg = [-10.1, 2.4, 8.3, 5.3, 3.9, 0.0]
# speed = [10.0] * 6
#
# sp.serialSend(deg, speed)
# sp.serialRead()
#
# deg = [-10.1, 2.4, 8.3, 5.3, 3.9, 0.0]
# speed = [10.0] * 6
#
# sp.serialSend(deg, speed)
# sp.serialRead()
