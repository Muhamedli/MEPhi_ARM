import serial.tools.list_ports
import time


def serialBegin(port = 5, baytrate = 115200):
    global ser
    port = f"COM{port}"  # Replace with the appropriate COM port name
    ser = serial.Serial(port, baytrate)

def serialSend(deg, speed):
    global output_text
    deg.extend(speed)
    output_text = ""
    output_text = "/".join(str(i) for i in deg)

    ser.write(output_text.encode('raw_unicode_escape'))
    print(output_text)

def serialRead():
    flag = 0
    while(not flag):
        flag = ser.read().decode()
    print(flag)

serialBegin()

array = [[0.2, 0, 0], [0, 0, 0.2], [-0.2, 0, 0], [0, 0, -0.2]]

deg = [-10.1, 2.4, 8.3, 5.3, 3.9, 0.0]
speed = [10.0] * 6

serialSend(deg, speed)
serialRead()

deg = [10.1, 2.4, 8.3, 5.3, 3.9, 0.0]
speed = [10.0] * 6

serialSend(deg, speed)
serialRead()
