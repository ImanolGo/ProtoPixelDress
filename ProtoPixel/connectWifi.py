import socket
import struct
import sys

import time
from time import time as tt
import numpy as np
import os.path

from openframeworks import *
from protopixel import Content

UDP_IP = "192.168.178.20"
UDP_PORT = 2390

content = Content('Virtual controller')
content.add_parameter("FPS_LIMIT", min=0, max=60, value=30)

content.add_parameter("Controller1", value=False)
content.add_parameter("audio_react1", value=False)
content.add_parameter("IP_1", value="192.168.20.232")

content.add_parameter("Controller2", value=False)
content.add_parameter("audio_react2", value=False)
content.add_parameter("IP_2", value="192.168.20.233")

content.add_parameter("Controller3", value=False)
content.add_parameter("audio_react3", value=False)
content.add_parameter("IP_3", value="192.168.20.234")

content.add_parameter("Controller4", value=False)
content.add_parameter("audio_react4", value=False)
content.add_parameter("IP_4", value="192.168.20.235")

content.add_parameter("Controller5", value=False)
content.add_parameter("audio_react5", value=False)
content.add_parameter("IP_5", value="192.168.20.236")


@content.parameter_changed('Output_name')
def output_name_changed(newval):
    #global FILEPATH
    #FILEPATH = "../../../"+newval+".txt"
    #print "New path:", newval
    pass

def setup():
    global controller, update_time, timmer, qframe, qtimmer, is_started,FPS, energy, curVol
    print "SETUP------------------------"
    FPS = 30
    controller = None
    update_time = 1.0/FPS
    timmer = tt()
    qframe = 0
    qtimmer = tt()
    is_started = True
    energy = 0
    curVol = 0
    #pt = ofToDataPath(".")
    #print pt,"-----------------ooooooooooo"
    

def update():
    global update_time, timmer, qframe, qtimmer, controller,FPS, energy, curVol

    buffer = content.get_sound_buffer()
     # get the absolute values 
    buffer = np.abs(buffer)

    scale = 15

    # get the sum of all values, to measure the energy
    
    curVol = int(buffer.sum())
    curVol = min(255,scale*curVol)
    #brightness = float(energy)/255.0
    
    
    energy  = (80*energy)/100;
    energy  = energy + (20*curVol)/100;
    brightness = 255

    if controller and controller.outlets[0] is not None:
        i = 0
        for q in range(4):
            #print "q", q
            if content['audio_react'+str(q+1)]:
                brightness = energy
            else:
                brightness = 255  

            msg = ""
            outlet = np.fromstring(controller.outlets[i],dtype=np.uint8)
            numlights = len(outlet) / 3
            if numlights < 200:
                msg = ''.join( chr(v*brightness/255) for v in outlet)
                msg = msg + ''.join( [chr(0)] * ((200-numlights)*3))
            else:
                msg = ''.join( chr(v*brightness/255) for v in outlet[0:600])
            i = i+1
            outlet = np.fromstring(controller.outlets[i],dtype=np.uint8)
            numlights = len(outlet) / 3
            if numlights < 200:
                msg = msg + ''.join( chr(v*brightness/255) for v in outlet)
                msg = msg + ''.join( [chr(0)] * ((200-numlights)*3))
            else:
                msg = msg + ''.join( chr(v*brightness/255) for v in outlet[0:600])
            i = i+1
            #print content['IP_'+str(i+1)]
            #print content['Controller'+str(i+1)]
            #msg = ''.join( [chr(255)] * ((400)*3))
            if content['Controller'+str(q+1)]:
                print msg
                try:
                    #print len(msg), content['IP_'+str(q+1)]
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
                    #sock.setsockopt(socket.IPPROTO_IP,socket.IP_TTL,4)
                    #sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL,10)
                    sock.sendto(msg, (content['IP_'+str(q+1)], UDP_PORT))
                except socket.error as e:
                    print "socket error {} at device: {} ({})".format(e,q+q,content['IP_'+str(q+1)])
        #controller sol
        if content['audio_react5']:
            brightness = energy
        else:
            brightness = 255 
        msg = ""
        outlet = np.fromstring(controller.outlets[5],dtype=np.uint8)
        numlights = len(outlet) / 3
        if numlights < 200:
            msg = msg + ''.join( [chr(0)] * ((200)*3))
        else:
            if numlights < 400:
                #print len(outlet)
                print (numlights-200)*3
                #print "-----------------"
                msg = ''.join( chr(v*brightness/255) for v in outlet[600:])
                msg = msg + ''.join( [chr(0)] * ((200-(numlights-200))*3))
                print "A"
            else:
                msg = msg + ''.join( chr(v*brightness/255) for v in outlet[600:1200])
                print "B"
        msg= msg+msg
        if content['Controller5']:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
                sock.setsockopt(socket.IPPROTO_IP,socket.IP_TTL,4)
                sock.sendto(msg, (content['IP_5'], UDP_PORT))
            except socket.error as e:
                print "socket error {} at device: {} ({})".format(e,q+q,content['IP_5'])

    #----------
    #FPS check
    #if qframe >= FPS-1:
    #    qframe = 0
    #    print tt() - qtimmer
    #    qtimmer = tt()
    #    print "------------------"
    #else:
    #    qframe = qframe + 1;
    #--------

    #--------
    #FPS limiter:
    actual = tt()
    elapsed = actual-timmer
    #30 fps --> 1/30
    diff = update_time- elapsed
    if diff > 0:
        time.sleep(diff)
    timmer = tt()
    FPS = content['FPS_LIMIT']
    update_time = 1.0/FPS
    #--------

def draw():
    
    global energy
    # we use the energy to change the color
    ofClear(energy,energy,energy,255)


def exit():
    global controller
    print "EXIT------------------------"
    if controller:
        controller.running = False
        controller.t.join() # just in case, for old versions of PotoPixel
        controller = None

def on_enable():
    global controller, is_started
    if not is_started:
        return
    print "ENABLE------------------------"
    if controller is None:
        controller = FakeTCPController()
        controller.listen() # obre el port
        controller.announce() # fa un anounce

def on_disable():
    global controller
    print "DISABLE------------------------"
    controller.running = False
    controller = None

class FakeTCPController(object):
    def __init__(self):
        self.name = "Wifi"
        self.mac = "00:00:00:00:00:01"
        self.t = content.Thread(target=self._process)
        self.t.daemon = True
        self.running = False
        self.outlets = [None]*8

    def announce(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        message_version = 2
        firmware_version = 1
        hardware_version = 2
        mac_addr_1, mac_addr_2, mac_addr_3, mac_addr_4, mac_addr_5, mac_addr_6 = (0, 0, 0, 0, 0, 0)
        actual_ip_1, actual_ip_2, actual_ip_3, actual_ip_4 = (127, 0, 0, 1)
        properties = 0
        actual_gateway_1, actual_gateway_2, actual_gateway_3, actual_gateway_4 = (192, 168, 20, 1)
        actual_mask_1, actual_mask_2, actual_mask_3, actual_mask_4 = (255, 255, 255, 0)
        device_name = "WIFI"
        static_ip_1, static_ip_2, static_ip_3, static_ip_4 = (192, 168, 20, 65)
        static_gateway_1, static_gateway_2, static_gateway_3, static_gateway_4 = (192, 168, 20, 1)
        static_mask_1, static_mask_2, static_mask_3, static_mask_4 = (255, 255, 255, 0)
        message = struct.pack('<HHB6B4BB4B4B16s4B4B4B',
                              message_version,
                              firmware_version,
                              hardware_version,
                              mac_addr_1, mac_addr_2, mac_addr_3, mac_addr_4, mac_addr_5, mac_addr_6,
                              actual_ip_1, actual_ip_2, actual_ip_3, actual_ip_4,
                              properties,
                              actual_gateway_1, actual_gateway_2, actual_gateway_3, actual_gateway_4,
                              actual_mask_1, actual_mask_2, actual_mask_3, actual_mask_4,
                              device_name,
                              static_ip_1, static_ip_2, static_ip_3, static_ip_4,
                              static_gateway_1, static_gateway_2, static_gateway_3, static_gateway_4,
                              static_mask_1, static_mask_2, static_mask_3, static_mask_4,
                              )
        s.sendto(message, ('localhost', 5006))

    def listen(self):
        self.running = True
        self.t.start()

    def stop(self):
        self.running = False

    def _process(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('localhost',5015))
        s.listen(0)
        #self.timmer = tt()
        while self.running:
            try:
                s.settimeout(0.2)
                (ss, _) = s.accept()
                ss.settimeout(None)
                print "New Connection"
                while self.running:
                    header = ss.recv(23)
                    if not header:
                        break
                    assert header[:5] == "PROTO"
                    LED_count = struct.unpack('>8H',header[7:7+8*2])
                    for i in range(8):
                        outletdata = ss.recv(LED_count[i]*3)
                        self.outlets[i] = outletdata
                    ss.send('ok')
            except socket.timeout:
                pass
            except socket.error:
                pass
        s.close()

    def __del__(self):
        self.running = False