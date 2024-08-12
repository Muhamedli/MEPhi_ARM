"""

код был написан для отладки тестовой сборки электроники; для монтроллера под управлением micropython

"""

from machine import Pin, ADC
from time import sleep
#import _thread

encoder_angle = 360                         #угол раствора энкодера
keyboard_input = 0                          #режим ввода угла поворота (1-клавиатура)
delay = 0.001                               #задержка между шагами         

DIR_1 = Pin(0, Pin.OUT)                     # направление движения 1 - по часовой, 0 - против
STEP_1 = Pin(4, Pin.OUT)                    # один шаг двигателя                 

DIR_2 = Pin(32, Pin.OUT)
STEP_2 = Pin(33, Pin.OUT)

DIR_3 = Pin(25, Pin.OUT)
STEP_3 = Pin(26, Pin.OUT)

DIR_4 = Pin(27, Pin.OUT)
STEP_4 = Pin(14, Pin.OUT)

DIR_5 = Pin(12, Pin.OUT)
STEP_5 = Pin(13, Pin.OUT)

DIR_6 = Pin(2, Pin.OUT)
STEP_6 = Pin(15, Pin.OUT)


DIR = [DIR_1, DIR_2, DIR_3, DIR_4, DIR_5, DIR_6]
STEP = [STEP_1, STEP_2, STEP_3, STEP_4, STEP_5, STEP_6]

#DIR = [DIR_1, DIR_2]
#STEP = [STEP_1, STEP_2]


Motors_steps_in_deegres = [0.05625, 0.05625, 0.05625, 0.05625, 0.05625, 0.05625]    # градус на один шаг

'''
for DRV8825
M0 M1 M2 steps
0  0  0   1.8
1  0  0   0.9
0  1  1   0.45
1  1  0   0.225
0  0  1   0.1125
1  0  1   0.05625
0  1  1   0.05625
1  1  1   0.05625   (+)   1 градус в 0,036 секунд, то есть 360 градусов это 12,96 секунд

for A4988
MS1 MS2 MS3 steps
0   0   0   1.8
1   0   0   0.9
0   1   0   0.45
1   1   0   0.225
1   1   1   0.1125  (+)
'''

motors_number = len(STEP)

MOTOR_current_position = [0 for i in range(motors_number)]



def recvie_angle():                                                                     #получение угла поворта
    global MOTOR_current_position
    
    if keyboard_input:
        input_data = list(map(int, input('угол?\n').split(' ')))                        #обработка данных с клавиатуры
    
    else:
        input_data = [90, 90, 90, 90, 90, 90]


    angle_processing(input_data)


def angle_processing(input_data):
    global MOTOR_current_position
    
    now = MOTOR_current_position
    new_angle = input_data                                                              # новое положение мотора после поворота ручки
    
    rotation_angle = [abs(new_angle[i] - now[i]) for i in range(motors_number)]         #угол, на который нужно повернуть
    rotation_direction = [new_angle[i] >= now[i] for i in range(motors_number)]         #направление, в котором нужно повернуть

    steps(rotation_direction, rotation_angle)
    
    MOTOR_current_position = input_data
    
    sleep(0.01)


def steps(rotation_direction, degrees):                                                 # шаги : направление и количество шагов по 1,8 градусов
    count_of_steps = [round(degrees[i] / Motors_steps_in_deegres[i]) for i in range(motors_number)]
    
    for index in range(motors_number):
        DIR[index].value(rotation_direction[index])                                     # установка направления
    
    while sum(count_of_steps) > 0:
        for index in range(motors_number):
            if count_of_steps[index] > 0:
                STEP[index].value(1)                                                    # подать напряжение на мотор
                sleep(delay)                                                            # задержка 0,01 секунда
                STEP[index].value(0)                                                    #снять напряжение с мотора
                sleep(delay)                                                            #чем быстрее идет смена подачи напрядения, тем выше скорость поворота
                count_of_steps[index] -= 1

#main
#potoc1 = _thread.start_new_thread(movement, [0])            # поток для первого мотора
#potoc2 = _thread.start_new_thread(movement, [1])            # поток для второго мотора

while True:
    recvie_angle()

