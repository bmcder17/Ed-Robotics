const int interruptPin = 2;
const int ledPin = 3;
volatile byte state = LOW;
void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), blink, CHANGE);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(ledPin, state);
  //Serial.print("whoops");
  //delay(1000);
}

void blink() {
  Serial.println("hi");
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  // If interrupts come faster than 200ms, assume it's a bounce and ignore
  if (interrupt_time - last_interrupt_time > 200) 
  {
    state = !state;
  }
  last_interrupt_time = interrupt_time;
  
}
