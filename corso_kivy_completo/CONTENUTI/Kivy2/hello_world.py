import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy


from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        return Label(text='Hello world',font_size='50sp')

MyApp().run()
