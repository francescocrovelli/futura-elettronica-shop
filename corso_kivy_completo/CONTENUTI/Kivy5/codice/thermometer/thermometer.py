#moduli importati
import kivy
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.properties import BoundedNumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.label import Label

from w1thermsensor import W1ThermSensor #modulo per il sensore di temperatura
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) #BCM
from Adafruit_CharLCD import Adafruit_CharLCD #modulo per il display LCD
fanPin=17 #relè fan 
thermoPin=24 #relè thermo

GPIO.setup(fanPin, GPIO.OUT)
GPIO.setup(thermoPin, GPIO.OUT)
GPIO.output(fanPin,False) #fan spento
GPIO.output(thermoPin,False)#thermo spento

lcd = Adafruit_CharLCD() #istanza per il display LCD
lcd.begin(16,2) #inizializzazione del display LCD
lcd.clear() #cancella il display LCD
temperature=0 #variabile di temperatura

sensor = W1ThermSensor() #istanza per il sensore di temperatura
       
class Gauge(Widget): #classe Gauge
    unit = NumericProperty(1.8) #unità di misura
    value = BoundedNumericProperty(0, min=0, max=100) #limiti min max del gauge
    file_gauge = "gauge.png" #file immagine del gauge
    file_needle = "needle.png" #file immagine del needle
    size_gauge = BoundedNumericProperty(128, min=128, max=256) #dimensione min max del gauge
    size_text = NumericProperty(10) #dimensione del testo

    def __init__(self, **kwargs): #funzione init
        super(Gauge, self).__init__(**kwargs) #funzione super

        self.gauge = Scatter( #creazione dello Scatter gauge
            size=(self.size_gauge, self.size_gauge),#dimensioni x e y
            do_rotation=False, #imposta la rotazione a False
            do_scale=False, #imposta la scala a False
            do_translation=False #imposta la traslazione a False
        )

        img_gauge = Image( #creazione dell'immagine del gauge
            source=self.file_gauge, #in base al file del gauge
            size=(self.size_gauge, self.size_gauge) #dimensioni predefinite
        )

        self.needle = Scatter( #creazione dello Scatter needle
            size=(self.size_gauge, self.size_gauge), #dimensioni x e y
            do_rotation=False, #imposta la rotazione a False
            do_scale=False, #imposta la scala a False
            do_translation=False #imposta la traslazione a False
        )

        img_needle = Image(#creazione dell'immagine del needle
            source=self.file_needle, #in base all'immagine del needle
            size=(self.size_gauge, self.size_gauge) #dimensioni predefinite
        )

        self.gauge_label = Label(font_size=20, markup=True) #etichetta del gauge
        self.gauge.add_widget(img_gauge) #aggiunta dell'immagine  gauge
        self.needle.add_widget(img_needle) #aggiunta dell'immagine needle

        self.add_widget(self.gauge) #aggiunta del widget gauge
        self.add_widget(self.needle) #aggiunta del widget needle
        self.add_widget(self.gauge_label) #aggiunta del widget label del gauge

        self.bind(pos=self.update) #binding al callback della posizione
        self.bind(size=self.update) #binding al callback di aggiornamento
        self.bind(value=self.turn) #binding al callback della rotazione

    def update(self, *args): #funzione di aggiornamento
        self.gauge.pos = self.pos #posizione del gauge
        self.needle.pos = (self.x, self.y) #posizione x del needle
        self.needle.center = self.gauge.center #centratura del needle
        self.gauge_label.center_x = self.gauge.center_x #centratura dell'etichetta
        self.gauge_label.center_y = self.gauge.center_y + (self.size_gauge / 4) #posizione x dell'etichetta

    def turn(self, *args): #funzione di rotazione
        self.needle.center_x = self.gauge.center_x #posizione x del centro del needle
        self.needle.center_y = self.gauge.center_y #posizione y del centro del needle
        self.needle.rotation = (50 * self.unit) - (self.value * self.unit) #rotazione del needle
        self.gauge_label.text = "[b]{0:.0f}[/b]".format(self.value) #testo dell'etichetta con il valore di temperatura

class ThermometerApp(App): #classe principale Thermometer
    increasing = NumericProperty(1) #incremento di 1 unità
    step = NumericProperty(1) #valore dello step   

    def build(self): #funzione build
        layout = BoxLayout(orientation='vertical', spacing= 20, padding=20) #layout tipo BoxLayout
        self.gauge = Gauge(value=0, size_gauge=256, size_text=25) #inizializza la classe del widget Gauge
        self.lbl_temp=Label(text="Temperature: ", font_size=24) #etichetta
        self.lbl_mess1=Label(text="Cooling fan: OFF", font_size=24) #etichetta
        self.lbl_mess2=Label(text="Thermostat: OFF", font_size=24) #etichetta
        layout.add_widget(self.lbl_temp) #aggiunta etichetta
        layout.add_widget(self.lbl_mess1) #aggiunta etichetta
        layout.add_widget(self.lbl_mess2) #aggiunta etichetta
        layout.add_widget(self.gauge) #aggiunta al layout del widget Gauge
        Clock.schedule_interval(lambda dt: self.gauge_increment(), 3) #intervallo di aggiornamento ogni 3 secondi
        return layout #ritorno del layout

    def gauge_increment(self): #calbback di incremento
        temperature = sensor.get_temperature()- 2 #lettura del sensore di temperatura
        self.lbl_temp.text="Temperature: " + str(temperature) #testo etichetta
        lcd.clear() #cancella il display LCD
        lcd.message("Temperature:\n") #stampa Temperature e un a capo
        lcd.message(str(temperature)) #stampa il dato di temperatura
        lcd.message(" C ") #stampa Celsius
        if temperature > 30: #se la temperatura supera 30 gradi...
            lcd.message("FAN ON") #messaggio sul display LCD
            GPIO.output(fanPin,True) #accende il ventilatore
            GPIO.output(thermoPin,False) #spegne il termo
            self.lbl_mess1.text="Cooling fan: ON" #testo etichetta
            self.lbl_mess2.text="Thermostat: OFF" #testo etichetta
        if temperature < 10: #se la temperatura è inferiore a 10 gradi...
            lcd.message("HEAT ON")#messaggio sul display LCD
            GPIO.output(fanPin,False) #spegne il ventilatore
            GPIO.output(thermoPin,True) #accende il termo
            self.lbl_mess1.text="Cooling fan: OFF" #testo etichetta
            self.lbl_mess2.text="Thermostat: ON" #testo etichetta
        if temperature <= 30 and temperature >= 10:
            GPIO.output(fanPin,False) #spegne il ventilatore
            GPIO.output(thermoPin,False) #spegne il termo
            lcd.message("ALL OFF")#messaggio sul display LCD
            self.lbl_mess1.text="Cooling fan: OFF" #testo etichetta
            self.lbl_mess2.text="Thermostat: OFF" #testo etichetta
            
        self.gauge.value = temperature
ThermometerApp().run()
