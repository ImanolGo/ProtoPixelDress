from openframeworks import *
from protopixel import Content
from random import randint
import math

print "CircleAnimation"


#a global variable
color = ofColor(255)
elapsedTime = 0.0
startColorIndex = 1
endColorIndex = 2
scaleFactor = 10
size = 170

content = Content("CircleAnimation")
content.FBO_SIZE = (size,size) #optional: define size of FBO, default=(100,100)

content.add_parameter("color1", type="color", value=ofColor(255, 255, 255))
content.add_parameter("color2", type="color", value=ofColor(255, 255, 255))
content.add_parameter("color3", type="color", value=ofColor(255, 255, 255))
content.add_parameter("change_hue", value=True)
content.add_parameter("color_speed", min=0.00, max=1.0, value=0.1)
content.add_parameter("speed", min=0.0, max=1.0, value=0.2)
content.add_parameter("circle_num", min=1, max=20, value=1)
content.add_parameter("stage_mode", value=False)



class Circle:
    frameSize = 170
    size = 0
    xPos = 0
    yPos = 0
    xOffset = 0
    yOffset = 0
    x_stage = 0
    y_stage = 0
    speed = 0.1

    def __init__(self):
        self.xOffset = randint(0,10000)
        self.yOffset = randint(0,10000)
        #print self.xOffset

    def update(self):

        t = (ofGetElapsedTimef()) * self.speed*0.5
        targetX = ofNoise(t + self.xOffset, 0)*(self.frameSize- 2*self.x_stage) + self.x_stage
        targetY = ofNoise(0 + self.yOffset , t)* (self.frameSize- 2*self.x_stage) + self.y_stage

        #targetX = ofNoise(t + self.xOffset, 0)*(self.frameSize)
        #targetY = ofNoise(0 + self.yOffset , t)* (self.frameSize) 

        self.xPos =  self.xPos  + ( targetX-  self.xPos  ) * 0.05
        self.yPos =  self.yPos  + ( targetY-  self.yPos  ) * 0.05

        angle = ofGetElapsedTimef()*self.speed*3 + self.xOffset
        targetSize = 70.0*(math.sin(angle)+1)*0.5 + 50

        self.size  = self.size  + ( targetSize-  self.size  ) * 0.05
        #print self.size 

    def draw(self):
        ofNoFill()
        ofDrawEllipse(self.xPos, self.yPos, self.size, self.size)

    def setSpeed(self, speed):
        self.speed = speed
        #print self.animationTime
        #
    def setStageOffsets(self, x, y):
        self.x_stage = x
        self.y_stage = y



circles = []


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
       

@content.parameter_changed('speed')
def parameter_changed(value):
    """
    This function is called every time a a_integer is changed.
    We get the new value as an argument
    """
    global circles

    for circle in circles:
        circle.setSpeed(content['speed'])


@content.parameter_changed('stage_mode')
def parameter_changed(value):

    if value == True:
        for circle in circles:
            circle.setStageOffsets(55,140)
    else:
        for circle in circles:
            circle.setStageOffsets(0,0)

def setup():
    """
    This will be called at the beggining, you set your stuff here
    """
    ofSetBackgroundAuto(False)

    global color, circles

    color = ofColor(content['color1'].r,content['color1'].g,content['color1'].b)

    for i in range(0, 20):
        circle = Circle()
        circle.setSpeed(content['speed'])
        circles.append(circle)
        #print "New Circle"


def update():
    """
    For every frame, before drawing, we update stuff
    """

    global elapsedTime, color, startColorIndex, endColorIndex, scaleFactor, circles

    for circle in circles:
        circle.update()

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
    global color, circles

    ofSetColor(0,0,0,10)
    ofFill()
    ofDrawRectangle(0,0,ofGetWidth(),ofGetHeight())

    ofSetColor(color)
    for i in range(0, content['circle_num']):
        circles[i].draw()
  

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
