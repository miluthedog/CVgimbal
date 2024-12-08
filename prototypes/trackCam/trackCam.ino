#include <Servo.h>

Servo myServo;
int pos = 90;

void setup() {
  Serial.begin(9600);
  myServo.attach(2);
  myServo.write(pos);
}

void loop() {
  if (Serial.available() > 0) {
    String incomingData = Serial.readStringUntil('\n');
    pos = incomingData.toInt();
    pos = constrain(pos, 0, 180);
    myServo.write(pos);
  }
  //delay(15);
}
