

'******************************************************************************
'* TIBBO VS DMX
'* Sistema di invio dati gps tramite sms
'* direttamente dal cellulare WISMO Q2501
'* Il sistema è basato su un PIC16F876
'* Questa sezione rappresenta l'unità da installare in auto 
'*
'* Data creazione 30/06/05
'******************************************************************************



DEFINE OSC 20


'@		DEVICE BOD_OFF		'disabilita il reset quando cala la tensione	
@		DEVICE HS_OSC

'Configurazione usart 250000
DEFINE HSER_BITS 9
DEFINE HSER_RCSTA 208 
DEFINE HSER_TXSTA 101
DEFINE HSER_BAUD 250000
DEFINE HSER_CLROERR 1 'Hser clear overflow automatically 



DEFINE DEBUG_REG PORTA
DEFINE DEBUG_BIT 3
DEFINE DEBUG_BAUD 38400  
DEFINE DEBUG_MODE 0  

SYMBOL	RES      =PORTC.5
SYMBOL	MD       =PORTC.4
SYMBOL	LEDV     =PORTA.1
SYMBOL	LEDR     =PORTA.2
SYMBOL  JUMP     =PORTA.0
SYMBOL  TX       =PORTC.2
SYMBOL  RX       =PORTC.3
SYMBOL  DMX      =PORTC.1
SYMBOL  IN       =PORTC.0
SYMBOL  TXDMX    =PORTC.6	     'TX



TMP             VAR     WORD
TMP1            VAR     WORD
VALORE          VAR     byte[65]
BREAK           VAR     WORD
NDMX            VAR     WORD
DATI            VAR     WORD






ADCON0=0
ADCON1=7
OPTION_REG.7=0     'PER 16F876






HIGH RES
HIGH MD

    DEBUG  "SYSTEM STARTUP",13,10   
    PAUSE 500

LOW RES


 CLEAR




LOW LEDR
High LEDV
For TMP=0 TO 5
	Toggle LEDV
	Pause 500
Next TMP
HIGH LEDV
    IF JUMP=0 THEN
        DEBUG "TX",10,13 
    ELSE
        DEBUG "RX",10,13
    ENDIF
        NDMX=0
MAIN:

NDMX= 512-(64*(    1+  1*PORTB.1+1*PORTB.2+1*PORTB.3+1*PORTB.4+1*PORTB.5+1*PORTB.6+1*PORTB.7))
'DEBUG "NDMX ",#NDMX,10,13

    IF JUMP=0 THEN
        LOW DMX
        LOW LEDR
        DATI=0
        PULSIN in,0,break
        
        IF BREAK>=40 THEN
            
            HSERIN 2000,MAIN,[tmp,tmp1]
            if tmp<>0 and tmp1<>0 then
                goto main
            endif
            
            FOR TMP=1 TO ndmx
                HSERIN 10,main,[tmp1]
            NEXT TMP
                
                FOR tmp=1 TO 64                       
                    hserin 10,EXITTX,[VALORE[TMP]]                    
                    DATI=DATI+1
                NEXT TMP
        
        EXITTX:   
                    PAUSE 3
                    high ledR 
                    SEROUT2 TX,6, ["*/",DATI]
                    FOR TMP=1 TO DATI
                        SEROUT2 TX,6, [VALORE[tmp]]
                                                       
                    NEXT TMP
                    
                    
'                    FOR TMP=1 TO DATI
'                        DEBUG "VALORE TX",#tmp, " -> ",#VALORE[tmp],13,10
                                                                 
'                    NEXT TMP
               
        ENDIF
     
    ELSE
        HIGH DMX
        LOW LEDR
'RILEGGI:        
'            SERIN2 RX,6,1000,MAIN,[TMP] 
'            IF TMP="*" THEN
                SERIN2 RX,6,1000,MAIN,[WAIT ("*/"),DATI]
'                IF TMP<>"/" THEN
'                    GOTO MAIN
'                ENDIF
'            ELSE
'                GOTO RILEGGI
'            ENDIF
            'DEBUG "DATI ",#DATI,13,10
            
'            FOR TMP=1 TO ndmx
                
'                SERIN2 RX,6,10,main,[tmp1]
'                'DEBUG "PRENDO I DMX ",TMP1,13,10
'            NEXT TMP
                
                FOR tmp=1 TO DATI                       
                    SERIN2 RX,6,200,EXITRX,[VALORE[TMP]]                    
                    'DATI=DATI+1
                NEXT TMP
        
        EXITRX:   
'                    FOR TMP=1 TO DATI
'                        DEBUG "VALORE RX",#tmp, " -> ",#VALORE[tmp],13,10                                                  
'                    NEXT TMP
                    'PAUSE 15
                    HIGH LEDR    
                    RCSTA.7=0
                    OUTPUT TXDMX
                    low TXDMX
                    
                    PAUSEUS 128 
                    RCSTA.7=1       
                    PAUSEUS 14
                    
                    FOR TMP=1 TO NDMX
                        HSEROUT [0]
                    NEXT TMP
  
                    FOR TMP=1 TO DATI                     
                        HSEROUT [VALORE[TMP]]
                    NEXT TMP
                            
      
        
        
    ENDIF



GOTO MAIN
