

#include <ESP8266WiFi.h>
//#include <OneWire.h>
//#include <DallasTemperature.h>

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



void setup() {
  Serial.begin(115200);
}

void loop() {
  // read the input on analog pin 0:
  float moist = analogRead(A0);
  // print out the value you read:
  Serial.println(moist);
  delay(1000);        // delay in between reads for stability
  
}




