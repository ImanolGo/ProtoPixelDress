from openframeworks import *
import os.path
from tempfile import mkdtemp
import math
from numpy import interp
        

class Fade:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.fbo = ofFbo()
        self.fbo.allocate(width,height)
        self.color = ofColor(255)
        self.setup()


    def setup(self):
        pass

    def update(self):
        self.updateColor()
        self.updateFbo()


    def updateFbo(self):
        self.fbo.begin()
        ofClear(0)
        ofSetColor(self.color)
        ofDrawRectangle(0,0,self.width,self.height)
        self.fbo.end()

    def draw(self):

        self.fbo.draw(0,0)
        #self.drawShader()
        
    def updateColor(self):
        angle = ofGetElapsedTimef()*1.7
        b = interp(angle,[-1,1],[50,255])
        #b = ofMap(angle, -1.0, 1.0, 50.0, 255.0)
        #brightness = int(255.0*((math.sin(angle)+1.0)*0.5))
        brightness = int(b)
        self.color.a = brightness
        #print self.color.a

    def setColor(self, color):
        self.color = color



        



