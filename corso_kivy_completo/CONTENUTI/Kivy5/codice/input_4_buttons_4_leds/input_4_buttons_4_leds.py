import os
#os.environ[“KIVY_WINDOW”] = ‘sdl2’ #uso con Raspberry Pi 4B
#os.environ[‘KIVY_GL_BACKEND’] = ‘gl’ #uso con Raspberry Pi 3B+

#moduli importati
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.clock import Clock
import RPi.GPIO as GPIO

buttonPin1 = 6 #pulsante 1 GPIO6 
buttonPin2 = 19 #pulsante 2 GPIO19 
buttonPin3 = 13 #pulsante 3 GPIO13 
buttonPin4 = 5 #pulsante 4 GPIO5 

led1=24 #GPIO del LED 1
led2=17 #GPIO del LED 2
led3=27 #GPIO del LED 3
led4=18 #GPIO del LED 4


GPIO.setmode(GPIO.BCM)
#modalità pull-up dei quattro pulsanti
GPIO.setup(buttonPin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#modalità OUT dei quattro LED
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)

class InputButton1(Button):
	def update(self, delayTime):
		if GPIO.input(buttonPin1) == True:
			self.state = 'normal'
			self.text="BUTTON OFF"
		else:
			self.state = 'down'
			self.text="BUTTON ON"			
			
class InputButton2(Button):
	def update(self, delayTime):
		if GPIO.input(buttonPin2) == True:
			self.state = 'normal'
			self.text="BUTTON OFF"
		else:
			self.state = 'down'
			self.text="BUTTON ON"			

class InputButton3(Button):
	def update(self, delayTime):
		if GPIO.input(buttonPin3) == True:
			self.state = 'normal'
			self.text="BUTTON OFF"
		else:
			self.state = 'down'
			self.text="BUTTON ON"			
class InputButton4(Button):
	def update(self, delayTime):
		if GPIO.input(buttonPin4) == True:
			self.state = 'normal'
			self.text="BUTTON OFF"
		else:
			self.state = 'down'
			self.text="BUTTON ON"			
			
class inputGPIO(App):
        def build(self):
                layout=GridLayout(cols=4,rows=4,spacing=20,padding=20)
                inputDisplay1 = InputButton1(text="BUTTON OFF"
                                             ,font_size="16sp"
                                             ,size=[180,180]
                                             ,size_hint=[None,None]
                                             ,background_normal = "square_button_green.png"
                                             ,background_down="square_button_red.png")
                inputDisplay2 = InputButton2(text="BUTTON OFF"
                                             ,font_size="16sp"
                                             ,size=[180,180]
                                             ,size_hint=[None,None]
                                             ,background_normal = "square_button_green.png"
                                             ,background_down="square_button_red.png")
                inputDisplay3 = InputButton3(text="BUTTON OFF"
                                             ,font_size="16sp"
                                             ,size=[180,180]
                                             ,size_hint=[None,None]
                                             ,background_normal = "square_button_green.png"
                                             ,background_down="square_button_red.png")
                inputDisplay4 = InputButton4(text="BUTTON OFF"
                                             ,font_size="16sp"
                                             ,size=[180,180]
                                             ,size_hint=[None,None]
                                             ,background_normal = "square_button_green.png"
                                             ,background_down="square_button_red.png")
                
                Clock.schedule_interval(inputDisplay1.update, 0.1)
                layout.add_widget(inputDisplay1)
                Clock.schedule_interval(inputDisplay2.update, 0.1)
                layout.add_widget(inputDisplay2)
                Clock.schedule_interval(inputDisplay3.update, 0.1)
                layout.add_widget(inputDisplay3)
                Clock.schedule_interval(inputDisplay4.update, 0.1)
                layout.add_widget(inputDisplay4)
                
                toggle1=ToggleButton(text="LED 1") #widget ToggleButton 1
                toggle2=ToggleButton(text="LED 2") #widget ToggleButton 2
                toggle3=ToggleButton(text="LED 3") #widget ToggleButton 3
                toggle4=ToggleButton(text="LED 4") #widget ToggleButton 4
                toggle1.bind(on_press=callback) #collegamento alla funzione callback
                toggle2.bind(on_press=callback) #collegamento alla funzione callback
                toggle3.bind(on_press=callback) #collegamento alla funzione callback
                toggle4.bind(on_press=callback) #collegamento alla funzione callback
                layout.add_widget(toggle1) #aggiunta del widget ToggleButton 1
                layout.add_widget(toggle2) #aggiunta del widget ToggleButton 2
                layout.add_widget(toggle3) #aggiunta del widget ToggleButton 3
                layout.add_widget(toggle4) #aggiunta del widget ToggleButton 4
                return layout
def callback(obj): #funzione di callback istanziata come oggetto ToggleButton
	if obj.text == 'LED 1': #se il testo di toggle1 è LED 1
		if obj.state == "down": #se lo stato di toggle1 è down
			GPIO.output(led1, GPIO.HIGH) #accendi il LED 1
		else: #altrimenti
			GPIO.output(led1, GPIO.LOW) # spegni il LED 1
	if obj.text == 'LED 2': #comportamento identico per il LED 2
		if obj.state == "down":
			GPIO.output(led2, GPIO.HIGH)
		else:
			GPIO.output(led2, GPIO.LOW)
	if obj.text == 'LED 3': #comportamento identico per il LED 3
		if obj.state == "down":
			GPIO.output(led3, GPIO.HIGH)
		else:
			GPIO.output(led3, GPIO.LOW)
	if obj.text == 'LED 4': #comportamento identico per il LED 4
		if obj.state == "down":
			GPIO.output(led4, GPIO.HIGH)
		else:
			GPIO.output(led4, GPIO.LOW)        

inputGPIO().run()
