from machine import Pin, ADC
from time import sleep
#import _thread

encoder_angle = 360                       #угол раствора энкодера
keyboard_input = 0                      #режим ввода угла поворота
delay = 0.00001                           #задержка между шагами         

DIR_1 = Pin(4, Pin.OUT)                 # направление движения 1 - по часовой, 0 - против
STEP_1 = Pin(2, Pin.OUT)                # один шаг двигателя
INPUT_1 = ADC(Pin(26))                  # подключение пина для ручки
INPUT_1.atten(ADC.ATTN_11DB)

DIR_2 = Pin(5, Pin.OUT)
STEP_2 = Pin(18, Pin.OUT)
INPUT_2 = ADC(Pin(27))
INPUT_2.atten(ADC.ATTN_11DB)

'''
DIR_3 = Pin(..., Pin.OUT)
STEP_3 = Pin(..., Pin.OUT)

DIR_4 = Pin(..., Pin.OUT)
STEP_4 = Pin(..., Pin.OUT)
'''

#DIR = [DIR_1, DIR_2, DIR_3, DIR_4, DIR_5, DIR_6]
#STEP = [STEP_1, STEP_2, STEP_3, STEP_4, STEP_5, STEP_6]

DIR = [DIR_1, DIR_2]
STEP = [STEP_1, STEP_2]
INPUT = [INPUT_1, INPUT_2]


Motors_steps_in_deegres = [0.1125, 0.1125, 0.05625, 0.05625, 0.05625, 0.05625]    # градус на один шаг


motors_number = len(STEP)

MOTOR_current_position = [0 for i in range(motors_number)]


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

def recvie_angle():                                                                     #получение угла поворта
    global MOTOR_current_position
    conflict = 0
    
    if keyboard_input:
        input_data = list(map(int, input('угол?\n').split(' ')))                        #обработка данных с клавиатуры
    else:
        input_data = list(map(lambda x: x.read()*(encoder_angle/4095) - encoder_angle/2, INPUT)) #обработка данных с энкодера
    
    for j in range(motors_number):
        if INPUT[j] != MOTOR_current_position[j]:
            conflict = 1
    
    if conflict:
        angle_processing(input_data)

def angle_processing(input_data):
    global MOTOR_deg
    
    now = MOTOR_current_position
    new_deg = input_data                                                        # новое положение мотора после поворота ручки
    
    rotation_angle = [abs(new_deg[i] - now[i]) for i in range(motors_number)]
    rotation_direction = [new_deg[i] >= now[i] for i in range(motors_number)]

    steps(rotation_direction, rotation_angle)
    
    MOTOR_current_position = input_data
    
    sleep(0.1)

def steps(rotation_direction, degrees):                           # шаги : направление и количество шагов по 1,8 градусов
    count_of_steps = [round(degrees[i] / Motors_steps_in_deegres[i]) for i in range(motors_number)]
    
    for index in range(motors_number):
        DIR[index].value(rotation_direction[index])                                 # установка направления
    
    while sum(count_of_steps) > 0:
        for index in range(motors_number):
            if count_of_steps[index] > 0:
                STEP[index].value(1)                                    # подать напряжение на мотор
                sleep(delay)                                           # задержка 0,01 секунда
                STEP[index].value(0)                                    # снять напряжение с мотора
                sleep(delay)                                           # чем быстрее идет смена подачи напрядения, тем выше скорость поворота
                count_of_steps[index] -= 1

#main
#potoc1 = _thread.start_new_thread(movement, [0])            # поток для первого мотора
#potoc2 = _thread.start_new_thread(movement, [1])            # поток для второго мотора

while True:
    recvie_angle()

