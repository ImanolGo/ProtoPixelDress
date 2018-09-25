from openframeworks import *
import os.path
from tempfile import mkdtemp
        

class Waves:

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
            self.shader.setUniform1f('iGlobalTime', ofGetElapsedTimef()*0.2)
            self.shader.setUniform3f('iResolution', float(self.width), float(self.height),0.0)
            self.shader.setUniform1f('inoise_grain', 0.7)
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
        uniform float inoise_grain;

        in vec4 position_frag;
          """


        self.frag_contents = """
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

        



