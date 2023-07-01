import os
#os.environ[“KIVY_WINDOW”] = ‘sdl2’ #uso con Raspberry Pi 4B
#os.environ[‘KIVY_GL_BACKEND’] = ‘gl’ #uso con Raspberry Pi 3B+

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock

import RPi.GPIO as GPIO

buttonPin1 = 6
pinStatus = 0
status = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def my_callback(dt):
        pinStatus = 0
        global status
        status = not status
        #print(pin)
        
class InputButton1(Button):
        def update(self, deltaTime):
                global pinStatus
                if GPIO.input(buttonPin1) == False & pinStatus==0:
                        pinStatus=1
                        #print(pin)
                        if status == 0:
                                self.state = 'down'
                                self.text="BUTTON ON"
                        if status == 1:
                                self.state = 'normal'
                                self.text="BUTTON OFF"
                        
                        Clock.schedule_once(my_callback,0.5)
			
class inputGPIO(App):
        def build(self):
                layout=GridLayout(cols=4,rows=4,spacing=20,padding=20)
                inputDisplay1 = InputButton1(text="BUTTON OFF"
                                             ,font_size="20sp"
                                             ,size=[256,256]
                                             ,size_hint=[None,None]
                                             ,background_normal = "button_up.png"
                                             ,background_down="button_down.png")
                
                Clock.schedule_interval(inputDisplay1.update, 0.5)
                layout.add_widget(inputDisplay1)
                return layout

inputGPIO().run()
