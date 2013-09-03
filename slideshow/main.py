import os, sys, random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.garden.moretransitions import PixelTransition, RippleTransition, BlurTransition, RVBTransition, RotateTransition
from kivy.properties import StringProperty
from kivy.clock import Clock

class Page(Screen):
	source = StringProperty()

class SlideShow(App):

	def build(self):
		
		rootPath = os.path.dirname(os.path.realpath(sys.argv[0]))
		
		self.photos = []
		for image in os.listdir(rootPath + '/Photos'):
			self.photos.append(rootPath + '/Photos/' + image)
		
		self.transitions = [ 
			BlurTransition(duration=1.5), 
			PixelTransition(duration=1.5), 
			RippleTransition(duration=1.5),
			RVBTransition(duration=2.0),
			RotateTransition(direction='down')
		] 
		
		# Create the screen manager
		r = random.randint(0, len(self.transitions) -1)
		self.screenManager = ScreenManager(transition=self.transitions[r])

		self.page1 = Page(name='page1', source = self.photos[0])
		self.page2 = Page(name='page2', source = self.photos[1])
		self.index = 0
		
		self.screenManager.add_widget(self.page1)
		self.screenManager.add_widget(self.page2)
		
		anim = Animation(
			scale=self.page1.background.scale*1.3, 
			duration=15.0
		)
		anim.start(self.page1.background)
		
		Clock.schedule_once(self.next, 10)
		
		return self.screenManager
		
	def next(self,*largs):
		
		Clock.unschedule(self.next)
		
		if(self.screenManager.current == 'page1'):
			next = 'page2'
			page = self.page2
		else:
			next = 'page1'
			page = self.page1
			
		self.index += 1
		if self.index == len(self.photos):
			self.index = 0
		page.source = self.photos[self.index]
		page.background.scale = 1.0		
		self.screenManager.transition = self.transitions[random.randint(0, len(self.transitions) -1)]
		self.screenManager.current = next
		
		anim = Animation(
			scale=page.background.scale*1.3, 
			duration=15.0
		)
		
		Clock.schedule_once(self.next, 10)
		
		anim.start(page.background)
		

if __name__ in ('__main__', '__android__'):
	SlideShow().run()
