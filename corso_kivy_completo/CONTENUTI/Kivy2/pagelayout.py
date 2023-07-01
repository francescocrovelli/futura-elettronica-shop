import os
os.environ['KIVY_GL_BACKEND'] = 'gl'

from kivy.base import runTouchApp
from kivy.lang import Builder

kv = '''
PageLayout:
    Button:
        text: 'page1'
    Button:
        text: 'page2'
    Button:
        text: 'page3'
'''
runTouchApp(Builder.load_string(kv))



