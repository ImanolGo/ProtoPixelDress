///////////////////////////////////////////////////////////////////
// A Capacitive Sensor interface for reading from a MPR121 module
//
// This code is under A Creative Commons Attribution/Share-Alike License
// http://creativecommons.org/licenses/by-sa/4.0/
// 2018, Imanol Gomez
///////////////////////////////////////////////////////////////////

#pragma once
#include "Arduino.h"
#include <Wire.h>
#include "Adafruit_MPR121.h"
#include "WifiManager.h"

class CapSensorManager{
public:

  CapSensorManager(WifiManager* wifiManager);
  
  /// set all information necessary to use the module and initialize it
  void setup();

  void initializeMPR121();

  void update();
   
  
private:

    void updateTouch();
    
    Adafruit_MPR121*  cap;  //Class controlling the MPR121 module
    uint16_t lasttouched = 0;
    uint16_t currtouched = 0;

    WifiManager* wifiManager;
    
};



CapSensorManager::CapSensorManager(WifiManager* wifiManager)
{
     this->wifiManager=wifiManager;
}

void CapSensorManager::setup()
{
    initializeMPR121();
}

void CapSensorManager::initializeMPR121()
{
    Serial.println("CapSensorManager::setup-> Starting Adafruit MPR121 Capacitive Touch"); 

    cap = new Adafruit_MPR121();
    // Default address is 0x5A, if tied to 3.3V its 0x5B
    // If tied to SDA its 0x5C and if SCL then 0x5D
    if (!cap->begin(0x5A)) {
      Serial.println("CapSensorManager::setup-> MPR121 not found, check wiring?");
      while (1);
    }
    Serial.println("CapSensorManager::setup-> MPR121 found!");
}


 void CapSensorManager::update()
 {
      this->updateTouch();
 }


 void CapSensorManager::updateTouch()
 {
        // Get the currently touched pads
      currtouched = cap->touched();
      
      for (uint8_t i=0; i<12; i++) {
        // it if *is* touched and *wasnt* touched before, alert!
        if ((currtouched & _BV(i)) && !(lasttouched & _BV(i)) ) {
          Serial.print("CapSensorManager::touched -> "); Serial.println(i);
          this->wifiManager->sendTouched(i);
  
        }
        // if it *was* touched and now *isnt*, alert!
        if (!(currtouched & _BV(i)) && (lasttouched & _BV(i)) ) {
          Serial.print("CapSensorManager::released -> "); Serial.println(i);
          this->wifiManager->sendReleased(i);
        }
      }
    
      // reset our state
      lasttouched = currtouched;
 }













