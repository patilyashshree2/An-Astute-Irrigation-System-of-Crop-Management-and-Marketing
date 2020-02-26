#include<ESP8266WiFi.h>
#include<PubSubClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 2 // DS18B20 on NodeMCU pin D4 
OneWire oneWire(ONE_WIRE_BUS);
//#include<string.h>


DallasTemperature DS18B20(&oneWire);

String result;
char* result_char=""; 
char* temp_0_str="";
char* temp_1_str="";
char* moist_str="";
char* dist_str="";
char* delimiter=",";

const int trigPin = 5;   //D1
const int echoPin = 4;   //D2
//char* result_char;
long duration;
int dist;
const char* ssid="123";
const char* password="lasya123";
const char* mqttServer="192.168.43.180";
const int mqttPort=1883;
const char* mqttUser="pi";
const char* mqttPassword="root";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  DS18B20.begin();
  Serial.println("Testing Dual Sensor data");
  
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid,password);
  
  while(WiFi.status()!=WL_CONNECTED){
    delay(500);
    Serial.println("connecting to wifi network...................");
  }
  Serial.println("Connected to wifi");

  client.setServer(mqttServer,mqttPort);
  client.setCallback(callback);

  while(!client.connected()){
    Serial.println("connecting to mqtt..................");

    if(client.connect("ESP8266Client",mqttUser,mqttPassword)){
      Serial.println("connected...");
    } else{

      Serial.print("failed with state ");
      Serial.println(client.state());
      Serial.println();
      delay(2000);
    }
  }

}


void callback(char* topic, byte* payload, unsigned int length){
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message: ");
  for(int i=0;i<length;i++){
    Serial.print((char)payload[i]);
  }

  Serial.println();
  Serial.println("-----------------------------------");
}


void loop() {
  float temp_0;
  float temp_1;
  DS18B20.requestTemperatures(); 
  temp_0 = DS18B20.getTempCByIndex(0); // Sensor 0 will capture Temp in Celcius
  temp_1 = DS18B20.getTempFByIndex(0); // Sensor 0 will capture Temp in Fahrenheit

 
 //dtostrf(temp_1,3,2,temp_1_str);
  
  // read the input on analog pin 0:
  
  float moist = analogRead(A0);
  dtostrf(moist,2,0,moist_str);
  
  // print out the value you read:

  
  //Serial.print("Temp_0: ");
  //Serial.print(temp_0);
  //Serial.print(" oC . Temp_1: ");
  //Serial.print(temp_1);
  //Serial.println(" oF ");

 // Serial.println(moist);
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
dtostrf(dist,3,2,dist_str);
 //dtostrf(temp_0,3,2,temp_0_str);
// Prints the distance on the Serial Monitor
//Serial.print("Distance: ");
//Serial.println(dist);
 
 //result=String(temp_0)+","+String(temp_1)+","+String(moist)+","+String(dist);

 result_char=new char[strlen(temp_0_str)+strlen(moist_str)+1];
 sprintf(result_char,"%s %s",temp_0_str,moist_str);
 //delay(500);
  client.publish("2_esp8266",result_char);
  client.subscribe("2_esp8266");
 delay(5000);
  client.loop();
 
  

}
