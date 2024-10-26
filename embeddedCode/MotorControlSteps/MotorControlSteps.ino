#include <Arduino.h>
#include <GyverStepper.h>
#include <ESP32Servo.h>
#include <StringUtils.h>

#define traj_array_len 300

//Дробление шага равно 16
GStepper<STEPPER2WIRE> stepper1(200 * 16 * 11, 18, 5);
GStepper<STEPPER2WIRE> stepper2(200 * 16 * 12, 17, 16);
GStepper<STEPPER2WIRE> stepper3(200 * 16 * 15, 27, 14);
GStepper<STEPPER2WIRE> stepper4(200 * 16 * 9, 2, 15);
GStepper<STEPPER2WIRE> stepper5(200 * 16 * 6, 26, 25);
GStepper<STEPPER2WIRE> stepper6(200 * 16 * 50, 33, 32);

Servo myservo;

float accel_stepper1 = 0;
float accel_stepper2 = 0;
float accel_stepper3 = 0;
float accel_stepper4 = 0;
float accel_stepper5 = 0;
float accel_stepper6 = 0;

int dir[6] = { 1, 1, 1, 1, 1, 1 };

int maxPackageExecutiveIndex = 0;

float pos[7] = { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };
float speedMass[6] = { 15.0, 10.0, 15.0, 25.0, 15.0, 20.0 };

bool isReadyAnnounced = false;
bool executive_flag = false;
int package_number = traj_array_len;
int package_read_index = 0;
int package_executive_index[6] = { 0, 0, 0, 0, 0, 0 };

double traj_speed[traj_array_len][6];
float traj_pos[traj_array_len][7];

void zeroArray(int ptr[6]) {
  for (int i = 0; i < 6; i++) {
    ptr[i] = 0;
  }
}

int maxArray(int ptr[6]){
  int maxI = 0;
  for(int i = 1;i < 6;i++) 
      if(ptr[i] > ptr[maxI])
        maxI = i;
  return ptr[maxI];
}


void setup() {
  stepper1.setRunMode(FOLLOW_POS);
  stepper1.setAccelerationDeg(accel_stepper1);
  // stepper1.autoPower(true);

  stepper2.setRunMode(FOLLOW_POS);
  stepper2.setAccelerationDeg(accel_stepper2);
  // stepper2.autoPower(true);

  stepper3.setRunMode(FOLLOW_POS);
  stepper3.setAccelerationDeg(accel_stepper3);
  // stepper3.autoPower(true);

  stepper4.setRunMode(FOLLOW_POS);
  stepper4.setAccelerationDeg(accel_stepper4);
  // stepper4.autoPower(true);

  stepper5.setRunMode(FOLLOW_POS);
  stepper5.setAccelerationDeg(accel_stepper5);
  // stepper5.autoPower(true);

  stepper6.setRunMode(FOLLOW_POS);
  stepper6.setAccelerationDeg(accel_stepper6);
  // stepper6.autoPower(true);

  // pinMode(2, OUTPUT);

  Serial.begin(115200);

  if (!myservo.attached()) {
    myservo.attach(13);
  }
}

void setSpeed() {
  stepper1.setMaxSpeedDeg(traj_speed[package_executive_index[0]][0]);  // в градусах/сек
  stepper2.setMaxSpeedDeg(traj_speed[package_executive_index[1]][1]);  // в градусах/сек
  stepper3.setMaxSpeedDeg(traj_speed[package_executive_index[2]][2]);  // в градусах/сек
  stepper4.setMaxSpeedDeg(traj_speed[package_executive_index[3]][3]);  // в градусах/сек
  stepper5.setMaxSpeedDeg(traj_speed[package_executive_index[4]][4]);  // в градусах/сек
  stepper6.setMaxSpeedDeg(traj_speed[package_executive_index[5]][5]);  // в градусах/сек
}

void Go() {
  if (executive_flag) {
    setSpeed();
    if (!stepper1.tick()) {
      stepper1.setTargetDeg(traj_pos[package_number][0], ABSOLUTE);
    }
    if (!stepper2.tick()) {
      stepper2.setTargetDeg(traj_pos[package_number][1], ABSOLUTE);
    }
    if (!stepper3.tick()) {
      stepper3.setTargetDeg(traj_pos[package_number][2], ABSOLUTE);
    }
    if (!stepper4.tick()) {
      stepper4.setTargetDeg(traj_pos[package_number][3], ABSOLUTE);
    }
    if (!stepper5.tick()) {
      stepper5.setTargetDeg(traj_pos[package_number][4], ABSOLUTE);
    }
    if (!stepper6.tick()) {
      stepper6.setTargetDeg(traj_pos[package_number][5], ABSOLUTE);
    }
    // myservo.write(traj_pos[package_executive_index[6]][6]);
  }
}
// строка типа: 10.0/20.0/ ... 15.0/15.0/ ... 10.0/10.0/ ... 10.0
// сперва 6 углов для шаговиков, потом 6 скоростей для шаговиков,
// последним указывается угол для серво
void Read(const Text &COM_port, float pos[], double speed[], bool withServo) {
  for (int i = 0; i < 6; i++) {
    pos[i] = COM_port.getSub(i, '/').toFloat();
    speed[i] = COM_port.getSub(i + 6, '/').toFloat();
  }
  if (withServo) {
    pos[6] = COM_port.getSub(12, '/').toFloat();
  }
}

String fast_read() {
  String ret;
  int c = Serial.read();
  while (Serial.available() > 0) {
    ret += (char)c;
    c = Serial.read();
  }
  return ret;
}

void InputData() {
  if (Serial.available() > 0) {

    String COM_port = fast_read();
    // Serial.println(COM_port);
    if (COM_port == "stop") {
      stepper1.brake();
      stepper2.brake();
      stepper3.brake();
      stepper4.brake();
      stepper5.brake();
      stepper6.brake();
    } else if (COM_port == "101") {
      package_number = max(package_read_index - 1, 0);
      if (traj_pos[package_number][0] < stepper1.getCurrentDeg()) {
        dir[0] = -1;
      } else {
        dir[0] = 1;
      }

      if (traj_pos[package_number][1] < stepper2.getCurrentDeg()) {
        dir[1] = -1;
      } else {
        dir[1] = 1;
      }

      if (traj_pos[package_number][2] < stepper3.getCurrentDeg()) {
        dir[2] = -1;
      } else {
        dir[2] = 1;
      }

      if (traj_pos[package_number][3] < stepper4.getCurrentDeg()) {
        dir[3] = -1;
      } else {
        dir[3] = 1;
      }

      if (traj_pos[package_number][4] < stepper5.getCurrentDeg()) {
        dir[4] = -1;
        // digitalWrite(2, HIGH);
      } else {
        dir[4] = 1;
        // digitalWrite(2, LOW);
      }

      if (traj_pos[package_number][5] < stepper6.getCurrentDeg()) {
        dir[5] = -1;
      } else {
        dir[5] = 1;
      }

      // Serial.println();
      // for(int i = 0; i < 6; i++){
      //   Serial.print(dir[i]);
      //   Serial.print(" ");
      // }
      // Serial.println();
      
      maxPackageExecutiveIndex = 0;
      package_read_index = 0;
      zeroArray(package_executive_index);
      executive_flag = true;
      Serial.print(2);
    } else {
      Read(COM_port, traj_pos[package_read_index], traj_speed[package_read_index], false);
      package_read_index += 1;
      Serial.print(1);
    }
  }
}
void OutputData() {
  if (stepper1.getCurrentDeg() * dir[0] > traj_pos[package_executive_index[0]][0] * dir[0]) {
    package_executive_index[0] += 1; 
  }

  if (stepper2.getCurrentDeg() * dir[1] > traj_pos[package_executive_index[1]][1] * dir[1]) {
    package_executive_index[1] += 1; 
  }

  if (stepper3.getCurrentDeg() * dir[2] > traj_pos[package_executive_index[2]][2] * dir[2]) {
    package_executive_index[2] += 1; 
  }

  if (stepper4.getCurrentDeg() * dir[3] > traj_pos[package_executive_index[3]][3] * dir[3]) {
    package_executive_index[3] += 1; 
  }

  if (stepper5.getCurrentDeg() * dir[4] > traj_pos[package_executive_index[4]][4] * dir[4]) {
    package_executive_index[4] += 1; 
  }

  if (stepper6.getCurrentDeg() * dir[5] > traj_pos[package_executive_index[5]][5] * dir[5]) {
    package_executive_index[5] += 1; 
  }

  // if(maxPackageExecutiveIndex != maxArray(package_executive_index)){
  //   maxPackageExecutiveIndex = maxArray(package_executive_index);
  //   Serial.print(maxPackageExecutiveIndex%10);
  // }
  

  if (executive_flag && (abs(stepper5.getCurrentDeg() - traj_pos[package_number - 1][4]) < 0.1) && (abs(stepper2.getCurrentDeg() - traj_pos[package_number - 1][1]) < 0.1) && (abs(stepper3.getCurrentDeg() - traj_pos[package_number - 1][2]) < 0.1) && (abs(stepper1.getCurrentDeg() - traj_pos[package_number - 1][0]) < 0.1) && (abs(stepper6.getCurrentDeg() - traj_pos[package_number - 1][5]) < 0.1) && (abs(stepper4.getCurrentDeg() - traj_pos[package_number - 1][3]) < 0.1)) {
    Serial.print(3);
    executive_flag = false;
    zeroArray(package_executive_index);
  }
}

void loop() {
  Go();
  OutputData();
  InputData();
}