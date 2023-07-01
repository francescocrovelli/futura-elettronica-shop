#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>
#include <dht.h>
dht DHT;
#define DHT11_PIN 4
#define PIN_LDR A0
#define PIN_LED 5
    
static const PROGMEM u1_t NWKSKEY[16] = { 0xB3, 0xDE, 0x56, 0xEE, 0x2D, 0x40, 0xE7, 0x17, 0x06, 0x31, 0x2C, 0x16, 0x18, 0x0E, 0x13, 0x9E };
static const u1_t PROGMEM APPSKEY[16] = { 0x3E, 0x25, 0x8D, 0x11, 0x77, 0x7C, 0x16, 0x95, 0xBF, 0x25, 0x5E, 0x94, 0x3E, 0x0F, 0xBE, 0xBC };
static const u4_t DEVADDR = 0x2601164B ; 

void os_getArtEui (u1_t* buf) { }
void os_getDevEui (u1_t* buf) { }
void os_getDevKey (u1_t* buf) { }
static osjob_t initjob,sendjob,blinkjob;

const unsigned TX_INTERVAL = 10;

const lmic_pinmap lmic_pins = {
    .nss = 10,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 9,
    .dio = {2, 6, 7},
};

float temperature,humidity;//valori float di lettura dal DHT11      
int tem,hum,lux; //variabili da inviare a TTN
uint8_t mydata[] = "000000"; //payload 

float valR = 0;      //variabile di lettura dell'ingresso analogico
float Vout = 0.0;    //voltaggio in uscita del partitore
float Vin = 5.0;     //tensione di alimentazione
float R_nota = 10000.0;  //valore della resistenza nota (10 Kohm)
float val_lux;           //valore lux                           
float Ldr = 0.0;         //valore calcolato della resistenza Ldr
float Ldr_1 = 75000.0;   //valore ldr di illuminamento unitario
float slope  = 0.66;     //valore gamma fotoresistenza (pendenza)
double Lux = 0.0;        //lux calcolati

void dht_read()
{      
      temperature = DHT.read11(DHT11_PIN); //rilevazione della temperatura
      tem = DHT.temperature;      
      humidity = DHT.read11(DHT11_PIN); //rilevazione dell'umidità
      hum = DHT.humidity;
      mydata[0]=84; //lettera T      
      mydata[1]=tem; //gradi temperatura
      mydata[2]=72; //lettera H     
      mydata[3]=hum; //percentuale umidità
      
      Serial.println("Temperature - Humidity:");
      Serial.print(tem);
      Serial.print("°C");
      Serial.print(" - ");
      Serial.print(hum);
      Serial.print("%");
      Serial.println();
}

void light_read(){
  valR = 0;
  for ( int i = 0; i<= 4; i++)  //lettura di 5 valori di LDR
  {
    int val_luxLdr = analogRead(PIN_LDR);
    delay (40);    
    valR = valR + val_luxLdr;
  }   
   valR = valR/5; // media aritmetica dei valori letti 
  //calcolo del valore della resistenza LDR
  Vout = (Vin/1024.0 * valR);    //conversione del valore in Volt
  Ldr = ((R_nota * Vin/Vout )- R_nota);    //calcolo della resistenza 
  
  //calcolo dei Lux
  Lux = pow((Ldr/Ldr_1), (1.0/-slope));
  lux = Lux; //double to int
  mydata[4]=76; //lettera L
  mydata[5]=lux; //invio dei lux 
}

void do_send(osjob_t* j){
    if (LMIC.opmode & OP_TXRXPEND) {
        Serial.println("OP_TXRXPEND, not sending");
    } else {
        
        dht_read(); //lettura DHT11
        light_read(); //lettura LDR

        LMIC_setTxData2(1, mydata, sizeof(mydata), 0);
        Serial.println("Packet queued");
        //Serial.print("LMIC.freq:");
        //Serial.println(LMIC.freq);
        //Serial.println("Receive data:");
    } 
}

void onEvent (ev_t ev) {
    //Serial.print(os_getTime());
    //Serial.print(": ");
    Serial.println(ev);
    switch(ev) {
        case EV_SCAN_TIMEOUT:
            Serial.println(F("EV_SCAN_TIMEOUT"));
            break;
        case EV_BEACON_FOUND:
            Serial.println(F("EV_BEACON_FOUND"));
            break;
        case EV_BEACON_MISSED:
            Serial.println(F("EV_BEACON_MISSED"));
            break;
        case EV_BEACON_TRACKED:
            Serial.println(F("EV_BEACON_TRACKED"));
            break;
        case EV_JOINING:
            Serial.println(F("EV_JOINING"));
            break;
        case EV_JOINED:
            Serial.println(F("EV_JOINED"));
            break;
        case EV_RFU1:
            Serial.println(F("EV_RFU1"));
            break;
        case EV_JOIN_FAILED:
            Serial.println(F("EV_JOIN_FAILED"));
            break;
        case EV_REJOIN_FAILED:
            Serial.println(F("EV_REJOIN_FAILED"));
            break;
        case EV_TXCOMPLETE:
            Serial.println(F("EV_TXCOMPLETE (includes waiting for RX windows)"));

char mydata[10]={0};
        if (LMIC.dataLen) 
        {
        Serial.println(F("Received "));
        Serial.print(LMIC.dataLen);
        Serial.println(F(" bytes of payload"));
        Serial.print("txCnt :"); Serial.println(LMIC.txCnt);
        Serial.print("txrxFlags :"); Serial.println(LMIC.txrxFlags);
        Serial.print("dataBeg :"); Serial.println(LMIC.dataBeg);        
        for (int i = 0; i < LMIC.dataLen; i++) 
        {
          if (LMIC.frame[LMIC.dataBeg + i] < 0x10) {
            Serial.print(F("0"));
          }
          Serial.print(LMIC.frame[LMIC.dataBeg + i], HEX);
          mydata[i]=char(LMIC.frame[LMIC.dataBeg + i]);          
          }
          }
            Serial.println();
            Serial.println(mydata);
            
            if (mydata[0]=='1') digitalWrite(PIN_LED,1);
            if (mydata[0]=='2') digitalWrite(PIN_LED,0);

            // Schedule next transmission
            os_setTimedCallback(&sendjob, os_getTime()+sec2osticks(TX_INTERVAL), do_send);
            break;
        case EV_LOST_TSYNC:
            Serial.println(F("EV_LOST_TSYNC"));
            break;
        case EV_RESET:
            Serial.println(F("EV_RESET"));
            break;
        case EV_RXCOMPLETE:
            // data received in ping slot
            Serial.println(F("EV_RXCOMPLETE"));
            break;
        case EV_LINK_DEAD:
            Serial.println(F("EV_LINK_DEAD"));
            break;
        case EV_LINK_ALIVE:
            Serial.println(F("EV_LINK_ALIVE"));
            break;
         default:
            Serial.println(F("Unknown event"));
            break;
    }
}

void setup() {
    Serial.begin(9600);
    os_init();
    LMIC_reset();
    LMIC_setClockError(MAX_CLOCK_ERROR * 5 / 100);

    pinMode(PIN_LED,OUTPUT);
    #if defined(CFG_eu868)
    LMIC_setupChannel(0, 868100000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
    LMIC_setupChannel(1, 868300000, DR_RANGE_MAP(DR_SF12, DR_SF7B), BAND_CENTI);      // g-band
    LMIC_setupChannel(2, 868500000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
    LMIC_setupChannel(3, 867100000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
    LMIC_setupChannel(4, 867300000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
    LMIC_setupChannel(5, 867500000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
    LMIC_setupChannel(6, 867700000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
    LMIC_setupChannel(7, 867900000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
    LMIC_setupChannel(8, 868800000, DR_RANGE_MAP(DR_FSK,  DR_FSK),  BAND_MILLI);      // g2-band    
    #endif
    
    #ifdef PROGMEM
    uint8_t appskey[sizeof(APPSKEY)];
    uint8_t nwkskey[sizeof(NWKSKEY)];
    memcpy_P(appskey, APPSKEY, sizeof(APPSKEY));
    memcpy_P(nwkskey, NWKSKEY, sizeof(NWKSKEY));
    LMIC_setSession (0x1, DEVADDR, nwkskey, appskey);
    #else
    LMIC_setSession (0x1, DEVADDR, NWKSKEY, APPSKEY);
    #endif
    LMIC_setLinkCheckMode(0);
    LMIC.dn2Dr = DR_SF9;
    LMIC_setDrTxpow(DR_SF7,14);
    do_send(&sendjob);
}


void loop() {
    os_runloop_once();       
}
