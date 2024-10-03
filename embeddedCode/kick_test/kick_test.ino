#include <GyverStepper.h>
#include <StringUtils.h>

GStepper<STEPPER2WIRE> stepper1(200 * 16 * 11, 18, 5);

float accel_stepper1 = 0;

float pos[7] = { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float speedMass[6] = { 15.0, 10.0, 15.0, 25.0, 15.0, 20.0 };
String COM_port = "45.0/10.0";

void setup() {
  stepper1.setRunMode(FOLLOW_POS);
  stepper1.setAccelerationDeg(accel_stepper1);

  setSpeed(speedMass);
}
void setSpeed(float speedMass[6]) {
  stepper1.setMaxSpeedDeg(speedMass[0]);  // в градусах/сек
}
void Go(){
  if (!stepper1.tick()) {
    stepper1.setTargetDeg(pos[0], ABSOLUTE);
  }
}

void Read(const Text& COM_port, float pos[], float speed[]) {
  for(int i = 0; i < 1; i++) {
    pos[i] = COM_port.getSub(i, '/').toFloat();
    speed[i] = COM_port.getSub(i + 1, '/').toFloat();
  }
}
void loop() {
  float i=0;
  while( i<90.0){
    if(!stepper1.tick()){
      pos[0] = i;
      speedMass[0] = 15.0 + i/2.0;
      setSpeed(speedMass);
      Go();
      i ++;
    }
  }
}