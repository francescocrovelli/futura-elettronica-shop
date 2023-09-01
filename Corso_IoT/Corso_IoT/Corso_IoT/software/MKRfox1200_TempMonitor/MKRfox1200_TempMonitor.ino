/*
 * Arduino MKR1200 e SigFox 
 * invio ad intervalli regolari al backend di SigFox la temperatura interna del modem
 * non viene usata la funzionalità  deep sleep per salvaguardare la comunicazione USB
 */

//#include <RTCZero.h>
//#include <ArduinoLowPower.h>
#include <SigFox.h> 

#define INTERVAL 10 //intervallo di tempo in minuti dell'invio

void setup() 
{
  Serial.begin(115200); // abilita la seriale per il debug
  while (!Serial) {};  // aspetta che la seriale sia avviata

  if (!SigFox.begin()) // verifica la presenza del modem sigfox
  {
    Serial.println("Shield error or not present!");
    return;
  }

  // Enable debug led and disable automatic deep sleep
   SigFox.debug();
  
  SigFox.reset(); //resetta il modem e la libreria
  delay(100);

  SigFox.end(); // pone il modem in modalità di basso consumo
}

void loop() 
{
  SigFox.begin(); // avvia il modulo
  delay(100); // attende che il mudulo sia inizializzato

  // legge la temperatura interna del modem
  int8_t value = (int8_t)SigFox.internalTemperature();
  Serial.print("Temp=");
  Serial.println(value);  // visualizzo il valore acquisito

  SigFox.beginPacket(); // prepara il modem per l'invio
  SigFox.write(value); // invia il valore 

  // invia il buffer al modem e verifica la corretta trasmissione
  int ret = SigFox.endPacket(false);  
  if (ret > 0) {
    Serial.println("No transmission");
  } else {
    Serial.println("Transmission ok");
  }
  delay(100);
  SigFox.end(); // pone il modem in modalità di basso consumo
  delay(100);
  Serial.println("go to sleep\n");
  delay(INTERVAL*60*1000);
}
