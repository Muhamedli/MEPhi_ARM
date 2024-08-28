#include <GyverStepper.h>
// #include <cstring>

GStepper<STEPPER2WIRE> stepper1(200 * 16 * 11, 18, 5);
GStepper<STEPPER2WIRE> stepper2(200 * 16 * 12, 17, 16);
GStepper<STEPPER2WIRE> stepper3(200 * 16 * 15, 27, 14);
GStepper<STEPPER2WIRE> stepper4(200 * 16 * 9, 2, 15);
GStepper<STEPPER2WIRE> stepper5(200 * 16 * 6, 26, 25);
GStepper<STEPPER2WIRE> stepper6(200 * 16 * 50, 33, 32);

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

float pos[6] = { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

bool isReadyAnnounced = false;

void setup() {
  stepper1.setRunMode(FOLLOW_POS);              // режим поддержания скорости
  stepper1.setMaxSpeedDeg(Max_speed_stepper1);  // в градусах/сек
  stepper1.setAccelerationDeg(accel_stepper1);
  stepper1.autoPower(true);

  stepper2.setRunMode(FOLLOW_POS);              // режим поддержания скорости
  stepper2.setMaxSpeedDeg(Max_speed_stepper2);  // в градусах/сек
  stepper2.setAccelerationDeg(accel_stepper2);
  stepper2.autoPower(true);

  stepper3.setRunMode(FOLLOW_POS);              // режим поддержания скорости
  stepper3.setMaxSpeedDeg(Max_speed_stepper3);  // в градусах/сек
  stepper3.setAccelerationDeg(accel_stepper3);
  stepper3.autoPower(true);

  stepper4.setRunMode(FOLLOW_POS);              // режим поддержания скорости
  stepper4.setMaxSpeedDeg(Max_speed_stepper4);  // в градусах/сек
  stepper4.setAccelerationDeg(accel_stepper4);
  stepper4.autoPower(true);

  stepper5.setRunMode(FOLLOW_POS);              // режим поддержания скорости
  stepper5.setMaxSpeedDeg(Max_speed_stepper5);  // в градусах/сек
  stepper5.setAccelerationDeg(accel_stepper5);
  stepper5.autoPower(true);

  stepper6.setRunMode(FOLLOW_POS);              // режим поддержания скорости
  stepper6.setMaxSpeedDeg(Max_speed_stepper6);  // в градусах/сек
  stepper6.setAccelerationDeg(accel_stepper6);
  stepper6.autoPower(true);

  Serial.begin(115200);
}
// Для указания абсолютной позиции в градусах. То есть, указываешь 90, он повернулся и остановился.
// Если ему еще раз указать 90, то он не сдвинеться, так как он уже находится в данной позиции.
void GO_ABSOLUTE() {
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
}
// Для изменения абсолютной позиции. То есть, вводим 10, то абсолютная позиция изменяется на 10 и идет остановка.
// Устанавливается новая абсолютная позиция Х+10, где Х - предыдущая абсолютная позиция.
void Split_ABSOLUTE(String data, float mass[]) {
  int i, j = 0, t = 0;
  for (i = 0; i < data.length(); i++) {
    if (data[i] == ' ') {
      mass[t] = data.substring(j, i).toFloat();
      j = i + 1;
      t++;
    }
  }
  mass[t] = data.substring(j).toFloat();
}
void InputData_ABSOLUTE() {
  if (Serial.available() > 1) {
    isReadyAnnounced = false;
    String COM_port = Serial.readString();
    if (COM_port == "stop") {
      stepper1.brake();
      stepper2.brake();
      stepper3.brake();
      stepper4.brake();
      stepper5.brake();
      stepper6.brake();
    } else {
      Split_ABSOLUTE(COM_port, pos);
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
  GO_ABSOLUTE();
  OutputData();
  InputData_ABSOLUTE();
}