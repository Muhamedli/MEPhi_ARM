#include <Arduino.h>
#include <GyverStepper.h>
#include <ESP32Servo.h>
#include <StringUtils.h>

#define traj_array_len 30

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

float pos[7] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float speedMass[6] = {15.0, 10.0, 15.0, 25.0, 15.0, 20.0};

bool isReadyAnnounced = false;
int package_number = traj_array_len;
int package_read_index = 0;
int package_executive_index = 0;

float traj_speed[traj_array_len][6];
float traj_pos[traj_array_len][7];
bool executive_flag = false;

void setup()
{
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

  setSpeed(speedMass);

  Serial.begin(921600);

  if (!myservo.attached())
  {
    myservo.attach(13);
  }
}

void setSpeed(float speedMass[6])
{
  stepper1.setMaxSpeedDeg(speedMass[0]); // в градусах/сек
  stepper2.setMaxSpeedDeg(speedMass[1]); // в градусах/сек
  stepper3.setMaxSpeedDeg(speedMass[2]); // в градусах/сек
  stepper4.setMaxSpeedDeg(speedMass[3]); // в градусах/сек
  stepper5.setMaxSpeedDeg(speedMass[4]); // в градусах/сек
  stepper6.setMaxSpeedDeg(speedMass[5]); // в градусах/сек
}

void Go()
{
  if (executive_flag)
  {
    // Serial.println("in");
    setSpeed(traj_speed[package_executive_index]);
    if (!stepper1.tick())
    {
      stepper1.setTargetDeg(traj_pos[package_executive_index][0], ABSOLUTE);
    }
    if (!stepper2.tick())
    {
      stepper2.setTargetDeg(traj_pos[package_executive_index][1], ABSOLUTE);
    }
    if (!stepper3.tick())
    {
      stepper3.setTargetDeg(traj_pos[package_executive_index][2], ABSOLUTE);
    }
    if (!stepper4.tick())
    {
      stepper4.setTargetDeg(traj_pos[package_executive_index][3], ABSOLUTE);
    }
    if (!stepper5.tick())
    {
      stepper5.setTargetDeg(traj_pos[package_executive_index][4], ABSOLUTE);
    }
    if (!stepper6.tick())
    {
      stepper6.setTargetDeg(traj_pos[package_executive_index][5], ABSOLUTE);
    }
    myservo.write(traj_pos[package_executive_index][6]);
  }
}
// строка типа: 10.0/20.0/ ... 15.0/15.0/ ... 10.0/10.0/ ... 10.0
// сперва 6 углов для шаговиков, потом 6 скоростей для шаговиков,
// последним указывается угол для серво
void Read(const Text &COM_port, float pos[], float speed[], bool withServo)
{
  for (int i = 0; i < 6; i++)
  {
    pos[i] = COM_port.getSub(i, '/').toFloat();
    speed[i] = COM_port.getSub(i + 6, '/').toFloat();
  }
  if (withServo)
  {
    pos[6] = COM_port.getSub(12, '/').toFloat();
  }
}

String fast_read()
{
  String ret;
  int c = Serial.read();
  while (Serial.available() > 0)
  {
    ret += (char)c;
    c = Serial.read();
  }
  return ret;
}

void InputData()
{
  if (Serial.available() > 0)
  {

    String COM_port = fast_read();
    // Serial.println(COM_port);
    if (COM_port == "stop")
    {
      stepper1.brake();
      stepper2.brake();
      stepper3.brake();
      stepper4.brake();
      stepper5.brake();
      stepper6.brake();
    }
    else if (COM_port == "101")
    {
      package_number = max(package_read_index - 1, 0);
      package_read_index = 0;
      isReadyAnnounced = false;
      executive_flag = true;
      Serial.print(3);
    }
    else
    {
      Read(COM_port, traj_pos[package_read_index], traj_speed[package_read_index], false);
      package_read_index += 1;
      Serial.print(1);
    }
  }
}
void OutputData()
{
  if (!isReadyAnnounced && !stepper1.tick() && !stepper2.tick() && !stepper3.tick() && !stepper4.tick() && !stepper5.tick() && !stepper6.tick())
  {
    isReadyAnnounced = true;
    if (package_executive_index == package_number-1)
    { 
      Serial.print(2);
      executive_flag = false;
      package_executive_index = 0;
       // Добавить спец символ для отправки новой траектории
    }
    else
    {
      //Serial.print(package_executive_index);
      package_executive_index += 1;
      isReadyAnnounced = false;
    }
  }
}

void loop()
{
  Go();
  OutputData();
  InputData();
}