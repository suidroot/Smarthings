/*
 * IRremote: IRsendDemo - demonstrates sending IR codes with IRsend
 * An IR LED must be connected to Arduino PWM pin 9.
 * Version 0.1 July, 2009
 * Copyright 2009 Ken Shirriff
 * http://arcfn.com
 * NEC: 61A0F00F tv power
 * NEC: 48B710EF auto sleep
 * NEC: 48B7609F  auto
 * NEC: 77E1505B apple tv up
 */

#include <IRremote.h>

IRsend irsend;
int buttonpin = 2;
int sw1pin = 4;
int sw2pin = 5;
int sw3pin = 6;



void setup()
{
  Serial.begin(9600);
  pinMode(buttonpin, INPUT);
  pinMode(sw1pin, INPUT);
  pinMode(sw2pin, INPUT);
  pinMode(sw3pin, INPUT);
}

void loop() {

  if (digitalRead(buttonpin) == HIGH) {

    if (digitalRead(sw1pin) == HIGH) {
      irsend.sendNEC(0x61A0F00F, 32); // Dynex TV power code
      Serial.println("TV Off");
    }

    if (digitalRead(sw2pin) == HIGH) {
      irsend.sendNEC(0x48B710EF, 32); // AirPutifier auto sleep
      Serial.println("AirPutifier auto sleep");
    }

    if (digitalRead(sw3pin) == HIGH) {
      irsend.sendNEC(0x48B7609F, 32); // AirPutifier auto
      Serial.println("AirPutifier auto");
    }
    
  delay(4000);  
  }
  
}
