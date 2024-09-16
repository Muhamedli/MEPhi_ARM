#include <GyverStepper.h>
#include <ESP32Servo.h>
#include <StringUtils.h>

GStepper<STEPPER2WIRE> stepper1(200 * 16 * 11, 18, 5);
GStepper<STEPPER2WIRE> stepper2(200 * 16 * 12, 17, 16);
GStepper<STEPPER2WIRE> stepper3(200 * 16 * 15, 27, 14);
GStepper<STEPPER2WIRE> stepper4(200 * 16 * 9, 2, 15);
GStepper<STEPPER2WIRE> stepper5(200 * 16 * 6, 26, 25);
GStepper<STEPPER2WIRE> stepper6(200 * 16 * 50, 33, 32);

Servo myservo;

float Max_speed_stepper1 = 15.0;
float Max_speed_stepper2 = 10.0;
float Max_speed_stepper3 = 15.0;
float Max_speed_stepper4 = 25.0;
float Max_speed_stepper5 = 15.0;
float Max_speed_stepper6 = 20.0;

float accel_stepper1 = 7.5;
float accel_stepper2 = 10.0;
float accel_stepper3 = 7.5;
float accel_stepper4 = 15.0;
float accel_stepper5 = 10.0;
float accel_stepper6 = 10.0;

float pos[7] = { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };
float speedMass[6];

bool isReadyAnnounced = false;

void setup() {
  stepper1.setRunMode(FOLLOW_POS);
  stepper1.setMaxSpeedDeg(Max_speed_stepper1);  // в градусах/сек
  stepper1.setAccelerationDeg(accel_stepper1);
  stepper1.autoPower(true);

  stepper2.setRunMode(FOLLOW_POS);
  stepper2.setMaxSpeedDeg(Max_speed_stepper2);  // в градусах/сек
  stepper2.setAccelerationDeg(accel_stepper2);
  stepper2.autoPower(true);

  stepper3.setRunMode(FOLLOW_POS);
  stepper3.setMaxSpeedDeg(Max_speed_stepper3);  // в градусах/сек
  stepper3.setAccelerationDeg(accel_stepper3);
  stepper3.autoPower(true);

  stepper4.setRunMode(FOLLOW_POS);
  stepper4.setMaxSpeedDeg(Max_speed_stepper4);  // в градусах/сек
  stepper4.setAccelerationDeg(accel_stepper4);
  stepper4.autoPower(true);

  stepper5.setRunMode(FOLLOW_POS);
  stepper5.setMaxSpeedDeg(Max_speed_stepper5);  // в градусах/сек
  stepper5.setAccelerationDeg(accel_stepper5);
  stepper5.autoPower(true);

  stepper6.setRunMode(FOLLOW_POS);
  stepper6.setMaxSpeedDeg(Max_speed_stepper6);  // в градусах/сек
  stepper6.setAccelerationDeg(accel_stepper6);
  stepper6.autoPower(true);

  Serial.begin(115200);

  if(!myservo.attached()) {
    myservo.attach(13); 
  }
}
void set_Speed(float speedMass[6]) {
  stepper1.setMaxSpeedDeg(speedMass[0]);  // в градусах/сек
  stepper2.setMaxSpeedDeg(speedMass[1]);  // в градусах/сек
  stepper3.setMaxSpeedDeg(speedMass[2]);  // в градусах/сек
  stepper4.setMaxSpeedDeg(speedMass[3]);  // в градусах/сек
  stepper5.setMaxSpeedDeg(speedMass[4]);  // в градусах/сек
  stepper6.setMaxSpeedDeg(speedMass[5]);  // в градусах/сек
}
void Go(){ 
  if (!stepper1.tick()) {
    stepper1.setTargetDeg(pos[0], ABSOLUTE);
  }
  if (!stepper2.tick()) {
    stepper2.setTargetDeg(pos[1], ABSOLUTE);
  }
  if (!stepper3.tick()) {
    stepper3.setTargetDeg(pos[2], ABSOLUTE);
  }
  if (!stepper4.tick()) {
    stepper4.setTargetDeg(pos[3], ABSOLUTE);
  }
  if (!stepper5.tick()) {
    stepper5.setTargetDeg(pos[4], ABSOLUTE);
  }
  if (!stepper6.tick()) {
    stepper6.setTargetDeg(pos[5], ABSOLUTE);
  }
  myservo.write(pos[6]);
}
// строка типа: 10.0/20.0/ ... 15.0/15.0/ ... 10.0/10.0/ ... 10.0
// сперва 6 углов для шаговиков, потом 6 скоростей для шаговиков, 
// потом 6 ускорений для шаговиков, последним указывается угол для серво
void Read(const Text& COM_port, float pos[], float speed[], bool withServo) {
  int i = 0;
  for(i; i < 6; i++) {
    pos[i] = COM_port.getSub(i, '/').toFloat();
    speed[i] = COM_port.getSub(i + 6, '/').toFloat();
    accel[i] = COM_port.getSub(i + 12, '/').toFloat();
  }
  if(withServo) {
    pos[6] = COM_port.getSub(18, '/').toFloat();
  }
}

void Split(String data, float mass[]){
  int i, j = 0, t = 0;
  for(i = 0; i < data.length(); i++){
    if(data[i] == ' '){
      mass[t] = data.substring(j, i).toFloat();
      j = i + 1;
      t++;
    }
  }
  mass[t] = data.substring(j).toFloat();
}

void InputData() {
  if (Serial.available() > 1) {
    isReadyAnnounced = false;
    String COM_port = Serial.readString();
    if(COM_port == "stop") {
      stepper1.brake();
      stepper2.brake();
      stepper3.brake();
      stepper4.brake();
      stepper5.brake();
      stepper6.brake();
    }
    else {
      //Read(COM_port, pos, speedMass, true);
      Split(COM_port, pos);
      }
    }
  }
}
void OutputData() {
  if (!isReadyAnnounced && !stepper1.tick() && !stepper2.tick() && !stepper3.tick() && !stepper4.tick() && !stepper5.tick() && !stepper6.tick()) {
    Serial.print('1');
    isReadyAnnounced = true;
  }
}
void loop() {
  Go();
  OutputData();
  InputData();
}