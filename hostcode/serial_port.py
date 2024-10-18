from tkinter.constants import ROUND

import serial
import traj_planning as tk
import time


def serialBegin(port=5, baytrate=115200):
    global ser
    port = f"COM{port}"  # Replace with the appropriate COM port name
    ser = serial.Serial(port, baytrate)
    print("wew")
    time.sleep(1)  # чтобы esp32 успела инициализироваться


def serialSend(deg, speed):
    deg = list(map(lambda x: round(x * 180 / 3.14159, ndigits=5), deg))
    speed = list(map(lambda x: round(x * 180 / 3.14159, ndigits=5), speed))

    for i in range(6):
        if(abs(speed[i]) < 0.001):
            deg[i] = tk.robot.q[i]

    dataArray = deg.extend(speed)
    tk.robot.q = deg

    output_text = ""
    output_text = "/".join(str(i) for i in dataArray)
    ser.write(bytes(output_text, 'utf-8'))
    print(bytes(output_text,'utf-8'))


def serialRead():
    flag = '0'
    while (flag == '0'):
        flag = ser.read()
        print(flag)


def sendTraj(traj):
    for i in range(2, len((traj.q))-1):
        traj.q[i][1] = traj.q[i][1] * -1
        traj.q[i][5] = traj.q[i][5] * -1
        print(i, end=' ')
        serialSend(traj.q[i], traj.qd[i])
        serialRead()
    ser.write(bytes("101a", 'utf-8'))
    serialRead()
    for i in range(len((traj.q))-4):
        serialRead()
        tk.env.step()
    serialRead()
