import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy

from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout

import RPi.GPIO as GPIO
	
ledPin_1 = 21 #40
ledPin_2 = 6 #31
ledPin_3 = 20 #38
ledPin_4 = 19 #35

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin_1, GPIO.OUT)
GPIO.setup(ledPin_2, GPIO.OUT)
GPIO.setup(ledPin_3, GPIO.OUT)
GPIO.setup(ledPin_4, GPIO.OUT)


def press_callback(obj):
	if obj.text == 'LED 1':
		if obj.state == "down":
			print ("button 1 on")
			GPIO.output(ledPin_1, GPIO.HIGH)
		else:
			print ("button 1 off")
			GPIO.output(ledPin_1, GPIO.LOW)
	if obj.text == 'LED 2':
		if obj.state == "down":
			print ("button 2 on")
			GPIO.output(ledPin_2, GPIO.HIGH)
		else:
			print ("button 2 off")
			GPIO.output(ledPin_2, GPIO.LOW)
	if obj.text == 'LED 3':
		if obj.state == "down":
			print ("button 3 on")
			GPIO.output(ledPin_3, GPIO.HIGH)
		else:
			print ("button off")
			GPIO.output(ledPin_3, GPIO.LOW)
	if obj.text == 'LED 4':
		if obj.state == "down":
			print ("button 4 on")
			GPIO.output(ledPin_4, GPIO.HIGH)
		else:
			print ("button 4 off")
			GPIO.output(ledPin_4, GPIO.LOW)

class MyApp(App):
        

	def build(self):
		layout = BoxLayout(orientation='horizontal')

		led_1 = ToggleButton(text="LED 1", size_hint=(.5,.5), pos_hint={'top': 0.9})
		
		led_2 = ToggleButton(text="LED 2", size_hint=(.5,.25),pos_hint={'top': 0.9})
		
		led_3 = ToggleButton(text="LED 3", size_hint=(.5,.25),pos_hint={'top': 0.9})
		
		led_4 = ToggleButton(text="LED 4", size_hint=(.5,1))
		

		layout.add_widget(led_1)
		layout.add_widget(led_2)
		layout.add_widget(led_3)
		layout.add_widget(led_4)

		

		return layout


MyApp().run()
