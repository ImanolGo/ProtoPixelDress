from protopixel import Content
from openframeworks import *

import os.path
from tempfile import mkdtemp

content = Content("SnowFlakes")

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
speedFactor = 0.6

content.add_parameter("color1", type="color", value=ofColor(255, 255, 255))
content.add_parameter("color2", type="color", value=ofColor(255, 255, 255))
content.add_parameter("color3", type="color", value=ofColor(255, 255, 255))
content.add_parameter("change_hue", value=True)
content.add_parameter("color_speed", min=0.00, max=1.0, value=0.1)
content.add_parameter("speed", min=0.01, max=1.0, value=0.5)
content.add_parameter("particles_direction", min=0, max=3, value=0)
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

def update():
    """
    For every frame, before drawing, we update stuff
    """

    if content['change_hue'] == False:
        return

    global elapsedTime, color, startColorIndex, endColorIndex, scaleFactor
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

    global speedFactor

    r = color.r/255.0
    g = color.g/255.0
    b = color.b/255.0

    speed = ofMap(content['speed'], 0.0, 1.0, 0.0, speedFactor);

    if shader.isLoaded():
        shader.begin()
        shader.setUniform3f('iColor', r,g,b)
        shader.setUniform3f('iResolution', float(content.FBO_SIZE[0]), float(content.FBO_SIZE[1]),0.0)
        shader.setUniform1f('iGlobalTime', ofGetElapsedTimef()*speed)
        shader.setUniform1i('iparticles_direction', content['particles_direction'])
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
uniform int iparticles_direction;

in vec4 position_frag;
"""

frag_contents = """
// This code can be found in 
// https://www.shadertoy.com/view/MscXD7
// and it's property of its creator.
// This is distributed for illustration purposes only.

#define _SnowflakeAmount 500    // Number of snowflakes
#define _BlizardFactor 0.2      // Fury of the storm !

vec2 uv;
uniform vec3 iColor = vec3(1.0,1.0,1.0);

float rnd(float x)
{
    return fract(sin(dot(vec2(x+47.49,38.2467/(x+2.3)), vec2(12.9898, 78.233)))* (43758.5453));
}

float drawCircle(vec2 center, float radius)
{
    return 1.0 - smoothstep(0.0, radius, length(uv - center));
}


void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    float invAr = iResolution.y / iResolution.x;

    if(iparticles_direction>1){
        uv = fragCoord.xy / iResolution.x;
    }
    else{
        uv = fragCoord.yx / iResolution.x;
    }
   
    fragColor = vec4(0, 0, 0, 1.0);
    float j;
    vec4 texColor = vec4(iColor, 1.0);
    
    for(int i=0; i<_SnowflakeAmount; i++)
    {
        j = float(i);
        float speed = 0.3+rnd(cos(j))*(0.7+0.5*cos(j/(float(_SnowflakeAmount)*0.25)));
        vec2 center = vec2((0.25-uv.y)*_BlizardFactor+rnd(j)+0.1*cos(iGlobalTime+sin(j)), mod(sin(j)-speed*(iGlobalTime*1.5*(0.1+_BlizardFactor)), 1.0));
        
        if(iparticles_direction%2 == 0){
            center = 1-center;
        }

        fragColor += (vec4(drawCircle(center, 0.001+speed*0.012))*texColor);
    }
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