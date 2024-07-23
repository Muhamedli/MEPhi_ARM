#define STEP1 18                                                                   //управляющие пины
#define STEP2 4
#define DIR1 43
#define DIR2 32
#define FREQ 10.0                                                                   //частота подачи сигнал на управляющий пин(для веб-управления)
#define DEGPERSTEP 1.0
#define MOTORNUM 2                                                                //колличество моторов
#define DATAPACKLENGTH 3                                                          //колличество данных, передающихся на один мотор

SemaphoreHandle_t sem1;                                     
SemaphoreHandle_t sem2;

QueueHandle_t queue1;
QueueHandle_t queue2;

struct motorData                                                                    //информация для инициализации мотора
{
    int num;
    int pinStep;
    int pinDir;
    float degPerStep;
};

struct taskPackage                                                                  //структура для передачи пакета данных на мотор
{
    float degrees;
    int speed;
    int accseleration;
};

bool flag1 = 0, flag2 = 0;                                                           //состояние процесса шагового мотора; 0 - ожидание; 1 - прерываение; 2 - работа

motorData motorData1 = {0, STEP1, DIR1, DEGPERSTEP};
motorData motorData2 = {1, STEP2, DIR2, DEGPERSTEP};

SemaphoreHandle_t *semArray[] = {&sem1, &sem2};
SemaphoreHandle_t *queueArray[] = {&queue1, &queue2};

bool flagArray[] = {flag1, flag2};

void setup(){
    Serial.begin(115200);

    sem1 = xSemaphoreCreateBinary();
    sem2 = xSemaphoreCreateBinary();
    
    queue1 = xQueueCreate(4, sizeof(taskPackage));
    queue2 = xQueueCreate(4, sizeof(taskPackage));

    xTaskCreate(&stepperMotor, "Step1", 2048, &motorData1, 1, NULL);
    xTaskCreate(&stepperMotor, "Step2", 2048, &motorData2, 1, NULL);
    xTaskCreate(gatekeeper, "Gatekeeper", 2048, NULL , 2, NULL);
}




void stepperMotor(void *pvParametrs){                                               //функция, управляющая шаговым двигателем
    static unsigned long startTime;
    motorData *motorInfo = (motorData *) pvParametrs;
    taskPackage currentTask;
    
    pinMode(motorInfo -> pinStep, OUTPUT);
    pinMode(motorInfo -> pinDir, OUTPUT);

    while(1){
        xSemaphoreTake(*(semArray[motorInfo->num]), portMAX_DELAY);                 //ожидание семафора для начало работы
        xQueueReceive(*(queueArray[motorInfo->num]), &currentTask, 0);              //считывание значения из очереди

        if(currentTask.speed>0) digitalWrite(motorInfo -> pinDir, HIGH);
        else if(currentTask.speed<0) digitalWrite(motorInfo -> pinDir, LOW);

        flagArray[motorInfo->num] = 0;

        unsigned long startTime = millis();
     
        for(int i = 0; i<(int) currentTask.degrees/(motorInfo->degPerStep); i++){

            int colission = (int)(((millis() - startTime) - i * 1000/(currentTask.speed/motorInfo->degPerStep))*1000);

            digitalWrite(motorInfo -> pinStep, HIGH);
            delayMicroseconds((int)(500000/(currentTask.speed/motorInfo->degPerStep)));
            digitalWrite(motorInfo -> pinStep, LOW);
            Serial.println("a");
            delayMicroseconds((int)(500000/(currentTask.speed/motorInfo->degPerStep) - colission));
            Serial.println("b");
            if(flagArray[motorInfo->num]==1){
                flagArray[motorInfo->num] = 0;
                break;
            }
        }

        delayMicroseconds(10);
    }
}

void gatekeeper(void *pvParametrs){
    int incomingByte = 0;
    int wrightingFlag = 0;

    taskPackage currentTask;
    while(1){
        if(Serial.available()>0){
            for(int i=0;i<=MOTORNUM;i++){
                for(int j = 0; j < DATAPACKLENGTH; j++){
                    incomingByte = Serial.parseInt();
                    switch (j)
                    {
                    case 0:
                        wrightingFlag = incomingByte;
                        break;
                    case 1:
                        currentTask.degrees = incomingByte;
                    case 2:
                        currentTask.speed = incomingByte*DEGPERSTEP;
                    default:
                        break;
                    }
                }
                //currentTask.speed = FREQ*DEGPERSTEP;
                
                if(i!=MOTORNUM && wrightingFlag == 1){
                    
                    Serial.println("send");
                    Serial.println(i);
                    Serial.println(currentTask.degrees);
                    flagArray[i] = 1;
                    xQueueSend(*(queueArray[i]), &currentTask, 0);
                    xSemaphoreGive(*(semArray[i]));
                }
            }
        }
        delay(30);
    }
}

void loop(){}
