'******************************************************************************
'* Boris Landoni
'* Utilizza un pic 16F877
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
DEFINE DEBUG_REG PORTC
DEFINE DEBUG_BIT 4
DEFINE DEBUG_BAUD 9600  
DEFINE DEBUG_MODE 0  


'Configurazione AD
DEFINE ADC_BITS 8       ' RISOLUZIONE 10 BIT
DEFINE ADC_CLOCK 3     	 ' SORGENTE CLOCK
DEFINE ADC_SAMPLEUS 50 ' CAMPIONAMENTO IN MICROSECONDI

'Definizione delle porte
SYMBOL  PULS    =PORTD.7	     'PULSANTE
SYMBOL  DIGITA  =PORTD.1	     'DIGIT A DEL DISPLAY 7 SEGMENTI
SYMBOL  DIGITB  =PORTD.0	     'DIGIT B DEL DISPLAY 7 SEGMENTI
SYMBOL  DIGITC  =PORTC.1	     'DIGIT C DEL DISPLAY 7 SEGMENTI
SYMBOL  DIGITD  =PORTC.2	     'DIGIT D DEL DISPLAY 7 SEGMENTI
SYMBOL  DIGITE  =PORTC.3	     'DIGIT E DEL DISPLAY 7 SEGMENTI
SYMBOL  DIGITF  =PORTD.2	     'DIGIT F DEL DISPLAY 7 SEGMENTI
SYMBOL  DIGITG  =PORTD.3	     'DIGIT G DEL DISPLAY 7 SEGMENTI
SYMBOL  DIGITP  =PORTC.0	     'DIGIT PUNTO DEL DISPLAY 7 SEGMENTI
SYMBOL  TX      =PORTC.6	     'TX


'Definizione delle variabili
CH1         VAR BYTE
CH2         VAR BYTE
CH3         VAR BYTE
CH4         VAR BYTE
CH5         VAR BYTE
CH6         VAR BYTE
CH7         VAR BYTE
CH8         VAR BYTE
CH1OLD      VAR BYTE
CH2OLD      VAR BYTE
CH3OLD      VAR BYTE
CH4OLD      VAR BYTE
CH5OLD      VAR BYTE
CH6OLD      VAR BYTE
CH7OLD      VAR BYTE
CH8OLD      VAR BYTE
CH1STA      VAR BYTE
CH2STA      VAR BYTE
CH3STA      VAR BYTE
CH4STA      VAR BYTE
CH5STA      VAR BYTE
CH6STA      VAR BYTE
CH7STA      VAR BYTE
CH8STA      VAR BYTE
START1      VAR BYTE
START2      VAR BYTE
START3      VAR BYTE
START4      VAR BYTE
START5      VAR BYTE
START6      VAR BYTE
START7      VAR BYTE
START8      VAR BYTE
CIFRA       VAR BYTE
TMP         VAR WORD
CENTINAIA   VAR BYTE
DECINE      VAR BYTE
UNITA       VAR BYTE
NDMX        VAR WORD
FUNZIONE    VAR BYTE
TMP1        VAR BYTE
TIMER       VAR BYTE
PAUSA       VAR BYTE
AVANTI      VAR BYTE
CASUALE     VAR BYTE

'DISABILITA I CONVERTITORI A/D
'ADCON0=0
'ADCON1=7
'ADCON1.7=1	'ALLINAMENTO A DESTRA 0000001111111111
OPTION_REG.7=0  'ABILITA RESISTENZE DI PULL-UP
EEPROM 0,[0,0,1,1] 'INDIRIZZO DMX DI PARTENZA

CLEAR

READ 0,CENTINAIA
READ 1,DECINE
READ 2,UNITA

NDMX=(CENTINAIA*100)+(DECINE*10)+UNITA 

DEBUG "NDMX ",#NDMX,10,13
    
GOSUB VISUADMX

'FOR CIFRA =0 TO 9
'    GOSUB  DISPLAY
'    PAUSE 1000
'NEXT CIFRA


CASUALE=1
PAUSA=5


MAIN:

    READ 0,CENTINAIA
    READ 1,DECINE
    READ 2,UNITA
    READ 3,FUNZIONE
    CIFRA=FUNZIONE
    GOSUB DISPLAY
    
    NDMX=(CENTINAIA*100)+(DECINE*10)+UNITA 
    
    ADCIN 7,CH1                                           
    ADCIN 6,CH2
    ADCIN 5,CH3
    ADCIN 4,CH4
    ADCIN 3,CH5
    ADCIN 2,CH6
    ADCIN 1,CH7
    ADCIN 0,CH8
    
    PAUSE 15
    
    'DEBUG    "CH1 ",#CH1,10,13,"CH2 ",#CH2,10,13,"CH3 ",#CH3,10,13,"CH4 ",#CH4,10,13,_
    '        _"CH5 ",#CH5,10,13,"CH6 ",#CH6,10,13,"CH7 ",#CH7,10,13,"CH8 ",#CH8,10,13,_
    '        _"PULSANTI",BIN PORTB,BIN PULS,10,13
    
'    TXSTA.5=0
    
    SELECT CASE FUNZIONE
        CASE 1
            GOSUB FLASH
        CASE 2
            GOSUB FLASHDOWN
        CASE 3
            GOSUB DESTRA
        CASE 4
            GOSUB SINISTRA
        CASE 5
            GOSUB DESTRANEG
        CASE 6
            GOSUB SINISTRANEG
        CASE 7
            GOSUB AVANTIINDIETRO
        CASE 8
            GOSUB RAND
    
                 
    END SELECT
    
    RCSTA.7=0
    OUTPUT TX
    low TX
    
    PAUSEUS 128 
    RCSTA.7=1       
    PAUSEUS 14
    
    FOR TMP=1 TO NDMX
        HSEROUT [0]
    NEXT TMP
     
    HSEROUT [CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8]
    

    'FOR TMP=1 TO NDMX
    '    DEBUG "0"
    'NEXT TMP
     
    'DEBUG #CH1,32,#CH2,32,#CH3,32,#CH4,32,#CH5,32,#CH6,32,#CH7,32,#CH8,10,13
    
    IF PULS=0   THEN
        TMP=0
        WHILE PULS=0 AND TMP<200
            TMP=TMP+1
            PAUSE 10
        WEND
        IF TMP<200 THEN
            CIFRA=15 'F
            GOSUB DISPLAY
            'PAUSE 500         
            GOSUB SELFUNZIONE
        ELSE
            CIFRA=10 'P
            GOSUB DISPLAY
            PAUSE 500
            CIFRA=13 'c
            GOSUB DISPLAY
            PAUSE 200
            UNITA=1
            DECINE=0
            CENTINAIA=0
            TMP=0
            GOSUB PROGDMX
        ENDIF
    ENDIF
        
    
GOTO MAIN



PROGDMX:
    CIFRA=0
    PAUSE 500
    GOSUB DISPLAY
    WHILE PULS=1
            
        PULSOUT DIGITP,10000 
        IF PORTB.1=0 THEN
            if CIFRA<9 then
                CIFRA=CIFRA+1
            else
                CIFRA=0
            endif
            GOSUB DISPLAY
            PAUSE 500
        ENDIF
        
        IF PORTB.0=0 THEN
            if CIFRA>0 then
                CIFRA=CIFRA-1            
            else
                CIFRA=9
            endif
            GOSUB DISPLAY
            PAUSE 500
        ENDIF
        
    WEND
    
    TMP=TMP+1
    IF TMP=1 THEN    'DECINE
        CENTINAIA=CIFRA
        CIFRA=12 'd
        GOSUB DISPLAY
        PAUSE 800
        GOTO PROGDMX
    ENDIF
    
    IF TMP=2 THEN    'UNITA
        DECINE=CIFRA
        CIFRA=11 'u
        GOSUB DISPLAY
        PAUSE 800
        GOTO PROGDMX
    ENDIF
        
        UNITA=CIFRA

    PAUSE 500
    
    GOSUB ROTEA
     
    NDMX=(CENTINAIA*100)+(DECINE*10)+UNITA
    IF NDMX>=505 THEN
        CENTINAIA=5
        DECINE=0
        UNITA=5
        NDMX=505
    ENDIF
    DEBUG "NDMX ",#NDMX,10,13
    
    WRITE 0,CENTINAIA
    WRITE 1,DECINE
    WRITE 2,UNITA
    
    
    GOSUB VISUADMX


RETURN


SELFUNZIONE:

        TMP1=1
        
        IF PORTB.0=0 THEN
            CIFRA=1
            GOTO EXIT
        ENDIF
        IF PORTB.1=0 THEN
            CIFRA=2
            GOTO EXIT
        ENDIF
        IF PORTB.2=0 THEN
            CIFRA=3
            GOTO EXIT
        ENDIF
        IF PORTB.3=0 THEN
            CIFRA=4
            GOTO EXIT
        ENDIF
        IF PORTB.4=0 THEN
            CIFRA=5
            GOTO EXIT
        ENDIF
        IF PORTB.5=0 THEN
            CIFRA=6
            GOTO EXIT
        ENDIF
        IF PORTB.6=0 THEN
            CIFRA=7
            GOTO EXIT
        ENDIF
        IF PORTB.7=0 THEN
            CIFRA=8
            GOTO EXIT
        ENDIF
    GOTO SELFUNZIONE
    
EXIT: 
    if PORTB.0=0 or PORTB.1=0 or PORTB.2=0 or PORTB.3=0 or PORTB.4=0 or PORTB.5=0 or PORTB.6=0 or PORTB.7=0 then
        goto EXIT
    ENDIF    
    FUNZIONE=CIFRA
    CIFRA=FUNZIONE
    WRITE 3,FUNZIONE


RETURN



FLASH:


    IF PORTB.0 = 0 THEN
        CH1=255
    ENDIF
    IF PORTB.1 = 0 THEN
        CH2=255
    ENDIF    
    IF PORTB.2 = 0 THEN
        CH3=255
    ENDIF    
    IF PORTB.3 = 0 THEN
        CH4=255
    ENDIF    
    IF PORTB.4 = 0 THEN
        CH5=255
    ENDIF
    IF PORTB.5 = 0 THEN
        CH6=255
    ENDIF
    IF PORTB.6 = 0 THEN
        CH7=255
    ENDIF
    IF PORTB.7 = 0 THEN
        CH8=255
    ENDIF

RETURN

FLASHDOWN:


    IF PORTB.0 = 0 THEN
        CH1=0
    ENDIF
    IF PORTB.1 = 0 THEN
        CH2=0
    ENDIF    
    IF PORTB.2 = 0 THEN
        CH3=0
    ENDIF    
    IF PORTB.3 = 0 THEN
        CH4=0
    ENDIF    
    IF PORTB.4 = 0 THEN
        CH5=0
    ENDIF
    IF PORTB.5 = 0 THEN
        CH6=0
    ENDIF
    IF PORTB.6 = 0 THEN
        CH7=0
    ENDIF
    IF PORTB.7 = 0 THEN
        CH8=0
    ENDIF

RETURN

DESTRA:
    TIMER=TIMER+1
        IF TIMER>PAUSA THEN
            TIMER=0
            TMP1=TMP1+1                
            IF TMP1>8 THEN
                TMP1=1
            ENDIF            
        ENDIF
            SELECT CASE TMP1
                CASE 1
                    CH1=255
                CASE 2
                    CH2=255
                CASE 3
                    CH3=255
                CASE 4
                    CH4=255
                CASE 5
                    CH5=255
                CASE 6
                    CH6=255
                CASE 7
                    CH7=255
                CASE 8
                    CH8=255
            END SELECT
            
        GOSUB VELOCITA
        
RETURN

SINISTRA:

    TIMER=TIMER+1
        IF TIMER>PAUSA THEN
            TIMER=0    
            TMP1=TMP1-1
            IF TMP1<1 THEN
                TMP1=8
            ENDIF 
            
        ENDIF
            SELECT CASE TMP1
                CASE 1
                    CH1=255
                CASE 2
                    CH2=255
                CASE 3
                    CH3=255
                CASE 4
                    CH4=255
                CASE 5
                    CH5=255
                CASE 6
                    CH6=255
                CASE 7
                    CH7=255
                CASE 8
                    CH8=255
            END SELECT
            
        GOSUB VELOCITA

RETURN




DESTRANEG:
    TIMER=TIMER+1
        IF TIMER>PAUSA THEN
            TIMER=0
            TMP1=TMP1+1                
            IF TMP1>8 THEN
                TMP1=1
            ENDIF            
        ENDIF
            SELECT CASE TMP1
                CASE 1
                    CH1=0
                CASE 2
                    CH2=0
                CASE 3
                    CH3=0
                CASE 4
                    CH4=0
                CASE 5
                    CH5=0
                CASE 6
                    CH6=0
                CASE 7
                    CH7=0
                CASE 8
                    CH8=0
            END SELECT
            
        GOSUB VELOCITA
        
RETURN

SINISTRANEG:


    TIMER=TIMER+1
        IF TIMER>PAUSA THEN
            TIMER=0    
            TMP1=TMP1-1
            IF TMP1<1 THEN
                TMP1=8
            ENDIF 
            
        ENDIF
            SELECT CASE TMP1
                CASE 1
                    CH1=0
                CASE 2
                    CH2=0
                CASE 3
                    CH3=0
                CASE 4
                    CH4=0
                CASE 5
                    CH5=0
                CASE 6
                    CH6=0
                CASE 7
                    CH7=0
                CASE 8
                    CH8=0
            END SELECT
            
        GOSUB VELOCITA

RETURN

AVANTIINDIETRO:


    TIMER=TIMER+1
        IF TIMER>PAUSA THEN
            TIMER=0    
            IF AVANTI=0 THEN                
                IF TMP1<1 THEN
                    TMP1=1
                    AVANTI=1
                ENDIF
                TMP1=TMP1-1                
            ELSE                            
                IF TMP1>8 THEN
                    TMP1=8
                    AVANTI=0
                ENDIF
                TMP1=TMP1+1
            ENDIF
        ENDIF
            SELECT CASE TMP1
                CASE 1
                    CH1=255
                CASE 2
                    CH2=255
                CASE 3
                    CH3=255
                CASE 4
                    CH4=255
                CASE 5
                    CH5=255
                CASE 6
                    CH6=255
                CASE 7
                    CH7=255
                CASE 8
                    CH8=255
            END SELECT
            
           GOSUB VELOCITA

RETURN





RAND:

    

    TIMER=TIMER+1
    IF TIMER>PAUSA THEN
        RANDOM TMP1
        for tmp=0 to tmp1
            CASUALE=CASUALE<<1
            IF CASUALE=0 THEN
                CASUALE=1
            ENDIF            
        next tmp
        TIMER=0
    ENDIF


    
        IF CASUALE.0=1 THEN
            CH1=255        
        ENDIF
        IF CASUALE.1=1 THEN
            CH2=255        
        ENDIF
        IF CASUALE.2=1 THEN
            CH3=255        
        ENDIF
        IF CASUALE.3=1 THEN
            CH4=255        
        ENDIF
        IF CASUALE.4=1 THEN
            CH5=255        
        ENDIF
        IF CASUALE.5=1 THEN
            CH6=255        
        ENDIF
        IF CASUALE.6=1 THEN
            CH7=255        
        ENDIF
        IF CASUALE.7=1 THEN
            CH8=255        
        ENDIF
    
    
       GOSUB VELOCITA 
            
RETURN


VELOCITA:

    IF PORTB.0 = 0 THEN
        PAUSA=5
    ENDIF
    IF PORTB.1 = 0 THEN
        PAUSA=10
    ENDIF    
    IF PORTB.2 = 0 THEN
        PAUSA=20
    ENDIF    
    IF PORTB.3 = 0 THEN
        PAUSA=30
    ENDIF    
    IF PORTB.4 = 0 THEN
        PAUSA=40
    ENDIF
    IF PORTB.5 = 0 THEN
        PAUSA=50
    ENDIF
    IF PORTB.6 = 0 THEN
        PAUSA=60
    ENDIF
    IF PORTB.7 = 0 THEN
        PAUSA=70
    ENDIF

RETURN

VISUADMX:
    CIFRA=CENTINAIA
    GOSUB DISPLAY
    PAUSE 500
    CIFRA=99
    GOSUB DISPLAY
    PAUSE 200
    CIFRA=DECINE
    GOSUB DISPLAY
    PAUSE 500
    CIFRA=99
    GOSUB DISPLAY
    PAUSE 200
    CIFRA=UNITA
    GOSUB DISPLAY
    PAUSE 500
    
    CIFRA=99
    GOSUB DISPLAY
    PAUSE 500

RETURN

ROTEA:

    CIFRA=99
    GOSUB DISPLAY
    HIGH DIGITA 
    PAUSE 200
    LOW  DIGITA
    HIGH DIGITB
    PAUSE 200
    LOW  DIGITB
    HIGH DIGITC
    PAUSE 200
    LOW  DIGITC
    HIGH DIGITD
    PAUSE 200
    LOW  DIGITD
    HIGH DIGITE
    PAUSE 200
    LOW  DIGITE
    HIGH DIGITF
    PAUSE 200
    LOW  DIGITF
    HIGH DIGITA 
    PAUSE 200
    LOW  DIGITA
    PAUSE 500

RETURN




DISPLAY:
    LOW DIGITA
    LOW DIGITB
    LOW DIGITC
    LOW DIGITD
    LOW DIGITE
    LOW DIGITF
    LOW DIGITG
    
    SELECT CASE CIFRA
        CASE 0
            HIGH DIGITA    
            HIGH DIGITB
            HIGH DIGITC
            HIGH DIGITD
            HIGH DIGITE
            HIGH DIGITF
        '    HIGH DIGITG
        CASE 1
        '    HIGH DIGITA    
            HIGH DIGITB
            HIGH DIGITC
        '    HIGH DIGITD
        '    HIGH DIGITE
        '    HIGH DIGITF
        '    HIGH DIGITG
        CASE 2
            HIGH DIGITA    
            HIGH DIGITB
        '    HIGH DIGITC
            HIGH DIGITD
            HIGH DIGITE
        '    HIGH DIGITF
            HIGH DIGITG
        CASE 3
            HIGH DIGITA    
            HIGH DIGITB
            HIGH DIGITC
            HIGH DIGITD
         '   HIGH DIGITE
         '   HIGH DIGITF
            HIGH DIGITG
        CASE 4
         '   HIGH DIGITA    
            HIGH DIGITB
            HIGH DIGITC
         '   HIGH DIGITD
         '   HIGH DIGITE
            HIGH DIGITF
            HIGH DIGITG
        CASE 5
            HIGH DIGITA    
         '   HIGH DIGITB
            HIGH DIGITC
            HIGH DIGITD
         '   HIGH DIGITE
            HIGH DIGITF
            HIGH DIGITG
        CASE 6
            HIGH DIGITA    
         '   HIGH DIGITB
            HIGH DIGITC
            HIGH DIGITD
            HIGH DIGITE
            HIGH DIGITF
            HIGH DIGITG
        CASE 7
            HIGH DIGITA    
            HIGH DIGITB
            HIGH DIGITC
         '   HIGH DIGITD
         '   HIGH DIGITE
         '   HIGH DIGITF
         '   HIGH DIGITG
        CASE 8
            HIGH DIGITA    
            HIGH DIGITB
            HIGH DIGITC
            HIGH DIGITD
            HIGH DIGITE
            HIGH DIGITF
            HIGH DIGITG
        CASE 9
            HIGH DIGITA    
            HIGH DIGITB
            HIGH DIGITC
            HIGH DIGITD
         '   HIGH DIGITE
            HIGH DIGITF
            HIGH DIGITG
         CASE 10
            HIGH DIGITA    
            HIGH DIGITB
          '  HIGH DIGITC
          '  HIGH DIGITD
            HIGH DIGITE
            HIGH DIGITF
            HIGH DIGITG
         CASE 11    'u
         '   HIGH DIGITA    
         '   HIGH DIGITB
            HIGH DIGITC
            HIGH DIGITD
            HIGH DIGITE
         '   HIGH DIGITF
         '   HIGH DIGITG
         CASE 12    'd
         '   HIGH DIGITA    
            HIGH DIGITB
            HIGH DIGITC
            HIGH DIGITD
            HIGH DIGITE
         '   HIGH DIGITF
            HIGH DIGITG
         CASE 13    'c
         '   HIGH DIGITA    
         '   HIGH DIGITB
         '   HIGH DIGITC
            HIGH DIGITD
            HIGH DIGITE
         '   HIGH DIGITF
            HIGH DIGITG
            
         CASE 15    'F
            HIGH DIGITA    
         '   HIGH DIGITB
         '   HIGH DIGITC
         '   HIGH DIGITD
            HIGH DIGITE
            HIGH DIGITF
            HIGH DIGITG
             
        END SELECT
        
'        pause 500

RETURN
