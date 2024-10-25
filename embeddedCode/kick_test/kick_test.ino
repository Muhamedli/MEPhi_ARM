#include <GyverStepper.h>
#include <StringUtils.h>

GStepper<STEPPER2WIRE> stepper1(200 * 16 * 11, 18, 5);

float accel_stepper1 = 0;

int i=0;

float pos[7] = { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
float speedMass[6] = { 5.0, 10.0, 15.0, 25.0, 15.0, 20.0 };
String COM_port = "45.0/10.0";

void setup() {
  stepper1.setRunMode(FOLLOW_POS);
  stepper1.setAccelerationDeg(accel_stepper1);
  stepper1.setTargetDeg(90, ABSOLUTE);
  setSpeed(speedMass);
  Serial.begin(115200);

}
void setSpeed(float speedMass[6]) {
  stepper1.setMaxSpeedDeg(speedMass[0]);  // в градусах/сек
}

void loop() {
  
  stepper1.tick();
  if(stepper1.getCurrentDeg() > (i+1) * 1.0){
    i ++;
    speedMass[0] = 5.0 + i*0.05;
    setSpeed(speedMass);
    Serial.println(stepper1.getCurrentDeg());
  }
}