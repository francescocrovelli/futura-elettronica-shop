import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout

class MyApp(App):
	
	def build(self):
		layout = RelativeLayout(size=(300, 300))
		btn = Button( text='Hello world', size_hint=(.25, .25), pos=(10, 10))
		layout.add_widget(btn)

		
		return layout

MyApp().run()
