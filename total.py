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
 
  while not checksum_found:
    telegram_line = ser.readline() # Lees een seriele lijn in.
    telegram_line = telegram_line.decode('ascii').strip() # Strip spaties en blanke regels
 
    #print (telegram_line) #debug
 
    if re.match(b'(?=1-0:1.7.0)', telegram_line): #1-0:1.7.0 = Actueel verbruik in kW
      # 1-0:1.7.0(0000.54*kW)
 
      kw = telegram_line[10:-4] # Knip het kW gedeelte eruit (0000.54)
      watt = float(kw) * 1000 # vermengvuldig met 1000 voor conversie naar Watt (540.0)
      watt = int(watt) # rond float af naar heel getal (540)

      now = datetime.now()
      current_time = now.strftime("%d/%m/%Y %H:%M:%S")
      #print("Current Time =", current_time, now)      
      print "[",current_time,"] - ", watt, " watt"
 
    # Check wanneer het uitroepteken ontavangen wordt (einde telegram)
    if re.match(b'(?=!)', telegram_line):
      checksum_found = True
 
  ser.close()
