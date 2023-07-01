import os
os.environ['KIVY_GL_BACKEND'] = 'gl'

from kivy.app import App 
from kivy.uix.widget import Widget 
from kivy.uix.label import Label 
from kivy.clock import Clock
from functools import partial
from kivy.uix.screenmanager import Screen
import RPi.GPIO as GPIO
import dht11
import datetime

temp = dht11.DHT11(pin=4)
temperature=0
humidity=0

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

class DisplayData(Label):
    
        def update(self, index, *args):
            result = temp.read()
            temperature = result.temperature
            if result.is_valid():

                print("Temperatura: %-3.1f C" % temperature)
                self.text = "Temperatura: "+str(temperature)
                self.font_size='30sp'
                self.size_hint=(0.5, 1.0)

class DisplayData2(Label):    
        def update(self, index, *args):
            result = temp.read()
            humidity = result.humidity
            if result.is_valid():

                print("Umidità: %-3.1f C" % humidity)
                self.text = "Umidità: "+str(humidity)
                self.font_size='30sp'
                self.size_hint=(1.4, 1.0)
                
class inputGPIO(App):
    def build(self):
        
        screen = Screen()
        
        duration = DisplayData()
        duration2 = DisplayData2()
        
        screen.add_widget(duration)
        screen.add_widget(duration2)
        Clock.schedule_interval(partial(duration.update, str(temperature)), 6)
        Clock.schedule_interval(partial(duration2.update, str(humidity)), 4)
        return screen


inputGPIO().run()
