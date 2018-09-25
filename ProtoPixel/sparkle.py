from openframeworks import *
import os.path
from tempfile import mkdtemp
        

class Sparkles:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.shader = ofShader()
        self.fbo = ofFbo()
        self.fbo.allocate(width,height)
        self.color = ofColor(255)
        self.setup()


    def setup(self):
        self.setupShader()

    def update(self):
        self.updateFbo()


    def updateFbo(self):
        self.fbo.begin()
        ofClear(0)
        ofSetColor(255)
        self.drawShader()
        self.fbo.end()

    def draw(self):

        self.fbo.draw(0,0)
        #self.drawShader()

    def drawShader(self):

        r = self.color.r/255.0
        g = self.color.g/255.0
        b = self.color.b/255.0

        if self.shader.isLoaded():
            self.shader.begin()
            self.shader.setUniform3f('iColor', r,g,b)
            self.shader.setUniform1f('iGlobalTime', ofGetElapsedTimef()*0.5)
            self.shader.setUniform3f('iResolution', float(self.width), float(self.height),0.0)
            ofDrawRectangle(-self.width/2.,-self.height/2.,self.width,self.height)
            #self.fbo.draw(0,0)
       
            self.shader.end()
        

    def setColor(self, color):
        self.color = color


    def setupShader(self):

        temp_dir = mkdtemp()
        frag_file = os.path.join(temp_dir,'s.frag')
        vert_file = os.path.join(temp_dir,'s.vert')
        shader_file_of = os.path.join(temp_dir,'s')

        self.vert_contents = """
        #version 150

        in vec4 position;
        out vec4 position_frag;

        void main() {
            gl_Position = position;
            position_frag = position;
        }
        """


        self.frag_contents_prefix = """
          #version 150
          out vec4 outputColor;
          uniform vec3 iResolution;
          uniform float iGlobalTime;
          uniform int iparticles_direction;

          in vec4 position_frag;
          """


        self.frag_contents = """
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

        self.frag_contents_suffix = """
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

        with open(frag_file,'w') as f:
            f.write(self.frag_contents_prefix)
            f.write(self.frag_contents)
            f.write(self.frag_contents_suffix)
        with open(vert_file,'w') as f:
            f.write(self.vert_contents)
        self.shader.load(shader_file_of)

        



