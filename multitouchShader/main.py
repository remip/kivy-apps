# kivy multitouch shader

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from shaderwidget import ShaderWidget



shader_monochrome = '''
#ifdef GL_ES
precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* uniform texture samplers */
uniform sampler2D texture0;

uniform vec2 resolution;
uniform float time;

uniform vec3 touches[20];

void main() {
    vec4 rgb = texture2D(texture0, tex_coord0);
    vec2 cPos = gl_FragCoord.xy;
    float thickness = 100.0;
    
	int touch = 0;
	for(int i=0; i< 20; i++) {
		if( touches[i].z > 0.5
        	&& touches[i].x - thickness/2 < cPos.x &&  cPos.x < touches[i].x + thickness/2
        	&& touches[i].y - thickness/2 < cPos.y &&  cPos.y < touches[i].y + thickness/2
        	) {
        		touch = 1;
        		break;
        	}
	}
    
    if(touch == 1) {
    	gl_FragColor = vec4(rgb.x, rgb.y, rgb.z, 1.0);
    } else {
    	float c = (rgb.x + rgb.y + rgb.z) * 0.3333;
    	gl_FragColor = vec4(c, c, c, 1.0);
    }
}
'''



class Background(Image):
	pass

class MultiTouchShaderApp(App):

	def build(self):
		
		root = FloatLayout()
		sw = ShaderWidget()
		root.add_widget(sw)
		sw.add_widget(Background())
		sw.fs = shader_monochrome
		
		return root

if __name__ in ('__main__', '__android__'):
	MultiTouchShaderApp().run()
