import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout

class MyApp(App):
        
	def build(self):
                layout = AnchorLayout(anchor_x='right', anchor_y='bottom')
                btn = Button(text='Hello World', width=40 + 20 * 5, size_hint=(None, 0.15))
                layout.add_widget(btn)


		
		return layout

MyApp().run()
