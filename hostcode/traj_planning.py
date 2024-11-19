import roboticstoolbox as rtb
import spatialmath as sm
import numpy as np
import swift

hight = 0.308

robot = rtb.models.MEPhI_ARM()
robot.q = robot.qz

env = swift.Swift()
env.launch(realtime=True)
env.add(robot)


def SolDegrees(tvec, trans_matrix, q=robot.qr, const_orient=True):
    sol = SolFinder(tvec, trans_matrix, const_orient, q)
    robot.q = sol
    env.step()
    sol = list(map(lambda x: round((x / np.pi * 180), ndigits=1), sol))
    return sol


# def TrajFromQToPoint(tvec, trans_matrix, q=robot.qr, const_orient=True):
#     sol = SolFinder(tvec, trans_matrix, const_orient, q)
#     traj = rtb.tools.trajectory.jtraj(q, sol, 10)
#     return traj


def SolFinder(tvec, trans_matrix, const_orient=True, q=robot.qr):
    '''поиск и верефикация решения в конечной точке'''

    new_y_axis_orientation = trans_matrix[1]

    if (const_orient):
        # new_y_axis_orientation[1] = 1 #Возможно здесь нужно будет потом заменить на ноль
        new_y_axis_orientation[2] = 0
        new_z_axis_orientation = [0, 0, 1]
    else:
        new_z_axis_orientation = trans_matrix[2]

    Tep = robot.fkine(q) * sm.SE3.Trans(tvec[0], tvec[1], tvec[2]) * sm.SE3.OA(new_y_axis_orientation,
                                                                               new_z_axis_orientation)
    sol = robot.ik_LM(Tep)

    if (chekTaskPresessing(tvec, sol[0], q)):
        return sol[0]
    else:
        print("trouble")
        return None


def chekTaskPresessing(tvec, sol, q):
    '''функция для сопоставления найденного решения и входных данных'''

    tvec_env, rvec_env = FromQtoVec(q, sol)
    if (abs(tvec[2] - tvec_env[2]) + abs(tvec[0] - tvec_env[0]) + abs(tvec[1] - tvec_env[1]) < 0.005):
        return 1
    else:
        return 0


def FromQtoVec(qBeg, qEnd):
    '''функция для нахождения вектора перемещения и матрицы перехода от одной конфигурации к другой'''

    tvec = [0, 0, 0]
    end_rmatx = [[], [], []]
    beg_rmatx = [[], [], []]

    for i in range(3):
        tvec[i] = ((robot.fkine(qEnd).A)[i][3] - (robot.fkine(qBeg).A)[i][3])
        beg_rmatx[i] = list((robot.fkine(qBeg).A)[i][:3])
        end_rmatx[i] = list((robot.fkine(qEnd).A)[i][:3])

    tvec = np.transpose(np.matmul(np.linalg.inv(np.array(beg_rmatx)), np.array(tvec).transpose()))

    trans_mtx = np.linalg.inv(np.array(end_rmatx)).dot(np.array(beg_rmatx))
    return tvec, trans_mtx


def jtrajFromCurToGiven(qFinish, travel_time = 3):
    global step_time

    step = 50
    step_time = travel_time / step
    time_vec = np.arange(0, travel_time, step_time)
    sol = None
    if qFinish is not None:
        sol = rtb.tools.trajectory.jtraj(robot.q, qFinish, time_vec)
    return sol

def ctrajFromCurToGiven(qFinish, time = 4):
    step = 50
    traj = rtb.tools.trajectory.ctraj(robot.fkine(robot.q), robot.fkine(qFinish), step)
    cartesian_sol = robot.ikine_LM(traj)
    
    
    velocity_array = np.ndarray(shape=(step - 1, 6))  # Создание массива для хранения скоростей в осях
    for i in range(step - 1):  # вычисление обобщенных скоростей в осях для каждой точки траектории
        for k in range(6):
            velocity_array[i][k] = (cartesian_sol.q[i + 1][k] - cartesian_sol.q[i][k]) / float(time/step)

    traj = rtb.tools.trajectory.Trajectory(name = "ctraj", s = cartesian_sol.q[1:], sd = velocity_array, t = time)
    return traj
