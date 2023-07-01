import os
os.environ['KIVY_GL_BACKEND'] = 'gl'

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout

class MyApp(App):
        
	def build(self):
                layout = StackLayout()
                for i in range(25):
                        btn = Button(text=str(i), width=40 + i * 5, size_hint=(None, 0.15))
                        layout.add_widget(btn)
		
		return layout

MyApp().run()
