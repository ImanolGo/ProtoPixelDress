from openframeworks import *
import os.path
from tempfile import mkdtemp
        

class Square:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.fbo = ofFbo()
        self.fbo.allocate(width,height)
        self.color = ofColor(255)
        self.currentAlpha = 1.0
        self.targetAlpha = 1.0
        self.setup()


    def setup(self):
        #self.setupShader()
        pass


    def update(self):
        self.updateAlpha()
        self.updateFbo()

    def updateAlpha(self):
        self.currentAlpha = self.currentAlpha + (self.targetAlpha - self.currentAlpha)*0.05
        self.color.a = int(self.currentAlpha*255)

    def updateFbo(self):
        self.fbo.begin()
        ofClear(0)
        ofSetColor(self.color)
        ofDrawRectangle(0,0,self.width,self.height)
        self.fbo.end()

    def draw(self):

        self.fbo.draw(0,0)       

    def setColor(self, color):
        self.color = color

    def setAlpha(self, alpha):
        self.targetAlpha = alpha