/*
  TPH Touch OSC
   
 Description:
 * Software reading and sending via OSC capacitive gestures

 Software:
 * Adafruit_MPR121 Library - https://github.com/adafruit/Adafruit_MPR121
 * CNMAT/OSC - https://github.com/CNMAT/OSC
 
 Hardware:
* MPR121 12-channel Capacitive touch sensor
* Adafruit HUZZAH32 - ESP32 Feather Board
   
 created 18 September 2018
 This code is under A Creative Commons Attribution/Share-Alike License http://creativecommons.org/licenses/by-sa/4.0/
   (2018) by Imanol Gomez
 
 */
 


#include "CapSensorManager.h"
#include "WifiManager.h"


WifiManager wifiManager;
CapSensorManager capSensorManager(&wifiManager);

void setup() {
  
    Serial.begin(115200);
    delay(1000);
    Serial.println("Starting Software!!!!");
    
    //capSensorManager.setup();
    wifiManager.setup();
}

void loop() 
{
    wifiManager.update();
    //capSensorManager.update();
    
  // put a delay so it isn't overwhelming
  //delay(10);
}
