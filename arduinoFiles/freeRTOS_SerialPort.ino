#define STEP1 18                                                                   //управляющие пины
#define STEP2 4
#define DIR1 43
#define DIR2 32
#define FREQ 20                                                                   //частота подачи сигнал на управляющий пин(для веб-управления)
#define MOTORNUM 2                                                                //колличество моторов
#define DATAPACKLENGTH 2                                                          //колличество данных, передающихся на один мотор

SemaphoreHandle_t sem1;                                     
SemaphoreHandle_t sem2;

QueueHandle_t queue1;
QueueHandle_t queue2;

struct motorData                                                                  //информация для инициализации мотора
{
    int num;
    int pinStep;
    int pinDir;
    float degPerStep;
};

struct taskPackage                                                                //структура для передачи пакета данных на мотор
{
    int degrees;
    int speed;
    int accseleration;
};

motorData motorData1 = {0, STEP1, DIR1, 10.0};
motorData motorData2 = {1, STEP2, DIR2, 10.0};

SemaphoreHandle_t *semArray[] = {&sem1, &sem2};
SemaphoreHandle_t *queueArray[] = {&queue1, &queue2};

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
    motorData *motorInfo = (motorData *) pvParametrs;
    taskPackage currentTask;
    
    pinMode(motorInfo -> pinStep, OUTPUT);
    pinMode(motorInfo -> pinDir, OUTPUT);

    while(1){
        //xSemaphoreTake(*(semArray[motorInfo->num]), portMAX_DELAY);                 //ожидание семафора для начало работы
        xQueueReceive(*(queueArray[motorInfo->num]), &currentTask, 0);              //считывание значения из очереди

        if(currentTask.speed>0) digitalWrite(motorInfo -> pinDir, HIGH);
        else if(currentTask.speed<0) digitalWrite(motorInfo -> pinDir, LOW);
     
        if(0< (int) currentTask.degrees/(motorInfo->degPerStep)){
            digitalWrite(motorInfo -> pinStep, HIGH);
            delay((int)(500/(float) (currentTask.speed/motorInfo->degPerStep)));
            digitalWrite(motorInfo -> pinStep, LOW);
            delay((int)(500/(float) currentTask.speed/motorInfo->degPerStep));
            currentTask.steps--;
        }
        delay(10);
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
                    default:
                        break;
                    }
                }
                currentTask.speed = FREQ*10;
                
                if(i!=MOTORNUM && wrightingFlag == 1){
                  Serial.println("send");
                  Serial.println(i);
                  Serial.println(currentTask.degrees);
                  xQueueSend(*(queueArray[i]), &currentTask, 0);
                  //xSemaphoreGive(*(semArray[i]));
                }
            }
        }
        delay(30);
    }
}

void loop(){}
