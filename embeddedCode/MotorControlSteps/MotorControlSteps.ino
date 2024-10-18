#include <Arduino.h>
#include <GyverStepper2.h>
#include <ESP32Servo.h>
#include <StringUtils.h>

#define traj_array_len 50

GStepper2<STEPPER2WIRE> stepper1(200 * 16 * 11, 18, 5);
GStepper2<STEPPER2WIRE> stepper2(200 * 16 * 12, 17, 16);
GStepper2<STEPPER2WIRE> stepper3(200 * 16 * 15, 27, 14);
GStepper2<STEPPER2WIRE> stepper4(200 * 16 * 9, 2, 15);
GStepper2<STEPPER2WIRE> stepper5(200 * 16 * 6, 26, 25);
GStepper2<STEPPER2WIRE> stepper6(200 * 16 * 50, 33, 32);

long steps_per_round[6] = {200 * 16 * 11, 200 * 16 * 12, 200 * 16 * 15, 200 * 16 * 9, 200 * 16 * 6, 200 * 16 * 50};

Servo myservo;

int accel_stepper1 = 0;
int accel_stepper2 = 0;
int accel_stepper3 = 0;
int accel_stepper4 = 0;
int accel_stepper5 = 0;
int accel_stepper6 = 0;

long pos[7] = {0, 0, 0, 0, 0, 0, 0};
long speedMass[6] = {15, 10, 15, 25, 15, 20};

bool isReadyAnnounced = false;
bool executive_flag = false;
int package_number = traj_array_len;
int package_read_index = 0;
int package_executive_index = 0;

long traj_speed[traj_array_len][6];
long traj_pos[traj_array_len][7];


void setup()
{
  
  stepper1.setAcceleration(accel_stepper1);
  // stepper1.autoPower(true);

  stepper1.setAcceleration(accel_stepper2);
  // stepper2.autoPower(true);

  stepper1.setAcceleration(accel_stepper3);
  // stepper3.autoPower(true);

  stepper1.setAcceleration(accel_stepper4);
  // stepper4.autoPower(true);

  stepper1.setAcceleration(accel_stepper5);
  // stepper5.autoPower(true);

  stepper1.setAcceleration(accel_stepper6);
  // stepper6.autoPower(true);

  setSpeed(speedMass);

  Serial.begin(921600);

  if (!myservo.attached())
  {
    myservo.attach(13);
  }
}

void setSpeed(long speedMass[6])
{
  stepper1.setMaxSpeed(speedMass[0]); // в градусах/сек
  stepper2.setMaxSpeed(speedMass[1]); // в градусах/сек
  stepper3.setMaxSpeed(speedMass[2]); // в градусах/сек
  stepper4.setMaxSpeed(speedMass[3]); // в градусах/сек
  stepper5.setMaxSpeed(speedMass[4]); // в градусах/сек
  stepper6.setMaxSpeed(speedMass[5]); // в градусах/сек
}

void Go()
{
  if (executive_flag)
  {
    setSpeed(traj_speed[package_executive_index]);
    if (!stepper1.tick())
    {
      stepper1.setTarget(traj_pos[package_executive_index][0], ABSOLUTE);
    }
    if (!stepper2.tick())
    {
      stepper2.setTarget(traj_pos[package_executive_index][1], ABSOLUTE);
    }
    if (!stepper3.tick())
    {
      stepper3.setTarget(traj_pos[package_executive_index][2], ABSOLUTE);
    }
    if (!stepper4.tick())
    {
      stepper4.setTarget(traj_pos[package_executive_index][3], ABSOLUTE);
    }
    if (!stepper5.tick())
    {
      stepper5.setTarget(traj_pos[package_executive_index][4], ABSOLUTE);
    }
    if (!stepper6.tick())
    {
      stepper6.setTarget(traj_pos[package_executive_index][5], ABSOLUTE);
    }
    myservo.write(traj_pos[package_executive_index][6]);
  }
}
// строка типа: 10.0/20.0/ ... 15.0/15.0/ ... 10.0/10.0/ ... 10.0
// сперва 6 углов для шаговиков, потом 6 скоростей для шаговиков,
// последним указывается угол для серво
void Read(const Text &COM_port, long pos[], long speed[], bool withServo)
{
  for (int i = 0; i < 6; i++)
  {
    pos[i] = (int) (COM_port.getSub(i, '/').toFloat() / 360.0) * steps_per_round[i];
    speed[i] = (int)(COM_port.getSub(i + 6, '/').toFloat() / 360.0) * steps_per_round[i];
  }
  if (withServo)
  {
    pos[6] = (int) (COM_port.getSub(12, '/').toFloat() / 180.0);
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
      package_executive_index = 0;
      isReadyAnnounced = false;
      executive_flag = true;

      Serial.print(2);
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
  if (executive_flag && !isReadyAnnounced && !stepper1.tick() && !stepper2.tick() && !stepper3.tick() && !stepper4.tick() && !stepper5.tick() && !stepper6.tick())
  {
    isReadyAnnounced = true;
    if (package_executive_index == package_number)
    {                      
          
      Serial.print(3);
      executive_flag = false;
      package_executive_index = 0;
    }
    else
    {
      Serial.print(package_executive_index%10);
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