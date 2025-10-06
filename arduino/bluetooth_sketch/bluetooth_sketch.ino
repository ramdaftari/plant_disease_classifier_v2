#include<SoftwareSerial.h>



SoftwareSerial B(0,1);
int x = 0;

void setup() {
  B.begin(38400);
}

void loop() {
  x=0;
  B.print(x);
  B.print(";");
  delay(2000);
  x=1;
  B.print(x);
  B.print(";");
  delay(2000);
}
