#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include "MQ135.h"
#include <ArduinoJson.h>

#define VIRTUAL_PIN 5
#define ANALOGPIN A0

MQ135 gasSensor = MQ135(ANALOGPIN);
 
void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(115200);                            //Serial connection
  WiFi.begin("suraj", "abcdefgh123");   //WiFi connection
 
  while (WiFi.status() != WL_CONNECTED) {  //Wait for the WiFI connection completion
 
    delay(500);
    Serial.println("Waiting for connection");
 
  }
 
}
 
void loop() {
 
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
 
    StaticJsonBuffer<300> JSONbuffer;   //Declaring static JSON buffer
    JsonObject& JSONencoder = JSONbuffer.createObject(); 
    float ppm = gasSensor.getPPM();
    Serial.println(ppm);
    JSONencoder["ppm"] = ppm;
    JSONencoder["username"] = "sita1";
 
    HTTPClient http;    //Declare object of class HTTPClient
 
    http.begin("http://192.168.43.21:8000/get-data/");      //Specify request destination
    http.addHeader("Content-Type", "application/json");  //Specify content-type header

    char JSONmessageBuffer[300];
    JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
    
    int httpCode = http.POST(JSONmessageBuffer);   //Send the request
    String payload = http.getString();                                        //Get the response payload
 
    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload
 
    http.end();  //Close connection
    if (ppm > 5){
      digitalWrite(13, HIGH); 
      delay(5000);
    }
    else{
      digitalWrite(13, LOW); 
    }
 
  } else {
 
    Serial.println("Error in WiFi connection");
 
  }
 
  delay(5000);  //Send a request every 30 seconds
 
}
