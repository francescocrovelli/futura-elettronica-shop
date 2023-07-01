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
buttonPin2 = 19
buttonPin3 = 13 

GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class InputButton1(Button):
	def update(self, delayTime):
		if GPIO.input(buttonPin1) == True:
			self.state = 'normal'			
		else:
			self.state = 'down'
			print (delayTime)
			
class InputButton2(Button):
	def update(self, delayTime):
		if GPIO.input(buttonPin2) == True:
			self.state = 'normal'
		else:
			self.state = 'down'
			print (delayTime)

class InputButton3(Button):
	def update(self, delayTime):
		if GPIO.input(buttonPin3) == True:
			self.state = 'normal'			
		else:
			self.state = 'down'
			print (delayTime)
			
class inputGPIO(App):
        

	def build(self):
		layout = GridLayout(cols=4, spacing=30, padding=30, row_default_height=150)

		inputDisplay1 = InputButton1(text="BUTTON 1")
		inputDisplay2 = InputButton2(text="BUTTON 2")
		inputDisplay3 = InputButton3(text="BUTTON 3")

		Clock.schedule_interval(inputDisplay1.update, 1.0/10.0)
		Clock.schedule_interval(inputDisplay2.update, 1.0/10.0)
		Clock.schedule_interval(inputDisplay3.update, 1.0/10.0)
		layout.add_widget(inputDisplay1)
		layout.add_widget(inputDisplay2)
		layout.add_widget(inputDisplay3)

		wimg = Image(source='logo.png')
		layout.add_widget(wimg)		

		return layout

inputGPIO().run()
