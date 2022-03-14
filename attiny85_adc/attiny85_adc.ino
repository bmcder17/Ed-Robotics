#include "SoftwareSerial.h"

const int Rx =3;
const int Tx = 4;
SoftwareSerial mySerial(Rx,Tx);

void setup() {
  // put your setup code here, to run once:
  pinMode(Rx, INPUT);
  pinMode(Tx,OUTPUT);
  mySerial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
   mySerial.println("hi"); 

}
