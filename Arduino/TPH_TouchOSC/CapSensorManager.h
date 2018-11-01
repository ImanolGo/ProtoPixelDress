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

#define NUM_TOUCH 12

class CapSensorManager{
public:

  CapSensorManager(WifiManager* wifiManager);
  
  /// set all information necessary to use the module and initialize it
  void setup();

  void initializeMPR121();

  void update();
   
  
private:

    void updateTouch();
    void setBase();
    
    Adafruit_MPR121*  cap;  //Class controlling the MPR121 module
    uint16_t lasttouched = 0;
    uint16_t currtouched = 0;
    uint16_t lastTouchedArray[NUM_TOUCH];
    bool touchState[NUM_TOUCH];
    uint16_t baseTouch[NUM_TOUCH];
    

    WifiManager* wifiManager;

    
    uint8_t threshold = 2;
};



CapSensorManager::CapSensorManager(WifiManager* wifiManager)
{
     this->wifiManager=wifiManager;
     for(int i=0; i<NUM_TOUCH; i++){
        lastTouchedArray[i] = 0;
     }
}

void CapSensorManager::setup()
{
    initializeMPR121();
    delay(1000);
    setBase();
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


void CapSensorManager::setBase()
{
     for (uint8_t i=0; i<NUM_TOUCH; i++) {
          baseTouch[i] =  cap->filteredData(i);
          touchState[i] = false;
     }

     Serial.println(" ");
     Serial.print("CapSensorManager::base -> ");
     for (uint8_t i=0; i<NUM_TOUCH; i++) {
         Serial.print( baseTouch[i] ); Serial.print(" ");
     }
     Serial.println(" ");
}

 void CapSensorManager::update()
 {
      this->updateTouch();

        // debugging info, what
//  Serial.print("\t\t\t\t\t\t\t\t\t\t\t\t\t 0x"); Serial.println(cap->touched(), HEX);
//  Serial.print("Filt: ");
//  for (uint8_t i=0; i<12; i++) {
//    Serial.print(cap->filteredData(i)); Serial.print("\t");
//  }
//  Serial.println();
//  Serial.print("Base: ");
//  for (uint8_t i=0; i<12; i++) {
//    Serial.print(cap->baselineData(i)); Serial.print("\t");
//  }
//  Serial.println();
//  
//  // put a delay so it isn't overwhelming
//  delay(100);
 }


 void CapSensorManager::updateTouch()
 {
      //Serial.print("CapSensorManager::diff -> ");
      
      for (uint8_t i=0; i<NUM_TOUCH; i++) {
          int diff =  baseTouch[i] - cap->filteredData(i);
           //Serial.print(cap->filteredData(i)); Serial.print(" ");
          if(diff >= this->threshold  && !touchState[i]){
             Serial.print("CapSensorManager::touched -> "); Serial.println(i);
             this->wifiManager->sendTouched(i);
             touchState[i]  = true;
          }

          if(diff < this->threshold && touchState[i] ){
             Serial.print("CapSensorManager::released -> "); Serial.println(i);
            this->wifiManager->sendReleased(i);
             touchState[i]  = false;
          }
     
     }
       //Serial.println(" ");
     
//        // Get the currently touched pads
//      currtouched = cap->touched();
//      
//      for (uint8_t i=0; i<12; i++) {
//        // it if *is* touched and *wasnt* touched before, alert!
//        if ((currtouched & _BV(i)) && !(lasttouched & _BV(i)) ) {
//          Serial.print("CapSensorManager::touched -> "); Serial.println(i);
//          this->wifiManager->sendTouched(i);
//  
//        }
//        // if it *was* touched and now *isnt*, alert!
//        if (!(currtouched & _BV(i)) && (lasttouched & _BV(i)) ) {
//          Serial.print("CapSensorManager::released -> "); Serial.println(i);
//          this->wifiManager->sendReleased(i);
//        }
//      }
//    
//      // reset our state
//      lasttouched = currtouched;

   // Serial.print("CapSensorManager::diff -> ");
//    for (uint8_t i=0; i<NUM_TOUCH; i++) {
//          int diff = cap->filteredData(i) - lastTouchedArray[i];
//         // Serial.print(diff); Serial.print(" ");
//          if(diff < -this->threshold){
//             Serial.print("CapSensorManager::touched -> "); Serial.println(i);
//             this->wifiManager->sendTouched(i);
//          }
//
//          if(diff > this->threshold){
//             Serial.print("CapSensorManager::released -> "); Serial.println(i);
//            //this->wifiManager->sendReleased(i);
//            this->wifiManager->sendTouched(i);
//          }
//
//          this->wifiManager->sendData(i,  cap->filteredData(i));
//          lastTouchedArray[i] = cap->filteredData(i);
//          
//          
//     }
//     
//     Serial.println(" ");
//     Serial.print("CapSensorManager::data -> ");
//     for (uint8_t i=0; i<NUM_TOUCH; i++) {
//         Serial.print( lastTouchedArray[i] ); Serial.print(" ");
//     }
//     Serial.println(" ");
 }
