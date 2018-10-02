from openframeworks import *
from protopixel import Content
import imp

content = Content("ProtoPixelDress")

sparkle_file = content.add_asset("sparkle.py")
sparkles = imp.load_source('sparkles',sparkle_file)

rainbow_file = content.add_asset("rainbow.py")
rainbow = imp.load_source('rainbow',rainbow_file)

fade_file = content.add_asset("fade.py")
fade = imp.load_source('fade',fade_file)

waves_file = content.add_asset("waves.py")
waves = imp.load_source('waves',waves_file)

circles_file = content.add_asset("circles.py")
circles = imp.load_source('circles',circles_file)

print "ProtoPixelDress"


#a global variable
elapsedTime = 0.0
size = 200
content.FBO_SIZE = (size,size) #optional: define size of FBO, default=(100,100)
targetAlpha = 1.0
currentAlpha = 0.0
currentColor = ofColor(255)
previousColor = ofColor(0)

content.add_parameter("gamma", min=0.0, max=1.0, value=0.1)
content.add_parameter("enableSparkles", value=True)
content.add_parameter("enableRainbow", value=True)
content.add_parameter("enableFade", value=True)
content.add_parameter("enableWaves", value=True)
content.add_parameter("enableCircles", value=True)
content.add_parameter("Color", type="color", value=ofColor(255,255,255))


def setup():
    """
    This will be called at the beggining, you set your stuff here
    """

    global size, sparkles, rainbow, fade, waves, circles

    rainbow = rainbow.Rainbow(size,size)
    sparkles = sparkles.Sparkles(size,size)
    fade = fade.Fade(size,size)
    waves = waves.Waves(size,size)
    circles = circles.Circles(size,size)


def update():
    """
    For every frame, before drawing, we update stuff
    """

    global sparkles, rainbow

    updateColor()

    if content["enableSparkles"]  == True:
        sparkles.update()

    if content["enableRainbow"]  == True:
        rainbow.update()

    if content["enableFade"]  == True:
        fade.update()

    if content["enableWaves"]  == True:
        waves.update()

    if content["enableCircles"]  == True:
        circles.update()

    
    

def updateColor():

    global currentAlpha, targetAlpha, previousColor, currentColor

    currentAlpha = currentAlpha + (targetAlpha - currentAlpha)*0.02
    
    if currentAlpha > 1.0:
        currentAlpha = 1.0

    newColor = previousColor.getLerped(currentColor, currentAlpha)
    setColors(newColor)
   # print currentAlpha
    #print newColor
    #print currentColor


def draw():
    """
    For every frame draw stuff. Do not forget to clear the frmebuffer!
    """
    global sparkles
   
    ofClear(0)

    if content["enableSparkles"]  == True:
        sparkles.draw()

    if content["enableRainbow"]  == True:
        rainbow.draw()

    if content["enableFade"]  == True:
        fade.draw()

    if content["enableWaves"]  == True:
        waves.draw()

    if content["enableCircles"]  == True:
        circles.draw()

  
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

def setColors(color):
    sparkles.setColor(color)
    fade.setColor(color)
    waves.setColor(color)
    circles.setColor(color)

def setNewColor(color):

    global currentAlpha, targetAlpha, previousColor, currentColor

    previousColor = previousColor.getLerped(currentColor, currentAlpha)
    currentColor = color
    currentAlpha = 0
    targetAlpha = 1


def disableAll():
    content["enableSparkles"]  = False
    content["enableFade"]  = False
    content["enableWaves"]  = False
    content["enableCircles"]  = False
    content["enableRainbow"]  = False


@content.parameter_changed('Color')
def parameter_changed(value):
    setNewColor(value)
    #setColors(value)
  

@content.OSC('/tph/touched')
def touched(i):
    print "/tph/touched " + str(i)
    if i==0:
        print "Set Color Red"
        setNewColor(ofColor(255,0,0))
    elif i==1:
        print "Set Color Green"
        setNewColor(ofColor(0,255,0))
    elif i==2:
        print "Set Color Blue"
        setNewColor(ofColor(0,0,255))
    elif i==3:
        print "Set Color Cyan"
        setNewColor(ofColor(0,255,255))
    elif i==4:
        print "Set Color Pink"
        setNewColor(ofColor(255,20,147))
    elif i==5:
        print "Set Color Purple"
        setNewColor(ofColor(255,0,255))
    # elif i==6:
    #     print "Set Color Lavender"
    #     setColors(ofColor(230,230,250))
    elif i==6:
        print "Set Color White"
        setNewColor(ofColor(255,255,255))

    elif i==7:
        print "Set Sparkles"
        disableAll()
        content["enableSparkles"]  = True

    elif i==8:
        print "Set Rainbow"
        disableAll()
        content["enableRainbow"]  = True

    elif i==9:
        print "Set Fade"
        disableAll()
        content["enableFade"]  = True

    elif i==10:
        print "Set Waves"
        disableAll()
        content["enableWaves"]  = True

    elif i==11:
        print "Set Circles"
        disableAll()
        content["enableCircles"]  = True



@content.OSC('/tph/released')
def released(i):
    print "/tph/released " + str(i) 


@content.OSC('/tph/autodiscovery')
def loopDrumsOSC(i):
    print "/tph/autodiscovery " + str(i) 





