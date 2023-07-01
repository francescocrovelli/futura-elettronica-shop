import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

class MyApp(App):
        
	def build(self):
		layout = GridLayout(cols=3)
		layout.add_widget(Label(text='Label 1',font_size='50sp'))
		layout.add_widget(Label(text='Label 2',font_size='50sp'))
		layout.add_widget(Label(text='Label 3',font_size='50sp'))
		layout.add_widget(Label(text='Label 4',font_size='50sp'))
		layout.add_widget(Label(text='Label 5',font_size='50sp'))
		layout.add_widget(Label(text='Label 6',font_size='50sp'))
		layout.add_widget(Label(text='Label 7',font_size='50sp'))
		layout.add_widget(Label(text='Label 8',font_size='50sp'))
		layout.add_widget(Label(text='Label 9',font_size='50sp'))
		return layout

MyApp().run()
