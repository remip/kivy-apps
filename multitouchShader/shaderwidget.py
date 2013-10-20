from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty
from kivy.graphics import RenderContext, Fbo, Color, Rectangle
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

class ShaderWidget(FloatLayout):

	# property to set the source code for fragment shader
	fs = StringProperty(None)

	# texture of the framebuffer
	texture = ObjectProperty(None)

	def __init__(self, **kwargs):
		# Instead of using canvas, we will use a RenderContext,
		# and change the default shader used.
		self.canvas = RenderContext(use_parent_projection=True)

		# We create a framebuffer at the size of the window
		# FIXME: this should be created at the size of the widget
		with self.canvas:
			self.fbo = Fbo(size=Window.size, use_parent_projection=True)

		# Set the fbo background to black.
		with self.fbo:
			Color(0, 0, 0)
			Rectangle(size=Window.size)

		# call the constructor of parent
		# if they are any graphics object, they will be added on our new canvas
		super(ShaderWidget, self).__init__(**kwargs)

		# We'll update our glsl variables in a clock
		Clock.schedule_interval(self.update_glsl, 0)

		# Don't forget to set the texture property to the texture of framebuffer
		self.texture = self.fbo.texture

	def update_glsl(self, *largs):
		self.canvas['time'] = Clock.get_boottime()
		self.canvas['resolution'] = map(float, self.size)

	def on_fs(self, instance, value):
		# set the fragment shader to our source code
		shader = self.canvas.shader
		old_value = shader.fs
		shader.fs = value
		if not shader.success:
			shader.fs = old_value
			raise Exception('Shader failed')
		
		self.canvas['touches'] = [ [0.0, 0.0, 0.0] for x in xrange(20)] # z is for touch_down


	def on_touch_down(self,touch):
		#find a free index
		for i in xrange(len(self.canvas['touches'])):
			if self.canvas['touches'][i][2] == 0.0:
				self.canvas['touches'][i][0] = touch.x
				self.canvas['touches'][i][1] = touch.y
				self.canvas['touches'][i][2] = 1.0
				touch.myindex = i
				break
		
		
	def on_touch_move(self,touch):
		if hasattr(touch,'myindex'):
			self.canvas['touches'][touch.myindex][0] = touch.x
			self.canvas['touches'][touch.myindex][1] = touch.y
	
	def on_touch_up(self,touch):
		if hasattr(touch,'myindex'):
			self.canvas['touches'][touch.myindex][2] = 0.0

	#
	# now, if we have new widget to add,
	# add their graphics canvas to our Framebuffer, not the usual canvas.
	#

	def add_widget(self, widget):
		c = self.canvas
		self.canvas = self.fbo
		super(ShaderWidget, self).add_widget(widget)
		self.canvas = c

	def remove_widget(self, widget):
		c = self.canvas
		self.canvas = self.fbo
		super(ShaderWidget, self).remove_widget(widget)
		self.canvas = c
