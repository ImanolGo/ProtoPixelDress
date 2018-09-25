from openframeworks import *
import os.path
from tempfile import mkdtemp
        

class Circles:

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
            self.shader.setUniform1f('iGlobalTime', ofGetElapsedTimef()*3.0)
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

        in vec4 position_frag;
          """


        self.frag_contents = """
        // This code can be found in 
        // https://www.shadertoy.com/view/ldX3zr
        // and it's property of its creator.
        // This is distributed for illustration purposes only.

        vec2 center = vec2(0.5,0.5);
        float speed = 0.035;
        uniform vec3 iColor = vec3(1.0,1.0,1.0);

        void mainImage( out vec4 fragColor, in vec2 fragCoord )
        {
            float invAr = iResolution.y / iResolution.x;

            vec2 uv = fragCoord.xy / iResolution.xy;

            vec3 col = vec4(uv,0.5+0.5,1.0).xyz;

            vec3 texcol;

            float x = (center.x-uv.x);
            float y = (center.y-uv.y) *invAr;

            float r = -sqrt(x*x + y*y); //uncoment this line to symmetric ripples
            //float r = -(x*x + y*y);
            float z = 1.0 + 1.0*sin((r+iGlobalTime*speed)/0.013);

            texcol.x = z;
            texcol.y = z;
            texcol.z = z;
            texcol = 1 - texcol;

            fragColor = vec4(iColor*texcol,1.0);
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

        



