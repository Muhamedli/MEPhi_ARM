import roboticstoolbox as rtb
import spatialmath as sm

robot = rtb.models.MEPhI_ARM()
robot.q = robot.qr

def TrajToSurf(x, y):
    hight = 0.28

    Tep = robot.fkine(robot.q) * sm.SE3.Trans(x, hight, y)
    sol = robot.ik_LM(Tep)
    
    traj = rtb.tools.trajectory.jtraj(robot.qz, sol[0], 100)
    return traj, Tep

def AnglePrint(x, y):
    x, y = 0.1, 0.1 
    traj1, Tep1 = TrajToSurf(x,y)
    print(*list(map(lambda x: round(x, ndigits=3),traj1.q[-1])), sep=" ")