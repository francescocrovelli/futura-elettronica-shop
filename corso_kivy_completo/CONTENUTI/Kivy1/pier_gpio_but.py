import os #modulo os di sistema
os.environ["KIVY_WINDOW"] = 'sdl2' #uso con Raspberry Pi 4B
#os.environ['KIVY_GL_BACKEND'] = 'gl' #uso con Raspberry Pi 3B+

import RPi.GPIO as GPIO #modulo RPi.GPIO di sistema
import time #modulo time di sistema

ledPin=21 #variabile per GPIO21
GPIO.setmode(GPIO.BCM) #modalità BCM della piedinatura GPIO
GPIO.setup(ledPin, GPIO.OUT) #imposta il pin del LED come uscita
GPIO.output(ledPin, False) #spegne il LED

from kivy.app import App #modulo App di Kivy 
from kivy.uix.button import Button #widget Button
from kivy.uix.label import Label #widget Label
from kivy.uix.boxlayout import BoxLayout #widget BoxLayout

class TestApp(App): #classe dell’applicazione chiamata TestApp
    def build(self): #funzione build all’interno della classe TestApp
        layout = BoxLayout(orientation='vertical') #Layout vertical, ovvero divisione orizzontale dello schermo in due parti
        
        blue = (0, 0, 1.5, 2.5) #variabile RGBA per il colore del pulsante
        btn =  Button(text='Touch me!', background_color=blue, font_size=48) #oggetto Button 
        btn.bind(on_press=self.callback) #istruzione bind per il callback alla pressione del pulsante
        self.label = Label(text="LED OFF", font_size='50sp') #oggetto Label
        layout.add_widget(btn) #aggiunge il widget Button al Layout
        layout.add_widget(self.label) #aggiunge il widget Label al Layout
        return layout #ritorno della funzione build con il Layout completo

    def callback(self, event): #funzione callback quando si preme il pulsante
        state = self.label.text #variabile dello stato del testo della Label
        if state == "LED ON": #se il testo della Label è “LED ON”…
            self.label.text = "LED OFF" #il testo della Label diventa “LED OFF”
            GPIO.output(ledPin, False) #spegne il LED
        if state == "LED OFF": #se il testo della Label è “LED OFF”…
            self.label.text = "LED ON" #il testo della Label diventa “LED ON”
            GPIO.output(ledPin, True) #accende il LED

TestApp().run() #istruzione per l’avvio dell’applicazione TestApp
