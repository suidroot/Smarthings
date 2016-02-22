/*
 * Smarthings to IR Remote control
 * An IR LED must be connected to Arduino PWM pin 9.
 *
 *
 * NEC: 61A0F00F tv power
 * NEC: 48B710EF auto sleep
 * NEC: 48B7609F  auto
 * NEC: 77E1505B apple tv up
 */

#include <IRremote.h>
#include <SoftwareSerial.h>   //TODO need to set due to some weird wire language linker, should we absorb this whole library into smartthings
#include <SmartThings.h>


#define PIN_THING_RX    3
#define PIN_THING_TX    2


SmartThingsCallout_t messageCallout;    // call out function forward decalaration
SmartThings smartthing(PIN_THING_RX, PIN_THING_TX, messageCallout);  // constructor

IRsend irsend;

int ledPin = 13;
bool isDebugEnabled;    // enable or disable debug in this example
int stateLED;           // state to track last set value of LED

void setup() {
// setup default state of global variables
  isDebugEnabled = true;
  stateLED = 0;                 // matches state of hardware pin set below
  
  if (isDebugEnabled) { // setup debug serial port
    // setup hardware pins 
    pinMode(ledPin, OUTPUT);     // define PIN_LED as an output
    digitalWrite(ledPin, LOW);   // set value to LOW (off) to match stateLED=0
    Serial.begin(9600);         // setup serial with a baud rate of 9600
    Serial.println("setup..");  // print out 'setup..' on start
  }
}


void loop() {
  // run smartthing logic
  smartthing.run();
}



void messageCallout(String message) {

  if (message != "") {
    if (isDebugEnabled) {
      stateLED = 1;                 // save state as 1 (on)
      digitalWrite(ledPin, HIGH);  // turn LED on
      smartthing.shieldSetLED(0, 0, 1);

      Serial.print("Received message: '");
      Serial.print(message);
      Serial.println("' ");
    }

    /*
     * NEC: 61A0F00F tv power
     * NEC: 48B710EF auto sleep
     * NEC: 48B7609F  auto
     * NEC: 77E1505B apple tv up
     */

    // Convery String to decimal (hex) IR code
    unsigned long ircode = stringToNum(message, 16);

    for (int i = 0; i < 3; i++) {
      irsend.sendNEC(ircode, 32);
    }

    if (isDebugEnabled) {
      delay(1000);
      stateLED = 0;                 // set state to 0 (off)
      digitalWrite(ledPin, LOW);   // turn LED off
      smartthing.shieldSetLED(0, 0, 0);
    } else {
      if (isDebugEnabled) {
        Serial.print("Received ping");
      }
    }
  }
}

unsigned long stringToNum(String s, int base) //10 for decimal, 16 for hex
{
  unsigned long i = 0;
  unsigned long value = 0;
  unsigned long place = s.length();
  char c;
  unsigned long sign = 1;

  for(i; i < s.length(); i++) 
  {     
    place--;     
    c = s[i];     
    if(c == '-') 
    {       
      sign = -1;     
    } else if (c >= '0' && c <= '9')  //0 to 9     
    {       
      value += ( c - '0') *  exponent(base,place);     
    } else if (c >= 'A' && ((c - 'A' + 10) < base))  //65     
    {       
      value += (( c - 'A') + 10) *  exponent(base,place);     
    }     
      else if (c >= 'a' && (c - 'a' +  10) < base)  //97
    {
      value += (( c - 'a') + 10) *  exponent(base,place);
    }     
  }
  value *= sign;
  return value;  
}

unsigned long exponent(int num, int power)
{
  unsigned long total = num;
  unsigned long i = 1;
  for(power;  i < power; i++)
  {
    total *=  num;
  }
  return (power == 0) ? 1 : total;

}




