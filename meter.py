#!/usr/bin/env python
# Python script om P1 telegram weer te geven
 
import re
import serial
import time
from datetime import datetime
 
# Seriele poort confguratie
ser = serial.Serial()
 
 # DSMR 4.0/4.2 > 115200 8N1:
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
 
ser.xonxoff = 0
ser.rtscts = 0
ser.timeout = 12
ser.port = "/dev/ttyUSB0"
ser.close()
 
while True:
  ser.open()
  checksum_found = False

  laag_watt = -1
  hoog_watt = -1
  laag_totaal = -1
  hoog_totaal = -1
  tarief_type = -1
  gas = -1
 
  while not checksum_found:
    telegram_line = ser.readline() # Lees een seriele lijn in.
    telegram_line = telegram_line.decode('ascii').strip() # Strip spaties en blanke regels
 
    #print (telegram_line) #debug
 
    if re.match(b'(?=1-0:1.7.0)', telegram_line): #1-0:1.7.0 = Actueel verbruik in kW
      laag_kw = telegram_line[10:-4] # Knip het kW gedeelte eruit (0000.54)
      laag_watt = float(laag_kw) * 1000 # vermengvuldig met 1000 voor conversie naar Watt (540.0)
      laag_watt = int(laag_watt) # rond float af naar heel getal (540)

    elif re.match(b'(?=1-0:2.7.0)', telegram_line): #1-0:1.7.0 = Actueel verbruik in kW
      hoog_kw = telegram_line[10:-4] # Knip het kW gedeelte eruit (0000.54)
      hoog_watt = float(hoog_kw) * 1000 # vermengvuldig met 1000 voor conversie naar Watt (540.0)
      hoog_watt = int(hoog_watt) # rond float af naar heel getal (540)

    elif re.match(b'(?=1-0:1.8.1)', telegram_line): # Laag tarief totaal
      laag_totaal = telegram_line[10:-7]  
      
    elif re.match(b'(?=1-0:1.8.2)', telegram_line): # Hoog tarief totaal
      hoog_totaal = telegram_line[10:-7]

    elif re.match(b'(?=0-0:96.14.0)', telegram_line): # Tarief type 1 of 0
      tarief_type = telegram_line[12:16]

    elif re.match(b'(?=0-2:24.2.1)', telegram_line): # Verbruik gas
      gas = telegram_line[26:35]

    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    
    # Check wanneer het uitroepteken ontavangen wordt (einde telegram)
    if re.match(b'(?=!)', telegram_line):
      checksum_found = True

  print "[", current_time, "]", laag_watt, hoog_watt, laag_totaal, hoog_totaal, tarief_type, gas
  ser.close()
