

#include <ESP8266WiFi.h>

 /*
  Created by Igor Jarc
 See http://iot-playground.com for details
 Please use community fourum on website do not contact author directly
 
 Code based on https://github.com/DennisSc/easyIoT-ESPduino/blob/master/sketches/ds18b20.ino
 
 External libraries:
 - https://github.com/adamvr/arduino-base64
 - https://github.com/milesburton/Arduino-Temperature-Control-Library
 
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 2 as published by the Free Software Foundation.
 */


//#define ONE_WIRE_BUS 2  // DS18B20 pin D4
//OneWire oneWire(ONE_WIRE_BUS);
//DallasTemperature DS18B20(&oneWire);



const int trigPin = 5;   //D1
const int echoPin = 4;   //D2

// defines variables
long duration;
int dist;


void setup() { 
  

pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin, INPUT); // Sets the echoPin as an Input
Serial.begin(9600); // Starts the serial communication

 

}



void loop() {



// Clears the trigPin
digitalWrite(trigPin, LOW);
delayMicroseconds(2);

// Sets the trigPin on HIGH state for 10 micro seconds
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);

// Reads the echoPin, returns the sound wave travel time in microseconds
duration = pulseIn(echoPin, HIGH);

// Calculating the distance
dist= duration*0.034/2;
// Prints the distance on the Serial Monitor
Serial.print("Distance: ");
Serial.println(dist);
delay(500);
}




