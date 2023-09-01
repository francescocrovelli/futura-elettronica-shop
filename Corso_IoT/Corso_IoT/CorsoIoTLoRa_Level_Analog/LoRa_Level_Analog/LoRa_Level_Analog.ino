/*
 * LoRaWAN + Arduino MKR WAN 1300 +  POT on A0
 * Invia il valore acquisito ad intervalli regolari
 */

#include <MKRWAN.h>

LoRaModem modem;

#include "arduino_secrets.h"

// Please enter your sensitive data in the arduino_secrets.h tab
String appEui = SECRET_APP_EUI;
String appKey = SECRET_APP_KEY;

int sensorPin = A0;
int sensorValue;
long intervalToSend = 60;  //every minutes

void setup()
{

  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial);

  Serial.println("Initialize modem ...");
  if (!modem.begin(EU868)) 
  {
    Serial.println("Failed to start module, rebooting MKRWAN in 1 seconds ...");
    delay(1000);
    NVIC_SystemReset();
    while(1) ;
  };
  
  Serial.print("Your module version is: ");
  Serial.println(modem.version());
  Serial.print("Your device EUI is: ");
  Serial.println(modem.deviceEUI());


  Serial.println("Try to join: ");
  int connected = modem.connected();
  int joinFailed = 0;
  
    while ( !connected && joinFailed < 10 )
    {
      connected = modem.joinOTAA(appEui, appKey);
      if (!connected) 
      {
        Serial.println("LoRaWAN network not joined, retry join in 10 seconds ...");
        delay(10000);
        joinFailed++;
      }    
    }


  if ( connected )
  {
    Serial.println("LoRaWAN network joined");
    //modem.setPort(10); //?
    /*
     * SET DataRate
     * dr 0 = SF12BW125
     * dr 1 = SF11BW125
     * dr 2 = SF10BW125
     * dr 3 = SF9BW125
     * dr 4 = SF8BW125
     * dr 5 = SF7BW125
    */    
     //   modem.dataRate(0);
 
    // adaptive data rate (ADR), the network automatically optimize your data rate.
    modem.setADR(true);    
  }
  else
  {
     Serial.println("Not connected to Network!");
     while(1);
  }
  
  // Set poll interval to 60 secs.
  // modem.minPollInterval(60);
  
  int error = modem.getADR();

  // Check status
  if( error == 0 ) 
  {
    Serial.println("Adaptive data rate status OK"); 
  }
  else 
  {
    Serial.println("No Adaptive data rate active"); 
  }
}

void loop() 
{
    // read the value from the sensor:
    sensorValue = analogRead(sensorPin);
    
    // scale the reading and fit into 1 byte
    sensorValue = sensorValue / 4; // 0-255 -> 1byte
    byte payload = sensorValue;
    Serial.print("Sensor value = " );
    Serial.println(sensorValue);
    delay(100);
              
    // send data
    modem.beginPacket();
    modem.write(payload);
    int err = modem.endPacket(false); //Return 1 if the packet was sent successfully, 0 if there was an error 
    if (err > 0) {
    Serial.println("Data sent correctly");
    } else {
    Serial.println("Error sending data");
    }
    
    delay(1000 * intervalToSend);
}
