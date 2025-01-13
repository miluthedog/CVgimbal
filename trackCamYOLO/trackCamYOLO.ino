#include <Wire.h>
#include <Servo.h>

Servo servoX;
Servo servoY;
Servo servoCamZ;
int position = 90;

const int MPU = 0x68;

int16_t accX, accY, accZ;
int16_t gyroX, gyroY, gyroZ;

const int servoXPin = 9;
const int servoYPin = 10;
const int servoCamZPin = 11;

void setup() {
  Serial.begin(9600);

  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);

  servoX.attach(servoXPin);
  servoY.attach(servoYPin);
  servoCamZ.attach(servoCamZPin);

  servoX.write(90);
  servoY.write(90);
  servoCamZ.write(position);
}

void loop() {
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 6, true); 
  
  accX = Wire.read() << 8 | Wire.read();
  accY = Wire.read() << 8 | Wire.read(); 
  accZ = Wire.read() << 8 | Wire.read(); 

  int angleX = map(accX, -17000, 17000, 0, 180); // threashold
  int angleY = map(accY, -17000, 17000, 0, 180);

  angleX = constrain(angleX, 0, 180);
  angleY = constrain(angleY, 0, 180);

  servoX.write(angleX);
  servoY.write(angleY);

  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    int newPosition = input.toInt();

    if (newPosition >= 0 && newPosition <= 180) {
      position = newPosition;
      servoCamZ.write(position);
    }
  }

  delay(10);
}
