import os
os.environ['KIVY_GL_BACKEND'] = 'gl'

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
ledPin=[21,6,20,19]

for i in range (0,4):
    GPIO.setup(ledPin[i], GPIO.OUT)
    GPIO.output(ledPin[i],0)

Builder.load_string("""
<LedScreen>:
    BoxLayout: #crea un layout con il widget BoxLayout
        orientation: "vertical" #orientamento 
        ToggleButton:   #aggiunge un widget ToggleButton         
            text: 'LED 1' #testo del widget
            on_press: root.led_switch1() #metodo per il bind alla funzione            
        ToggleButton: #come sopra
            text: 'LED 2'
            on_press: root.led_switch2()                        
        ToggleButton: #come sopra
            text: 'LED 3'
            on_press: root.led_switch3()            
        ToggleButton: #come sopra
            text: 'LED 4'
            on_press: root.led_switch4()            
""")
            
class LedScreen(Screen):    

    def led_switch1(self):
        if GPIO.input(ledPin[0])== GPIO.LOW:
            print ("LED "+str(ledPin[0]) + " on")
            GPIO.output(ledPin[0],1)            
            return
        if GPIO.input(ledPin[0])== GPIO.HIGH:
            print ("LED "+str(ledPin[0]) + " off")
            GPIO.output(ledPin[0],0)            
            return

    def led_switch2(self):
        if GPIO.input(ledPin[1])== GPIO.LOW:
            print ("LED "+str(ledPin[1]) + " on")
            GPIO.output(ledPin[1],1)            
            return
        if GPIO.input(ledPin[1])== GPIO.HIGH:
            print ("LED "+str(ledPin[1]) + " off")
            GPIO.output(ledPin[1],0)            
            return

    def led_switch3(self):
        if GPIO.input(ledPin[2])== GPIO.LOW:
            print ("LED "+str(ledPin[2]) + " on")
            GPIO.output(ledPin[2],1)            
            return
        if GPIO.input(ledPin[2])== GPIO.HIGH:
            print ("LED "+str(ledPin[2]) + " off")
            GPIO.output(ledPin[2],0)            
            return

    def led_switch4(self):
        if GPIO.input(ledPin[3])== GPIO.LOW:
            print ("LED "+str(ledPin[3]) + " on")
            GPIO.output(ledPin[3],1)            
            return
        if GPIO.input(ledPin[3])== GPIO.HIGH:
            print ("LED "+str(ledPin[3]) + " off")
            GPIO.output(ledPin[3],0)            
            return

sm = ScreenManager()
sm.add_widget(LedScreen())
    
class LedApp(App):

    def build(self):
        return sm

LedApp().run()
