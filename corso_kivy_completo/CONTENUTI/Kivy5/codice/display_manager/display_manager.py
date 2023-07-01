import os
#os.environ["KIVY_WINDOW"] = 'sdl2' #uso con Raspberry Pi 4B
os.environ["KIVY_GL_BACKEND"] = 'gl' #uso con Raspberry Pi 3B+

#moduli Kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager

from Adafruit_CharLCD import Adafruit_CharLCD #libreria per il display LCD
lcd = Adafruit_CharLCD() #oggetto lcd
lcd.begin(16,2) #inizializzazione del display LCD
lcd.clear() #cancella il display LCD

modifier='' #variabile per il modifier
capslock=False #variabile per il flag di capslock

#classe per il container della keyboard, dei pulsanti e della Label
Builder.load_string('''
<KeyboardScreen>:
    displayLabel1: displayLabel1
    displayLabel2: displayLabel2  
    kbContainer: kbContainer
    BoxLayout:
        orientation: 'vertical'
        Label:
            size_hint_y: 0.1
            font_size: 24
            text: "LCD Monitor Manager"
        Button:
            size_hint_y: 0.3
            text_size: self.size
            text: "Hello World!"
            halign: 'left'
            valign: 'center'
            background_normal: "display.png"
            font_size: 80
            font_name:"lcd1.ttf"
            color: (1,1,1,1)
            id: displayLabel1
            on_press: root.switch1()            
        Button:
            size_hint_y: 0.3
            text: "0123456789ABCDEF"
            text_size: self.size
            halign: 'left'
            valign: 'center'
            background_normal: "display.png"
            font_size: 80
            font_name:"lcd1.ttf"
            color: (1,1,1,1)
            id: displayLabel2
            on_press: root.switch2()            
        BoxLayout:
            id: kbContainer
            size_hint_y: 0.2
            orientation: "horizontal"
            padding: 15
            size_hint_x: None
        Widget:
            size_hint_y: 0.5
''')

class KeyboardScreen(Screen): #classe per la keyboard
    displayLabel1 = ObjectProperty() #proprietà dell'oggetto Label1
    displayLabel2 = ObjectProperty() #proprietà dell'oggetto Label2
    kbContainer = ObjectProperty() #proprietà dell'oggetto container

    def __init__(self, **kwargs): #funzione init
        super(KeyboardScreen, self).__init__(**kwargs) #funzione super
        self.set_layout('qwerty') #chiama la funzione per il layout qwerty

    def set_layout(self, layout): #funzione per impostare il layout
        kb = Window.request_keyboard(
            self._keyboard_close, self) #richiesta della keyboard di sistema
        self._keyboard = kb.widget #widget della keyboard
        self._keyboard.layout = layout #layout della keyboard con il layout passato
        self._keyboard.bind(on_key_down=self.key_down,
                            on_key_up=self.key_up) #binding alle funzioni di callback

    def _keyboard_close(self, *args): #funzione per la chiusura della keyboard
        if self._keyboard: #se la keyboard è attiva
            self._keyboard.unbind(on_key_down=self.key_down) #scollega il callback
            self._keyboard.unbind(on_key_up=self.key_up) #scollega il callback
            self._keyboard = None #la keyboard viene chiusa

    def key_down(self, keyboard, keycode, text, modifiers): #funzione di callback tasto premuto
        global modifier #variabile globale
        global capslock #variabile globale
        modifier=keycode #il modifier viene letto
        if modifier == 'capslock': #se il modifier è capslock...
            capslock = not capslock #... la variabile capslock è True/False
    
    def key_up(self, keyboard, keycode, *args):#funzione di callback tasto rilasciato
        #print(modifier) #stampa il modifier
        if isinstance(keycode, tuple): #se la specifica del tipo di keycode è una tupla...
            keycode = keycode[1] #... keycode è il primo elemento della tupla
        if keycode == "spacebar": #se keycode è spacebar
            keycode = " " #... keycode è uno spazio
        if keycode == "backspace": #se backspace è True...
            self.displayLabel2.text = self.displayLabel2.text [:-1]#... cancella l'ultimo carattere
            if len(self.displayLabel2.text) < 1:
                self.displayLabel1.text = self.displayLabel1.text [:-1]#... cancella l'ultimo carattere
            #se keycode non è un modifier...
        if keycode == 'escape':
            lcd.clear()
            self.displayLabel1.text=""
            self.displayLabel2.text=""
                
        if keycode != 'capslock'\
           and keycode != 'tab'\
           and keycode != 'shift'\
           and keycode != 'backspace'\
           and keycode != 'escape'\
           and keycode != 'enter':
            if capslock == True and keycode!="None": #se caplocks è True...
                keycode = keycode.upper() #... keycode è tutto maiuscolo

            if len(self.displayLabel1.text)<16: #se la lunghezza del testo è inferiore a 16...
                print(len(self.displayLabel1.text))
                self.displayLabel1.text += u"{0}".format(keycode) #il carattere viene aggiunto al precedente con uno spazio
            else:
                if len(self.displayLabel2.text)<16: #se la lunghezza del testo è inferiore a 16...
                    self.displayLabel2.text += u"{0}".format(keycode) #il carattere viene aggiunto al precedente con uno spazio
    def switch1(self): #funzione di callback
        message = self.displayLabel1.text #il messaggio è quello del testo del pulsante
        lcd.clear()
        lcd.message(message) #messaggio al display LCD
        lcd.message("\n") #messaggio di a capo
        print (message) #stampa il messaggio
        return                    
    def switch2(self): #funzione identica alla precedente
        message = self.displayLabel2.text
        lcd.message(message)
        print (message)
        return
    
class KeyboardDemo(App):
    sm = None  # Root screen manager
    def build(self): #funzione build
        self.sm = ScreenManager() # creazione dello screen manager
        self.sm.add_widget(KeyboardScreen(name="keyboard")) #aggiunta della keyboard
        return self.sm #ritorno dello screen manager

KeyboardDemo().run() #esecuzione dell'app principale
