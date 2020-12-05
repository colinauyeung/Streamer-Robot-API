/*
    Modified from https://www.arduino.cc/en/Tutorial/BuiltInExamples/Button

*/

// constants won't change. They're used here to set pin numbers:
const int buttonPin = 4;     // the number of the pushbutton pin
const int buttonPin1 = 3;     // the number of the pushbutton pin
const int buttonPin2 = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status
int buttonState1 = 0;         // variable for reading the pushbutton status
int buttonState2 = 0;         // variable for reading the pushbutton status
char Val[4] = {'0', '0', '0', '\n'};
char prev[4] = "000\n";

void setup() {
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600); // open the serial port at 9600 bps:
}

void loop() {
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);
  buttonState1 = digitalRead(buttonPin1);
  buttonState2 = digitalRead(buttonPin2);

  if (buttonState1 == LOW) {
    Val[0] = '1'; 
  }
  else{
    Val[0] = '0';
  }
  if (buttonState2 == LOW) {
    Val[2] = '1';
  }
  else{
    Val[2] = '0';
  }
  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == LOW) {
    // turn LED on:
    digitalWrite(ledPin, HIGH);
    Val[1] = '1';
  } else {
    // turn LED off:
    digitalWrite(ledPin, LOW);

    Val[1] = '0';
  }
  if(prev[0] != Val[0] or prev[1] != Val[1] or prev[2] != Val[2]){
    prev[0] = Val[0];
    prev[1] = Val[1];
    prev[2] = Val[2];
    Serial.print(Val);
  }
}
