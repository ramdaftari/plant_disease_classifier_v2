#include<SoftwareSerial.h>
#include<Stepper.h>

SoftwareSerial B(0,1);
int x = 0;

const int stepsPerRevolution = 200;
Stepper mobile(stepsPerRevolution, 6, 12, 10, 11);

int enA = 9;
int in1 = 8;
int in2 = 7;

int enB = 3;
int in3 = 5;
int in4 = 4;

void setup() {
  B.begin(38400);

  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  mobile.setSpeed(60);

}

void loop() {
  /*
  x=0;
  B.print(x);
  B.print(";");
  delay(2000);
  x=1;
  B.print(x);
  B.print(";");
  delay(2000);
  */
  x = 0;
  moveForward(5000);
  mobile.step(stepsPerRevolution);
  
  B.print(1);
  B.print(";");
  delay(5000);
  mobile.step(-stepsPerRevolution);
}

void moveForward(int duration){
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);

  analogWrite(enA, 255);
  analogWrite(enB, 255);

  delay(duration);

  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void moveBackward(int duration){
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);

  analogWrite(enA, 255);
  analogWrite(enB, 255);

  delay(duration);

  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void moveLeft(int duration){
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);

  analogWrite(enA, 255);
  analogWrite(enB, 255);

  delay(duration);

  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void moveRight(int duration){
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);

  analogWrite(enA, 255);
  analogWrite(enB, 255);

  delay(duration);

  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}
