
'***************************************************
'* MF566
'* Il sistema invia tramite seriale i messaggi ricevuti e le chiamate
'* 
'* Il sistema è basato su un PIC16F876 lavorante a 20 MHz
'* Ultimo aggiornamento 30/08/2004 
'******************************************************************************

DEFINE OSC 20
@		DEVICE HS_OSC

'Configurazione usart 250000
DEFINE HSER_BITS 9
DEFINE HSER_RCSTA 208 
DEFINE HSER_TXSTA 101
DEFINE HSER_BAUD 250000
DEFINE HSER_CLROERR 1 'Hser clear overflow automatically 

'Debug
DEFINE DEBUG_REG PORTA
DEFINE DEBUG_BIT 2
DEFINE DEBUG_BAUD 9600  
DEFINE DEBUG_MODE 0  

SYMBOL  IN       =PORTC.0
SYMBOL	LED1     =PORTC.1		'LED
SYMBOL	LED2     =PORTC.3		'LED
SYMBOL	LED3     =PORTA.5		'LED
SYMBOL	LED4     =PORTA.3		'LED
SYMBOL	LED5     =PORTC.4		'LED
SYMBOL	LED6     =PORTC.5		'LED

INPUT	IN

TMP             VAR     WORD
TMP1            VAR     WORD
VALORE          VAR     WORD
BREAK           VAR     WORD
NDMX            VAR     WORD
Clear

ADCON0=0
ADCON1=7
OPTION_REG.7=0	'Abilita resistenze di pull-up

'Scroll led

    LOW LED1
    LOW LED2
    LOW LED3
    LOW LED4
    LOW LED5
    LOW LED6

FOR VALORE=0 TO 250 STEP 10



    IF VALORE > 1 THEN
        HIGH LED1
    ENDIF
    IF VALORE > 42 THEN
        HIGH LED2
    ENDIF
    IF VALORE > 84 THEN
        HIGH LED3
    ENDIF
    IF VALORE > 126 THEN
        HIGH LED4
    ENDIF
    IF VALORE > 168 THEN
        HIGH LED5
    ENDIF
    IF VALORE > 210 THEN
        HIGH LED6
    ENDIF
    
    pause 150

NEXT VALORE

    LOW LED1
    LOW LED2
    LOW LED3
    LOW LED4
    LOW LED5
    LOW LED6


'Fine scroll led



MAIN:

NDMX=0
NDMX=PORTB
NDMX.8=PORTA.0
NDMX.9=PORTA.1
ndmx = ndmx ^ %0000001111111111
DEBUG "NDMX ",#NDMX,10,13

PULSIN in,0,break

IF BREAK>=45 THEN

    HSERIN 1000,MAIN,[tmp1,VALORE]
    if tmp1<>0 and VALORE<>0 then
        DEBUG "EXIT ",#NDMX,10,13
        goto main
    endif
    
    FOR TMP=0 TO ndmx
        HSERIN 20,main,[VALORE]
    NEXT TMP                   
    
'    FOR TMP=NDMX TO 511
'        HSERIN 10,main,[TMP1]
'    NEXT TMP
    



    DEBUG "valore ",#valore,10,13
    HPWM 1,VALORE,2000
    LOW LED1
    LOW LED2
    LOW LED3
    LOW LED4
    LOW LED5
    LOW LED6

    IF VALORE > 1 THEN
        HIGH LED1
    ENDIF
    IF VALORE > 42 THEN
        HIGH LED2
    ENDIF
    IF VALORE > 84 THEN
        HIGH LED3
    ENDIF
    IF VALORE > 126 THEN
        HIGH LED4
    ENDIF
    IF VALORE > 168 THEN
        HIGH LED5
    ENDIF
    IF VALORE > 210 THEN
        HIGH LED6
    ENDIF
       
ENDIF


GOTO MAIN
