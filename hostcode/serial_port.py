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
    dataArray = list(map(lambda x: round(x * 180 / 3.14159, ndigits=2), deg))
    dataArray.extend(list(map(lambda x: round(x * 180 / 3.14159, ndigits=4), speed)))
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
        tk.robot.q = traj.q[i]
        traj.q[i][1] = traj.q[i][1] * -1
        traj.q[i][5] = traj.q[i][5] * 0
        tk.env.step()
        serialSend(traj.q[i], traj.qd[i])
        serialRead()
    ser.write(bytes("101a", 'utf-8'))
    serialRead()
    # print((len((traj.q))-10) * 2 + 10)
    # for i in range(len((traj.q))//10 * 20 + len((traj.q))%10):
    #     serialRead()
    serialRead()
