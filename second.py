import serial

display = serial.Serial("/dev/ttyAMA0", 115200, 1)

display.open()





display.write(b"Hello World sagt das Python Programm")
