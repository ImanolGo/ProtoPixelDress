from openframeworks import *
from protopixel import Content
from tempfile import mkdtemp
import os.path
from random import randint
import imp

from OSC import OSCClient, OSCMessage

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


OSC_DEST_IP = "localhost"
OSC_BROADCAST_IP = "192.168.8.255"
OSC_BROADCAST_PORT =  2346
OSC_DEST_PORT = 2345

# To send OSC messages we need an OSC Client
oscclient = OSCClient()

print "ProtoPixelDress"


#a global variable
elapsedTime = 0.0
change_time = 60
size = 200
content.FBO_SIZE = (size,size) #optional: define size of FBO, default=(100,100)
targetAlpha = 1.0
currentAlpha = 0.0
currentColor = ofColor(255)
previousColor = ofColor(0)
shader = ofShader()
colorIndex = 0
modeIndex = 0


content.add_parameter("gamma", min=0.0, max=1.0, value=0.6)
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
    ofEnableAlphaBlending()

    setupShader()

    touched(colorIndex)
    touched(modeIndex)


def update():
    """
    For every frame, before drawing, we update stuff
    """

    global sparkles, rainbow

    updateTime()
    updateColor()

    sparkles.update()
    rainbow.update()
    fade.update()
    waves.update() 
    circles.update()

    #print "update"
        

def updateTime():
    global elapsedTime, change_time, colorIndex, modeIndex

    elapsedTime+=ofGetLastFrameTime()
    if elapsedTime>change_time:

        # colorIndex = (colorIndex + 1)%7
        # touched(colorIndex)
        # print "Changed Color"

        # if colorIndex == 0:
        #     modeIndex = (modeIndex+1)%5
        #     touched(modeIndex + 7)
        #     print "Changed Mode"

        mode = randint(0,4)
        touched(mode)
        color = randint(5,11)
        touched(color)
        print "changedModeColor"
        
        elapsedTime = 0
       


def updateColor():

    global currentAlpha, targetAlpha, previousColor, currentColor

    currentAlpha = currentAlpha + (targetAlpha - currentAlpha)*0.02
    
    if currentAlpha > 1.0:
        currentAlpha = 1.0

    newColor = previousColor.getLerped(currentColor, currentAlpha)
    setColors(newColor)
    sendColor(newColor)
   # print currentAlpha
    #print newColor
    #print currentColor

def sendColor(color):

    message = OSCMessage() #Create the OSC Message
    message.setAddress("/tph/color") #Define the OSC Address
    message.append(int(color.r))
    message.append(int(color.g))
    message.append(int(color.b))
    oscclient.sendto(message,(OSC_DEST_IP,OSC_DEST_PORT)) #send osc message


def draw():
    """
    For every frame draw stuff. Do not forget to clear the frmebuffer!
    """
    global sparkles, shader

    ofClear(0)

    if shader.isLoaded():
        shader.begin()
        shader.setUniform1f('gamma', content["gamma"])
        
        ofClear(0)

        sparkles.draw()
        rainbow.draw()
        fade.draw()
        waves.draw()
        circles.draw()    

        shader.end()

   
    # ofClear(0)

    # if content["enableSparkles"]  == True:
    #     sparkles.draw()

    # if content["enableRainbow"]  == True:
    #     rainbow.draw()

    # if content["enableFade"]  == True:
    #     fade.draw()

    # if content["enableWaves"]  == True:
    #     waves.draw()

    # if content["enableCircles"]  == True:
    #     circles.draw()

  
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

def setAlphas(value):
    sparkles.setAlpha(value)
    waves.setAlpha(value)
    rainbow.setAlpha(value)
    fade.setAlpha(value)
    circles.setAlpha(value)

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
    global elapsedTime

    print "/tph/touched " + str(i)

    elapsedTime = 0.0

    if i==11:
        print "Set Color Red"
        setNewColor(ofColor(255,0,0))
    elif i==9:
        print "Set Color Green"
        setNewColor(ofColor(0,255,0))
    elif i==7:
        print "Set Color Blue"
        setNewColor(ofColor(0,0,255))
    elif i==8:
        print "Set Color Cyan"
        setNewColor(ofColor(0,255,255))
    elif i==6:
        print "Set Color Magenta"
        setNewColor(ofColor(255,0,255))
    elif i==10:
        print "Set Color Yellow"
        setNewColor(ofColor(255,255,0))
    elif i==5:
        print "Set Color White"
        setNewColor(ofColor(255,255,255))

    elif i==1:
        print "Set Sparkles"
        setAlphas(0)
        sparkles.setAlpha(1)

    elif i==0:
        print "Set Rainbow"
        setAlphas(0)
        rainbow.setAlpha(1)

    elif i==3:
        print "Set Fade"
        setAlphas(0)
        fade.setAlpha(1)

    elif i==2:
        print "Set Waves"
        setAlphas(0)
        waves.setAlpha(1)

    elif i==4:
        print "Set Circles"
        setAlphas(0)
        circles.setAlpha(1)


    message = OSCMessage() #Create the OSC Message
    message.setAddress("/tph/mode") #Define the OSC Address
    message.append(int(i))
    oscclient.sendto(message,(OSC_DEST_IP,OSC_DEST_PORT)) #send osc message



@content.OSC('/tph/released')
def released(i):
    print "/tph/released " + str(i) 


@content.OSC('/tph/autodiscovery')
def sendAutodiscovery(i):
    print "/tph/autodiscovery " + str(i)
    message = OSCMessage() #Create the OSC Message
    message.setAddress("/tph/autodiscovery") #Define the OSC Address
    message.append(int(i))
    oscclient.sendto(message,(OSC_BROADCAST_IP,OSC_BROADCAST_PORT)) #send osc message


@content.parameter_changed('enableWaves')
def parameter_changed(value):
    setAlphas(0)
    waves.setAlpha(value)
    print "Waves: ", value

@content.parameter_changed('enableSparkles')
def parameter_changed(value):
    setAlphas(0)
    sparkles.setAlpha(value)
    print "Sparkles: ", value

@content.parameter_changed('enableRainbow')
def parameter_changed(value):
    setAlphas(0)
    rainbow.setAlpha(value)
    print "Rainbow: ", value

@content.parameter_changed('enableFade')
def parameter_changed(value):
    setAlphas(0)
    fade.setAlpha(value)
    print "Fade: ", value

@content.parameter_changed('enableCircles')
def parameter_changed(value):
    setAlphas(0)
    circles.setAlpha(value)
    print "Circles: ", value

def setupShader():

    global shader

    temp_dir = mkdtemp()
    frag_file = os.path.join(temp_dir,'s.frag')
    vert_file = os.path.join(temp_dir,'s.vert')
    shader_file_of = os.path.join(temp_dir,'s')

    vert_contents = """
    #version 150

    // these are for the programmable pipeline system
    uniform mat4 modelViewProjectionMatrix;

    in vec4 position;
    in vec2 texcoord;

    out vec2 texCoordVarying;

    void main()
    {
        texCoordVarying = texcoord;
        
        gl_Position = modelViewProjectionMatrix * position;
    }
    """

    frag_contents_prefix = """
    #version 150    // <-- version my machine suports

    uniform sampler2DRect texture0;
    uniform float gamma = 0.2;

    in vec2 texCoordVarying;

    out vec4 outputColor;
    """

    frag_contents = """
            
    void main(){


        vec2 pos = texCoordVarying;
            

        //Output of the shader
        outputColor = texture(texture0, pos);
        outputColor.rgb = pow(outputColor.rgb, vec3(1.0 / gamma));
        
    }

    """

    frag_contents_suffix = """
        
        
    """    

    with open(frag_file,'w') as f:
        f.write(frag_contents_prefix)
        f.write(frag_contents)
        f.write(frag_contents_suffix)
    with open(vert_file,'w') as f:
        f.write(vert_contents)
    shader.load(shader_file_of)






