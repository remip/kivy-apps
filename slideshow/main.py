import os, sys, random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.garden.moretransitions import PixelTransition, RippleTransition, BlurTransition, RVBTransition, RotateTransition, TileTransition, FastSlideTransition, ShatterTransition
from kivy.properties import StringProperty, AliasProperty
from kivy.clock import Clock
from kivy.utils import platform

class Page(Screen):
    source = StringProperty()

class ZoomImage(Image):

    def get_norm_image_size(self):
        if not self.texture:
            return self.size
        ratio = self.image_ratio
        w, h = self.size
        tw, th = self.texture.size

        iw = w
        ih = iw / ratio

        if ih < h:
            ih = h
            iw = ih * ratio

        return iw, ih

    norm_image_size = AliasProperty(get_norm_image_size, None, bind=(
        'texture', 'size', 'image_ratio', 'allow_stretch'))

class SlideShow(App):

    def build(self):

        self.photos = []
        picture_path = []

        #search for photos
        if platform == 'win':
            picture_path = [ os.path.join(os.environ['USERPROFILE'], 'Pictures') ]
        elif platform == 'macos':
            picture_path = [ os.path.join(os.pathexpanduser("~"), 'Pictures', 'Photos') ]
        elif platform == 'android':
            picture_path = ['/sdcard/Pictures/', '/sdcard/DCIM']

        if picture_path:
            for path in picture_path:
                for root, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        if filename.endswith(('.jpg', '.jpeg', '.JPG', '.JPEG')):
                            self.photos.append(os.path.join(root, filename))
            random.shuffle(self.photos)

        # use stock photos if nothing food
        if len(self.photos) == 0:

            rootPath = os.path.dirname(os.path.realpath(sys.argv[0]))

            for image in os.listdir(rootPath + '/Photos'):
                self.photos.append(rootPath + '/Photos/' + image)

        self.transitions = [
            BlurTransition(duration=1.5),
            PixelTransition(duration=1.5),
            RippleTransition(duration=1.5),
            RVBTransition(duration=2.0),
            RotateTransition(direction='down'),
            #not compatible with android:
            #TileTransition(duration=1.5),
            #FastSlideTransition(direction='right')
            #ShatterTransition(direction='up')
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
            scale=page.background.scale*1.1,
            duration=10.0
        )

        Clock.schedule_once(self.next, 10)

        anim.start(page.background)


if __name__ in ('__main__', '__android__'):
    SlideShow().run()
