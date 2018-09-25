from openframeworks import *
from protopixel import Content
from random import randint
import math

print "Pulse"

#a global variable
color = ofColor(255)
elapsedTime = 0.0
startColorIndex = 1
endColorIndex = 2
brightness = 0.0
scaleFactor = 10
speedFactor = 20

content = Content("Pulse")
content.FBO_SIZE = (170,170) #optional: define size of FBO, default=(100,100)

content.add_parameter("color1", type="color", value=ofColor(255, 255, 255))
content.add_parameter("color2", type="color", value=ofColor(255, 255, 255))
content.add_parameter("color3", type="color", value=ofColor(255, 255, 255))
content.add_parameter("change_hue", value=True)
content.add_parameter("color_speed", min=0.00, max=1.0, value=0.1)
content.add_parameter("speed", min=0.0, max=1.0, value=0.1)
content.add_parameter("stage_mode", value=False)


@content.parameter_changed('change_hue')
def parameter_changed(value):
    """
    This function is called every time a a_integer is changed.
    We get the new value as an argument
    """
    global color

    if value == False:
        color.r = content['color1'].r
        color.g = content['color1'].g
        color.b = content['color1'].b
        elapsedTime = 0
        startColorIndex = 1
        endColorIndex = 2

@content.parameter_changed('color1')
def parameter_changed(value):
    """
    This function is called every time a a_integer is changed.
    We get the new value as an argument
    """
    global color

    print value
    if content['change_hue'] == False:
        color.r = content['color1'].r
        color.g = content['color1'].g
        color.b = content['color1'].b
       

def setup():
    """
    This will be called at the beggining, you set your stuff here
    """
    global color
    color = ofColor(content['color1'].r,content['color1'].g,content['color1'].b)


def update():
    """
    For every frame, before drawing, we update stuff
    """

    global elapsedTime, color, startColorIndex, endColorIndex, brightness, scaleFactor, brightness, speedFactor

    angle = ofGetElapsedTimef()* content['speed']*speedFactor
   
    targetBrightness = 255.0*(math.sin(angle)+1)*0.5

    brightness =  brightness + ( targetBrightness - brightness ) * 0.1

    #angle = ofGetElapsedTimef()*currentSpeed*10
    

    if content['change_hue'] == False:
        return

    
    elapsedTime+=ofGetLastFrameTime()
    time = ofMap(content['color_speed'], 0,1, scaleFactor, scaleFactor/20.0)

    if elapsedTime>time:
        elapsedTime = 0
        startColorIndex = endColorIndex
        endColorIndex = (endColorIndex+1)%3 + 1

    amt = elapsedTime/(time)
    startColorStr = 'color' + str(startColorIndex)
    endColorStr = 'color' + str(endColorIndex)
    color.r = int(ofLerp(content[startColorStr].r, content[endColorStr].r, amt))
    color.g = int(ofLerp(content[startColorStr].g, content[endColorStr].g, amt))
    color.b = int(ofLerp(content[startColorStr].b, content[endColorStr].b, amt))


def draw():
    """
    For every frame draw stuff. Do not forget to clear the frmebuffer!
    """
    global color, brightness
    
    color.a =  int(brightness)
    ofBackground( color )

def exit():
    """
    Before removing the script, in case you have pending business.
    """
    pass


def on_enable():
    """
    This function is called when this content just got enabled.
    """
    pass


def on_disable():
    """
    This function is called when this content just got disabled.
    `update` and `draw` functions are not called while this content is disabled.
    """
    pass
