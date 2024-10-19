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
    for i in range(6):
        if(abs(speed[i]) < 0.001):
            deg[i] = tk.robot.q[i]
                
    tk.robot.q = deg

    dataArray = list(map(lambda x: round(x * 180 / 3.14159, ndigits=5), deg))
    dataArray.extend(list(map(lambda x: round(x * 180 / 3.14159, ndigits=5), speed)))

    for i in [1, 5]:
        dataArray[i] *= -1

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
    for i in range(1, len((traj.q))-1):
        print(i, end=' ')
        serialSend(traj.q[i], traj.qd[i])
        serialRead()
    ser.write(bytes("101a", 'utf-8'))
    serialRead()
    for i in range(len((traj.q))-3):
        serialRead()
        tk.robot.q = traj.q[i]
        tk.env.step()
    serialRead()
