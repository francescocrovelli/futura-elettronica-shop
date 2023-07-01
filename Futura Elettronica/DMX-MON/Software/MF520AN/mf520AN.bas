

'***************************************************
'* MF520
'* Dimmer
'* Si basa su un PIC12F675
'* Ultimo aggiornamento 04/1/2005
'***************************************************

DEFINE OSC 4
DEFINE ADC_BITS 8       ' Set number of bits in result
DEFINE ADC_CLOCK 1     ' Set clock source 
DEFINE ADC_SAMPLEUS 100 ' Set sampling time in microseconds 
DEFINE OSCCAL_1K 1

@		DEVICE MCLR_OFF 

SYMBOL	ZERO     =GPIO.1	    
SYMBOL	TRIAC    =GPIO.2	
SYMBOL	ZERO2    =GPIO.3
SYMBOL	LEDV     =GPIO.4
SYMBOL	LEDR     =GPIO.5


TMP     VAR     WORD
TIME    VAR     WORD

OUTPUT TRIAC
OUTPUT LEDV
OUTPUT LEDR
INPUT  ZERO
INPUT  ZERO2

OPTION_REG=%00000000
CMCON =%00000111
ADCON0=%00000000
ANSEL=%00000000
WPU=%00000010       'GP1 con res pull up
IOCB=%00000000
INTCON=%00000000



LOW LEDR
HIGH LEDV
FOR TMP=0 TO 5
    TOGGLE LEDV
    TOGGLE LEDR
    PAUSE 500
NEXT TMP
LOW LEDV
LOW LEDR
low triac
CLEAR



MAIN:
   
    
    IF TIME>=80 THEN
        TMP=(TIME-80)*58
        LOW LEDR
    ELSE 
        HIGH ledr
        TMP=0
    ENDIF
    
    
    LOW LEDV
 IF TMP<9000 THEN
    TMP=9000-TMP
 ELSE
    TMP=0
    HIGH LEDV
 ENDIF

    GOSUB dimmer

              

GOTO MAIN

DIMMER:

IF ZERO=1 THEN
    'pauseus 100
    if zero=1 then
        
        pAUSEUS TMP
        HIGH triac
        'HIGH LEDR
        'PAUSEUS 500
        ADCIN 0,TIME
        LOW TRIAC
        while zero=1 
        '    HIGH ledV            
        wend
        'LOW LEDR
        
'        PAUSEUS 9000              
        PAUSEUS TMP              
        HIGH triac
        'HIGH LEDR
        'PAUSEUS 500
        ADCIN 0,TIME
        LOW TRIAC
        'LOW LEDR
        
        
        'LOW LEDV
    endif
ENDIF

RETURN


'PASSAGGIO:

'    IF ZERO=1 THEN
        
'        PAUSEUS 500
'        HIGH LEDR
'        PAUSEUS 10000
'        LOW LEDR
'        while zero=1 
'            low ledr
'        wend
'    ENDIF

'RETURN

'ROUTINE0:
    
'    IF ZERO=1 THEN
        
'        PAUSEUS 1600
        
'        HIGH triac
'        PAUSEUS 1000
'        LOW TRIAC
'        PAUSEUS 9000              
'        HIGH triac
'        PAUSEUS 1000
'        LOW TRIAC
'        while zero=1 
'            low ledr
'        wend
'    ENDIF
'RETURN




'ROUTINE0_OLD:
    
'    IF ZERO=1 THEN
        
'        PAUSEUS 1700
'        pulsout triac,100        
'        while zero=1 
'            low ledr
'        wend
'        'PAUSE 8
'        pulsout triac,100                
'    ENDIF
'RETURN


'ROUTINE50:
    
'    IF ZERO=1 THEN
        
'        PAUSEUS 4700
'        pulsout triac,100        
'        while zero=1 
'            low ledr
'        wend
'        PAUSEUS 4000
'        pulsout triac,100                
'    ENDIF
'RETURN


'ROUTINE100:
    

'RETURN


'ROUTINE50_old:
    
'    IF ZERO=0 THEN
'        pause 4
'        pulsout triac,100
'        while zero=0 
'            low ledr
'        wend
'        pause 6
'        pulsout triac,100        
'    ENDIF
'RETURN


