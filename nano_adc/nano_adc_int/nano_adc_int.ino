const int interruptPin = 2;
const int ledPin = 3;
volatile byte state = LOW;
const int n = 10;
const int minIN = 170;
const int maxIN = 710;
const int deltaIN = 540;
const int maxTheta = 135;
int samples[n];
void setup() {
  //pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), avg_analog, CHANGE);
  Serial1.begin(9600);
  delay(100);
}

void loop() {
  
  //digitalWrite(ledPin, state);
  //Serial.println("whoops");
  delay(10);
}

void blink() {
  //Serial.println("hi");
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  // If interrupts come faster than 200ms, assume it's a bounce and ignore
  if (interrupt_time - last_interrupt_time > 200) 
  {
    avg_analog();
    state = !state;
  }
  last_interrupt_time = interrupt_time;
  
}

void avg_analog() {
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  //Serial.println("help");
  // If interrupts come faster than 200ms, assume it's a bounce and ignore
  if (interrupt_time - last_interrupt_time > 200) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        samples[i] = analogRead(A7);
        //Serial.println(samples[i]);
        total += samples[i];
        //SSerial.println(total);
    }
    int avg = total / n;
    //Serial.print("[");
    //for (int i = 0; i < n; i++) {
       // Serial.print(samples[i]);
        //if (i < (n-1)) Serial.print(",");
    //}
    //Serial.println("]");
    //Serial.println(avg);
    //Serial.println(avg);
    //convert from mv to theta
    if (avg < 170){
      avg = 170;
    }
    else if (avg > 710) {
      avg = 710;
    }
    int offset = avg-170;
    //Serial.println(offset);
    float theta_p = offset / 540.0;
    //Serial.println(theta_p);
    int theta = theta_p * 135;
    Serial1.print(theta);
  }
  last_interrupt_time = interrupt_time;
  
}
