import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

class MyApp(App):
	
	def build(self):
		layout = FloatLayout(size=(300, 300))
		button = Button(text='Hello world',size_hint=(.5, .25),pos=(20, 20))
		layout.add_widget(button)
		return layout

MyApp().run()
