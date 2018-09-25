from protopixel import Content
from openframeworks import *

import os.path
from tempfile import mkdtemp

content = Content("Noise")

side = 256
content.FBO_SIZE = (side,side)
shaderfile = content.add_asset('shader')
shader = ofShader()

temp_dir = mkdtemp()
frag_file = os.path.join(temp_dir,'s.frag')
vert_file = os.path.join(temp_dir,'s.vert')
shader_file_of = os.path.join(temp_dir,'s')

#a global variable
color = ofColor(255)
elapsedTime = 0.0
startColorIndex = 1
endColorIndex = 2
scaleFactor = 10
currentTime = 0
timeFactor = 0.5
speedFactor = 2.0

content.add_parameter("color1", type="color", value=ofColor(255, 255, 255))
content.add_parameter("color2", type="color", value=ofColor(255, 255, 255))
content.add_parameter("color3", type="color", value=ofColor(255, 255, 255))
content.add_parameter("change_hue", value=True)
content.add_parameter("color_speed", min=0.00, max=1.0, value=0.1)
content.add_parameter("speed", min=0.0, max=1.0, value=0.3)
content.add_parameter("noise_grain", min=0.00, max=1.0, value=0.1)
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

    global currentTime, timefactor

    if content['shader path']:
        shader_path_changed(content['shader path'])

    with open(frag_file,'w') as f:
        f.write(frag_contents_prefix)
        f.write(frag_contents)
        f.write(frag_contents_suffix)
    with open(vert_file,'w') as f:
        f.write(vert_contents)
    shader.load(shader_file_of)

    global color
    color = ofColor(content['color1'].r,content['color1'].g,content['color1'].b)

    currentTime = ofGetElapsedTimef()*content['speed']*timefactor

def update():
    """
    For every frame, before drawing, we update stuff
    """

    if content['change_hue'] == False:
        return

    global elapsedTime, color, startColorIndex, endColorIndex, timeFactor, scaleFactor, currentTime
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

    targetTime = ofGetElapsedTimef()*content['speed']*timeFactor
    currentTime = currentTime  + (targetTime - currentTime)*0.1

def draw():

    global color, currentTime, speedFactor
    
    r = color.r/255.0
    g = color.g/255.0
    b = color.b/255.0

    speed = ofMap(content['speed'], 0.0, 1.0, 0.0, speedFactor)

    if shader.isLoaded():
        shader.begin()
        shader.setUniform3f('iColor', r,g,b)
        shader.setUniform3f('iResolution', float(content.FBO_SIZE[0]), float(content.FBO_SIZE[1]),0.0)
        shader.setUniform1f('iGlobalTime', ofGetElapsedTimef()*speed)
        #shader.setUniform1f('iGlobalTime', currentTime)
        shader.setUniform1f('inoise_grain', content['noise_grain']*10.0)
        ofDrawRectangle(-side/2.,-side/2.,side,side)
        shader.end()

@content.parameter_changed('shader path')
def shader_path_changed(p):
    print p
    frag_contents = open(p).read()
    with open(frag_file,'w') as f:
        f.write(frag_contents_prefix)
        f.write(frag_contents)
        f.write(frag_contents_suffix)
    with open(vert_file,'w') as f:
        f.write(vert_contents)
    shader.load(shader_file_of)


vert_contents = """
#version 150

in vec4 position;
out vec4 position_frag;

void main() {
    gl_Position = position;
    position_frag = position;
}
"""

frag_contents_prefix = """
#version 150
out vec4 outputColor;
uniform vec3 iResolution;
uniform float iGlobalTime;
uniform float inoise_grain;

in vec4 position_frag;
"""

frag_contents = """
// This code can be found in 
// https://www.shadertoy.com/view/Ms3SWs
// and it's property of its creator.
// This is distributed for illustration purposes only.

uniform vec3 iColor = vec3(1.0,1.0,1.0);

float hash(vec2 p)
{
    vec3 p3  = fract(vec3(p.xyx) * 0.1031);
    p3 += dot(p3, p3.yzx + 19.19);
    return fract((p3.x + p3.y) * p3.z);
}

float ang(vec2 uv, vec2 center){
    return atan((uv.y-center.y),(uv.x-center.x));
}

float spir(vec2 uv, vec2 loc){
    float dist1=length(uv-loc);
    float dist2=dist1*dist1;
    float layer6=sin((ang(uv,loc)+dist2-iGlobalTime)*6.0);
    layer6 = layer6*dist1;
    return layer6;
}

float ripl(vec2 uv, vec2 loc, float speed, float frequency){
    return sin(iGlobalTime*speed-length(uv-loc)*frequency);
}

float height(in vec2 uv){
    float layer1=sin(iGlobalTime*8.54-inoise_grain*sin(length(uv-vec2(-0.41,-0.47)))*55.0);
    float layer2=sin(iGlobalTime*7.13-inoise_grain*sin(length(uv-vec2(1.35,1.32)))*43.0);
    float layer3=sin(iGlobalTime*7.92-inoise_grain*sin(length(uv-vec2(-0.34,1.28)))*42.5);
    float layer4=sin(iGlobalTime*6.71-inoise_grain*sin(length(uv-vec2(1.23,-0.24)))*47.2);

    float spiral=spir(uv,vec2(0.5,0.5));
    spiral*=3.0;
    
    float temp = layer1+layer2+layer3+layer4+spiral;
    
    float b=smoothstep(-1.5,7.0,temp);
    return b*2.0;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 uv=fragCoord.xy/iResolution.x;
    
    float waveHeight=0.02+height(uv);
    
    vec3 color=vec3(waveHeight*iColor.r,waveHeight*iColor.g,waveHeight*iColor.b);
    
    fragColor = vec4( color, 1.0 );
}

"""

frag_contents_suffix = """
void main()
{
    vec2 pos = position_frag.xy;
    pos.x /= 2.0;
    pos.y /= 2.0;
    pos.x += 0.5;
    pos.y += 0.5;
    pos.x *= iResolution.x;
    pos.y *= iResolution.y;
    mainImage( outputColor, pos);
}
"""