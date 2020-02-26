// Henry's Bench
//Checking to ensure you can connect ESP-12E to a router
     
    #include <ESP8266WiFi.h>
     
    const char* ssid     = "Moto G (5S) Plus 4343";
    const char* password = "yashshreez";     

    int wifiStatus;
     
    void setup() {
      
      Serial.begin(115200);\
      delay(200);
      
     
     
      // We start by connecting to a WiFi network
     
      Serial.println();
      Serial.println();
      Serial.print("Your are connecting to;");
      Serial.println(ssid);
      
      WiFi.begin(ssid, password);
      
      while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
      }
     
 }   
     
void loop() {
      wifiStatus = WiFi.status();

      if(wifiStatus == WL_CONNECTED){
         Serial.println("");
         Serial.println("Your ESP is connected!");  
         Serial.println("Your IP address is: ");
         Serial.println(WiFi.localIP());  
      }
      else{
        Serial.println("");
        Serial.println("WiFi not connected");
      }
      delay(1000); // check for connection every once a second

}

