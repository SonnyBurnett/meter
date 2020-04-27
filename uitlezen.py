#!/usr/bin/env python
# Python script om P1 telegram weer te geven
 
import re
import serial
 
# Seriele poort confguratie
ser = serial.Serial()
 
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
 
ser.xonxoff = 0
ser.rtscts = 0
ser.timeout = 12
ser.port = "/dev/ttyUSB0"
ser.close()
 
ser.open()
checksum_found = False

telegram_list = [] 
y=1
while not checksum_found:
  telegram_line = ser.readline() # Lees een seriele lijn in.
  telegram_line.decode('ascii').strip()
  print(y, telegram_line)
  y=y+1
  telegram_list.append(telegram_line)
 
  # Check wanneer het uitroepteken ontvangen wordt (einde telegram)
  if re.match(b'(?=!)', telegram_line):
    checksum_found = True
 
ser.close()
if y > 40:
  print("Tarief 1: (laag)      ",telegram_list[6][10:-7])
  print("Tarief 2: (hoog)      ",telegram_list[7][10:-7])
  print("Actief tarief:        ",telegram_list[10][12:16])
  print("huidig verbruik laag: ",telegram_list[11][10:-5].strip("*"))
  print("huidig verbruik hoog: ",telegram_list[12][10:-5].strip("*"))
  print("gasverbruik:          ",telegram_list[39][-15:-6])

