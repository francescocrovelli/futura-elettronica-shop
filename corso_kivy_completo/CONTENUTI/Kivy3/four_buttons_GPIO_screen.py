# -*- coding: utf-8 -*-
import os
os.environ['KIVY_GL_BACKEND'] = 'gl'

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
import RPi.GPIO as GPIO #modulo RPi.GPIO di sistema
GPIO.setmode(GPIO.BCM) #modalità BCM della piedinatura GPIO
ledPin=[21,6,20] #array di LED

for i in range (0,3): #ciclo for per impostare la modalità OUT e spegnere tutti I LED
    GPIO.setup(ledPin[i], GPIO.OUT)
    GPIO.output(ledPin[i],0)

Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: "vertical" #orientamento del layout 
        Button:
            text: 'Goto LED screen'
            background_color: [0,0,1,1]
            on_press: root.manager.current = 'settings'
        Button:
            size_hint_x: .25
            size_hint_y: .25
            pos_hint: {'right': 1}
            text: 'Quit'
            on_press: root.quit_app()

<LedScreen>:
    BoxLayout:
        orientation: "horizontal" #orientamento del layout
        Button:
            text: 'LED 1'
            on_press: root.led_switch1()                        
        Button:
            text: 'LED 2'
            on_press: root.led_switch2()                        
        Button:
            text: 'LED 3'
            on_press: root.led_switch3()                        
        Button:
            background_color: [0,1,1,1]
            text: 'Back to main menu'
            on_press: root.manager.current = 'menu'
""")


class LedScreen(Screen): #classe LedScreen derivata da Screen   
    def led_switch1(self): #funzione per il primo LED
        if GPIO.input(ledPin[0])== GPIO.LOW: #se il LED è spento
            GPIO.output(ledPin[0],1)            #accende il LED 
            return				
        if GPIO.input(ledPin[0])== GPIO.HIGH: #se il LED è acceso
            GPIO.output(ledPin[0],0)            #spegne il LED
            return
    def led_switch2(self): #funzione per il primo LED
        if GPIO.input(ledPin[1])== GPIO.LOW: #se il LED è spento
            GPIO.output(ledPin[1],1)            #accende il LED 
            return				
        if GPIO.input(ledPin[1])== GPIO.HIGH: #se il LED è acceso
            GPIO.output(ledPin[1],0)            #spegne il LED
            return
    def led_switch3(self): #funzione per il primo LED
        if GPIO.input(ledPin[2])== GPIO.LOW: #se il LED è spento
            GPIO.output(ledPin[2],1)            #accende il LED 
            return				
        if GPIO.input(ledPin[2])== GPIO.HIGH: #se il LED è acceso
            GPIO.output(ledPin[2],0)            #spegne il LED
            return

class MenuScreen(Screen):
    def quit_app(self):
        print ("End")
        exit()
        
# Crea lo screen manager
#sm = ScreenManager(transition=FadeTransition())
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(LedScreen(name='settings'))

class MenuApp(App): 

    def build(self): #costruisce lo screen manager
        return sm

MenuApp().run()
