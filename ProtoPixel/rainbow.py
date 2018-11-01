from openframeworks import *
import os.path
from tempfile import mkdtemp
        

class Rainbow:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.shader = ofShader()
        self.fbo = ofFbo()
        self.fbo.allocate(width,height)
        self.color = ofColor(255)
        self.currentAlpha = 1.0
        self.targetAlpha = 1.0
        self.elapsedTime = 0.0
        self.one_day_in_seconds = 60*60*24
        self.speed = 0.1
        self.setup()


    def setup(self):
        self.setupShader()

    def update(self):
        self.updateTime()
        self.updateAlpha()
        self.updateFbo()

    def updateAlpha(self):
        self.currentAlpha = self.currentAlpha + (self.targetAlpha - self.currentAlpha)*0.05
        p = -( self.currentAlpha * (self.currentAlpha - 2))
        self.color.a = int(p*255)

    def updateTime(self):
        self.elapsedTime += ofGetLastFrameTime()
        if self.elapsedTime > self.one_day_in_seconds:
            self.elapsedTime-= self.one_day_in_seconds

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
        a = self.color.a/255.0

        if self.shader.isLoaded():
            self.shader.begin()
            self.shader.setUniform4f('iColor', r,g,b,a)
            self.shader.setUniform1f('iGlobalTime', self.elapsedTime*self.speed)
            self.shader.setUniform3f('iResolution', float(self.width), float(self.height),0.0)
            ofDrawRectangle(-self.width/2.,-self.height/2.,self.width,self.height)
            #self.fbo.draw(0,0)
       
            self.shader.end()
        

    def setColor(self, color):
        self.color = color

    def setAlpha(self, alpha):
        self.targetAlpha = alpha

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
          uniform vec4 iColor = vec4(1.0);

          in vec4 position_frag;
          """


        self.frag_contents = """
            #define FALLING_SPEED  0.25
            #define STRIPES_FACTOR 5.0

            //get sphere
            float sphere(vec2 coord, vec2 pos, float r) {
                vec2 d = pos - coord; 
                return smoothstep(60.0, 0.0, dot(d, d) - r * r);
            }

            //main
            void mainImage( out vec4 fragColor, in vec2 fragCoord )
            {
                //normalize pixel coordinates
                vec2 uv         = fragCoord / iResolution.xy;
                //pixellize uv
                vec2 clamped_uv = (round(fragCoord / STRIPES_FACTOR) * STRIPES_FACTOR) / iResolution.xy;
                //get pseudo-random value for stripe height
                float value     = fract(sin(clamped_uv.x) * 43758.5453123);
                //create stripes
                vec3 col        = vec3(1.0);
                //add color
                    col       *= clamp(cos(iGlobalTime * 0.9 + uv.xyx + vec3(0, 2, 4)), 0.0, 1.0);
                //add glowing ends
                    // col     += vec3(sphere(fragCoord, 
                      //                        vec2(clamped_uv.x, (1.0 - 2.0 * mod((iGlobalTime * (FALLING_SPEED + value / 5.0)) + value, 0.5))) * iResolution.xy, 
                        //                      0.9)) / 2.0; 
                //add screen fade
                    // col       *= vec3(exp(-pow(abs(uv.y - 0.5), 6.0) / pow(2.0 * 0.05, 2.0)));
                // Output to screen
                fragColor       = vec4(col,iColor.a);
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

        



