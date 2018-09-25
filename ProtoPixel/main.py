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

print "ProtoPixelDress"


#a global variable
elapsedTime = 0.0
size = 200
content.FBO_SIZE = (size,size) #optional: define size of FBO, default=(100,100)
targetAlpha = 0.0
currentAlpha = 0.0
 

content.add_parameter("enableSparkles", value=True)
content.add_parameter("enableRaibow", value=True)
content.add_parameter("enableFade", value=True)
content.add_parameter("Color", type="color", value=ofColor(255,255,255))


def setup():
    """
    This will be called at the beggining, you set your stuff here
    """

    global size, sparkles, rainbow, fade

    rainbow = rainbow.Rainbow(size,size)
    sparkles = sparkles.Sparkles(size,size)
    fade = fade.Fade(size,size)
   


def update():
    """
    For every frame, before drawing, we update stuff
    """

    global sparkles, rainbow

    if content["enableSparkles"]  == True:
        sparkles.update()

    if content["enableRaibow"]  == True:
        rainbow.update()

    if content["enableFade"]  == True:
        fade.update()

    
    updateAlpha()

def updateAlpha():
	global currentAlpha, targetAlpha

	currentAlpha = currentAlpha + (targetAlpha - currentAlpha)*0.05
	#print currentAlpha


def draw():
    """
    For every frame draw stuff. Do not forget to clear the frmebuffer!
    """
    global sparkles
   
    ofClear(0)

    if content["enableSparkles"]  == True:
        sparkles.draw()

    if content["enableRaibow"]  == True:
        rainbow.draw()

    if content["enableFade"]  == True:
        fade.draw()
        
  
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


@content.parameter_changed('Color')
def parameter_changed(value):
    sparkles.setColor(value)
    fade.setColor(value)


@content.OSC('/tph/touched')
def loopDrumsOSC(i):
    print "/tph/touched " + i 


@content.OSC('/tph/released')
def loopDrumsOSC(i):
    print "/tph/released " + i 





