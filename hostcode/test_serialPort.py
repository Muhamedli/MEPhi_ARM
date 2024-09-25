import serial.tools.list_ports
import time

def sendValues(deg, speed):
    deg.extend(speed)
    output_text = ""
    for i in deg:
        output_text += str(i) + "/"

    #ser.write(output_text.encode('raw_unicode_escape'))

    print(output_text)


# port = "COM5"  # Replace with the appropriate COM port name
# baudrate = 115200  # Replace with the desired baud rate
#
# ser = serial.Serial(port, baudrate=baudrate)

deg = [-3.1, 2.4, 8.3, 5.3, 3.9, 0.0]
speed = [10.0] * 6

sendValues(deg, speed)

time.sleep(5)
