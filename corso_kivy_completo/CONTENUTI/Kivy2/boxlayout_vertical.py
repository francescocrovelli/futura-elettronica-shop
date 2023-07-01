import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        btn1 = Button(text='Hello', font_size='50sp')
        btn2 = Button(text='World', font_size='50sp')
        layout.add_widget(btn1)
        layout.add_widget(btn2)

        return layout

MyApp().run()
