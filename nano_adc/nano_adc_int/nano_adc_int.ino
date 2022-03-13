const int interruptPin = 2;
const int ledPin = 3;
volatile byte state = LOW;
const int n = 10;
int samples[n];
void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), avg_analog, RISING);
  Serial.begin(9600);
}

void loop() {
  
  //digitalWrite(ledPin, state);
  //Serial.print("whoops");
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
    for (int i = 0; i < n; i++) {
       // Serial.print(samples[i]);
        //if (i < (n-1)) Serial.print(",");
    }
    //Serial.println("]");
    Serial.println(avg);
  }
  last_interrupt_time = interrupt_time;
  
}
