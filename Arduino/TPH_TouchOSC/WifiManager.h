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
#include <WiFi.h>
#include <WiFiUdp.h>
#include <ArduinoOSC.h>

#define DISCOVERY_TIMER 3000
#define WIFI_TIMEOUT 3000              // checks WiFi every ...ms. Reset after this time, if WiFi cannot reconnect.
#define LOCAL_PORT 7000 
#define SEND_PORT 7001 


//The udp library class

String ip;
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

    static void callbackAutodiscovery(OSCMessage& m);

  private:

    void initializeWifi();
    void initializeOSC();
    
    void parseOsc();
    void connectToWiFi(const char * ssid, const char * pwd);
    void sendAutodiscovery();

    String getIpString(IPAddress& _ip);
   
    String ssid;
    String pass;
   
    WiFiUDP udp;
    ArduinoOSCWiFi osc;
    unsigned long autodiscovery_timer;
    bool _touched;
    
};


WifiManager::WifiManager()
{
  
//    ssid = "TPH Operations";
//    pass = "TheFUTURE!Sno3";

    ssid = "Don't worry, be happy!";
    pass = "whyistheskysohigh?";

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
    initializeOSC();
}

void WifiManager::initializeWifi()
{  
    Serial.println("WifiManager::connect wifi");
    connectToWiFi(ssid.c_str(), pass.c_str());
}

void WifiManager::initializeOSC()
{
     osc.begin(udp, LOCAL_PORT);
     osc.addCallback("/tph/autodiscovery", &callbackAutodiscovery);
}

void WifiManager::callbackAutodiscovery(OSCMessage& m)
{ 
    Serial.println("WifiManager:got autodiscovery!!");
    is_connected = true;
    ip = String(m.getIpAddress());
    ip = "192.168.178.20";

    //const char* ipAddress = m.getIpAddress();
    
    Serial.print("WifiManager:callbackAutodiscovery: sending to: ");
    Serial.println(ip);
}


void WifiManager::update()
{
    parseOsc();
    sendAutodiscovery();
}


void WifiManager::parseOsc()
{
    osc.parse();
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
      case SYSTEM_EVENT_STA_GOT_IP:
          //When connected set 
          Serial.print("WifiManager::WiFi connected! IP address: ");
          Serial.println(WiFi.localIP());  
          //initializes the UDP state
          //This initializes the transfer buffer
  
          Serial.print("WifiManager::Listening to port: ");
          Serial.println(LOCAL_PORT); 
          wifiConnected = true;
          break;
      case SYSTEM_EVENT_STA_DISCONNECTED:
          Serial.println("WifiManager::WiFi lost connection");
          wifiConnected = false;
          //software_Reset();
          break;
    }
}


void WifiManager::sendTouched(int i)
{
     if(!is_connected) return;

      OSCMessage msg;
      msg.beginMessage(ip.c_str(), SEND_PORT);
      msg.setOSCAddress("/tph/touched");
      msg.addArgInt32(i);
      osc.send(msg);
}

void WifiManager::sendReleased(int i)
{
    if(!is_connected) return;

      OSCMessage msg;
      msg.beginMessage(ip.c_str(), SEND_PORT);
      msg.setOSCAddress("/tph/released");
      msg.addArgInt32(i);
      osc.send(msg);
}

String WifiManager::getIpString(IPAddress& _ip)
{
    String str = String(_ip[0]);
    str += ".";
    str += String(_ip[1]);
    str += ".";
    str += String(_ip[2]);
    str += ".";
    str += String(_ip[3]);
    return str;
}

void WifiManager::sendAutodiscovery()
{
  //if(is_connected || !wifiConnected) return;

  if (!wifiConnected) return;

  if(!is_connected) return;

  if( millis() - autodiscovery_timer > DISCOVERY_TIMER)
  {
      _touched = !_touched;

      if(_touched){
        this->sendTouched(0);
      }
      else{
        this->sendReleased(0);
      }

      Serial.println("WifiManager::Autodiscovery sent!");
      autodiscovery_timer = millis();
  }
}

