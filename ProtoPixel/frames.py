from openframeworks import *
from protopixel import Content
from tempfile import mkdtemp
import os.path
from random import randint
import imp

content = Content("ProtoPixeFrames")


print "ProtoPixeFrames"

color = ofColor(255)
shader = ofShader()
targetAlpha = 1.0
currentAlpha = 0.0

size = 10
content.FBO_SIZE = (size, size)
content.add_parameter("gamma", min=0.0, max=1.0, value=0.9)
content.add_parameter("Color", type="color", value=ofColor(255,255,255))

rainbow_file = content.add_asset("rainbow.py")
rainbow = imp.load_source('rainbow',rainbow_file)

square_file = content.add_asset("square.py")
square = imp.load_source('square',square_file)


def setup():
    """
    This will be called at the beggining, you set your stuff here
    """

    global rainbow, square

    rainbow = rainbow.Rainbow(size,size)
    square = square.Square(size,size)
    setupShader()
    setupFbo()
    

def update():
    """
    For every frame, before drawing, we update stuff
    """
    updateColor()
    rainbow.update()
    square.update()
        

def updateColor():
    global color, currentAlpha, targetAlpha
    setColors(color)

    currentAlpha = currentAlpha + (targetAlpha - currentAlpha)*0.05
    
    if currentAlpha > 1.0:
        currentAlpha = 1.0


def draw():
    """
    For every frame draw stuff. Do not forget to clear the frmebuffer!
    """
    global shader, rainbow, square

    ofClear(0)

    if shader.isLoaded():
        shader.begin()
        shader.setUniform1f('gamma', content["gamma"])
        shader.setUniform1f('alpha', currentAlpha)
        
        rainbow.draw()
        square.draw()   

        shader.end()

    #fbo.draw(0,0)   

  
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


def setAlphas(value):
    square.setAlpha(value)
    rainbow.setAlpha(value)

def setColors(color):
    square.setColor(color)

def resetAlpha():
    global currentAlpha, targetAlpha
    currentAlpha = 0
    targetAlpha = 1

@content.parameter_changed('Color')
def parameter_changed(value):

    global color

    color.r = value.r
    color.g = value.g
    color.b = value.b


@content.OSC('/tph/color')
def colorReceived(r,g,b):
    global color

   # print "/tph/color " + str(r)
   
    color.r = r
    color.b = b
    color.g = g

@content.OSC('/tph/mode')
def mode(i):

    print "/tph/mode " + str(i)

    resetAlpha()

    if i==8:
        print "Set Rainbow"
        setAlphas(0)
        rainbow.setAlpha(1)
    else:
        setAlphas(0)
        square.setAlpha(1)


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
    uniform float alpha = 1.0;

    in vec2 texCoordVarying;

    out vec4 outputColor;
    """

    frag_contents = """
            
    void main(){


        vec2 pos = texCoordVarying;
            

        //Output of the shader
        outputColor = texture(texture0, pos);
        outputColor.rgb = pow(outputColor.rgb, vec3(1.0 / gamma));
        outputColor.a = alpha;
        
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






