from openframeworks import *
from protopixel import Content
from random import randint
import math

print "SquareAnimation"

#a global variable
size = 170
yPos = - 170
xPos = 0
animationType = 3
prev_animationType = -1
width = size
height =  size
color = ofColor(255)
elapsedTime = 0.0
startColorIndex = 1
endColorIndex = 2
spacing = 8
numLines = 1000
scale = 1.0
scaleFactor = 10
speedFactor = 100.0

content = Content("SquareAnimation")
content.FBO_SIZE = (size,size) #optional: define size of FBO, default=(100,100)

content.add_parameter("color1", type="color", value=ofColor(255, 255, 255))
content.add_parameter("color2", type="color", value=ofColor(255, 255, 255))
content.add_parameter("color3", type="color", value=ofColor(255, 255, 255))
content.add_parameter("change_hue", value=True)
content.add_parameter("color_speed", min=0.00, max=1.0, value=0.1)
content.add_parameter("speed", min=0.0, max=1.0, value=0.2)
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
       
@content.parameter_changed('stage_mode')
def parameter_changed(value):

    updateSwipeValues()
       


def updateSwipeValues():

    global size, xPos, yPos, width, height, animationType, elapsedTime, color, startColorIndex, endColorIndex, speedFactor, yOffset, xOffset

    while True:
        index = randint(0,3)
        if animationType != index:
            animationType = index
            break
       
    print "Animation Type = ", animationType


    if content['stage_mode'] == True:
        yOffset = 140
        xOffset = 55
    else:
        yOffset = 0
        xOffset = 0
    
    if animationType == 0:
        xPos = 0
        width = size 
        height = size/40
        yPos =  yOffset
            
    elif animationType == 1:
        xPos = 0
        width = size 
        height = size/40
        yPos = size + height
            
    elif animationType == 2:
        yPos = 0
        height = size
        width = size/40
        xPos = -width + xOffset
            
    elif animationType == 3:
        yPos = 0
        height = size
        width = size/40
        xPos = size - xOffset



def setup():
    """
    This will be called at the beggining, you set your stuff here
    """
    ofSetBackgroundAuto(False)

    global color,  xPos, yPos, width, height
    color = ofColor(content['color1'].r,content['color1'].g,content['color1'].b)

    yPos = 0
    height = size
    width = size/40
    xPos = size + width


def update():
    """
    For every frame, before drawing, we update stuff
    """

    global size, scale, xPos, yPos, width, height, animationType, elapsedTime, color, startColorIndex, endColorIndex, numLines, spacing, scaleFactor, prev_animationType, yOffset, xOffset
   
    angle = ofGetElapsedTimef()*content['speed']*20
    scale = 2*(math.sin(angle)+1)*0.5 + 0.5

    speed = ofMap(content['speed'], 0.0, 1.0, speedFactor/7, speedFactor)

    if animationType == 0:
    	
    	
    	yPos += ofGetLastFrameTime() * speed
    	#if yPos>size + numLines*spacing + numLines*height:
        	#yPos = -height
         #   pass
    elif animationType == 1:
    	
    	
    	yPos -= ofGetLastFrameTime() * speed
    	#if yPos < 0 - numLines*spacing - numLines*height:
        #	yPos = size + height
    elif animationType == 2:
        
        xPos += ofGetLastFrameTime() * speed
        #if xPos>size + numLines*spacing + numLines*width:
            #xPos = -width
         #   pass
    elif animationType == 3:

        xPos -= ofGetLastFrameTime() * speed
        #if xPos < 0 - numLines*spacing - numLines*width:
         #   xPos = size + width


    if ofGetFrameNum() % 400 == 0:
        updateSwipeValues()

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
    global color, xPos, yPos, width, height, spacing

    ofSetColor(0,0,0,30)
    ofDrawRectangle(0,0,ofGetWidth(),ofGetHeight())
    ofFill()

    ofSetColor(color)
    for i in range(0, numLines):
        if animationType == 0:
            ofDrawRectangle(xPos, yPos - height*spacing*i, width, scale*height)
        elif animationType == 1:
             ofDrawRectangle(xPos, yPos + height*spacing*i, width, scale*height)
        elif animationType == 2:
            ofDrawRectangle(xPos - width*spacing*i, yPos, scale*width, height)
        elif animationType == 3:
            ofDrawRectangle(xPos + width*spacing*i, yPos, scale*width, height)
    #ofDrawRectangle(0, 0, 170, 170)
   

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
