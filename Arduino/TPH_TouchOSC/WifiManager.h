///////////////////////////////////////////////////////////////////
// Class controlling the wifi connection
//
//
// This code is under A Creative Commons Attribution/Share-Alike License
// http://creativecommons.org/licenses/by-sa/4.0/
// 2018, Imanol Gomez
///////////////////////////////////////////////////////////////////


#define OUTPUT_CHANNEL 0
#define HEADER_SIZE 7

#pragma once
#include "Arduino.h"

#ifdef ESP32
  #include <WiFi.h>
#else
  #include <ESP8266WiFi.h>
#endif
  
  
#include <WiFiUdp.h>
#include <OSCMessage.h>
#include <OSCBundle.h>
#include <OSCData.h>

#define DISCOVERY_TIMER 3000
#define WIFI_TIMEOUT 3000              // checks WiFi every ...ms. Reset after this time, if WiFi cannot reconnect.
#define LOCAL_PORT 2346 
#define SEND_PORT 2345 


//The udp library class

WiFiUDP udp;
IPAddress ipSend;
bool wifiConnected = false;
bool is_connected = false;


class WifiManager
{

  public:
    
    WifiManager();
    
    void setup();
    void update();

    static void WiFiEvent(WiFiEvent_t event);

    void sendTouched(int i);

    void sendReleased(int i);

    void sendData(int i, int value);

    static void callbackAutodiscovery(OSCMessage& m);

  private:

    void initializeWifi();
   
    void parseOsc();
    void connectToWiFi(const char * ssid, const char * pwd);
    void sendAutodiscovery();
   
    String ssid;
    String pass;
   

    unsigned long autodiscovery_timer;
    bool _touched;
    
};


WifiManager::WifiManager()
{

      ssid =  "ppxnode-4BE2201";
      pass =  "password";

//    ssid = "TPH Operations";
//    pass = "TheFUTURE!Sno3";

//    ssid     =  "TP-LINK_54E4";
//    pass = "27155332";
    

    wifiConnected = false;
    autodiscovery_timer =  millis();
    is_connected = false;
     _touched = false;

}

void WifiManager::setup()
{
    Serial.println("WifiManager::setup");
    initializeWifi();
}

void WifiManager::initializeWifi()
{  
    Serial.println("WifiManager::connect wifi");
    connectToWiFi(ssid.c_str(), pass.c_str());
}

void WifiManager::callbackAutodiscovery(OSCMessage& m)
{ 
    Serial.println("WifiManager:got autodiscovery!!");
    is_connected = true;
    ipSend = udp.remoteIP();
    //ipSend = "192.168.178.20";

    //const char* ipAddress = m.getIpAddress();
    
    Serial.print("WifiManager:callbackAutodiscovery: sending to: ");
    Serial.print(ipSend);
    Serial.print(", port:  ");
    Serial.println(SEND_PORT);
}


void WifiManager::update()
{
    parseOsc();
    sendAutodiscovery();
}


void WifiManager::parseOsc()
{
    if (!wifiConnected) return;
    
    int size = udp.parsePacket();
    if (size > 0) {
      OSCMessage msg;
      while (size--) {
         msg.fill(udp.read());
      }
      if (!msg.hasError()) {
        msg.dispatch("/tph/autodiscovery", callbackAutodiscovery);
      } else {
        OSCErrorCode error = msg.getError();
        Serial.print("WifiManager::parseOsc-> Error: ");
        Serial.println(error);
      }
      
    }

}



void WifiManager::connectToWiFi(const char * ssid, const char * pwd){
  Serial.println("WifiManager::Connecting to WiFi network: " + String(ssid));

  // delete old config
  WiFi.disconnect(true);
  //register event handlerpin
  WiFi.onEvent(WiFiEvent);
 // WiFi.config(ip, gateway, subnet);
  WiFi.setAutoReconnect(true);
  WiFi.setAutoConnect(true);
  
  //Initiate connection
  WiFi.begin(ssid, pwd);

  Serial.println("WifiManager::Waiting for WIFI connection...");
}


//wifi event handler
void WifiManager::WiFiEvent(WiFiEvent_t event){
 
    switch(event) {

      #ifdef ESP32
      case SYSTEM_EVENT_STA_GOT_IP:
          //When connected set 
          Serial.print("WifiManager::WiFi connected! IP address: ");
          Serial.println(WiFi.localIP());  
          //initializes the UDP state
          //This initializes the transfer buffer
  
          Serial.print("WifiManager::Listening to port: ");
          Serial.println(LOCAL_PORT); 
          udp.begin(LOCAL_PORT);
          wifiConnected = true;
          ipSend = WiFi.localIP();
          ipSend[3] = 255;
          break;
      case SYSTEM_EVENT_STA_DISCONNECTED:
          Serial.println("WifiManager::WiFi lost connection");
          wifiConnected = false;
          //software_Reset();
          break;

        #else

        case WIFI_EVENT_STAMODE_GOT_IP:
           //When connected set 
          Serial.print("WifiManager::WiFi connected! IP address: ");
          Serial.println(WiFi.localIP());  
          //initializes the UDP state
          //This initializes the transfer buffer
  
          Serial.print("WifiManager::Listening to port: ");
          Serial.println(LOCAL_PORT); 
          udp.begin(LOCAL_PORT);
          wifiConnected = true;
          ipSend = WiFi.localIP();
          ipSend[3] = 1;
          break;
      case WIFI_EVENT_STAMODE_DISCONNECTED:
          Serial.println("WifiManager::WiFi lost connection");
          wifiConnected = false;
          //software_Reset();
          break;

          #endif
    }
}


void WifiManager::sendTouched(int i)
{
    // if(!is_connected) return;

     OSCMessage msg("/tph/touched");
     msg.add(i);
     udp.beginPacket(ipSend, SEND_PORT);
     msg.send(udp);
     udp.endPacket();
     msg.empty();
    

//      OSCMessage msg;
//      msg.beginMessage(ip.c_str(), SEND_PORT);
//      msg.setOSCAddress("/tph/touched");
//      msg.addArgInt32(i);
//      osc.send(msg);
}

void WifiManager::sendData(int i, int value)
{
    // if(!is_connected) return;

     OSCMessage msg("/tph/data");
     msg.add(i);
     msg.add(value);
     udp.beginPacket(ipSend, SEND_PORT);
     msg.send(udp);
     udp.endPacket();
     msg.empty();
    

//      OSCMessage msg;
//      msg.beginMessage(ip.c_str(), SEND_PORT);
//      msg.setOSCAddress("/tph/touched");
//      msg.addArgInt32(i);
//      osc.send(msg);
}


void WifiManager::sendReleased(int i)
{
    //if(!is_connected) return;

     OSCMessage msg("/tph/released");
     msg.add(i);
     udp.beginPacket(ipSend, SEND_PORT);
     msg.send(udp);
     udp.endPacket();
     msg.empty();

//      OSCMessage msg;
//      msg.beginMessage(ip.c_str(), SEND_PORT);
//      msg.setOSCAddress("/tph/released");
//      msg.addArgInt32(i);
//      osc.send(msg);
}


void WifiManager::sendAutodiscovery()
{
  if(is_connected || !wifiConnected) return;

  if( millis() - autodiscovery_timer > DISCOVERY_TIMER)
  {
//      _touched = !_touched;
//
//      if(_touched){
//        this->sendTouched(0);
//      }
//      else{
//        this->sendReleased(0);
//      }
      
      IPAddress ip = WiFi.localIP();
      ip[3] = 255;
      
       OSCMessage msg("/tph/autodiscovery");
       msg.add(1);
       udp.beginPacket(ip, SEND_PORT);
       msg.send(udp);
       udp.endPacket();
       msg.empty();

      Serial.println("WifiManager::Autodiscovery sent!");
      autodiscovery_timer = millis();
  }
}
