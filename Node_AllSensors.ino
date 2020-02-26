#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 2 // DS18B20 on NodeMCU pin D4 
OneWire oneWire(ONE_WIRE_BUS);
#include<string.h>
#include<stdlib.h>

DallasTemperature DS18B20(&oneWire);
const char* nmcu_id="node_1";
const int trigPin = 5;   //D1
const int echoPin = 4;   //D2
//char* result_char;
long duration_;
int dist;
const char* ssid = "MotoG";
const char* password = "yashshreez";

WiFiUDP Udp;
unsigned int localUdpPort = 1885;  // local port to listen on
char incomingPacket[255];  // buffer for incoming packets
char  replyPacket[] = "";  // a reply string to send back
char status_reply[]="alive";

void setup()
{
  Serial.begin(115200);
  Serial.println();
  
  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");
  
  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);
  
}


void loop()
{
  int packetSize = Udp.parsePacket();
  if (packetSize)
  {
    // receive incoming UDP packets
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(incomingPacket, 255);
    if (len > 0)
    {
      incomingPacket[len] = 0;
    }
    Serial.printf("UDP packet contents: %s\n", incomingPacket);
    if (strcmp(incomingPacket,"aiscmm_smart_irrigation_169.254.152.165_sensor_status")==0)
    {
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
      Udp.write(status_reply);
      Udp.endPacket();
    }

    else if (strcmp(incomingPacket,"aiscmm_smart_irrigation_169.254.152.165_sensor_data")==0)
    {
     float temp_0;
  float temp_1;
  DS18B20.requestTemperatures(); 
  temp_0 = DS18B20.getTempCByIndex(0); // Sensor 0 will capture Temp in Celcius
  temp_1 = DS18B20.getTempFByIndex(0); // Sensor 0 will capture Temp in Fahrenheit

  Serial.print("Temp_0: ");
  Serial.print(temp_0);
  Serial.print(" oC . Temp_1: ");
  Serial.print(temp_1);
  Serial.println(" oF ");
  delay(1000);
  
  // read the input on analog pin 0:
  float moist = analogRead(A0);
  // print out the value you read:
  Serial.println(moist);
    delay(1000);
     sprintf(replyPacket,"%f,%f,%f",temp_0,temp_1,moist);

   
     Serial.println(replyPacket);
    
     // send back a reply, to the IP address and port we got the packet from
     Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
     Udp.write(replyPacket);
     Udp.endPacket();
    }
  }
}

